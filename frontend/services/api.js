import axios from 'axios';

export const axiosInstance = axios.create({
  baseURL: 'http://0.0.0.0:8000/api/',
  // baseURL: process.env.REACT_APP_BACKEND_URL
});

const sendGetRequest = async (url, config) => {
  let data, error;
  try {
    const res = await axiosInstance.get(url, config);
    data = res.data;
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
