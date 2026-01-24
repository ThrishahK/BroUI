import { useState, useEffect } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { 
  getQuestionWithTestCases, 
  createTestCase, 
  updateTestCase, 
  deleteTestCase 
} from "../../utils/api";

export default function TestCaseManager() {
  const { questionId } = useParams();
  const [question, setQuestion] = useState(null);
  const [testCases, setTestCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTestCase, setEditingTestCase] = useState(null);
  const [formData, setFormData] = useState({
    expected_output: "",
    is_active: true,
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [questionId]);

  const loadData = async () => {
    try {
      const questionData = await getQuestionWithTestCases(questionId);
      setQuestion(questionData);
      setTestCases(questionData.test_cases || []);
    } catch (error) {
      console.error("Failed to load data:", error);
      if (error.message.includes("401")) {
        navigate("/admin/login");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTestCase) {
        await updateTestCase(editingTestCase.id, formData);
      } else {
        await createTestCase(questionId, formData);
      }
      setShowModal(false);
      setEditingTestCase(null);
      resetForm();
      loadData();
    } catch (error) {
      alert("Failed to save test case: " + error.message);
    }
  };

  const handleEdit = (testCase) => {
    setEditingTestCase(testCase);
    setFormData({
      expected_output: testCase.expected_output,
      is_active: testCase.is_active,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this test case?")) return;
    try {
      await deleteTestCase(id);
      loadData();
    } catch (error) {
      alert("Failed to delete test case: " + error.message);
    }
  };

  const resetForm = () => {
    setFormData({
      expected_output: "",
      is_active: true,
    });
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    navigate("/admin/login");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <p className="text-white">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <Link to="/admin/questions" className="text-purple-400 hover:text-purple-300">
                ← Back to Questions
              </Link>
              <h1 className="text-2xl font-bold text-white">Test Case Manager</h1>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Question Info */}
        {question && (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">{question.title}</h2>
            <div className="flex items-center space-x-4 text-sm text-gray-400">
              <span className={`px-2 py-1 rounded-full ${
                question.difficulty === 'easy' ? 'bg-green-500/20 text-green-400' :
                question.difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                {question.difficulty}
              </span>
              <span>Points: {question.points}</span>
              <span>Test Cases: {testCases.length}</span>
            </div>
            <p className="text-gray-300 mt-4">{question.description}</p>
          </div>
        )}

        {/* Test Cases Section */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-white">Test Cases</h2>
          <button
            onClick={() => {
              setEditingTestCase(null);
              resetForm();
              setShowModal(true);
            }}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span>Add Test Case</span>
          </button>
        </div>

        {/* Test Cases List */}
        <div className="space-y-4">
          {testCases.length === 0 ? (
            <div className="bg-gray-800 rounded-lg p-8 border border-gray-700 text-center">
              <p className="text-gray-400">No test cases found. Add one to get started!</p>
            </div>
          ) : (
            testCases.map((tc, index) => (
              <div key={tc.id} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">Test Case {index + 1}</h3>
                    <span className={`inline-block px-2 py-1 text-xs rounded-full mt-2 ${
                      tc.is_active ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'
                    }`}>
                      {tc.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(tc)}
                      className="text-yellow-400 hover:text-yellow-300 px-3 py-1 border border-yellow-400 rounded"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(tc.id)}
                      className="text-red-400 hover:text-red-300 px-3 py-1 border border-red-400 rounded"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Expected Output:</label>
                  <pre className="bg-gray-900 border border-gray-700 rounded-lg p-4 text-gray-300 overflow-x-auto">
                    {tc.expected_output}
                  </pre>
                </div>
              </div>
            ))
          )}
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg max-w-2xl w-full">
            <div className="p-6">
              <h3 className="text-xl font-bold text-white mb-4">
                {editingTestCase ? "Edit Test Case" : "Add New Test Case"}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Expected Output
                  </label>
                  <textarea
                    value={formData.expected_output}
                    onChange={(e) => setFormData({ ...formData, expected_output: e.target.value })}
                    className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white font-mono h-32"
                    placeholder="Enter the expected output for this test case..."
                    required
                  />
                  <p className="text-sm text-gray-400 mt-2">
                    Tip: Enter the exact output your brocode program should produce.
                  </p>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="tc_is_active"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                    className="mr-2"
                  />
                  <label htmlFor="tc_is_active" className="text-sm text-gray-300">Active</label>
                </div>
                <div className="flex space-x-4">
                  <button
                    type="submit"
                    className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg"
                  >
                    {editingTestCase ? "Update" : "Create"}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false);
                      setEditingTestCase(null);
                      resetForm();
                    }}
                    className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
