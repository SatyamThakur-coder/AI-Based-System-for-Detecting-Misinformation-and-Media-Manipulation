'use client'

import { useEffect, useState } from 'react'
import { reviewApi } from '@/lib/api'
import { CheckCircle, XCircle, Flag, Loader2, AlertTriangle, Shield, Clock, Users } from 'lucide-react'
import clsx from 'clsx'

export default function ReviewPage() {
    const [queue, setQueue] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [selectedItem, setSelectedItem] = useState<any>(null)
    const [actionLoading, setActionLoading] = useState(false)
    const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null)

    useEffect(() => { loadQueue() }, [])

    const loadQueue = async () => {
        try {
            const data = await reviewApi.getQueue()
            setQueue(data.items || [])
        } catch (error) {
            console.error('Failed to load review queue:', error)
        } finally {
            setLoading(false)
        }
    }

    const showFeedback = (type: 'success' | 'error', message: string) => {
        setFeedback({ type, message })
        setTimeout(() => setFeedback(null), 3000)
    }

    const handleApprove = async (contentId: number) => {
        setActionLoading(true)
        try {
            await reviewApi.approve(contentId, 'current-user', 'Human Reviewer', 'Approved after review')
            showFeedback('success', 'Decision approved successfully!')
            await loadQueue()
            setSelectedItem(null)
        } catch (error) {
            showFeedback('error', 'Failed to approve. Please try again.')
        } finally {
            setActionLoading(false)
        }
    }

    const handleReject = async (contentId: number) => {
        const reason = prompt('Please provide a reason for rejection:')
        if (!reason) return
        setActionLoading(true)
        try {
            await reviewApi.reject(contentId, 'current-user', 'Human Reviewer', reason)
            showFeedback('success', 'Content rejected successfully.')
            await loadQueue()
            setSelectedItem(null)
        } catch (error) {
            showFeedback('error', 'Failed to reject. Please try again.')
        } finally {
            setActionLoading(false)
        }
    }

    const handleFlag = async (contentId: number) => {
        const reason = prompt('Please provide a reason for flagging:')
        if (!reason) return
        setActionLoading(true)
        try {
            await reviewApi.flag(contentId, 'current-user', 'Human Reviewer', reason)
            showFeedback('success', 'Content flagged for investigation.')
            await loadQueue()
            setSelectedItem(null)
        } catch (error) {
            showFeedback('error', 'Failed to flag. Please try again.')
        } finally {
            setActionLoading(false)
        }
    }

    const getRiskStyle = (level: string) => {
        switch (level) {
            case 'critical': return 'bg-red-500/20 text-red-300 border-red-500/30'
            case 'high': return 'bg-orange-500/20 text-orange-300 border-orange-500/30'
            case 'medium': return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
            default: return 'bg-green-500/20 text-green-300 border-green-500/30'
        }
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-64 gap-4">
                <Loader2 className="w-10 h-10 text-primary-400 animate-spin" />
                <p className="text-gray-500">Loading review queue...</p>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="relative">
                <div className="absolute -top-10 -left-10 w-40 h-40 bg-orange-500/10 rounded-full blur-3xl pointer-events-none" />
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
                    Review Queue
                </h1>
                <p className="text-gray-400 mt-3 text-lg font-light">Review flagged content requiring human verification</p>
            </div>

            {/* Feedback Toast */}
            {feedback && (
                <div className={clsx(
                    'fixed top-6 right-6 z-50 px-5 py-3 rounded-xl border text-sm font-medium shadow-xl transition-all',
                    feedback.type === 'success' ? 'bg-green-500/20 border-green-500/30 text-green-300' : 'bg-red-500/20 border-red-500/30 text-red-300'
                )}>
                    {feedback.message}
                </div>
            )}

            {/* Queue Stats */}
            <div className="grid grid-cols-3 gap-4">
                {[
                    { label: 'Pending', value: queue.length, icon: Clock, color: 'text-blue-400 bg-blue-500/20' },
                    { label: 'High Risk', value: queue.filter(i => i.analysis?.risk_level === 'high' || i.analysis?.risk_level === 'critical').length, icon: AlertTriangle, color: 'text-red-400 bg-red-500/20' },
                    { label: 'Reviewed', value: queue.filter(i => i.reviewed).length, icon: Users, color: 'text-green-400 bg-green-500/20' },
                ].map((stat) => {
                    const Icon = stat.icon
                    return (
                        <div key={stat.label} className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-5 flex items-center gap-4">
                            <div className={clsx('p-3 rounded-xl', stat.color)}>
                                <Icon className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-500 uppercase tracking-wide">{stat.label}</p>
                                <p className="text-3xl font-bold text-white">{stat.value}</p>
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Queue List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Queue Items */}
                <div className="space-y-3">
                    <h2 className="text-lg font-semibold text-gray-300">Pending Items</h2>

                    {queue.length === 0 ? (
                        <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-10 text-center">
                            <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-3" />
                            <p className="text-gray-400 font-medium">No items in review queue</p>
                            <p className="text-gray-600 text-sm mt-1">All analyzed content has been reviewed</p>
                        </div>
                    ) : (
                        queue.map((item) => (
                            <div
                                key={item.content_id}
                                onClick={() => setSelectedItem(item)}
                                className={clsx(
                                    'bg-gray-900/40 backdrop-blur-md rounded-2xl border p-4 cursor-pointer transition-all duration-200 hover:bg-gray-800/50',
                                    selectedItem?.content_id === item.content_id
                                        ? 'border-primary-500/50 shadow-lg shadow-primary-500/10'
                                        : 'border-white/5 hover:border-white/10'
                                )}
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <p className="font-semibold text-gray-200">{item.file_name || `Content #${item.content_id}`}</p>
                                        <p className="text-xs text-gray-500 mt-0.5 capitalize">{item.content_type}</p>
                                    </div>
                                    {item.analysis?.risk_level && (
                                        <span className={clsx('px-2.5 py-1 rounded-lg text-xs font-semibold border', getRiskStyle(item.analysis.risk_level))}>
                                            {item.analysis.risk_level.toUpperCase()}
                                        </span>
                                    )}
                                </div>

                                <div className="space-y-1 text-sm">
                                    {item.analysis?.is_deepfake === 1 && (
                                        <p className="text-red-400 flex items-center gap-1.5">
                                            <Shield className="w-3.5 h-3.5" />
                                            Deepfake detected ({Math.round((item.analysis.deepfake_confidence || 0) * 100)}% confidence)
                                        </p>
                                    )}
                                    {item.analysis?.fact_check_status && (
                                        <p className="text-orange-400 flex items-center gap-1.5">
                                            <AlertTriangle className="w-3.5 h-3.5" />
                                            Fact check: {item.analysis.fact_check_status}
                                        </p>
                                    )}
                                    {item.reviewed && (
                                        <p className="text-green-400 flex items-center gap-1.5">
                                            <CheckCircle className="w-3.5 h-3.5" />
                                            Reviewed: {item.review_decision}
                                        </p>
                                    )}
                                </div>

                                <p className="text-xs text-gray-600 mt-3">
                                    {new Date(item.upload_timestamp).toLocaleString()}
                                </p>
                            </div>
                        ))
                    )}
                </div>

                {/* Review Panel */}
                <div className="lg:sticky lg:top-8">
                    {selectedItem ? (
                        <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6 space-y-6">
                            <div>
                                <h2 className="text-xl font-semibold text-white">Review Details</h2>
                                <p className="text-sm text-gray-500 mt-1">{selectedItem.file_name || `Content #${selectedItem.content_id}`}</p>
                            </div>

                            {/* AI Analysis Summary */}
                            {selectedItem.analysis && (
                                <div className="space-y-3">
                                    <h3 className="font-semibold text-gray-300 uppercase text-xs tracking-wider">AI Analysis Summary</h3>
                                    <div className="space-y-2">
                                        <div className="flex justify-between items-center py-2 border-b border-white/5">
                                            <span className="text-gray-400 text-sm">Risk Level</span>
                                            <span className={clsx('font-semibold text-sm px-2.5 py-1 rounded-lg border', getRiskStyle(selectedItem.analysis.risk_level))}>
                                                {(selectedItem.analysis.risk_level || 'unknown').toUpperCase()}
                                            </span>
                                        </div>
                                        {selectedItem.analysis.is_deepfake !== -1 && selectedItem.analysis.is_deepfake !== undefined && (
                                            <div className="flex justify-between items-center py-2 border-b border-white/5">
                                                <span className="text-gray-400 text-sm">Deepfake</span>
                                                <span className={clsx('font-semibold text-sm', selectedItem.analysis.is_deepfake === 1 ? 'text-red-400' : 'text-green-400')}>
                                                    {selectedItem.analysis.is_deepfake === 1 ? 'Detected' : 'Not Detected'}
                                                </span>
                                            </div>
                                        )}
                                        {selectedItem.analysis.fact_check_status && (
                                            <div className="flex justify-between items-center py-2 border-b border-white/5">
                                                <span className="text-gray-400 text-sm">Fact Check</span>
                                                <span className="font-semibold text-sm text-gray-200">{selectedItem.analysis.fact_check_status}</span>
                                            </div>
                                        )}
                                    </div>

                                    {selectedItem.analysis.explanation && (
                                        <div className="mt-4 p-4 bg-gray-800/50 rounded-xl">
                                            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Explanation</p>
                                            <p className="text-sm text-gray-300 leading-relaxed">{selectedItem.analysis.explanation}</p>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Action Buttons */}
                            {!selectedItem.reviewed ? (
                                <div className="space-y-3">
                                    <h3 className="font-semibold text-gray-300 uppercase text-xs tracking-wider">Take Action</h3>
                                    <button
                                        onClick={() => handleApprove(selectedItem.content_id)}
                                        disabled={actionLoading}
                                        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 hover:bg-green-500 text-white rounded-xl disabled:opacity-40 transition-colors font-medium"
                                    >
                                        {actionLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle className="w-4 h-4" />}
                                        Approve AI Decision
                                    </button>
                                    <button
                                        onClick={() => handleReject(selectedItem.content_id)}
                                        disabled={actionLoading}
                                        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-red-600 hover:bg-red-500 text-white rounded-xl disabled:opacity-40 transition-colors font-medium"
                                    >
                                        <XCircle className="w-4 h-4" />
                                        Reject AI Decision
                                    </button>
                                    <button
                                        onClick={() => handleFlag(selectedItem.content_id)}
                                        disabled={actionLoading}
                                        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-orange-300 border border-orange-500/30 rounded-xl disabled:opacity-40 transition-colors font-medium"
                                    >
                                        <Flag className="w-4 h-4" />
                                        Flag for Investigation
                                    </button>
                                </div>
                            ) : (
                                <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-4 text-center">
                                    <CheckCircle className="w-8 h-8 text-green-400 mx-auto mb-2" />
                                    <p className="font-semibold text-green-300">Already Reviewed</p>
                                    <p className="text-sm text-green-500 mt-1">Decision: {selectedItem.review_decision}</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-10 text-center">
                            <Shield className="w-12 h-12 text-gray-600 mx-auto mb-3" />
                            <p className="text-gray-400 font-medium">Select an item to review</p>
                            <p className="text-gray-600 text-sm mt-1">Click on a queue item on the left</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
