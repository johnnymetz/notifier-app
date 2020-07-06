import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://10.0.0.113:8000/api/',
  // baseURL: process.env.REACT_APP_BACKEND_URL
});

export const fetchData = async url => {
  let error, data;
  try {
    const res = await axiosInstance.get(url);
    if (res.status === 200) {
      data = res.data;
    } else {
      error = res.statusText;
    }
  } catch (err) {
    error = err.toString();
  }
  return { error, data };
};
