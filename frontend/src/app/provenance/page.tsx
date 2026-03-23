'use client'

import { useState } from 'react'
import { provenanceApi, contentApi } from '@/lib/api'
import { Fingerprint, Shield, CheckCircle, XCircle, Loader2, Search, FileText, Clock, Hash } from 'lucide-react'
import clsx from 'clsx'

export default function ProvenancePage() {
    const [contentId, setContentId] = useState('')
    const [certificate, setCertificate] = useState<any>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [recentItems, setRecentItems] = useState<any[]>([])
    const [loadedRecent, setLoadedRecent] = useState(false)

    const loadRecent = async () => {
        if (loadedRecent) return
        try {
            const data = await contentApi.getRecent(10)
            setRecentItems(data.items || [])
        } catch (e) {
            // Silently fail
        }
        setLoadedRecent(true)
    }

    const lookupProvenance = async () => {
        if (!contentId.trim()) return
        setLoading(true)
        setError(null)
        setCertificate(null)

        try {
            const data = await provenanceApi.getCertificate(parseInt(contentId))
            setCertificate(data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Content not found or no analysis available.')
        } finally {
            setLoading(false)
        }
    }

    // Load recent items on first render
    if (!loadedRecent) loadRecent()

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            {/* Header */}
            <div className="relative">
                <div className="absolute -top-10 -left-10 w-40 h-40 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
                    Content Provenance
                </h1>
                <p className="text-gray-400 mt-3 text-lg font-light">
                    Track content authenticity with digital fingerprints and certificates
                </p>
            </div>

            {/* Lookup Section */}
            <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Search className="w-5 h-5 text-gray-400" />
                    Lookup Certificate
                </h2>
                <div className="flex gap-3">
                    <input
                        type="number"
                        value={contentId}
                        onChange={(e) => setContentId(e.target.value)}
                        placeholder="Enter Content ID (e.g., 1, 2, 3...)"
                        className="flex-1 bg-gray-800/50 border border-white/10 text-gray-200 placeholder-gray-600 rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                        onKeyDown={(e) => e.key === 'Enter' && lookupProvenance()}
                    />
                    <button
                        onClick={lookupProvenance}
                        disabled={loading || !contentId.trim()}
                        className="px-6 py-3 bg-primary-600 hover:bg-primary-500 text-white rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium flex items-center gap-2"
                    >
                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Fingerprint className="w-4 h-4" />}
                        Verify
                    </button>
                </div>

                {/* Quick select from recent */}
                {recentItems.length > 0 && !certificate && (
                    <div className="mt-4">
                        <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Recent content:</p>
                        <div className="flex flex-wrap gap-2">
                            {recentItems.map((item: any) => (
                                <button
                                    key={item.id}
                                    onClick={() => { setContentId(String(item.id)); }}
                                    className="px-3 py-1.5 bg-gray-800/50 border border-white/5 rounded-lg text-xs text-gray-400 hover:text-white hover:border-primary-500/30 transition-colors"
                                >
                                    #{item.id} — {item.file_name || item.content_type}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* Error */}
            {error && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-6">
                    <div className="flex items-center gap-3">
                        <XCircle className="w-5 h-5 text-red-400" />
                        <p className="text-red-300">{error}</p>
                    </div>
                </div>
            )}

            {/* Certificate Display */}
            {certificate && (
                <div className="space-y-5">
                    {/* Authenticity Banner */}
                    <div className={clsx(
                        'rounded-2xl p-6 border',
                        certificate.certificate?.is_authentic
                            ? 'bg-green-500/10 border-green-500/30'
                            : 'bg-red-500/10 border-red-500/30'
                    )}>
                        <div className="flex items-center gap-4">
                            <div className={clsx(
                                'p-3 rounded-xl',
                                certificate.certificate?.is_authentic ? 'bg-green-500/20' : 'bg-red-500/20'
                            )}>
                                {certificate.certificate?.is_authentic
                                    ? <CheckCircle className="w-8 h-8 text-green-400" />
                                    : <XCircle className="w-8 h-8 text-red-400" />
                                }
                            </div>
                            <div>
                                <h3 className={clsx(
                                    'text-2xl font-bold',
                                    certificate.certificate?.is_authentic ? 'text-green-300' : 'text-red-300'
                                )}>
                                    {certificate.certificate?.is_authentic ? 'Authentic Content' : 'Manipulation Detected'}
                                </h3>
                                <p className="text-gray-400 text-sm mt-0.5">
                                    {certificate.file_name || `Content #${certificate.content_id}`} — {certificate.content_type}
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Certificate Details */}
                    <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                        <div className="flex items-center gap-3 mb-5">
                            <div className="p-2 rounded-lg bg-primary-500/20">
                                <Shield className="w-5 h-5 text-primary-400" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Authenticity Certificate</h3>
                        </div>

                        <div className="space-y-3">
                            {[
                                { label: 'Certificate ID', value: certificate.certificate?.certificate_id, icon: Hash },
                                { label: 'Content ID', value: certificate.content_id, icon: FileText },
                                { label: 'Risk Level', value: (certificate.certificate?.risk_level || 'unknown').toUpperCase() },
                                { label: 'Confidence', value: `${Math.round((certificate.certificate?.confidence || 0) * 100)}%` },
                                { label: 'Issued At', value: certificate.certificate?.issued_at ? new Date(certificate.certificate.issued_at).toLocaleString() : 'N/A', icon: Clock },
                            ].map((row) => (
                                <div key={row.label} className="flex justify-between items-center py-2 border-b border-white/5">
                                    <span className="text-gray-400 text-sm">{row.label}</span>
                                    <span className="font-medium text-gray-200 text-sm">{row.value}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Digital Fingerprint */}
                    <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2 rounded-lg bg-emerald-500/20">
                                <Fingerprint className="w-5 h-5 text-emerald-400" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Digital Fingerprint (SHA-256)</h3>
                        </div>
                        <div className="bg-gray-800/50 rounded-xl p-4 border border-white/5">
                            <code className="text-xs text-emerald-400 font-mono break-all leading-relaxed">
                                {certificate.certificate?.digital_fingerprint || 'N/A'}
                            </code>
                        </div>
                    </div>

                    {/* Analysis Summary */}
                    {certificate.certificate?.analysis_summary && (
                        <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                            <h3 className="text-lg font-semibold text-white mb-4">Analysis Summary</h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {[
                                    {
                                        label: 'Deepfake',
                                        detected: certificate.certificate.analysis_summary.deepfake_detected,
                                    },
                                    {
                                        label: 'Manipulation',
                                        detected: certificate.certificate.analysis_summary.manipulation_detected,
                                    },
                                    {
                                        label: 'Fact Check',
                                        detected: certificate.certificate.analysis_summary.fact_check_status === 'False' || certificate.certificate.analysis_summary.fact_check_status === 'Misleading',
                                        value: certificate.certificate.analysis_summary.fact_check_status,
                                    },
                                ].map((item) => (
                                    <div
                                        key={item.label}
                                        className={clsx(
                                            'p-4 rounded-xl border text-center',
                                            item.detected
                                                ? 'bg-red-500/10 border-red-500/20'
                                                : 'bg-green-500/10 border-green-500/20'
                                        )}
                                    >
                                        <p className="text-sm text-gray-400 mb-1">{item.label}</p>
                                        <p className={clsx(
                                            'font-bold text-lg',
                                            item.detected ? 'text-red-300' : 'text-green-300'
                                        )}>
                                            {item.value || (item.detected ? 'Detected' : 'Clear')}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
