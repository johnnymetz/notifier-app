import axios from 'axios';

class ApiClient {
  constructor(baseURL) {
    this.axiosInstance = axios.create({ baseURL });
  }

  async get(url, config) {
    let data, error, status;
    try {
      const res = await this.axiosInstance.get(url, config);
      data = res.data;
      status = res.status;
    } catch (err) {
      error = err.toString();
      status = err.response.status;
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
      error = err.response?.data.detail || err.toString();
      status = err.response.status;
    }
    return { data, error, status };
  }

  async authenticatedGet(url) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    const { data, error } = await this.get(url, { headers });
    return { data, error };
  }

  async authenticatedPost(url, payload) {
    const accessToken = localStorage.getItem('accessToken');
    const headers = { Authorization: `Bearer ${accessToken}` };
    const { data, error } = await this.post(url, payload, { headers });
    return { data, error };
  }

  /////////////////////////
  // JWT
  /////////////////////////
  async login(username, password) {
    let { data, error } = await apiClient.post('token/', {
      username,
      password,
    });
    if (data) {
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      ({ data, error } = await this.authenticatedGet('user/'));
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
      const { data, error, status } = await apiClient.post('token/verify/', {
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
      const { data, error } = await apiClient.post('token/refresh/', {
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
}

const apiClient = new ApiClient(
  'http://0.0.0.0:8000/api/'
  // process.env.REACT_APP_BACKEND_URL
);

export default apiClient;
