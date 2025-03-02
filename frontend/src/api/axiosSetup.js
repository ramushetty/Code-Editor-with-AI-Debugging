import axios from 'axios';
import Cookies from 'js-cookie';


// console.log(process.env.REACT_APP_API_URL)
// console.log(process.env.REACT_APP_API_URL)
// Create an Axios instance with a base URL (update this to match your backend)
const apiClient = axios.create({
  
  // baseURL: process.env.REACT_APP_API_URL, 
  // baseURL: import.meta.env.VITE_REACT_APP_API_URL
  baseURL: 'http://localhost:8000/api/v1'
});

// Add a request interceptor to attach the JWT from cookies
// apiClient.interceptors.request.use(
//   (config) => {
//     // Retrieve the token from cookies
//     const token = Cookies.get('access_token');
//     if (token) {
//       // Add the token to the Authorization header
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => Promise.reject(error)
// );

export default apiClient;
