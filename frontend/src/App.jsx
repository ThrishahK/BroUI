import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Challenge from "./pages/Challenge";
import Docs from "./pages/Docs";
import DocsRead from "./pages/DocsRead";
import Result from "./pages/Result";
import Leaderboard from "./pages/Leaderboard";
import AdminLogin from "./pages/admin/AdminLogin";
import AdminDashboard from "./pages/admin/AdminDashboard";
import QuestionManager from "./pages/admin/QuestionManager";
import TestCaseManager from "./pages/admin/TestCaseManager";
import TeamManager from "./pages/admin/TeamManager";
import ProtectedAdminRoute from "./components/ProtectedAdminRoute";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/challenge" element={<ProtectedRoute><Challenge /></ProtectedRoute>} />
        <Route path="/docs" element={<ProtectedRoute><Docs /></ProtectedRoute>} />
        <Route path="/docs/read" element={<ProtectedRoute><DocsRead /></ProtectedRoute>} />
        <Route path="/result" element={<ProtectedRoute><Result /></ProtectedRoute>} />
        <Route path="/leaderboard" element={<Leaderboard />} />

        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<ProtectedAdminRoute><AdminDashboard /></ProtectedAdminRoute>} />
        <Route path="/admin/questions" element={<ProtectedAdminRoute><QuestionManager /></ProtectedAdminRoute>} />
        <Route path="/admin/questions/:questionId/testcases" element={<ProtectedAdminRoute><TestCaseManager /></ProtectedAdminRoute>} />
        <Route path="/admin/teams" element={<ProtectedAdminRoute><TeamManager /></ProtectedAdminRoute>} />
      </Routes>
    </BrowserRouter>
  );
}
