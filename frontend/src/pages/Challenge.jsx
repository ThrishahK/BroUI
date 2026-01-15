import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Timer from "../components/Timer";
import { useEffect } from "react";


export default function Challenge() {
  const navigate = useNavigate();

  const [current, setCurrent] = useState(1);
  const [uploadedFile, setUploadedFile] = useState(null);
// ---------- FULLSCREEN SHORTCUT ----------
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key.toLowerCase() === "f") {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen();
        } else {
          document.exitFullscreen();
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
  const [questions, setQuestions] = useState(
    Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      status: "not_attempted", // saved | flagged
      text: "",
       answer: "",
    }))
  );

  const markQuestion = (status) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === current ? { ...q, status } : q
      )
    );
  };

  // ---------- RESULT STATS ----------
  const getStats = () => {
    const saved = questions.filter(q => q.status === "saved").length;
    const flagged = questions.filter(q => q.status === "flagged").length;
    const unattempted = questions.filter(q => q.status === "not_attempted").length;
    return { saved, flagged, unattempted };
  };

  // ---------- AUTO SUBMIT ----------
  const autoSubmit = () => {
    const stats = getStats();
    navigate("/result", { state: stats });
  };

  // ---------- MANUAL SUBMIT ----------
  const manualSubmit = () => {
    const confirmSubmit = window.confirm(
      "Are you sure you want to submit the challenge? You will not be able to make changes after submission."
    );

    if (confirmSubmit) {
      const stats = getStats();
      navigate("/result", { state: stats });
    }
  };

  // ---------- FILE UPLOAD ----------
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith(".homie")) {
      alert("Please upload only .homie files.");
      return;
    }

    setUploadedFile(file);
  };

  const currentQuestion = questions.find((q) => q.id === current);

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex relative overflow-hidden">

     

      {/* Sidebar */}
      <div className="w-72 p-4 bg-black/40 backdrop-blur-md grid grid-cols-5 gap-3 z-10">
        {questions.map((q) => {
          const isActive = q.id === current;

          return (
            <button
              key={q.id}
              onClick={() => setCurrent(q.id)}
              className={`h-12 rounded-xl font-bold transition-all duration-300
                hover:scale-110
                ${isActive ? "ring-4 ring-purple-400" : ""}
                ${
                  q.status === "saved"
                    ? "bg-green-500 glow-green"
                    : q.status === "flagged"
                    ? "bg-blue-500 glow-blue"
                    : "bg-red-500"
                }
              `}
            >
              {q.id}
            </button>
          );
        })}
      </div>

      {/* Main */}
      <div className="flex-1 p-10 relative z-10">

        {/* Timer */}
        <div className="absolute top-6 right-10">
          <Timer onTimeUp={autoSubmit} />
        </div>

        <h1 className="text-2xl font-bold mb-6">
          Question {current}
        </h1>

        {/* Question Card */}
        <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl animate-fadeIn">

          {/* Question Display */}
          <div className="mb-6 p-4 rounded-xl bg-black/40 border border-purple-500">
            <h2 className="font-semibold text-purple-300 mb-2">
              Problem Statement
            </h2>
            {currentQuestion.text ? (
              <p className="text-gray-200 whitespace-pre-line">
                {currentQuestion.text}
              </p>
            ) : (
              <p className="text-gray-400 italic">
                Question will appear here when loaded.
              </p>
            )}
          </div>

          {/* File Upload */}
          <div className="mb-4">
            <label className="block mb-2 font-medium text-purple-300">
              Upload Solution File (.homie)
            </label>

            <input
              type="file"
              accept=".homie"
              onChange={handleFileUpload}
              className="block w-full text-sm text-gray-300
                         file:mr-4 file:py-2 file:px-4
                         file:rounded-full file:border-0
                         file:bg-purple-600 file:text-white
                         hover:file:glow-purple"
            />

            {uploadedFile && (
              <p className="mt-2 text-green-400 text-sm">
                Uploaded: {uploadedFile.name}
              </p>
            )}
          </div>

          {/* Code Area */}
          <textarea
  rows="8"
  value={currentQuestion.answer}
  onChange={(e) =>
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === current
          ? { ...q, answer: e.target.value }
          : q
      )
    )
  }
  className="w-full bg-black/30 border border-gray-600 rounded p-3 mb-4
             focus:outline-none focus:ring-2 focus:ring-purple-500"
  placeholder="Write your Bro Code solution here..."
/>

          {/* Bottom Controls */}
          <div className="flex justify-between items-center mt-6">

            {/* Prev / Next */}
            <div className="flex gap-3">
              <button
                disabled={current === 1}
                onClick={() => setCurrent(c => c - 1)}
                className="px-4 py-2 rounded-full bg-gray-700
                           disabled:opacity-40 hover:scale-105 transition"
              >
                Prev
              </button>

              <button
                disabled={current === 30}
                onClick={() => setCurrent(c => c + 1)}
                className="px-4 py-2 rounded-full bg-gray-700
                           disabled:opacity-40 hover:scale-105 transition"
              >
                Next
              </button>
            </div>

            {/* Save / Flag */}
            <div className="flex gap-4">
              <button
                onClick={() => markQuestion("saved")}
                className="bg-green-600 px-4 py-2 rounded-full
                           hover:scale-105 hover:glow-green transition"
              >
                Save
              </button>

              <button
                onClick={() => markQuestion("flagged")}
                className="bg-blue-600 px-4 py-2 rounded-full
                           hover:scale-105 hover:glow-blue transition"
              >
                Flag
              </button>
            </div>
          </div>

          {/* Submit */}
          {current === 30 && (
            <button
              onClick={manualSubmit}
              className="mt-6 bg-purple-600 px-6 py-3 rounded-full
                         hover:scale-105 hover:glow-purple transition"
            >
              Submit Challenge
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
