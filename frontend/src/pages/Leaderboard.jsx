import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { leaderboardAPI } from "../utils/api";

export default function Leaderboard() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await leaderboardAPI.getLeaderboard();
      setRows(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Failed to load leaderboard:", e);
      setError("Failed to load leaderboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Leaderboard</h1>
          <div className="flex gap-3">
            <button
              onClick={load}
              className="bg-purple-600 px-4 py-2 rounded-full hover:scale-105 transition"
            >
              Refresh
            </button>
            <button
              onClick={() => navigate("/")}
              className="bg-gray-700 px-4 py-2 rounded-full hover:scale-105 transition"
            >
              Home
            </button>
          </div>
        </div>

        {loading && <p className="text-gray-300">Loading...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && !error && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl overflow-hidden">
            <table className="w-full text-left">
              <thead className="bg-black/40">
                <tr>
                  <th className="p-4">Rank</th>
                  <th className="p-4">Team</th>
                  <th className="p-4">USN</th>
                  <th className="p-4">Solved</th>
                  <th className="p-4">Score</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.team_id} className="border-t border-white/10">
                    <td className="p-4 font-bold">{r.rank}</td>
                    <td className="p-4">{r.team_name || "—"}</td>
                    <td className="p-4">{r.team_leader_usn}</td>
                    <td className="p-4">{r.solved}</td>
                    <td className="p-4 font-bold text-purple-300">{r.score}</td>
                  </tr>
                ))}
                {rows.length === 0 && (
                  <tr>
                    <td className="p-4 text-gray-400" colSpan={5}>
                      No teams yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

