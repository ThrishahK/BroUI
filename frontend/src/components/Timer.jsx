import { useEffect, useState } from "react";

const TOTAL_TIME = 3 * 60 * 60; 
export default function Timer({ onTimeUp }) {
  const [seconds, setSeconds] = useState(() => {
    const saved = localStorage.getItem("brocode_timer");
    return saved ? Number(saved) : TOTAL_TIME;
  });

  useEffect(() => {
    if (seconds <= 0) {
      localStorage.removeItem("brocode_timer");
      onTimeUp && onTimeUp();
      return;
    }

    const interval = setInterval(() => {
      setSeconds((prev) => {
        const next = prev - 1;
        localStorage.setItem("brocode_timer", next);
        return next;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [seconds, onTimeUp]);

  const h = String(Math.floor(seconds / 3600)).padStart(2, "0");
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
  const s = String(seconds % 60).padStart(2, "0");

  return (
    <div className="font-mono text-purple-300 text-lg">
      ⏱ {h}:{m}:{s}
    </div>
  );
}
