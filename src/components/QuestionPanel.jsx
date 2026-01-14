export default function QuestionPanel({ id, mark }) {
  return (
    <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl">
      <h2 className="text-xl font-bold mb-2">Question {id}</h2>

      <p className="text-gray-300 mb-4">
        Solve the problem using Bro Code syntax.
      </p>

      <textarea
        rows="8"
        className="w-full bg-black/30 border border-gray-600 rounded p-3 mb-4"
      />

      <div className="flex gap-4">
        <button
          onClick={() => mark("saved")}
          className="px-4 py-2 bg-green-600 rounded-full"
        >
          Save
        </button>
        <button
          onClick={() => mark("flagged")}
          className="px-4 py-2 bg-blue-600 rounded-full"
        >
          Flag
        </button>
      </div>
    </div>
  );
}
