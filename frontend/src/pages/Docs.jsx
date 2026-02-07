import { useNavigate } from "react-router-dom";

export default function Docs() {
  const navigate = useNavigate();
  const challengeLive = true; // control later from backend

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white overflow-hidden">
      {/* TUI-style top bar */}
      <header className="border-b-2 border-purple-500/50 bg-black/50 backdrop-blur-sm font-mono">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-3">
          <span className="text-purple-400 select-none">[BROCODE]</span>
          <span className="text-gray-500">|</span>
          <span className="text-gray-400">/docs</span>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8 md:py-12">
        {/* TUI frame: main content box */}
        <div
          className="relative rounded-xl overflow-hidden border-2 border-purple-500/40 bg-black/30 backdrop-blur-sm"
          style={{ boxShadow: "0 0 40px rgba(168, 85, 247, 0.15), inset 0 0 80px rgba(0,0,0,0.3)" }}
        >
          {/* Corner brackets (TUI aesthetic) */}
          <div className="absolute top-0 left-0 w-8 h-8 border-l-2 border-t-2 border-purple-400/80 rounded-tl-lg" aria-hidden />
          <div className="absolute top-0 right-0 w-8 h-8 border-r-2 border-t-2 border-purple-400/80 rounded-tr-lg" aria-hidden />
          <div className="absolute bottom-0 left-0 w-8 h-8 border-l-2 border-b-2 border-purple-400/80 rounded-bl-lg" aria-hidden />
          <div className="absolute bottom-0 right-0 w-8 h-8 border-r-2 border-b-2 border-purple-400/80 rounded-br-lg" aria-hidden />

          <div className="p-8 md:p-12 flex flex-col md:flex-row items-center gap-10 md:gap-14">
            {/* Left: poster + title block */}
            <div className="flex flex-col items-center md:items-start flex-shrink-0">
              <div className="relative mb-6 rounded-lg overflow-hidden border-2 border-purple-500/30 shadow-xl shadow-purple-900/30 w-full max-w-[280px] md:max-w-[320px]">
                <img
                  src="/bro.jpeg"
                  alt="CSI Brocode"
                  className="w-full h-auto block"
                />
                <div className="absolute inset-0 rounded-lg ring-2 ring-purple-400/20 pointer-events-none" aria-hidden />
              </div>
              <div className="font-mono text-gray-400 text-sm text-center md:text-left">
                ADAPT • CODE • DOMINATE
              </div>
            </div>

            {/* Right: copy + actions */}
            <div className="text-center md:text-left flex-1">
              <h1 className="text-3xl md:text-4xl font-bold mb-2 font-mono tracking-tight">
                Bro Code Documentation
              </h1>
              <p className="text-gray-300 mb-8 max-w-lg leading-relaxed">
                You are required to carefully go through the Bro Code language
                documentation before starting the challenge. This document contains
                all syntax rules, keywords, and examples allowed during the contest.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                <button
                  onClick={() => {
                    // #region agent log
                    fetch('http://127.0.0.1:7244/ingest/363f383c-78b1-424a-8ec9-283c7a04277c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'Docs.jsx:ReadDocs',message:'Read Documentation clicked',data:{target:'/docs/read'},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D1'})}).catch(()=>{});
                    // #endregion
                    navigate("/docs/read");
                  }}
                  className="px-6 py-3 rounded-lg bg-purple-600 hover:bg-purple-500 border border-purple-400/30 hover:scale-[1.02] transition-all duration-300 font-medium shadow-lg shadow-purple-900/30 hover:shadow-purple-500/20"
                >
                  Read Documentation
                </button>
                <button
                  disabled={!challengeLive}
                  onClick={() => {
                    // #region agent log
                    fetch('http://127.0.0.1:7244/ingest/363f383c-78b1-424a-8ec9-283c7a04277c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'Docs.jsx:StartChallenge',message:'Start Challenge clicked',data:{target:'/challenge'},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D1'})}).catch(()=>{});
                    // #endregion
                    navigate("/challenge");
                  }}
                  className={`px-6 py-3 rounded-lg transition-all duration-300 font-medium border
                    ${challengeLive
                      ? "bg-green-600 hover:bg-green-500 border-green-400/30 hover:scale-[1.02] shadow-lg shadow-green-900/30 hover:shadow-green-500/20"
                      : "bg-gray-600 border-gray-500 cursor-not-allowed"
                    }`}
                >
                  Start Challenge
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Subtle TUI hint */}
        <p className="mt-6 text-center font-mono text-gray-500 text-sm">
          &gt; read docs first, then start challenge
        </p>
      </div>
    </div>
  );
}
