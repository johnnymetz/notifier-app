import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://10.0.0.113:8000/api/',
  // baseURL: process.env.REACT_APP_BACKEND_URL
});

export const sendGetRequest = async (url, config) => {
  let data, error;
  try {
    const res = await axiosInstance.get(url, config);
    if (res.status === 200) {
      data = res.data;
    } else {
      error = res.statusText;
    }
  } catch (err) {
    error = err.toString();
  }
  return { data, error };
};

export const sendAuthenticatedGetRequest = async url => {
  const accessToken = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${accessToken}` };
  const { data, error } = await sendGetRequest(url, { headers });
  return { data, error };
};

export const loginUser = async (username, password) => {
  let loggedIn = false,
    error;
  try {
    const res = await axiosInstance.post('token/', {
      username,
      password,
    });
    if (res.status === 200) {
      const data = res.data;
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      loggedIn = true;
    } else {
      error = res.statusText;
    }
  } catch (err) {
    error = err.response?.data.detail || err.toString();
  }
  return { loggedIn, error };
};

export const logoutUser = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

export const verifyToken = async () => {
  let verified = false,
    error;
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken) {
    try {
      const res = await axiosInstance.post('token/verify/', {
        token: accessToken,
      });
      if (res.status === 200) {
        verified = true;
      } else {
        error = res.statusText;
      }
    } catch (err) {
      error = err.response?.data.detail || err.toString();
    }
  }
  if (error) {
    console.log(`Error verifying token: ${error}`);
  }
  return verified;
};
