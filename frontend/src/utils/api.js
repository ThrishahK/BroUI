// API utility functions for BroCode Challenge Platform

// Dynamic API base URL for any network configuration
const getApiBaseUrl = () => {
  // Check if custom URL is set via environment
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // For flexible LAN access: use the same hostname/IP as the frontend
  // This works regardless of network setup - localhost, LAN IP, or any other IP
  const currentHost = window.location.hostname;

  // Always use the same host as the frontend for the backend
  // The backend CORS is configured to allow all origins in DEBUG mode
  return `http://${currentHost}:8000/api`;
};

const API_BASE_URL = getApiBaseUrl();

// Helper function to get auth headers
const getAuthHeaders = () => {
  // In LAN testing mode (when CORS allows all origins), auth might not work
  // For now, skip auth headers to avoid CORS issues during testing
  const isLanTesting = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';

  if (isLanTesting) {
    console.log('LAN testing mode: skipping auth headers to avoid CORS issues');
    return {}; // Skip auth headers for LAN testing
  }

  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// Helper function to get admin auth headers
const getAdminAuthHeaders = () => {
  const token = localStorage.getItem('admin_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// Generic API call function
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// Authentication API
export const authAPI = {
  login: async (teamLeaderUsn, password) => {
    const response = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        team_leader_usn: teamLeaderUsn,
        password: password,
      }),
    });

    // Store the token
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
    }

    return response;
  },

  getCurrentTeam: async () => {
    return await apiCall('/auth/me');
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('team_leader_usn');
  },
};

// Questions API
export const questionsAPI = {
  getPublicQuestions: async () => {
    return await apiCall('/questions/public/all');
  },

  getPublicQuestion: async (questionId) => {
    return await apiCall(`/questions/public/${questionId}`);
  },
};

// Challenge API
export const challengeAPI = {
  startChallenge: async () => {
    return await apiCall('/challenge/start', {
      method: 'POST',
    });
  },

  getChallengeStatus: async () => {
    return await apiCall('/challenge/status');
  },

  updateSubmission: async (questionId, data) => {
    return await apiCall(`/challenge/submission/${questionId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  executeSubmission: async (questionId, code_answer) => {
    return await apiCall(`/challenge/execute/${questionId}`, {
      method: 'POST',
      body: JSON.stringify({ code_answer }),
    });
  },

  uploadFile: async (questionId, file) => {
    const formData = new FormData();
    formData.append('file', file);

    return await apiCall(`/challenge/upload/${questionId}`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
        // Don't set Content-Type, let browser set it for FormData
      },
      body: formData,
    });
  },

  submitChallenge: async (submissions) => {
    return await apiCall('/challenge/submit', {
      method: 'POST',
      body: JSON.stringify({ submissions }),
    });
  },
};

// Admin API
export const adminAPI = {
  // Auth
  login: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/admin/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    return await response.json();
  },

  verify: async () => {
    const url = `${API_BASE_URL}/admin/auth/verify`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error('Unauthorized');
    }
    return await response.json();
  },

  // Questions
  getQuestions: async () => {
    const url = `${API_BASE_URL}/admin/questions`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  getQuestionWithTestCases: async (questionId) => {
    const url = `${API_BASE_URL}/admin/questions/${questionId}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  createQuestion: async (questionData) => {
    const url = `${API_BASE_URL}/admin/questions`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
      body: JSON.stringify(questionData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  updateQuestion: async (questionId, questionData) => {
    const url = `${API_BASE_URL}/admin/questions/${questionId}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
      body: JSON.stringify(questionData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  deleteQuestion: async (questionId) => {
    const url = `${API_BASE_URL}/admin/questions/${questionId}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return;
  },

  // Test Cases
  getTestCases: async (questionId) => {
    const url = `${API_BASE_URL}/admin/questions/${questionId}/testcases`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  createTestCase: async (questionId, testCaseData) => {
    const url = `${API_BASE_URL}/admin/questions/${questionId}/testcases`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
      body: JSON.stringify(testCaseData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  updateTestCase: async (testCaseId, testCaseData) => {
    const url = `${API_BASE_URL}/admin/testcases/${testCaseId}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
      body: JSON.stringify(testCaseData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  deleteTestCase: async (testCaseId) => {
    const url = `${API_BASE_URL}/admin/testcases/${testCaseId}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return;
  },

  // Teams
  getTeams: async () => {
    const url = `${API_BASE_URL}/admin/teams`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  createTeam: async (teamData) => {
    const url = `${API_BASE_URL}/admin/teams`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
      body: JSON.stringify(teamData),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },

  deleteTeam: async (teamId) => {
    const url = `${API_BASE_URL}/admin/teams/${teamId}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return;
  },

  // Sessions
  getSessions: async () => {
    const url = `${API_BASE_URL}/admin/sessions`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...getAdminAuthHeaders(),
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  },
};

// Helper exports for admin pages
export const adminLogin = adminAPI.login;
export const getQuestions = adminAPI.getQuestions;
export const getQuestionWithTestCases = adminAPI.getQuestionWithTestCases;
export const createQuestion = adminAPI.createQuestion;
export const updateQuestion = adminAPI.updateQuestion;
export const deleteQuestion = adminAPI.deleteQuestion;
export const getTestCases = adminAPI.getTestCases;
export const createTestCase = adminAPI.createTestCase;
export const updateTestCase = adminAPI.updateTestCase;
export const deleteTestCase = adminAPI.deleteTestCase;
export const getTeams = adminAPI.getTeams;
export const createTeam = adminAPI.createTeam;
export const deleteTeam = adminAPI.deleteTeam;

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: async () => {
    const res = await fetch("http://localhost:8000/api/leaderboard");
    return res.json();
  },
};


// Health check
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
    return await response.json();
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'error', message: error.message };
  }
};