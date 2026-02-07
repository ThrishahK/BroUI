import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Result() {
  const navigate = useNavigate();
  const { state } = useLocation();

  // Support both: backend response (total_saved/total_flagged/total_unattempted) and auto-submit (saved/flagged/unattempted)
  const { saved, flagged, unattempted, total_saved, total_flagged, total_unattempted } = state || {};
  const savedCount = saved ?? total_saved ?? 0;
  const flaggedCount = flagged ?? total_flagged ?? 0;
  const unattemptedCount = unattempted ?? total_unattempted ?? 0;

  // #region agent log
  useEffect(() => {
    fetch('http://127.0.0.1:7244/ingest/363f383c-78b1-424a-8ec9-283c7a04277c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'Result.jsx:mount',message:'Result page mounted',data:{stateKeys:state?Object.keys(state):[],savedCount,flaggedCount,unattemptedCount},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'R1'})}).catch(()=>{});
  }, [state, savedCount, flaggedCount, unattemptedCount]);
  // #endregion

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex items-center justify-center">
      <div className="bg-white/10 backdrop-blur-md p-10 rounded-2xl text-center max-w-md">

        <h1 className="text-3xl font-bold mb-4">
          Challenge Submitted Successfully
        </h1>

        <p className="text-gray-300 mb-6">
          You have successfully completed the challenge.  
          Results will be announced soon.
        </p>

        <div className="text-left mb-6 space-y-2">
          <p>Questions Saved: <b>{savedCount}</b></p>
          <p>Questions Flagged: <b>{flaggedCount}</b></p>
          <p>Unattempted Questions: <b>{unattemptedCount}</b></p>
        </div>

        <button
          onClick={() => navigate("/")}
          className="bg-red-600 px-6 py-3 rounded-full
                     hover:scale-105 transition"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
