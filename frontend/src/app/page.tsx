'use client'

import { useEffect, useState } from 'react'
import { AlertCircle, FileText, Shield, Activity, ArrowRight, Clock } from 'lucide-react'
import { MetricsCard } from '@/components/ui/MetricsCard'
import { analyticsApi, contentApi } from '@/lib/api'

export default function OverviewPage() {
    const [overview, setOverview] = useState<any>(null)
    const [recentItems, setRecentItems] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadOverview()
    }, [])

    const loadOverview = async () => {
        try {
            const [data, recent] = await Promise.all([
                analyticsApi.getOverview(),
                contentApi.getRecent(5).catch(() => ({ items: [] })),
            ])
            setOverview(data)
            setRecentItems(recent.items || [])
        } catch (error) {
            console.error('Failed to load overview:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="relative mb-12">
                <div className="absolute -top-10 -left-10 w-40 h-40 bg-primary-500/20 rounded-full blur-3xl pointer-events-none" />
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
                    Overview Dashboard
                </h1>
                <p className="text-gray-400 mt-3 text-lg font-light tracking-wide">Monitor your content verification activity</p>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricsCard
                    title="Total Analyzed"
                    value={overview?.total_content_analyzed || 0}
                    icon={FileText}
                    iconColor="text-blue-600"
                />
                <MetricsCard
                    title="Misinformation"
                    value={overview?.misinformation_detected || 0}
                    icon={AlertCircle}
                    iconColor="text-red-600"
                />
                <MetricsCard
                    title="Deepfakes"
                    value={overview?.deepfakes_flagged || 0}
                    icon={Shield}
                    iconColor="text-orange-600"
                />
                <MetricsCard
                    title="Accuracy"
                    value={`${overview?.accuracy_rate || 0}%`}
                    icon={Activity}
                    iconColor="text-green-600"
                />
            </div>

            {/* Performance Stats */}
            <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-8 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/15 transition-colors duration-700" />
                <h2 className="text-xl font-semibold mb-6 text-white inline-flex items-center gap-2">
                    <Activity className="w-5 h-5 text-indigo-400" />
                    System Performance
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                    <div>
                        <p className="text-sm text-gray-400 uppercase tracking-wider font-medium">Average Processing Time</p>
                        <div className="flex items-end gap-2 mt-2">
                            <p className="text-4xl font-bold text-white">{Number(overview?.avg_processing_time_ms || 0).toFixed(0)}</p>
                            <span className="text-gray-500 mb-1 font-medium pb-1">ms</span>
                        </div>
                    </div>
                    <div>
                        <p className="text-sm text-gray-400 uppercase tracking-wider font-medium">System Status</p>
                        <div className="flex items-center gap-3 mt-3">
                            <div className="relative flex h-4 w-4">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-4 w-4 bg-green-500 border-2 border-green-800"></span>
                            </div>
                            <p className="text-2xl font-bold text-white tracking-tight">Operational</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Activity */}
            {recentItems.length > 0 && (
                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5 text-gray-400" />
                        Recent Activity
                    </h2>
                    <div className="space-y-2">
                        {recentItems.map((item: any) => (
                            <div
                                key={item.id}
                                className="flex items-center justify-between p-3 rounded-xl bg-gray-800/30 hover:bg-gray-800/50 transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-primary-500/20 flex items-center justify-center">
                                        <FileText className="w-4 h-4 text-primary-400" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-200">{item.file_name || `Content #${item.id}`}</p>
                                        <p className="text-xs text-gray-500 capitalize">{item.content_type}</p>
                                    </div>
                                </div>
                                <span className="text-xs text-gray-600">
                                    {item.created_at ? new Date(item.created_at).toLocaleDateString() : ''}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
                <a
                    href="/analyze"
                    className="relative group overflow-hidden rounded-2xl p-8 cursor-pointer transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_8px_30px_rgba(37,99,235,0.2)]"
                >
                    <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-indigo-800 opacity-90 group-hover:opacity-100 transition-opacity duration-500" />
                    <div className="relative z-10 flex flex-col h-full justify-between">
                        <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center mb-4 text-white border border-white/20">
                            <AlertCircle className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-white mb-2">Analyze Content</h3>
                            <p className="text-primary-100 text-sm leading-relaxed">Upload and verify media for misinformation using multimodal AI models.</p>
                        </div>
                        <ArrowRight className="w-5 h-5 text-white/50 group-hover:text-white group-hover:translate-x-1 transition-all mt-4" />
                    </div>
                </a>

                <a
                    href="/review"
                    className="bg-gray-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-8 hover:bg-gray-800/60 transition-all duration-500 hover:-translate-y-2 cursor-pointer group"
                >
                    <div className="w-12 h-12 rounded-xl bg-gray-800 flex items-center justify-center mb-4 text-gray-300 border border-white/10 group-hover:border-primary-500/50 group-hover:text-primary-400 transition-colors">
                        <Shield className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-200 mb-2 group-hover:text-white transition-colors">Review Queue</h3>
                    <p className="text-gray-500 text-sm leading-relaxed group-hover:text-gray-400 transition-colors">Check flagged content requiring human review and domain expertise.</p>
                </a>

                <a
                    href="/analytics"
                    className="bg-gray-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-8 hover:bg-gray-800/60 transition-all duration-500 hover:-translate-y-2 cursor-pointer group"
                >
                    <div className="w-12 h-12 rounded-xl bg-gray-800 flex items-center justify-center mb-4 text-gray-300 border border-white/10 group-hover:border-indigo-500/50 group-hover:text-indigo-400 transition-colors">
                        <FileText className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-200 mb-2 group-hover:text-white transition-colors">View Analytics</h3>
                    <p className="text-gray-500 text-sm leading-relaxed group-hover:text-gray-400 transition-colors">Generate detailed metrics and performance reports over time.</p>
                </a>
            </div>
        </div>
    )
}
