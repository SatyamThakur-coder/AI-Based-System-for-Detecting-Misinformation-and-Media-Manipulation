'use client'

import { useState } from 'react'
import { DragDropUpload } from '@/components/DragDropUpload'
import { AnalysisResults } from '@/components/AnalysisResults'
import { analysisApi } from '@/lib/api'
import { Loader2, Cpu, Zap } from 'lucide-react'

export default function AnalyzePage() {
    const [analyzing, setAnalyzing] = useState(false)
    const [result, setResult] = useState<any>(null)
    const [error, setError] = useState<string | null>(null)

    const handleFileUpload = async (file: File) => {
        setAnalyzing(true)
        setError(null)
        setResult(null)

        try {
            const formData = new FormData()
            formData.append('file', file)
            const response = await analysisApi.uploadAndAnalyze(formData)
            setResult(response.result)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Analysis failed. Please check if the backend server is running.')
        } finally {
            setAnalyzing(false)
        }
    }

    const handleTextSubmit = async (text: string) => {
        setAnalyzing(true)
        setError(null)
        setResult(null)

        try {
            const formData = new FormData()
            formData.append('text', text)
            const response = await analysisApi.uploadAndAnalyze(formData)
            setResult(response.result)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Analysis failed. Please check if the backend server is running.')
        } finally {
            setAnalyzing(false)
        }
    }

    const handleUrlSubmit = async (url: string) => {
        setAnalyzing(true)
        setError(null)
        setResult(null)

        try {
            const formData = new FormData()
            formData.append('url', url)
            const response = await analysisApi.uploadAndAnalyze(formData)
            setResult(response.result)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Analysis failed. Please check if the backend server is running.')
        } finally {
            setAnalyzing(false)
        }
    }

    return (
        <div className="max-w-5xl mx-auto space-y-8">
            {/* Header */}
            <div className="relative">
                <div className="absolute -top-10 -left-10 w-40 h-40 bg-primary-500/20 rounded-full blur-3xl pointer-events-none" />
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
                    Analyze Content
                </h1>
                <p className="text-gray-400 mt-3 text-lg font-light">
                    Upload media or enter text to detect misinformation and deepfakes
                </p>
            </div>

            {/* Upload Section */}
            <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                <DragDropUpload
                    onFileSelect={handleFileUpload}
                    onTextSubmit={handleTextSubmit}
                    onUrlSubmit={handleUrlSubmit}
                />
            </div>

            {/* Analysis Status */}
            {analyzing && (
                <div className="bg-primary-500/10 border border-primary-500/30 rounded-2xl p-8">
                    <div className="flex items-center gap-5">
                        <div className="relative">
                            <Cpu className="w-10 h-10 text-primary-400" />
                            <div className="absolute inset-0 rounded-full bg-primary-500/30 animate-ping" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-primary-100 text-lg">Analyzing Content...</h3>
                            <p className="text-sm text-primary-300 mt-1">
                                Running deepfake detection, fact-checking, and provenance analysis via Gemini AI
                            </p>
                            <div className="flex gap-2 mt-3">
                                {['Deepfake Detection', 'Fact Checking', 'Provenance'].map((step, i) => (
                                    <span key={i} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary-500/20 text-primary-300 text-xs font-medium">
                                        <Loader2 className="w-3 h-3 animate-spin" />
                                        {step}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-6">
                    <div className="flex items-start gap-4">
                        <div className="w-10 h-10 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
                            <span className="text-red-400 font-bold text-lg">!</span>
                        </div>
                        <div>
                            <h3 className="font-semibold text-red-100">Analysis Error</h3>
                            <p className="text-sm text-red-300 mt-1">{error}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Results Display */}
            {result && !analyzing && (
                <div>
                    <div className="flex items-center gap-3 mb-6">
                        <Zap className="w-5 h-5 text-primary-400" />
                        <h2 className="text-2xl font-bold text-white">Analysis Results</h2>
                    </div>
                    <AnalysisResults result={result} />
                </div>
            )}
        </div>
    )
}
