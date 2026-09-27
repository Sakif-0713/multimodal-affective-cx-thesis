import Link from 'next/link';

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Header */}
      <section className="relative overflow-hidden rounded-2xl glass-panel p-8 sm:p-12 border border-indigo-900/40">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-800/60 text-indigo-300 text-xs font-medium">
            <span>✨ Capstone Research & Technical Monorepo</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Multimodal Affective Computing for Enterprise CX Decision Support Systems
          </h1>
          <p className="text-slate-300 text-base sm:text-lg leading-relaxed">
            An empirical investigation fusing text semantic embeddings (RoBERTa), acoustic prosody (Librosa MFCCs & Pitch), and facial expression analysis (MediaPipe + FER at 5 FPS) to detect acute customer dissatisfaction in real-time.
          </p>

          <div className="flex flex-wrap gap-4 pt-2">
            <Link
              href="/submit"
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-semibold text-sm shadow-xl shadow-indigo-600/25 transition-all transform hover:-translate-y-0.5 flex items-center space-x-2"
            >
              <span>🎙️ Launch Customer Review Portal</span>
            </Link>
            <Link
              href="/dashboard"
              className="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-semibold text-sm transition-all flex items-center space-x-2"
            >
              <span>📈 Open BI Triage Dashboard</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Tri-Modal Architecture Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-xl space-y-3 border-t-2 border-t-cyan-500">
          <div className="w-10 h-10 rounded-lg bg-cyan-950/80 text-cyan-400 flex items-center justify-center font-bold text-lg">
            🔤
          </div>
          <h3 className="text-lg font-bold text-white">NLP Text Pipeline</h3>
          <p className="text-sm text-slate-400">
            RoBERTa (<code className="text-xs bg-slate-900 px-1 py-0.5 rounded text-cyan-300">SamLowe/roberta-base-go_emotions</code>) inferring 28 emotion classes mapped to 6 target classes.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-xl space-y-3 border-t-2 border-t-indigo-500">
          <div className="w-10 h-10 rounded-lg bg-indigo-950/80 text-indigo-400 flex items-center justify-center font-bold text-lg">
            🎙️
          </div>
          <h3 className="text-lg font-bold text-white">Acoustic Prosody Pipeline</h3>
          <p className="text-sm text-slate-400">
            Librosa extracting 13 MFCCs, fundamental pitch ($F_0$), Zero-Crossing Rate (ZCR), and RMS energy from raw audio streams.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-xl space-y-3 border-t-2 border-t-purple-500">
          <div className="w-10 h-10 rounded-lg bg-purple-950/80 text-purple-400 flex items-center justify-center font-bold text-lg">
            📹
          </div>
          <h3 className="text-lg font-bold text-white">Vision FER Pipeline</h3>
          <p className="text-sm text-slate-400">
            MediaPipe Face Mesh landmark extraction with 5 FPS frame sampling and MobileNet-FER probability classification.
          </p>
        </div>
      </section>

      {/* Decision-Level Late Fusion Formula */}
      <section className="glass-panel p-8 rounded-2xl border border-slate-800 space-y-6">
        <div className="flex items-center space-x-3">
          <span className="p-2 rounded-lg bg-indigo-950 text-indigo-400 text-xl">🧮</span>
          <h2 className="text-xl font-bold text-white">Mathematical Late Fusion & CSI Index</h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 font-mono text-sm space-y-2">
            <p className="text-slate-400 font-sans text-xs font-semibold uppercase tracking-wider">Late Fusion Formula</p>
            <p className="text-indigo-300 font-semibold text-base">
              Score(e) = w_text * P_text(e) + w_audio * P_audio(e) + w_video * P_video(e)
            </p>
            <p className="text-xs text-slate-400">
              Default Weights: <span className="text-emerald-400">w_text = 0.50</span>, <span className="text-indigo-400">w_audio = 0.25</span>, <span className="text-purple-400">w_video = 0.25</span>
            </p>
          </div>

          <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 font-mono text-sm space-y-2">
            <p className="text-slate-400 font-sans text-xs font-semibold uppercase tracking-wider">Customer Satisfaction Index (CSI)</p>
            <p className="text-emerald-300 font-semibold text-base">
              CSI = (P_joy + 0.5 * P_neutral + 0.5 * P_surprise) * 100
            </p>
            <p className="text-xs text-rose-400">
              Escalation Trigger: Anger + Disappointment &ge; 0.60
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
