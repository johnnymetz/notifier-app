import axios from 'axios';

class ApiClient {
  constructor(baseURL) {
    this.axiosInstance = axios.create({ baseURL });
  }

  //////////////////////////////////
  // Base Methods
  //////////////////////////////////
  async get(url, config) {
    let data, error, status;
    try {
      const res = await this.axiosInstance.get(url, config);
      data = res.data;
      status = res.status;
    } catch (err) {
      error = err.message;
      status = err.response?.status;
    }
    return { data, error, status };
  }

  async post(url, payload, config) {
    let data, error, status;
    try {
      const res = await this.axiosInstance.post(url, payload, config);
      data = res.data;
      status = res.status;
    } catch (err) {
      error = err.response?.data.detail || err.response?.data || err.message;
      status = err.response?.status;
    }
    return { data, error, status };
  }

  async patch(url, payload, config) {
    let data, error, status;
    try {
      const res = await this.axiosInstance.patch(url, payload, config);
      data = res.data;
      status = res.status;
    } catch (err) {
      error = err.response?.data.detail || err.message;
      status = err.response?.status;
    }
    return { data, error, status };
  }

  async delete(url, config) {
    let error, status;
    try {
      const res = await this.axiosInstance.delete(url, config);
      status = res.status;
    } catch (err) {
      error = err.response?.data.detail || err.message;
      status = err.response?.status;
    }
    return { error, status };
  }

  async options(url, config) {
    let data, error, status;
    try {
      const res = await this.axiosInstance.options(url, config);
      data = res.data;
      status = res.status;
    } catch (err) {
      error = err.message;
      status = err.response?.status;
    }
    return { data, error, status };
  }

  //////////////////////////////////
  // Authenticated Base Methods
  //////////////////////////////////
  async authenticatedGet(url) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    return await this.get(url, { headers });
  }

  async authenticatedPost(url, payload) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    return await this.post(url, payload, { headers });
  }

  async authenticatedPatch(url, payload) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    return await this.patch(url, payload, { headers });
  }

  async authenticatedDelete(url) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    return await this.delete(url, { headers });
  }

  async authenticatedOptions(url) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    return await this.options(url, { headers });
  }

  //////////////////////////////////
  // User Management
  //////////////////////////////////
  async login(payload) {
    let { data, error } = await apiClient.post('auth/jwt/create/', payload);
    if (data) {
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      ({ data, error } = await this.getCurrentUser());
    }
    return { data, error };
  }

  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  async verifyToken() {
    let verified = false;
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      console.log('Verifying token...');
      const { data, error, status } = await apiClient.post('auth/jwt/verify/', {
        token: accessToken,
      });
      if (data) {
        verified = true;
        console.log('Token verified');
      } else if (status === 401) {
        const refreshed = await this.refreshToken();
        if (refreshed) {
          verified = true;
        } else {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      } else {
        console.log(`Unable to verify token: ${error}`);
      }
    } else {
      console.log('No token to verify');
    }
    return verified;
  }

  async refreshToken() {
    let refreshed = false;
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      const { data, error } = await apiClient.post('auth/jwt/refresh/', {
        refresh: refreshToken,
      });
      if (data) {
        localStorage.setItem('accessToken', data.access);
        refreshed = true;
        console.log('Token refreshed');
      } else {
        console.log(`Unable to refresh token: ${error}`);
      }
    } else {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      console.log('No refresh token');
    }
    return refreshed;
  }

  async getCurrentUser() {
    return await apiClient.authenticatedGet('auth/users/me/');
  }

  async createUser(payload) {
    return await apiClient.post(`auth/users/`, payload);
  }

  async updateUser(payload) {
    return await apiClient.authenticatedPatch(`auth/users/me/`, payload);
  }

  async activateUser(payload) {
    return await apiClient.post(`auth/users/activation/`, payload);
  }

  async setEmail(payload) {
    return await apiClient.authenticatedPost(`auth/users/set_email/`, payload);
  }

  async setPassword(payload) {
    return await apiClient.authenticatedPost(
      `auth/users/set_password/`,
      payload
    );
  }

  async sendResetPasswordEmail(payload) {
    return await apiClient.post(`auth/users/reset_password/`, payload);
  }

  async resetPassword(payload) {
    return await apiClient.post(`auth/users/reset_password_confirm/`, payload);
  }

  //////////////////////////////////
  // User Events
  //////////////////////////////////
  async createEvent(payload) {
    return await apiClient.authenticatedPost('events/', payload);
  }

  async updateEvent(eventId, payload) {
    return await apiClient.authenticatedPatch(`events/${eventId}/`, payload);
  }

  async deleteEvent(eventId) {
    return await apiClient.authenticatedDelete(`events/${eventId}/`);
  }

  async getEventTypeChoices() {
    const { data, error } = await apiClient.authenticatedOptions(`events/`);
    if (data) {
      return data.actions.POST.type.choices;
    } else {
      console.error(`Unable to pull type choices: ${error}`);
    }
  }
}

const apiClient = new ApiClient(process.env.NEXT_PUBLIC_API_HOST);

export default apiClient;
