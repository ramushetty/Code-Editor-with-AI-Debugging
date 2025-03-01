import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Register.module.css';

/**
 * Register component provides a registration form with validation.
 * On successful registration, the user is redirected to the Login page.
 */
const Register = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(''); // clear error on change
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validate password and confirmPassword
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    
    try {
      // Replace '/api/register' with your actual backend endpoint
      await axios.post('/api/register', {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });
      
      // On success, redirect the user to the Login page
      navigate('/login');
    } catch (err) {
      // Display error message returned from backend or a default message
      setError(err.response?.data?.message || 'Registration failed');
    }
  };

  const goToLogin = () => {
    navigate('/login');
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Collab Code Editor</h1>
      <h2 className={styles.subtitle}>Register</h2>
      {error && <p className={styles.error}>{error}</p>}
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="username">Username:</label>
          <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="email">Email:</label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">Password:</label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="confirmPassword">Confirm Password:</label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className={styles.submitButton}>
          Register
        </button>
      </form>
      <p className={styles.switchText}>
        Already have an account?{' '}
        <span className={styles.switchLink} onClick={goToLogin}>
          Log in.
        </span>
      </p>
    </div>
  );
};

export default Register;
