# API Documentation

## Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication
Currently no authentication required. In production, implement JWT or API key authentication.

---

## 📤 Analysis Endpoints

### Upload and Analyze Content
```
POST /api/analyze/upload
```

Upload media or text for analysis.

**Request Body (multipart/form-data):**
```
file: File (optional) - Image, video, or audio file
text: string (optional) - Text content to analyze
url: string (optional) - URL to analyze
```

**Response:**
```json
{
  "content_id": 1,
  "analysis_id": 1,
  "status": "success",
  "result": {
    "is_deepfake": 0,
    "deepfake_confidence": 0.15,
    "is_manipulated": 0,
    "manipulation_type": null,
    "fact_check_status": "True",
    "fact_check_confidence": 0.85,
    "claims": ["Extracted claim 1", "Extracted claim 2"],
    "evidence": [...],
    "explanation": "Analysis completed. Content appears authentic.",
    "risk_level": "low",
    "overall_confidence": 0.85,
    "processing_time_ms": 1250
  }
}
```

### Get Analysis Results
```
GET /api/analyze/{content_id}
```

Retrieve analysis results for specific content.

**Response:**
```json
{
  "content_id": 1,
  "status": "completed",
  "result": {
    "analysis_id": 1,
    "is_deepfake": 0,
    "deepfake_confidence": 0.15,
    ...
  }
}
```

---

## 👥 Review Endpoints

### Get Review Queue
```
GET /api/review/queue?risk_level={level}&limit={count}
```

Get pending items for human review.

**Query Parameters:**
- `risk_level` (optional): Filter by risk level (low/medium/high/critical)
- `limit` (optional): Max number of items (default: 20)

**Response:**
```json
{
  "total": 5,
  "items": [
    {
      "content_id": 1,
      "content_type": "image",
      "file_name": "suspicious_image.jpg",
      "upload_timestamp": "2024-01-15T10:30:00Z",
      "analysis": {
        "is_deepfake": 1,
        "deepfake_confidence": 0.85,
        "risk_level": "high",
        "explanation": "..."
      },
      "reviewed": false,
      "review_decision": null
    }
  ]
}
```

### Approve AI Decision
```
POST /api/review/{content_id}/approve
```

**Request Body:**
```json
{
  "reviewer_id": "user@example.com",
  "reviewer_name": "John Doe",
  "notes": "Optional feedback"
}
```

**Response:**
```json
{
  "status": "approved",
  "content_id": 1
}
```

### Reject AI Decision
```
POST /api/review/{content_id}/reject
```

**Request Body:**
```json
{
  "reviewer_id": "user@example.com",
  "reviewer_name": "John Doe",
  "reason": "AI analysis was incorrect because..."
}
```

### Flag for Investigation
```
POST /api/review/{content_id}/flag
```

**Request Body:**
```json
{
  "reviewer_id": "user@example.com",
  "reviewer_name": "John Doe",
  "reason": "Requires deeper investigation"
}
```

---

## 📊 Analytics Endpoints

### Get Dashboard Overview
```
GET /api/analytics/overview
```

**Response:**
```json
{
  "total_content_analyzed": 1523,
  "misinformation_detected": 87,
  "deepfakes_flagged": 23,
  "accuracy_rate": 94.5,
  "avg_processing_time_ms": 850
}
```

### Get Performance Metrics
```
GET /api/analytics/metrics
```

**Response:**
```json
{
  "accuracy": 94.5,
  "precision": 92.3,
  "recall": 89.7,
  "f1_score": 91.0,
  "avg_latency_ms": 850,
  "human_agreement_rate": 93.2
}
```

### Get Trends
```
GET /api/analytics/trends?days={count}
```

**Query Parameters:**
- `days` (optional): Number of days (default: 7)

**Response:**
```json
{
  "content_analyzed": [
    {"date": "2024-01-15", "count": 45},
    {"date": "2024-01-16", "count": 52}
  ],
  "deepfakes_detected": [
    {"date": "2024-01-15", "count": 3},
    {"date": "2024-01-16", "count": 5}
  ]
}
```

---

## 🔧 System Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "services": "operational"
}
```

---

## 📝 Data Schemas

### Risk Levels
- `low`: Confidence < 40%
- `medium`: Confidence 40-60%
- `high`: Confidence 60-80%
- `critical`: Confidence > 80%

### Fact Check Status
- `True`: Verified as accurate
- `False`: Verified as false
- `Misleading`: Partially true/misleading
- `Unverified`: Cannot verify

### Deepfake Detection
- `is_deepfake`: -1 (uncertain), 0 (no), 1 (yes)
- `deepfake_confidence`: 0.0 to 1.0

---

## ⚠️ Error Responses

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error
