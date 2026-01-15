import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex items-center justify-center">
      <div className="max-w-2xl text-center">
        <h1 className="text-5xl font-extrabold">
          Welcome to <span className="text-purple-400">Bro Code</span>
        </h1>

        <p className="mt-4 text-gray-300">
          The ultimate syntax vibe check. Please log in to read the Bro Code
          documentation before starting the challenge.
        </p>

        <div className="mt-8 flex justify-center">
          <div className="flex gap-4">
            <button
              onClick={() => navigate("/login")}
              className="px-6 py-3 bg-purple-600 rounded-full
                         hover:scale-105 hover:glow-purple transition-all duration-300"
            >
              Login
            </button>
            <button
              onClick={() => navigate("/leaderboard")}
              className="px-6 py-3 bg-white/10 rounded-full
                         hover:scale-105 transition-all duration-300"
            >
              Leaderboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
