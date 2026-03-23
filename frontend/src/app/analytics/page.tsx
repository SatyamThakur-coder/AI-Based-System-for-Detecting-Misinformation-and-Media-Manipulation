'use client'

import { useEffect, useState } from 'react'
import { analyticsApi } from '@/lib/api'
import { Loader2, TrendingUp, Target, Zap, Users, BarChart3, Database, Sparkles } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

const CHART_THEME = {
    grid: '#1f2937',
    axis: '#4b5563',
    tooltip: {
        contentStyle: { background: '#111827', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', color: '#e5e7eb' },
        labelStyle: { color: '#9ca3af' },
    }
}

export default function AnalyticsPage() {
    const [metrics, setMetrics] = useState<any>(null)
    const [overview, setOverview] = useState<any>(null)
    const [trends, setTrends] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [seeding, setSeeding] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => { loadAnalytics() }, [])

    const loadAnalytics = async () => {
        setLoading(true)
        try {
            const [metricsData, trendsData, overviewData] = await Promise.all([
                analyticsApi.getMetrics(),
                analyticsApi.getTrends(7),
                analyticsApi.getOverview(),
            ])
            setMetrics(metricsData)
            setTrends(trendsData)
            setOverview(overviewData)
        } catch (e) {
            setError('Failed to load analytics data. Please check if the backend server is running.')
        } finally {
            setLoading(false)
        }
    }

    const seedDemoData = async () => {
        setSeeding(true)
        try {
            await axios.post(`${API_BASE}/analytics/seed-demo`)
            await loadAnalytics()
        } catch (e) {
            console.error('Failed to seed demo data:', e)
        } finally {
            setSeeding(false)
        }
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-64 gap-4">
                <Loader2 className="w-10 h-10 text-primary-400 animate-spin" />
                <p className="text-gray-500">Loading analytics data...</p>
            </div>
        )
    }

    if (error) {
        return (
            <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-8 text-center">
                <p className="text-red-300 font-medium">{error}</p>
            </div>
        )
    }

    const metricCards = [
        { label: 'Accuracy', value: metrics?.accuracy, icon: Target, color: 'text-blue-400', bar: 'bg-blue-500', glow: 'bg-blue-500/20' },
        { label: 'Precision', value: metrics?.precision, icon: TrendingUp, color: 'text-green-400', bar: 'bg-green-500', glow: 'bg-green-500/20' },
        { label: 'Recall', value: metrics?.recall, icon: Target, color: 'text-purple-400', bar: 'bg-purple-500', glow: 'bg-purple-500/20' },
        { label: 'F1 Score', value: metrics?.f1_score, icon: Users, color: 'text-orange-400', bar: 'bg-orange-500', glow: 'bg-orange-500/20' },
    ]

    const needsData = metrics?.needs_reviews && (!trends?.content_analyzed?.length || trends.content_analyzed.length <= 1)

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="relative flex items-start justify-between">
                <div>
                    <div className="absolute -top-10 -left-10 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
                    <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
                        Analytics & Reports
                    </h1>
                    <p className="text-gray-400 mt-3 text-lg font-light">Performance metrics and detection trends</p>
                </div>
                <button
                    onClick={seedDemoData}
                    disabled={seeding}
                    className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl disabled:opacity-50 transition-colors font-medium flex items-center gap-2 text-sm shadow-lg shadow-indigo-500/20"
                >
                    {seeding ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    {seeding ? 'Generating...' : 'Generate Demo Data'}
                </button>
            </div>

            {/* Info banner when no data */}
            {needsData && (
                <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-2xl p-5 flex items-center gap-4">
                    <div className="p-2 rounded-lg bg-indigo-500/20 shrink-0">
                        <Database className="w-5 h-5 text-indigo-400" />
                    </div>
                    <div>
                        <p className="text-indigo-200 font-medium">Analytics need data to display</p>
                        <p className="text-indigo-300/60 text-sm mt-0.5">
                            Click <strong>&quot;Generate Demo Data&quot;</strong> to populate the analytics with 7 days of realistic sample data,
                            or analyze content and submit reviews to generate real metrics.
                        </p>
                    </div>
                </div>
            )}

            {/* Overview Stats Row */}
            {overview && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                        { label: 'Total Analyzed', value: overview.total_content_analyzed, color: 'text-blue-400' },
                        { label: 'Misinformation', value: overview.misinformation_detected, color: 'text-red-400' },
                        { label: 'Deepfakes', value: overview.deepfakes_flagged, color: 'text-orange-400' },
                        { label: 'Reviews', value: overview.total_reviews || metrics?.total_reviews || 0, color: 'text-green-400' },
                    ].map((stat) => (
                        <div key={stat.label} className="bg-gray-900/40 backdrop-blur-md rounded-xl border border-white/5 p-4 text-center">
                            <p className="text-xs text-gray-500 uppercase tracking-wider">{stat.label}</p>
                            <p className={`text-3xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
                        </div>
                    ))}
                </div>
            )}

            {/* Performance Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                {metricCards.map((card) => {
                    const Icon = card.icon
                    const val = card.value?.toFixed(1) || '0.0'
                    return (
                        <div key={card.label} className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-5 relative group overflow-hidden hover:-translate-y-1 transition-transform duration-300">
                            <div className={`absolute top-0 right-0 w-24 h-24 rounded-full blur-3xl opacity-20 group-hover:opacity-30 transition-opacity ${card.glow}`} />
                            <div className="flex items-center justify-between mb-3">
                                <p className="text-sm text-gray-400 uppercase tracking-wider font-medium">{card.label}</p>
                                <div className={`p-2 rounded-lg ${card.glow}`}>
                                    <Icon className={`w-4 h-4 ${card.color}`} />
                                </div>
                            </div>
                            <p className={`text-4xl font-bold ${card.color}`}>{val}<span className="text-lg text-gray-500">%</span></p>
                            <div className="mt-3 bg-gray-800 rounded-full h-1.5 overflow-hidden">
                                <div className={`${card.bar} h-full rounded-full transition-all duration-1000`} style={{ width: `${card.value || 0}%` }} />
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* System Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <div className="flex items-center gap-3 mb-1">
                        <div className="p-2 rounded-lg bg-yellow-500/20">
                            <Zap className="w-5 h-5 text-yellow-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-white">Average Latency</h3>
                    </div>
                    <p className="text-5xl font-bold text-white mt-4">
                        {metrics?.avg_latency_ms?.toFixed(0) || overview?.avg_processing_time_ms?.toFixed(0) || 0}
                        <span className="text-xl text-gray-500 ml-1">ms</span>
                    </p>
                    <p className="text-sm text-gray-500 mt-2">Per content analysis</p>
                </div>

                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <div className="flex items-center gap-3 mb-1">
                        <div className="p-2 rounded-lg bg-indigo-500/20">
                            <Users className="w-5 h-5 text-indigo-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-white">Human Agreement Rate</h3>
                    </div>
                    <p className="text-5xl font-bold text-white mt-4">
                        {metrics?.human_agreement_rate?.toFixed(1) || 0}
                        <span className="text-xl text-gray-500 ml-1">%</span>
                    </p>
                    <p className="text-sm text-gray-500 mt-2">AI decisions validated by reviewers</p>
                </div>
            </div>

            {/* Trend Charts */}
            {trends && (
                <div className="space-y-5">
                    <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-2 rounded-lg bg-primary-500/20">
                                <BarChart3 className="w-5 h-5 text-primary-400" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Content Analyzed (Last 7 Days)</h3>
                        </div>
                        {trends.content_analyzed?.length > 0 ? (
                            <ResponsiveContainer width="100%" height={260}>
                                <LineChart data={trends.content_analyzed}>
                                    <CartesianGrid strokeDasharray="3 3" stroke={CHART_THEME.grid} />
                                    <XAxis dataKey="date" stroke={CHART_THEME.axis} tick={{ fill: '#6b7280', fontSize: 12 }} />
                                    <YAxis stroke={CHART_THEME.axis} tick={{ fill: '#6b7280', fontSize: 12 }} />
                                    <Tooltip {...CHART_THEME.tooltip} />
                                    <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2.5} dot={{ fill: '#3b82f6', r: 4 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="h-64 flex items-center justify-center">
                                <p className="text-gray-600">No trend data yet. Analyze some content or generate demo data.</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-2 rounded-lg bg-red-500/20">
                                <BarChart3 className="w-5 h-5 text-red-400" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Deepfakes Detected (Last 7 Days)</h3>
                        </div>
                        {trends.deepfakes_detected?.length > 0 ? (
                            <ResponsiveContainer width="100%" height={260}>
                                <BarChart data={trends.deepfakes_detected}>
                                    <CartesianGrid strokeDasharray="3 3" stroke={CHART_THEME.grid} />
                                    <XAxis dataKey="date" stroke={CHART_THEME.axis} tick={{ fill: '#6b7280', fontSize: 12 }} />
                                    <YAxis stroke={CHART_THEME.axis} tick={{ fill: '#6b7280', fontSize: 12 }} />
                                    <Tooltip {...CHART_THEME.tooltip} />
                                    <Bar dataKey="count" fill="#ef4444" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="h-64 flex items-center justify-center">
                                <p className="text-gray-600">No deepfakes detected in the last 7 days.</p>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Evaluation Summary */}
            <div className="relative rounded-2xl p-8 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-primary-800/40 to-indigo-900/40 rounded-2xl" />
                <div className="absolute inset-0 border border-primary-500/20 rounded-2xl" />
                <div className="relative z-10">
                    <h3 className="text-2xl font-bold text-white mb-6">Evaluation Summary</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {[
                            { label: 'Accuracy', value: metrics?.accuracy },
                            { label: 'Precision', value: metrics?.precision },
                            { label: 'Recall', value: metrics?.recall },
                            { label: 'F1 Score', value: metrics?.f1_score },
                        ].map((item) => (
                            <div key={item.label}>
                                <p className="text-primary-300 text-sm mb-1">{item.label}</p>
                                <p className="text-4xl font-bold text-white">{item.value?.toFixed(1) || '0.0'}<span className="text-lg text-primary-400">%</span></p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
