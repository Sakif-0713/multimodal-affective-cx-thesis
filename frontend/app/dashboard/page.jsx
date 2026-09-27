'use client';

import { useState, useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid
} from 'recharts';
import { AlertTriangle, CheckCircle2, Send, RefreshCw, Filter, ShieldAlert, Award, Zap } from 'lucide-react';

// Simulated Real-Time Dataset representing Enterprise CX Submissions
const INITIAL_SUBMISSIONS = [
  {
    id: 'SUB-9801',
    timestamp: '12:04:12',
    customer: 'Enterprise Client #1042',
    text: 'My credit card was charged twice for the billing cycle and customer support line has been disconnected for hours!',
    dominant: 'anger',
    csi: 14.5,
    angerDisappointment: 0.88,
    isAcute: true,
    touchpoint: 'billing',
    modalities: ['text', 'audio', 'video'],
    probs: { anger: 0.62, disappointment: 0.26, neutral: 0.05, joy: 0.01, sadness: 0.04, surprise: 0.02 },
    status: 'pending'
  },
  {
    id: 'SUB-9802',
    timestamp: '11:58:45',
    customer: 'Standard User #5021',
    text: 'The package arrived three days late and the outer box was crushed. Very disappointed with delivery.',
    dominant: 'disappointment',
    csi: 22.0,
    angerDisappointment: 0.74,
    isAcute: true,
    touchpoint: 'delivery',
    modalities: ['text', 'audio'],
    probs: { anger: 0.24, disappointment: 0.50, neutral: 0.15, joy: 0.02, sadness: 0.07, surprise: 0.02 },
    status: 'pending'
  },
  {
    id: 'SUB-9803',
    timestamp: '11:42:10',
    customer: 'Premium VIP #8812',
    text: 'The new UI navigation update looks sleek and smooth. Checkout was effortless.',
    dominant: 'joy',
    csi: 92.5,
    angerDisappointment: 0.04,
    isAcute: false,
    touchpoint: 'ui_ux',
    modalities: ['text', 'video'],
    probs: { anger: 0.01, disappointment: 0.03, neutral: 0.10, joy: 0.82, sadness: 0.01, surprise: 0.03 },
    status: 'resolved'
  },
  {
    id: 'SUB-9804',
    timestamp: '11:30:19',
    customer: 'Corporate Account #209',
    text: 'The app crashes every time I try to open invoice settings. Please fix this bug.',
    dominant: 'disappointment',
    csi: 35.0,
    angerDisappointment: 0.61,
    isAcute: true,
    touchpoint: 'ui_ux',
    modalities: ['text', 'audio', 'video'],
    probs: { anger: 0.31, disappointment: 0.30, neutral: 0.25, joy: 0.04, sadness: 0.08, surprise: 0.02 },
    status: 'pending'
  },
  {
    id: 'SUB-9805',
    timestamp: '11:15:02',
    customer: 'Retail Buyer #3190',
    text: 'Recieved my replacement item. Helpful support representative on the phone.',
    dominant: 'joy',
    csi: 86.0,
    angerDisappointment: 0.08,
    isAcute: false,
    touchpoint: 'customer_support',
    modalities: ['text', 'audio'],
    probs: { anger: 0.02, disappointment: 0.06, neutral: 0.20, joy: 0.68, sadness: 0.01, surprise: 0.03 },
    status: 'resolved'
  }
];

const EMOTION_COLORS = {
  anger: '#ef4444',
  disappointment: '#f97316',
  neutral: '#64748b',
  joy: '#10b981',
  sadness: '#3b82f6',
  surprise: '#8b5cf6'
};

export default function DashboardPage() {
  const [submissions, setSubmissions] = useState(INITIAL_SUBMISSIONS);
  const [touchpointFilter, setTouchpointFilter] = useState('all');
  const [riskFilter, setRiskFilter] = useState('all');
  const [selectedCase, setSelectedCase] = useState(null);
  const [dispatchingId, setDispatchingId] = useState(null);
  const [dispatchSuccess, setDispatchSuccess] = useState(null);

  // Filtered dataset
  const filteredData = useMemo(() => {
    return submissions.filter(item => {
      const matchTouchpoint = touchpointFilter === 'all' || item.touchpoint === touchpointFilter;
      const matchRisk = riskFilter === 'all' || (riskFilter === 'acute' ? item.isAcute : !item.isAcute);
      return matchTouchpoint && matchRisk;
    });
  }, [submissions, touchpointFilter, riskFilter]);

  // Aggregate Metrics
  const totalSubmissions = submissions.length;
  const acuteAlerts = submissions.filter(s => s.isAcute).length;
  const acuteRate = ((acuteAlerts / totalSubmissions) * 100).toFixed(1);
  const avgCSI = (submissions.reduce((acc, curr) => acc + curr.csi, 0) / totalSubmissions).toFixed(1);
  const pendingEscalations = submissions.filter(s => s.isAcute && s.status === 'pending').length;

  // Emotion Aggregates for Recharts Pie/Bar
  const emotionChartData = useMemo(() => {
    const totals = { anger: 0, disappointment: 0, neutral: 0, joy: 0, sadness: 0, surprise: 0 };
    submissions.forEach(sub => {
      Object.keys(totals).forEach(key => {
        totals[key] += sub.probs[key] || 0;
      });
    });
    return Object.keys(totals).map(key => ({
      name: key.toUpperCase(),
      value: Number((totals[key] / submissions.length * 100).toFixed(1)),
      color: EMOTION_COLORS[key]
    }));
  }, [submissions]);

  // Touchpoint Friction Chart Data
  const touchpointFrictionData = useMemo(() => {
    const friction = {};
    submissions.forEach(sub => {
      const tp = sub.touchpoint.toUpperCase();
      if (!friction[tp]) friction[tp] = { touchpoint: tp, acuteCount: 0, total: 0 };
      friction[tp].total += 1;
      if (sub.isAcute) friction[tp].acuteCount += 1;
    });
    return Object.values(friction);
  }, [submissions]);

  // Timeline Trend Data
  const timelineData = [
    { time: '09:00', csi: 72.0, acuteAlerts: 1 },
    { time: '10:00', csi: 68.5, acuteAlerts: 2 },
    { time: '11:00', csi: 54.0, acuteAlerts: 3 },
    { time: '12:00', csi: 49.2, acuteAlerts: 4 }
  ];

  // Webhook Escalation Trigger Simulation
  const handleDispatchEscalation = (id) => {
    setDispatchingId(id);
    setTimeout(() => {
      setSubmissions(prev => prev.map(s => s.id === id ? { ...s, status: 'dispatched' } : s));
      setDispatchingId(null);
      setDispatchSuccess(`Escalation ticket for ${id} dispatched to Executive PagerDuty & Slack channel!`);
      setTimeout(() => setDispatchSuccess(null), 5000);
    }, 1200);
  };

  return (
    <div className="space-y-8">
      {/* Dashboard Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
            <span>📈</span> Executive BI Triage & Affective Decision Support
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time decision support system monitoring acute customer dissatisfaction ($\text&#123;Anger&#125; + \text&#123;Disappointment&#125; \ge 0.60$).
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setSubmissions([...INITIAL_SUBMISSIONS])}
            className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700/80 text-xs font-semibold text-slate-300 hover:text-white flex items-center space-x-1.5 transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh Feed</span>
          </button>
        </div>
      </div>

      {dispatchSuccess && (
        <div className="p-4 rounded-xl bg-emerald-950/90 border border-emerald-700/80 text-emerald-200 text-sm flex items-center justify-between animate-in fade-in duration-300">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span>{dispatchSuccess}</span>
          </div>
          <button onClick={() => setDispatchSuccess(null)} className="text-emerald-400 font-bold">&times;</button>
        </div>
      )}

      {/* KPI Key Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-indigo-500 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Total Ingested Triage</span>
          <div className="flex justify-between items-baseline">
            <span className="text-3xl font-extrabold text-white font-mono">{totalSubmissions}</span>
            <span className="text-xs text-indigo-400 font-semibold">+12% vs last hour</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-rose-500 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Acute Dissatisfaction Rate</span>
          <div className="flex justify-between items-baseline">
            <span className="text-3xl font-extrabold text-rose-400 font-mono">{acuteRate}%</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-800 font-semibold">
              High Risk
            </span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-emerald-500 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Average CSI Index</span>
          <div className="flex justify-between items-baseline">
            <span className="text-3xl font-extrabold text-emerald-400 font-mono">{avgCSI} / 100</span>
            <span className="text-xs text-emerald-400 font-semibold">Target &ge; 70.0</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-amber-500 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Pending Escalations</span>
          <div className="flex justify-between items-baseline">
            <span className="text-3xl font-extrabold text-amber-400 font-mono">{pendingEscalations}</span>
            <span className="text-xs text-amber-400 font-semibold">Action Required</span>
          </div>
        </div>
      </div>

      {/* Analytics Visualizers Grid (Recharts) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Emotion Distribution */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center justify-between">
            <span>Fused Emotion Distribution Breakdown</span>
            <span className="text-xs font-mono text-slate-400">6 Target Classes</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={emotionChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {emotionChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Touchpoint Friction Heatmap */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center justify-between">
            <span>Aspect Touchpoint Friction Analysis</span>
            <span className="text-xs font-mono text-slate-400">MABSA Categories</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={touchpointFrictionData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="touchpoint" stroke="#94a3b8" fontSize={10} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="total" name="Total Feedbacks" fill="#6366f1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="acuteCount" name="Acute Dissatisfaction" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Acute Dissatisfaction Alert & Escalation Feed */}
      <div className="glass-panel p-6 rounded-2xl space-y-6 border border-rose-900/30">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-6 h-6 text-rose-500 animate-pulse" />
            <div>
              <h3 className="text-lg font-bold text-white">Real-Time BI Acute Dissatisfaction Queue</h3>
              <p className="text-xs text-slate-400">Filterable feedback queue flagged by multimodal late fusion engine.</p>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center space-x-1.5 text-xs">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-400">Touchpoint:</span>
              <select
                value={touchpointFilter}
                onChange={(e) => setTouchpointFilter(e.target.value)}
                className="bg-slate-900 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1 font-mono text-xs outline-none"
              >
                <option value="all">All Touchpoints</option>
                <option value="billing">Billing</option>
                <option value="delivery">Delivery</option>
                <option value="ui_ux">UI / UX</option>
                <option value="customer_support">Customer Support</option>
              </select>
            </div>

            <div className="flex items-center space-x-1.5 text-xs">
              <span className="text-slate-400">Risk Level:</span>
              <select
                value={riskFilter}
                onChange={(e) => setRiskFilter(e.target.value)}
                className="bg-slate-900 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1 font-mono text-xs outline-none"
              >
                <option value="all">All Risk Tiers</option>
                <option value="acute">Acute Only (&ge;0.60)</option>
                <option value="normal">Normal Baseline</option>
              </select>
            </div>
          </div>
        </div>

        {/* Feedback Cards Feed */}
        <div className="space-y-4">
          {filteredData.map((item) => (
            <div
              key={item.id}
              className={`p-5 rounded-xl border transition-all ${
                item.isAcute
                  ? 'bg-rose-950/40 border-rose-800/60 hover:border-rose-600'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <div className="space-y-2 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-mono font-bold text-slate-300">{item.id}</span>
                    <span className="text-xs text-slate-500 font-mono">• {item.timestamp}</span>
                    <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {item.customer}
                    </span>
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded-full bg-indigo-950 text-indigo-300 border border-indigo-800">
                      📍 {item.touchpoint.toUpperCase()}
                    </span>
                    {item.isAcute && (
                      <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-rose-600 text-white animate-pulse">
                        ACUTE ESCALATION
                      </span>
                    )}
                  </div>

                  <p className="text-sm text-slate-200 font-medium italic">&quot;{item.text}&quot;</p>

                  <div className="flex flex-wrap items-center gap-4 text-xs font-mono pt-1">
                    <span className="text-slate-400">
                      Dominant: <strong className="text-white capitalize">{item.dominant}</strong>
                    </span>
                    <span className="text-slate-400">
                      Anger+Disappointment: <strong className={item.isAcute ? 'text-rose-400' : 'text-emerald-400'}>
                        {(item.angerDisappointment * 100).toFixed(0)}%
                      </strong>
                    </span>
                    <span className="text-slate-400">
                      CSI: <strong className={item.csi < 50 ? 'text-rose-400' : 'text-emerald-400'}>{item.csi}</strong>
                    </span>
                  </div>
                </div>

                {/* Dispatch Trigger Action Button */}
                <div className="flex items-center space-x-3 shrink-0 w-full lg:w-auto justify-end">
                  {item.status === 'dispatched' ? (
                    <span className="px-4 py-2 rounded-xl bg-emerald-950 border border-emerald-700 text-emerald-300 text-xs font-mono font-bold flex items-center space-x-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      <span>Ticket Dispatched</span>
                    </span>
                  ) : item.isAcute ? (
                    <button
                      onClick={() => handleDispatchEscalation(item.id)}
                      disabled={dispatchingId === item.id}
                      className="px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center space-x-2 transition-all shadow-lg shadow-rose-600/30"
                    >
                      {dispatchingId === item.id ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <Zap className="w-4 h-4" />
                      )}
                      <span>Dispatch CX Escalation</span>
                    </button>
                  ) : (
                    <span className="text-xs text-slate-500 font-mono italic">No Action Needed</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
