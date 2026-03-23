import './globals.css'
import type { Metadata } from 'next'
import { Navigation } from '@/components/Navigation'

export const metadata: Metadata = {
    title: 'AI FactGuard Studio | Combat Misinformation & Deepfakes',
    description: 'AI-powered platform for detecting misinformation and deepfakes in multimodal content',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" className="dark">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
            </head>
            <body className="bg-gray-950 text-gray-100 antialiased selection:bg-primary-500/30">
                <div className="flex min-h-screen relative overflow-hidden">
                    {/* Background Ambient Orbs */}
                    <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-600/10 blur-[120px] pointer-events-none animate-pulse-slow" />
                    <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-600/10 blur-[120px] pointer-events-none animate-pulse-slow" />
                    {/* Sidebar Navigation */}
                    <Navigation />

                    {/* Main Content */}
                    <main className="flex-1 ml-64 p-8 relative z-10">
                        {children}
                    </main>
                </div>
            </body>
        </html>
    )
}
