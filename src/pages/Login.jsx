import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [usn, setUsn] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    const cleanedUSN = usn.trim().toUpperCase();
    const cleanedPassword = password.trim();

    if (!cleanedUSN || !cleanedPassword) {
      alert("Both Team Leader USN and Password are required.");
      return;
    }

    // Store for later use if needed
    localStorage.setItem("team_leader_usn", cleanedUSN);

    navigate("/docs");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 flex items-center justify-center text-white">
      <div className="bg-white/10 backdrop-blur-md p-8 rounded-2xl w-96">

        <h2 className="text-2xl font-bold mb-6 text-center">
          Team Login
        </h2>

        {/* USN */}
        <input
          value={usn}
          onChange={(e) => setUsn(e.target.value)}
          placeholder="Team Leader USN"
          className="w-full p-3 mb-4 rounded bg-black/30 border border-gray-600
                     focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        {/* Password */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="w-full p-3 mb-6 rounded bg-black/30 border border-gray-600
                     focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <button
          onClick={handleLogin}
          className="w-full bg-purple-600 py-3 rounded-full
                     hover:scale-105 hover:glow-purple transition-all duration-300"
        >
          Login
        </button>
      </div>
    </div>
  );
}
