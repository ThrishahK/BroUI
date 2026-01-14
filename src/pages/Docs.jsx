import { useNavigate } from "react-router-dom";

export default function Docs() {
  const navigate = useNavigate();
  const challengeLive = true; // control later from backend

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex items-center justify-center">
      
      <div className="text-center max-w-2xl">

        <h1 className="text-4xl font-bold mb-4">
          Bro Code Documentation
        </h1>

        <p className="text-gray-300 mb-6">
          You are required to carefully go through the Bro Code language
          documentation before starting the challenge. This document contains
          all syntax rules, keywords, and examples allowed during the contest.
        </p>

        <a
          href="/BroCode_Documentation.pdf"
          download
          className="inline-block mb-8 bg-purple-600 px-6 py-3 rounded-full
                     hover:scale-105 hover:glow-purple transition-all duration-300"
        >
          Download Documentation
        </a>

        <div>
          <button
            disabled={!challengeLive}
            onClick={() => navigate("/challenge")}
            className={`px-8 py-3 rounded-full transition-all duration-300
              ${
                challengeLive
                  ? "bg-green-600 hover:scale-105 hover:glow-green"
                  : "bg-gray-600 cursor-not-allowed"
              }
            `}
          >
            Start Challenge
          </button>
        </div>

      </div>
    </div>
  );
}
