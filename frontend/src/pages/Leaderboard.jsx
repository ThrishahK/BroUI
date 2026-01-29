import { useEffect, useState } from "react";
import { leaderboardAPI } from "../utils/api";

export default function Leaderboard() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const data = await leaderboardAPI.getLeaderboard();
      setRows(Array.isArray(data) ? data : []);
    } finally {
      setLoading(false);
    }
  };

  // Auto refresh every 30s
  useEffect(() => {
    load();
    const i = setInterval(load, 30000);
    return () => clearInterval(i);
  }, []);

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-8">
      <div className="w-full max-w-3xl animate-fadeIn">

        {/* Title */}
        <h1 className="text-center text-4xl font-extrabold mb-8 tracking-widest">
          🏆 LEADERBOARD
        </h1>

        {loading && <p className="text-center text-gray-400">Loading…</p>}

        {!loading && (
          <div className="space-y-4">
            {rows.map((r, i) => {
              const rank = i + 1;

              return (
                <div
                  key={i}
                  className={`flex items-center justify-between px-6 py-4 rounded-xl
                    transition hover:scale-[1.02]
                    ${rank === 1 ? "bg-yellow-500/20 glow-yellow" : ""}
                    ${rank === 2 ? "bg-gray-400/20" : ""}
                    ${rank === 3 ? "bg-orange-400/20" : ""}
                    ${rank > 3 ? "bg-white/10" : ""}
                  `}
                >
                  {/* Rank */}
                  <div className="text-3xl font-black w-14 text-center">
                    {rank === 1 ? "👑" : rank}
                  </div>

                  {/* Team */}
                  <div className="flex-1 px-4">
                    <div className="text-xl font-bold">
                      {r.team_name}
                    </div>
                    <div className="text-sm text-gray-400">
                      {r.team_leader_usn}
                    </div>
                  </div>

                  {/* Solved */}
                  <div className="text-center w-20">
                    <div className="text-sm text-gray-400">Solved</div>
                    <div className="font-bold">{r.solved}</div>
                  </div>

                  {/* Score */}
                  <div className="text-2xl font-extrabold text-purple-300 w-24 text-right">
                    {r.score}
                  </div>
                </div>
              );
            })}

            {rows.length === 0 && (
              <p className="text-center text-gray-400">No teams yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
