"""
Deepfake detection using heuristic analysis + optional CNN model
PyTorch is OPTIONAL — falls back to heuristic-only detection
"""
import os
import tempfile
import numpy as np
from typing import Dict, Any, Optional
from PIL import Image

# OpenCV import
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("[DeepfakeDetector] OpenCV not available — limited image analysis")

# PyTorch import (optional)
try:
    import torch
    import torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("[DeepfakeDetector] PyTorch not available — using heuristic-only detection")


class DeepfakeDetectorCNN:
    """Simple CNN for deepfake detection (only used if PyTorch available)"""

    def __init__(self):
        if not HAS_TORCH:
            return
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128 * 28 * 28, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 1),
            nn.Sigmoid(),
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.model.eval()


class DeepfakeDetector:
    """Deepfake detection service with graceful fallbacks"""

    def __init__(self):
        self.cnn = None
        if HAS_TORCH:
            try:
                self.cnn = DeepfakeDetectorCNN()
                print("[DeepfakeDetector] CNN model initialized")
            except Exception as e:
                print(f"[DeepfakeDetector] CNN init failed: {e}")

    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze image for deepfake manipulation"""
        try:
            image = Image.open(image_path).convert("RGB")
            image_array = np.array(image.resize((224, 224)))

            # Face detection
            face_analysis = self._detect_faces(image_path)

            # Feature extraction
            features = self._extract_manipulation_features(image_array)

            # Get prediction
            if self.cnn and HAS_TORCH:
                prediction = self._predict_with_model(image_array)
            else:
                prediction = self._heuristic_detection(features)

            confidence = prediction["confidence"]
            return {
                "is_deepfake": 1 if confidence > 0.7 else 0,
                "confidence": confidence,
                "features_detected": features,
                "face_analysis": face_analysis,
                "manipulation_type": prediction.get("manipulation_type"),
                "explanation": self._generate_explanation(prediction, features),
            }
        except Exception as e:
            print(f"[DeepfakeDetector] Image analysis error: {e}")
            return self._default_result()

    async def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Analyze video for deepfake manipulation"""
        if not HAS_CV2:
            return {
                "is_deepfake": -1,
                "confidence": 0.0,
                "frames_analyzed": 0,
                "explanation": "Video analysis requires OpenCV. Install opencv-python.",
            }

        try:
            cap = cv2.VideoCapture(video_path)
            frame_results = []
            frame_count = 0
            sample_rate = 30  # every 30th frame

            while cap.isOpened() and frame_count < 300:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % sample_rate == 0:
                    # Save frame to temp file
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        tmp_path = tmp.name
                        cv2.imwrite(tmp_path, frame)

                    try:
                        result = await self.analyze_image(tmp_path)
                        frame_results.append(result)
                    finally:
                        os.unlink(tmp_path)

                frame_count += 1

            cap.release()

            if frame_results:
                avg_confidence = float(np.mean([r["confidence"] for r in frame_results]))
                return {
                    "is_deepfake": 1 if avg_confidence > 0.7 else 0,
                    "confidence": avg_confidence,
                    "frames_analyzed": len(frame_results),
                    "manipulation_type": "video_manipulation" if avg_confidence > 0.7 else None,
                    "explanation": f"Analyzed {len(frame_results)} frames. Average deepfake confidence: {avg_confidence:.0%}",
                }
            return self._default_result()

        except Exception as e:
            print(f"[DeepfakeDetector] Video analysis error: {e}")
            return self._default_result()

    def _detect_faces(self, image_path: str) -> Dict[str, Any]:
        """Detect faces using OpenCV Haar cascade"""
        if not HAS_CV2:
            return {"faces_detected": 0, "face_regions": []}
        try:
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            img = cv2.imread(image_path)
            if img is None:
                return {"faces_detected": 0, "face_regions": []}
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            return {
                "faces_detected": len(faces),
                "face_regions": [
                    {"x": int(x), "y": int(y), "w": int(w), "h": int(h)}
                    for x, y, w, h in faces
                ],
            }
        except Exception:
            return {"faces_detected": 0, "face_regions": []}

    def _extract_manipulation_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Extract features indicating manipulation"""
        features = {}

        if not HAS_CV2:
            return {"analysis_limited": True}

        try:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            # Edge variance (GAN artifacts tend to have unusual patterns)
            laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            features["edge_variance"] = round(laplacian_var, 2)
            features["suspicious_edge_patterns"] = bool(laplacian_var < 50 or laplacian_var > 500)

            # Color histogram analysis
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            features["color_distribution_anomaly"] = bool(float(np.std(hist)) > 1000)

            # Compression artifact detection
            edges = cv2.Canny(image, 100, 200)
            edge_density = float(np.sum(edges)) / float(edges.size)
            features["compression_artifacts"] = bool(edge_density > 0.1)

            # Error Level Analysis (simplified)
            features["edge_density"] = round(edge_density, 4)

        except Exception as e:
            features["error"] = str(e)

        return features

    def _predict_with_model(self, image: np.ndarray) -> Dict[str, Any]:
        """Use CNN model for prediction"""
        try:
            import torch
            img_tensor = torch.FloatTensor(image).permute(2, 0, 1).unsqueeze(0) / 255.0
            img_tensor = img_tensor.to(self.cnn.device)

            with torch.no_grad():
                output = self.cnn.model(img_tensor)
                confidence = output.item()

            return {
                "confidence": confidence,
                "manipulation_type": "face_swap" if confidence > 0.7 else None,
            }
        except Exception as e:
            print(f"[DeepfakeDetector] Model prediction error: {e}")
            return {"confidence": 0.5, "manipulation_type": None}

    def _heuristic_detection(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Heuristic-based detection when model unavailable"""
        score = 0.3

        if features.get("suspicious_edge_patterns"):
            score += 0.2
        if features.get("color_distribution_anomaly"):
            score += 0.2
        if features.get("compression_artifacts"):
            score += 0.1

        return {
            "confidence": min(score, 0.95),
            "manipulation_type": "potential_gan_generated" if score > 0.6 else None,
        }

    def _generate_explanation(self, prediction: Dict, features: Dict) -> str:
        """Generate human-readable explanation"""
        conf = prediction["confidence"]

        if conf > 0.7:
            reasons = []
            if features.get("suspicious_edge_patterns"):
                reasons.append("unusual edge patterns characteristic of GAN artifacts")
            if features.get("color_distribution_anomaly"):
                reasons.append("abnormal color distribution")
            if features.get("compression_artifacts"):
                reasons.append("suspicious compression artifacts")

            reason_text = ", ".join(reasons) if reasons else "multiple manipulation indicators"
            return f"High probability of manipulation detected ({conf:.0%}) due to {reason_text}."
        elif conf > 0.5:
            return f"Medium confidence ({conf:.0%}) of potential manipulation. Manual review recommended."
        else:
            return f"Low confidence ({conf:.0%}) of manipulation. Content appears authentic."

    def _default_result(self) -> Dict[str, Any]:
        return {
            "is_deepfake": -1,
            "confidence": 0.0,
            "features_detected": {},
            "explanation": "Analysis failed or inconclusive",
        }


# Global detector instance
deepfake_detector = DeepfakeDetector()
