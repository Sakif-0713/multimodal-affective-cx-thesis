import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'Multimodal Affective Computing | CX Decision Support System',
  description: 'An Empirical Investigation into Multimodal Affective Computing for Enterprise Customer Experience Decision Support Systems',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="flex flex-col min-h-screen bg-slate-950 text-slate-100">
        {/* Navigation Bar */}
        <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/60 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                𝚿
              </div>
              <div>
                <span className="font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-indigo-300 text-lg tracking-tight">
                  AffectiveCX
                </span>
                <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-950/80 text-indigo-300 border border-indigo-800/50">
                  Capstone Engine
                </span>
              </div>
            </Link>

            <nav className="flex items-center space-x-1 sm:space-x-4">
              <Link
                href="/submit"
                className="px-3 sm:px-4 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-all flex items-center space-x-2"
              >
                <span>🎙️</span>
                <span className="hidden xs:inline">Customer Portal</span>
              </Link>
              <Link
                href="/dashboard"
                className="px-3 sm:px-4 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-all flex items-center space-x-2"
              >
                <span>📈</span>
                <span className="hidden xs:inline">Executive BI Dashboard</span>
              </Link>
              <div className="pl-2 border-l border-slate-800 flex items-center">
                <span className="flex h-2.5 w-2.5 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
                <span className="ml-2 text-xs font-mono text-emerald-400 font-semibold hidden md:inline">
                  FastAPI: 8000
                </span>
              </div>
            </nav>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0">
            <p>Capstone Thesis Implementation: Multimodal Affective Computing (NLP + Acoustic Prosody + Vision FER)</p>
            <p className="font-mono">FastAPI v0.110 • Next.js 14 • SpaCy • RoBERTa • Librosa • MediaPipe</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
