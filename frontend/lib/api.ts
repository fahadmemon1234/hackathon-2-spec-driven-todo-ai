// Base API URL
const BASE_URL = 'http://localhost:8000'; // Backend API URL

// API client with JWT auto-attachment
export const api = {
  // Get JWT from cookies
  async getJwtToken(): Promise<string | null> {
    try {
      // In a client-side context, we need to get the token differently
      // For now, we'll still use localStorage as cookies aren't accessible on the client
      // In a real implementation, we'd handle this differently
      const token = localStorage.getItem('auth-token');
      return token || null;
    } catch (error) {
      console.error('Error getting JWT token:', error);
      return null;
    }
  },

  // Get all tasks for the authenticated user with optional filters
  async getTasks(status?: string, priority?: string, category?: string, sort?: string, search?: string): Promise<any[]> {
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    // Build query parameters
    const queryParams = new URLSearchParams();
    if (status) queryParams.append('status', status);
    if (priority) queryParams.append('priority', priority);
    if (category) queryParams.append('category', category);
    if (sort) queryParams.append('sort', sort);
    if (search) queryParams.append('search', search);

    const queryString = queryParams.toString();
    const url = `${BASE_URL}/api/tasks${queryString ? '?' + queryString : ''}`;

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      }
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  },

  // Create a new task
  async createTask(data: { title: string; description?: string; priority?: string; category?: string }): Promise<any> {
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const response = await fetch(`${BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      }
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return response.json();
  },

  // Get a specific task
  async getTask(id: string): Promise<any> {
    debugger;
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const response = await fetch(`${BASE_URL}/api/tasks/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error(`Failed to fetch task: ${response.statusText}`);
    }

    return response.json();
  },

  // Update a task
  async updateTask(data: { id: string; title?: string; description?: string; priority?: string; category?: string; completed?: boolean }): Promise<any> {
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const { id, ...updateData } = data; // Extract id and spread the rest

    const response = await fetch(`${BASE_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData), // Send only the update fields, not the id
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 403) {
        throw new Error('Forbidden: You do not have permission to update this task');
      } else if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return response.json();
  },

  // Toggle task completion status
  async toggleComplete(id: string): Promise<any> {
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const response = await fetch(`${BASE_URL}/api/tasks/${id}/complete`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 403) {
        throw new Error('Forbidden: You do not have permission to update this task');
      } else if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error(`Failed to toggle task completion: ${response.statusText}`);
    }

    return response.json();
  },

  // Delete a task
  async deleteTask(id: string): Promise<boolean> {
    const token = await api.getJwtToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const response = await fetch(`${BASE_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 403) {
        throw new Error('Forbidden: You do not have permission to delete this task');
      } else if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }

    return response.status === 204;
  }
};