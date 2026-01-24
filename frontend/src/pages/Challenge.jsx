import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Timer from "../components/Timer";
import { challengeAPI, questionsAPI } from "../utils/api";
import questionsData from "../data/questions.json";

export default function Challenge() {
  const navigate = useNavigate();

  const [current, setCurrent] = useState(0); // Track question index (0-based)
  const [questions, setQuestions] = useState([]);
  const [_submissions, setSubmissions] = useState([]);
  const [_session, setSession] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [executeStatus, setExecuteStatus] = useState({}); // { [questionId]: { loading, result, attempts } }

  // Shuffle array utility
  const shuffleArray = (array) => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

  // Initialize challenge on component mount
  useEffect(() => {
    const initializeChallenge = async () => {
      try {
        setIsLoading(true);
        setError("");

        // Step 1: Try to start challenge session (or get existing one)
        let sessionData;
        try {
          sessionData = await challengeAPI.startChallenge();
          setSession(sessionData.session);
        } catch (err) {
          // If session already exists, just get the status instead
          if (err.message.includes("already has an active")) {
            console.log("Session already exists, loading status...");
            const statusData = await challengeAPI.getChallengeStatus();
            setSession(statusData.session);
          } else {
            throw err;
          }
        }

        // Step 2: Fetch all active questions from backend
        const apiQuestions = await questionsAPI.getPublicQuestions();
        console.log("Fetched questions:", apiQuestions);

        if (!apiQuestions || apiQuestions.length === 0) {
          throw new Error("No questions available from backend");
        }

        // Step 3: Initialize questions with API data
        const initializedQuestions = apiQuestions.map((q) => ({
          id: q.id,
          question_id: q.question_id, // E01, M04, H10, etc.
          title: q.title,
          description: q.description,
          sample_input: q.sample_input,
          sample_output: q.sample_output,
          difficulty: q.difficulty,
          points: q.points,
          status: "not_attempted",
          answer: "",
          attempts: 0,
          is_correct: false,
          is_locked: false,
          last_result: null,
        }));

        // Step 4: Group questions by difficulty in ascending order (no shuffling)
        const easyQuestions = initializedQuestions.filter(q => q.question_id?.startsWith('E')).sort((a, b) => a.question_id.localeCompare(b.question_id));
        const mediumQuestions = initializedQuestions.filter(q => q.question_id?.startsWith('M')).sort((a, b) => a.question_id.localeCompare(b.question_id));
        const hardQuestions = initializedQuestions.filter(q => q.question_id?.startsWith('H')).sort((a, b) => a.question_id.localeCompare(b.question_id));
        
        // Combine: E, M, H (in ascending order)
        const orderedQuestions = [...easyQuestions, ...mediumQuestions, ...hardQuestions];
        setQuestions(orderedQuestions);

        // Step 5: Get initial challenge status and merge with questions
        const statusData = await challengeAPI.getChallengeStatus();
        setSubmissions(statusData.submissions || []);

        // Merge submission execution state into questions
        const submissionByQid = new Map(
          (statusData.submissions || []).map((s) => [s.question_id, s])
        );

        setQuestions((prev) =>
          prev.map((q) => {
            const s = submissionByQid.get(q.id);
            return s
              ? {
                  ...q,
                  status: s.status || q.status,
                  answer: s.code_answer ?? q.answer,
                  is_correct: !!s.is_correct,
                  is_locked: !!s.is_locked,
                  attempts: s.attempts ?? 0,
                  last_result: s.last_result ?? null,
                }
              : q;
          })
        );
      } catch (error) {
        console.error("Failed to initialize challenge:", error);
        setError(error.message || "Failed to start challenge. Please try logging in again.");
        navigate("/login");
      } finally {
        setIsLoading(false);
      }
    };

    initializeChallenge();
  }, [navigate]);

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

  // (initializeChallenge moved inside useEffect to satisfy hook deps)

  const markQuestion = async (status) => {
    const currentQ = questions[current];
    if (!currentQ) return;

    try {
      // Update question status locally first for immediate UI feedback
      setQuestions((prev) =>
        prev.map((q) =>
          q.id === currentQ.id ? { ...q, status } : q
        )
      );

      // Update submission via API
      await challengeAPI.updateSubmission(currentQ.id, {
        code_answer: currentQ.answer,
        status: status,
      });
    } catch (error) {
      console.error("Failed to update submission:", error);
      // Revert local change on error
      setQuestions((prev) =>
        prev.map((q) =>
          q.id === currentQ.id ? { ...q, status: "not_attempted" } : q
        )
      );
    }
  };

  const executeCurrent = async () => {
    const q = questions[current];
    if (!q) return;
    if (q.is_locked || q.is_correct) {
      alert("This question is already correct and locked!");
      return;
    }

    if (!q.answer || q.answer.trim() === "") {
      alert("Please write some code before executing!");
      return;
    }

    try {
      setExecuteStatus((prev) => ({ ...prev, [q.id]: { loading: true } }));
      console.log(`Executing question ${q.id} with code:`, q.answer);

      const res = await challengeAPI.executeSubmission(q.id, q.answer);
      console.log("Execution result:", res);

      // Update the question with the result
      setQuestions((prev) =>
        prev.map((item) =>
          item.id === q.id
            ? {
                ...item,
                attempts: res.attempts,
                last_result: res.result,
                is_correct: res.is_correct,
                is_locked: res.is_locked,
                status: res.is_correct ? "submitted" : item.status,
              }
            : item
        )
      );

      setExecuteStatus((prev) => ({
        ...prev,
        [q.id]: { 
          loading: false, 
          result: res.result, 
          attempts: res.attempts,
          resultMessage: res.is_correct ? "✅ Correct!" : "❌ Wrong. Try again!"
        },
      }));
    } catch (e) {
      console.error("Execute failed:", e);
      setExecuteStatus((prev) => ({ 
        ...prev, 
        [q.id]: { loading: false, error: true, errorMessage: e.message } 
      }));
      alert("Execute failed: " + e.message);
    }
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
  const manualSubmit = async () => {
    const confirmSubmit = window.confirm(
      "Are you sure you want to submit the challenge? You will not be able to make changes after submission."
    );

    if (confirmSubmit) {
      try {
        // Prepare submissions data - only include non-empty answers
        const submissions = questions
          .filter(q => q.answer && q.answer.trim() !== "")
          .map(q => ({
            question_id: q.id,
            code_answer: q.answer,
            status: q.status,
          }));

        console.log("Submitting challenge with submissions:", submissions);

        // Submit challenge
        const response = await challengeAPI.submitChallenge(submissions);
        console.log("Submission response:", response);

        // Navigate to result page with stats
        navigate("/result", { state: response });
      } catch (error) {
        console.error("Failed to submit challenge:", error);
        alert("Failed to submit challenge: " + error.message);
      }
    }
  };

  const currentQuestion = questions[current];
  const execState = executeStatus[currentQuestion?.id] || {};

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto mb-4"></div>
          <p className="text-gray-300">Loading challenge...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex items-center justify-center">
        <div className="text-center max-w-md">
          <h2 className="text-2xl font-bold text-red-400 mb-4">Error</h2>
          <p className="text-gray-300 mb-6">{error}</p>
          <button
            onClick={() => navigate("/login")}
            className="bg-purple-600 px-6 py-3 rounded-full hover:scale-105 transition"
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white flex relative overflow-hidden">

     

      
      {/* Sidebar */}
<div className="w-80 p-6 bg-black/40 backdrop-blur-md flex flex-col gap-6 z-10 border-r border-purple-500/30 overflow-y-auto">
  <h2 className="text-xl font-bold text-purple-400 mb-2 px-2">Challenges</h2>
  
  {[
    { label: "Level 1: Easy", range: questions.slice(0, 10) },
    { label: "Level 2: Medium", range: questions.slice(10, 20) },
    { label: "Level 3: Hard", range: questions.slice(20, 30) }
  ].map((group, gIdx) => (
    <div key={gIdx} className="animate-fadeIn">
      <p className="text-[10px] text-gray-500 mb-3 px-2 uppercase tracking-[0.2em] font-bold">
        {group.label}
      </p>
      <div className="grid grid-cols-5 gap-2">
        {group.range.map((q) => {
          const globalIdx = questions.findIndex(item => item.id === q.id);
          const isActive = globalIdx === current;

          return (
            <button
              key={q.id}
              onClick={() => setCurrent(globalIdx)}
              className={`h-10 w-full rounded-lg font-bold text-xs transition-all duration-300
                ${isActive ? "ring-2 ring-white scale-110 z-20" : "opacity-80 hover:opacity-100"}
                ${
                  q.is_correct ? "bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.4)]" :
                  q.status === "flagged" ? "bg-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.4)]" :
                  q.attempts > 0 ? "bg-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.4)]" :
                  "bg-red-500/40 border border-red-500/50"
                }
              `}
            >
              {q.id}
            </button>
          );
        })}
      </div>
    </div>
  ))}
</div>

      {/* Main */}
      <div className="flex-1 p-10 relative z-10">

        {/* Timer */}
        <div className="absolute top-6 right-10">
          <Timer onTimeUp={autoSubmit} />
        </div>

        <h1 className="text-2xl font-bold mb-6">
          Question {current + 1} {currentQuestion?.question_id && `(${currentQuestion.question_id})`}
        </h1>

        {/* Question Card */}
        <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl animate-fadeIn">

          {/* Question Display */}
          <div className="mb-6 p-4 rounded-xl bg-black/40 border border-purple-500">
            <h2 className="font-semibold text-purple-300 mb-2">
              Problem Statement
            </h2>
            {currentQuestion ? (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-purple-200">
                  {currentQuestion.title}
                </h3>
                <p className="text-gray-200 whitespace-pre-line">
                  {currentQuestion.description}
                </p>
                
                {/* Hardcoded Input Instructions */}
                {/* {currentQuestion.question_id && questionsData[currentQuestion.question_id] && (
                  <div className="bg-yellow-900/30 border-2 border-yellow-500 rounded-lg p-4">
                    <h4 className="text-yellow-300 font-bold mb-2 flex items-center gap-2">
                      <span>⚠️</span>
                      <span>Use these input values:</span>
                    </h4>
                    <div className="bg-black/60 p-3 rounded text-lg text-green-300 font-mono">
                      {questionsData[currentQuestion.question_id].hardcodedInput
                        .split('\n')
                        .map(line => {
                          const match = line.match(/=\s*(.+);/);
                          return match ? match[1].trim() : null;
                        })
                        .filter(Boolean)
                        .join(', ')}
                    </div>
                  </div>
                )} */}

                {currentQuestion.sample_input && (
                  <div>
                    <h4 className="text-purple-300 font-medium mb-1">Sample Input:</h4>
                    <pre className="bg-black/50 p-2 rounded text-sm text-gray-300">
                      {currentQuestion.sample_input}
                    </pre>
                  </div>
                )}
                {currentQuestion.sample_output && (
                  <div>
                    <h4 className="text-purple-300 font-medium mb-1">Expected Output:</h4>
                    <pre className="bg-black/50 p-2 rounded text-sm text-gray-300">
                      {currentQuestion.sample_output}
                    </pre>
                  </div>
                )}
                <div className="flex gap-4 text-sm">
                  <span className="text-blue-400">Difficulty: {currentQuestion.difficulty}</span>
                  <span className="text-green-400">Points: {currentQuestion.points}</span>
                </div>
              </div>
            ) : (
              <p className="text-gray-400 italic">
                Loading question...
              </p>
            )}
          </div>

          {/* Code Area */}
          <textarea
  rows="8"
  value={currentQuestion?.answer || ""}
  onChange={(e) =>
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === currentQuestion?.id
          ? { ...q, answer: e.target.value }
          : q
      )
    )
  }
  className="w-full bg-black/30 border border-gray-600 rounded p-3 mb-4
             focus:outline-none focus:ring-2 focus:ring-purple-500"
  placeholder="Write your Bro Code solution here..."
  disabled={!!currentQuestion?.is_locked}
/>

          {/* Execute */}
          <div className="flex items-center justify-between gap-4 mb-4">
            <button
              onClick={executeCurrent}
              disabled={!currentQuestion || currentQuestion.is_locked || execState.loading}
              className="bg-purple-600 px-4 py-2 rounded-full disabled:opacity-40 hover:scale-105 transition"
            >
              {execState.loading ? "Executing..." : currentQuestion?.is_locked ? "Correct (Locked)" : "Execute"}
            </button>

            <div className="text-sm text-gray-300 flex gap-6">
              {typeof currentQuestion?.attempts === "number" && (
                <span className="mr-2">Attempts: <b>{currentQuestion.attempts}</b>/5</span>
              )}
              {execState.resultMessage && (
                <span className={execState.resultMessage.includes("✅") ? "text-green-400" : "text-red-400"}>
                  <b>{execState.resultMessage}</b>
                </span>
              )}
              {execState.errorMessage && (
                <span className="text-orange-400"><b>Error: {execState.errorMessage}</b></span>
              )}
            </div>
          </div>

          {/* Bottom Controls */}
          <div className="flex justify-between items-center mt-6">

            {/* Prev / Next */}
            <div className="flex gap-3">
              <button
                disabled={current === 0}
                onClick={() => setCurrent(c => c - 1)}
                className="px-4 py-2 rounded-full bg-gray-700
                           disabled:opacity-40 hover:scale-105 transition"
              >
                Prev
              </button>

              <button
                disabled={current === questions.length - 1}
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
          {current === questions.length - 1 && (
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
