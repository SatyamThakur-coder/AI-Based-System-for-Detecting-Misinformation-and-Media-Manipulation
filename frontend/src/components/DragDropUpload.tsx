'use client'

import { useState, useCallback } from 'react'
import { Upload as UploadIcon, X, FileText, Image as ImageIcon, Video, Music, Link, Type } from 'lucide-react'
import clsx from 'clsx'

interface DragDropUploadProps {
    onFileSelect: (file: File) => void
    onTextSubmit?: (text: string) => void
    onUrlSubmit?: (url: string) => void
    acceptedTypes?: string[]
}

export function DragDropUpload({ onFileSelect, onTextSubmit, onUrlSubmit, acceptedTypes }: DragDropUploadProps) {
    const [isDragging, setIsDragging] = useState(false)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [inputMode, setInputMode] = useState<'file' | 'text' | 'url'>('file')
    const [textInput, setTextInput] = useState('')
    const [urlInput, setUrlInput] = useState('')

    const handleDrag = useCallback((e: React.DragEvent) => { e.preventDefault(); e.stopPropagation() }, [])
    const handleDragIn = useCallback((e: React.DragEvent) => { e.preventDefault(); e.stopPropagation(); setIsDragging(true) }, [])
    const handleDragOut = useCallback((e: React.DragEvent) => { e.preventDefault(); e.stopPropagation(); setIsDragging(false) }, [])

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        setIsDragging(false)
        const files = e.dataTransfer.files
        if (files && files.length > 0) {
            const file = files[0]
            setSelectedFile(file)
            onFileSelect(file)
        }
    }, [onFileSelect])

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files
        if (files && files.length > 0) {
            const file = files[0]
            setSelectedFile(file)
            onFileSelect(file)
        }
    }

    const getFileIcon = (file: File) => {
        if (file.type.startsWith('image/')) return ImageIcon
        if (file.type.startsWith('video/')) return Video
        if (file.type.startsWith('audio/')) return Music
        return FileText
    }

    const tabs = [
        { id: 'file', label: 'Upload File', icon: UploadIcon },
        { id: 'text', label: 'Text Input', icon: Type },
        { id: 'url', label: 'From URL', icon: Link },
    ] as const

    return (
        <div className="space-y-5">
            {/* Input Mode Tabs */}
            <div className="flex gap-1 bg-gray-800/50 rounded-xl p-1">
                {tabs.map(tab => {
                    const Icon = tab.icon
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setInputMode(tab.id)}
                            className={clsx(
                                'flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                                inputMode === tab.id
                                    ? 'bg-gray-700 text-white shadow-sm'
                                    : 'text-gray-400 hover:text-gray-200'
                            )}
                        >
                            <Icon className="w-4 h-4" />
                            {tab.label}
                        </button>
                    )
                })}
            </div>

            {/* File Upload Area */}
            {inputMode === 'file' && (
                <div
                    onDragEnter={handleDragIn}
                    onDragLeave={handleDragOut}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={clsx(
                        'border-2 border-dashed rounded-xl p-10 text-center transition-all duration-300',
                        isDragging
                            ? 'border-primary-500 bg-primary-500/10'
                            : 'border-white/10 hover:border-white/20 bg-gray-800/20'
                    )}
                >
                    {selectedFile ? (
                        <div className="flex items-center justify-center gap-4">
                            {(() => {
                                const Icon = getFileIcon(selectedFile)
                                return <Icon className="w-12 h-12 text-primary-400" />
                            })()}
                            <div className="text-left">
                                <p className="font-medium text-white">{selectedFile.name}</p>
                                <p className="text-sm text-gray-400">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                            <button
                                onClick={() => setSelectedFile(null)}
                                className="ml-4 p-2 rounded-lg hover:bg-red-500/20 text-gray-400 hover:text-red-400 transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                    ) : (
                        <>
                            <div className="mx-auto w-16 h-16 rounded-2xl bg-gray-700/50 flex items-center justify-center mb-4">
                                <UploadIcon className="w-8 h-8 text-gray-400" />
                            </div>
                            <p className="mt-2 text-lg font-medium text-gray-200">Drag and drop your file here</p>
                            <p className="text-gray-500 mt-1">or click to browse files</p>
                            <p className="text-sm text-gray-600 mt-2">Supports images, videos, audio files (max 100MB)</p>
                            <input
                                type="file"
                                onChange={handleFileInput}
                                className="hidden"
                                id="file-upload"
                                accept={acceptedTypes?.join(',') || 'image/*,video/*,audio/*'}
                            />
                            <label
                                htmlFor="file-upload"
                                className="mt-5 inline-block px-6 py-2.5 bg-primary-600 hover:bg-primary-500 text-white rounded-xl cursor-pointer transition-colors font-medium"
                            >
                                Choose File
                            </label>
                        </>
                    )}
                </div>
            )}

            {/* Text Input */}
            {inputMode === 'text' && (
                <div className="space-y-3">
                    <textarea
                        value={textInput}
                        onChange={(e) => setTextInput(e.target.value)}
                        placeholder="Enter text to analyze for misinformation (e.g., news article, claim, tweet)..."
                        className="w-full h-48 bg-gray-800/50 border border-white/10 text-gray-200 placeholder-gray-600 rounded-xl p-4 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all resize-none"
                    />
                    <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-500">{textInput.length} characters</span>
                        <button
                            onClick={() => onTextSubmit?.(textInput)}
                            disabled={!textInput.trim()}
                            className="px-6 py-2.5 bg-primary-600 hover:bg-primary-500 text-white rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium"
                        >
                            Analyze Text
                        </button>
                    </div>
                </div>
            )}

            {/* URL Input */}
            {inputMode === 'url' && (
                <div className="space-y-3">
                    <input
                        type="url"
                        value={urlInput}
                        onChange={(e) => setUrlInput(e.target.value)}
                        placeholder="https://example.com/article-to-check"
                        className="w-full bg-gray-800/50 border border-white/10 text-gray-200 placeholder-gray-600 rounded-xl p-4 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                    />
                    <div className="flex justify-end">
                        <button
                            onClick={() => onUrlSubmit?.(urlInput)}
                            disabled={!urlInput.trim()}
                            className="px-6 py-2.5 bg-primary-600 hover:bg-primary-500 text-white rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium"
                        >
                            Analyze URL
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}
