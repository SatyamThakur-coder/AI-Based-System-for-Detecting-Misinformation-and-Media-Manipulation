import { LucideIcon } from 'lucide-react'

interface MetricsCardProps {
    title: string
    value: string | number
    icon: LucideIcon
    change?: number
    iconColor?: string
}

export function MetricsCard({ title, value, icon: Icon, change, iconColor = 'text-primary-600' }: MetricsCardProps) {
    return (
        <div className="relative group bg-gray-900/40 backdrop-blur-md rounded-2xl border border-white/5 p-6 transition-all duration-500 hover:bg-gray-800/50 hover:border-white/10 hover:-translate-y-1">
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500" />
            <div className="relative z-10 flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-400 font-medium tracking-wide uppercase">{title}</p>
                    <p className="text-3xl font-bold mt-2 text-white tracking-tight">{value}</p>
                    {change !== undefined && (
                        <div className={`inline-flex items-center gap-1 mt-3 px-2 py-1 rounded-md text-xs font-medium ${change >= 0 ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                            {change >= 0 ? '+' : ''}{change}% <span className="text-gray-500 font-normal">from last week</span>
                        </div>
                    )}
                </div>
                <div className={`p-4 rounded-xl shadow-lg relative ${iconColor.replace('text-', 'bg-').replace('-600', '-500/20')} backdrop-blur-sm border ${iconColor.replace('text-', 'border-').replace('-600', '-500/20')}`}>
                    <div className={`absolute inset-0 rounded-xl blur-md opacity-50 ${iconColor.replace('text-', 'bg-').replace('-600', '-500')}`} />
                    <Icon className={`w-8 h-8 relative z-10 ${iconColor.replace('-600', '-400')}`} strokeWidth={1.5} />
                </div>
            </div>
        </div>
    )
}
