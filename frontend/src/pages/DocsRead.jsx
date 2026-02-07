import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

/**
 * DocsRead – stream/documentation viewer at /docs/read.
 * Renders the Bro Code PDF in-page so everyone can read without downloading.
 */
export default function DocsRead() {
  const navigate = useNavigate();
  const pdfUrl = "/BroCode_Documentation.pdf";

  // #region agent log
  useEffect(() => {
    fetch('http://127.0.0.1:7244/ingest/363f383c-78b1-424a-8ec9-283c7a04277c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'DocsRead.jsx:mount',message:'DocsRead page mounted',data:{path:'/docs/read'},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D1'})}).catch(()=>{});
  }, []);
  // #endregion

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white">
      {/* TUI-style top bar */}
      <header className="border-b-2 border-purple-500/50 bg-black/60 backdrop-blur-sm font-mono">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-purple-400 select-none">[BROCODE]</span>
            <span className="text-gray-400">|</span>
            <span className="text-gray-300">docs/read</span>
          </div>
          <button
            onClick={() => navigate("/docs")}
            className="px-4 py-2 rounded border border-purple-500/60 text-purple-300 hover:bg-purple-500/20 hover:border-purple-400 transition-all duration-200 font-mono text-sm"
          >
            ← Back to /docs
          </button>
        </div>
      </header>

      {/* TUI frame around viewer */}
      <main className="max-w-7xl mx-auto p-4 md:p-6">
        <div
          className="relative rounded-lg overflow-hidden border-2 border-purple-500/40 bg-black/40 shadow-lg shadow-purple-900/20"
          style={{ boxShadow: "inset 0 0 60px rgba(168, 85, 247, 0.05)" }}
        >
          {/* Corner accents (TUI style) */}
          <div className="absolute top-0 left-0 w-6 h-6 border-l-2 border-t-2 border-purple-400/70 rounded-tl" aria-hidden />
          <div className="absolute top-0 right-0 w-6 h-6 border-r-2 border-t-2 border-purple-400/70 rounded-tr" aria-hidden />
          <div className="absolute bottom-0 left-0 w-6 h-6 border-l-2 border-b-2 border-purple-400/70 rounded-bl" aria-hidden />
          <div className="absolute bottom-0 right-0 w-6 h-6 border-r-2 border-b-2 border-purple-400/70 rounded-br" aria-hidden />

          <div className="p-2 md:p-3">
            <div className="bg-gray-900/80 rounded border border-gray-700/50 overflow-hidden" style={{ minHeight: "calc(100vh - 12rem)" }}>
              <iframe
                title="Bro Code Documentation"
                src={`${pdfUrl}#toolbar=1&navpanes=1&scrollbar=1`}
                className="w-full h-[calc(100vh-14rem)] min-h-[600px] rounded"
                allow="fullscreen"
              />
            </div>
          </div>
        </div>

        <p className="mt-3 text-center text-gray-400 font-mono text-sm">
          Document streams in-browser. No download required.
        </p>
      </main>
    </div>
  );
}
