import axios from 'axios';
import Cookies from 'js-cookie';

// Create an Axios instance with a base URL (update this to match your backend)
const apiClient = axios.create({
  baseURL: 'https://your-backend-api.com', // Replace with your backend URL
});

// Add a request interceptor to attach the JWT from cookies
apiClient.interceptors.request.use(
  (config) => {
    // Retrieve the token from cookies
    const token = Cookies.get('jwt');
    if (token) {
      // Add the token to the Authorization header
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
