import { useNavigate, useLocation } from "react-router-dom";

export default function Result() {
  const navigate = useNavigate();
  const { state } = useLocation();

  const { saved = 0, flagged = 0, unattempted = 0 } = state || {};

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
          <p>Questions Saved: <b>{saved}</b></p>
          <p>Questions Flagged: <b>{flagged}</b></p>
          <p>Unattempted Questions: <b>{unattempted}</b></p>
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
