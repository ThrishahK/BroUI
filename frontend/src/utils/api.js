// API utility functions for BroCode Challenge Platform

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
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

// Admin API (for future use)
export const adminAPI = {
  getTeams: async () => {
    return await apiCall('/admin/teams');
  },

  createTeam: async (teamData) => {
    return await apiCall('/admin/teams', {
      method: 'POST',
      body: JSON.stringify(teamData),
    });
  },

  getSessions: async () => {
    return await apiCall('/admin/sessions');
  },
};

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: async () => {
    return await apiCall('/leaderboard/');
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