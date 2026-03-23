'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, Upload, CheckSquare, BarChart3, Fingerprint, Shield } from 'lucide-react'
import clsx from 'clsx'

export function Navigation() {
    const pathname = usePathname()

    const navItems = [
        { name: 'Overview', href: '/', icon: Home },
        { name: 'Analyze', href: '/analyze', icon: Upload },
        { name: 'Review Queue', href: '/review', icon: CheckSquare },
        { name: 'Analytics', href: '/analytics', icon: BarChart3 },
        { name: 'Provenance', href: '/provenance', icon: Fingerprint },
    ]

    return (
        <nav className="fixed left-0 top-0 h-screen w-64 bg-gray-950/60 backdrop-blur-2xl border-r border-white/5 px-4 py-6 shadow-[4px_0_24px_-12px_rgba(0,0,0,0.5)] z-50">
            {/* Logo/Brand */}
            <div className="mb-10 px-2 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-primary-500/20 animate-glow">
                    <Shield className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400">FactGuard</h1>
                    <p className="text-[10px] text-primary-400 font-semibold tracking-[0.2em] uppercase">AI Studio</p>
                </div>
            </div>

            {/* Navigation Links */}
            <ul className="space-y-1.5">
                {navItems.map((item) => {
                    const Icon = item.icon
                    const isActive = pathname === item.href

                    return (
                        <li key={item.name}>
                            <Link
                                href={item.href}
                                className={clsx(
                                    'flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300 relative group',
                                    isActive
                                        ? 'text-white bg-white/[0.08] shadow-inner border border-white/10'
                                        : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]'
                                )}
                            >
                                {isActive && (
                                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 rounded-r-full bg-primary-500" />
                                )}
                                <Icon className={clsx("w-[18px] h-[18px] relative z-10 transition-colors duration-300", isActive ? "text-primary-400" : "group-hover:text-gray-300")} />
                                <span className="relative z-10 font-medium tracking-wide text-[13px]">{item.name}</span>
                            </Link>
                        </li>
                    )
                })}
            </ul>

            {/* Footer */}
            <div className="absolute bottom-6 left-4 right-4">
                <div className="p-4 rounded-xl bg-gradient-to-b from-white/[0.03] to-transparent border border-white/5">
                    <div className="flex items-center gap-2 mb-1">
                        <div className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                        </div>
                        <span className="text-[11px] text-gray-400 font-medium tracking-wide">System Online</span>
                    </div>
                    <p className="text-[10px] text-gray-600 mt-0.5">v2.0.0 • SQLite</p>
                </div>
            </div>
        </nav>
    )
}
