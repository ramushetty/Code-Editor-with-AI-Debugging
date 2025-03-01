import React, { useState } from 'react';
import styles from './Login.module.css';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

/**
 * Login component provides a login form for user authentication.
 * On successful authentication, stores JWT in a cookie.
 */
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Replace '/api/login' with your actual backend endpoint
      const response = await axios.post('/api/login', { username, password });
      const token = response.data.token;
      
      // Store JWT in a cookie (expires in 7 days)
      Cookies.set('jwt', token, { expires: 7 });
      
      // Redirect to the code editor page
      window.location.href = '/editor';
    } catch (err) {
      // Display error message returned from backend or a default error message
      setError(err.response?.data?.message || 'Authentication failed');
    }
  };

  const goToRegister = () => {
    navigate('/register');
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Collab Code Editor</h1>
      <h2 className={styles.subtitle}>Login</h2>
      {error && <p className={styles.error}>{error}</p>}
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="username">Username:</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">Password:</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className={styles.submitButton}>
          Login
        </button>
      </form>
      <p className={styles.switchText}>
              Don't Have an Account?{' '}
              <span className={styles.switchLink} onClick={goToRegister}>
                Register
              </span>
            </p>
    </div>
  );
};

export default Login;
