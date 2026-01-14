export default function QuestionSidebar({ questions, setCurrent }) {
  return (
    <div className="w-72 p-4 bg-black/40 backdrop-blur-md">
      <div className="grid grid-cols-5 gap-3">
        {questions.map(q => (
          <button
            key={q.id}
            onClick={() => setCurrent(q.id)}
            className={`h-12 rounded-xl font-bold
              ${q.status === "saved" && "bg-green-500"}
              ${q.status === "flagged" && "bg-blue-500"}
              ${q.status === "not_attempted" && "bg-red-500"}
            `}
          >
            {q.id}
          </button>
        ))}
      </div>
    </div>
  );
}
