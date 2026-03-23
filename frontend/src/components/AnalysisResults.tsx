import { AlertTriangle, CheckCircle, XCircle, HelpCircle, Brain, Shield, Database, Newspaper } from 'lucide-react'
import clsx from 'clsx'

interface AnalysisResultsProps {
    result: any
}

export function AnalysisResults({ result }: AnalysisResultsProps) {
    if (!result) return null

    const riskConfig: Record<string, { bg: string; border: string; text: string; badge: string }> = {
        critical: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-300', badge: 'bg-red-500/20 text-red-300' },
        high: { bg: 'bg-orange-500/10', border: 'border-orange-500/30', text: 'text-orange-300', badge: 'bg-orange-500/20 text-orange-300' },
        medium: { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-300', badge: 'bg-yellow-500/20 text-yellow-300' },
        low: { bg: 'bg-green-500/10', border: 'border-green-500/30', text: 'text-green-300', badge: 'bg-green-500/20 text-green-300' },
    }

    const getRiskConfig = (riskLevel: string) => riskConfig[riskLevel] || riskConfig.medium

    const getRiskIcon = (riskLevel: string) => {
        switch (riskLevel) {
            case 'critical':
            case 'high': return <XCircle className="w-7 h-7" />
            case 'medium': return <AlertTriangle className="w-7 h-7" />
            case 'low': return <CheckCircle className="w-7 h-7" />
            default: return <HelpCircle className="w-7 h-7" />
        }
    }

    const risk = getRiskConfig(result.risk_level)
    const confidencePct = Math.round((result.overall_confidence || 0) * 100)

    return (
        <div className="space-y-5">
            {/* Risk Level Banner */}
            <div className={clsx('border rounded-2xl p-6', risk.bg, risk.border)}>
                <div className="flex items-center justify-between flex-wrap gap-4">
                    <div className="flex items-center gap-4">
                        <div className={clsx('p-3 rounded-xl', risk.badge)}>
                            {getRiskIcon(result.risk_level)}
                        </div>
                        <div>
                            <h3 className={clsx('text-xl font-bold capitalize', risk.text)}>
                                {result.risk_level || 'Unknown'} Risk
                            </h3>
                            <p className="text-gray-400 text-sm mt-0.5">AI analysis completed</p>
                        </div>
                    </div>
                    <div className="text-right">
                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Overall Confidence</p>
                        <div className="flex items-center gap-2">
                            <div className="w-24 h-2 bg-gray-800 rounded-full overflow-hidden">
                                <div
                                    className={clsx('h-full rounded-full', risk.badge.split(' ')[0])}
                                    style={{ width: `${confidencePct}%` }}
                                />
                            </div>
                            <span className={clsx('text-2xl font-bold', risk.text)}>{confidencePct}%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Deepfake Detection */}
            {result.is_deepfake !== undefined && result.is_deepfake !== -1 && (
                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <div className="flex items-center gap-3 mb-5">
                        <div className="p-2 rounded-lg bg-purple-500/20">
                            <Shield className="w-5 h-5 text-purple-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-white">Deepfake Detection</h3>
                    </div>
                    <div className="space-y-3">
                        <div className="flex justify-between items-center py-2 border-b border-white/5">
                            <span className="text-gray-400">Status</span>
                            <span className={clsx('font-semibold px-3 py-1 rounded-lg text-sm', result.is_deepfake === 1 ? 'bg-red-500/20 text-red-300' : 'bg-green-500/20 text-green-300')}>
                                {result.is_deepfake === 1 ? '⚠ Manipulation Detected' : '✓ No Manipulation'}
                            </span>
                        </div>
                        <div className="flex justify-between items-center py-2 border-b border-white/5">
                            <span className="text-gray-400">Confidence</span>
                            <span className="font-bold text-white">{Math.round((result.deepfake_confidence || 0) * 100)}%</span>
                        </div>
                        {result.manipulation_type && (
                            <div className="flex justify-between items-center py-2">
                                <span className="text-gray-400">Manipulation Type</span>
                                <span className="font-medium text-gray-200 capitalize">{result.manipulation_type.replace(/_/g, ' ')}</span>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Fact Check Results */}
            {result.fact_check_status && (
                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <div className="flex items-center gap-3 mb-5">
                        <div className="p-2 rounded-lg bg-blue-500/20">
                            <Database className="w-5 h-5 text-blue-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-white">Fact Check</h3>
                    </div>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center py-2 border-b border-white/5">
                            <span className="text-gray-400">Verdict</span>
                            <span className={clsx(
                                'font-semibold px-3 py-1 rounded-lg text-sm',
                                result.fact_check_status === 'True' ? 'bg-green-500/20 text-green-300' :
                                    result.fact_check_status === 'False' ? 'bg-red-500/20 text-red-300' :
                                        result.fact_check_status === 'Misleading' ? 'bg-orange-500/20 text-orange-300' :
                                            'bg-gray-700 text-gray-300'
                            )}>
                                {result.fact_check_status}
                            </span>
                        </div>
                        {result.fact_check_confidence && (
                            <div className="flex justify-between items-center py-2 border-b border-white/5">
                                <span className="text-gray-400">Confidence</span>
                                <span className="font-bold text-white">{Math.round((result.fact_check_confidence || 0) * 100)}%</span>
                            </div>
                        )}

                        {/* Claims */}
                        {result.claims && result.claims.length > 0 && (
                            <div className="mt-4">
                                <p className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wider">Extracted Claims</p>
                                <ul className="space-y-2">
                                    {result.claims.map((claim: string, idx: number) => (
                                        <li key={idx} className="text-sm text-gray-300 bg-gray-800/50 p-3 rounded-xl border-l-2 border-primary-500">
                                            {claim}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Evidence Sources */}
                        {result.evidence && result.evidence.length > 0 && (
                            <div className="mt-4">
                                <p className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wider">Evidence Sources</p>
                                <ul className="space-y-2">
                                    {result.evidence.map((source: any, idx: number) => (
                                        <li key={idx} className="text-sm bg-blue-500/10 border border-blue-500/20 p-4 rounded-xl">
                                            <p className="font-medium text-blue-200">{source.claim || source.source || source.text}</p>
                                            <p className="text-gray-400 mt-1">{source.status || source.explanation}</p>
                                            {(source.url || (source.sources && source.sources[0])) && (
                                                <a
                                                    href={source.url || source.sources[0]}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="text-primary-400 hover:text-primary-300 mt-2 inline-block text-xs underline"
                                                >
                                                    View Source →
                                                </a>
                                            )}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Live News Evidence */}
            {result.news_articles && result.news_articles.length > 0 && (
                <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                    <div className="flex items-center gap-3 mb-5">
                        <div className="p-2 rounded-lg bg-emerald-500/20">
                            <Newspaper className="w-5 h-5 text-emerald-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-white">Live News Evidence</h3>
                        <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full font-medium">
                            {result.news_articles.length} article{result.news_articles.length > 1 ? 's' : ''}
                        </span>
                    </div>
                    <div className="space-y-3">
                        {result.news_articles.map((article: any, idx: number) => (
                            <div key={idx} className="bg-emerald-500/5 border border-emerald-500/15 rounded-xl p-4 hover:border-emerald-500/30 transition-colors">
                                <div className="flex items-start justify-between gap-3">
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-xs font-medium text-emerald-400 bg-emerald-500/15 px-2 py-0.5 rounded">
                                                {article.source}
                                            </span>
                                            {article.published && (
                                                <span className="text-xs text-gray-500">
                                                    {new Date(article.published).toLocaleDateString()}
                                                </span>
                                            )}
                                        </div>
                                        <p className="font-medium text-gray-200 text-sm leading-snug">{article.title}</p>
                                        {article.description && (
                                            <p className="text-xs text-gray-400 mt-1.5 line-clamp-2">{article.description}</p>
                                        )}
                                    </div>
                                    {article.image_url && (
                                        <img
                                            src={article.image_url}
                                            alt=""
                                            className="w-16 h-16 rounded-lg object-cover flex-shrink-0"
                                            onError={(e) => { (e.target as HTMLImageElement).style.display = 'none' }}
                                        />
                                    )}
                                </div>
                                {article.url && (
                                    <a
                                        href={article.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-emerald-400 hover:text-emerald-300 mt-2 inline-block text-xs underline"
                                    >
                                        Read Full Article →
                                    </a>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* AI Explanation */}
            <div className="bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 rounded-lg bg-indigo-500/20">
                        <Brain className="w-5 h-5 text-indigo-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-white">AI Explanation</h3>
                </div>
                <p className="text-gray-300 leading-relaxed">{result.explanation || 'Analysis completed successfully.'}</p>
            </div>

            {/* Processing Info */}
            {result.processing_time_ms && (
                <div className="text-center">
                    <span className="text-xs text-gray-600 bg-gray-800/30 px-4 py-2 rounded-full">
                        ⚡ Analysis completed in {result.processing_time_ms}ms
                    </span>
                </div>
            )}
        </div>
    )
}
