import React, { useState } from 'react';
import apiClient from '../api/axiosSetup';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import styles from './Navbar.module.css';

/**
 * Navbar component displays the application title, a Collaborate (or End/Leave) button, and a Logout button.
 * Clicking Logout deletes the JWT cookie and redirects to the login page.
 * Clicking Collaborate opens a modal with two partitions for hosting or joining a collaboration session.
 */
const Navbar = ({ title }) => {
  const navigate = useNavigate();

  // Modal and collaboration states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');
  const [inputCode, setInputCode] = useState('');
  const [copied, setCopied] = useState(false);
  const [modalError, setModalError] = useState('');
  // collabMode: null (not in session), "host" (session started), "guest" (session joined)
  const [collabMode, setCollabMode] = useState(null);

  // Generate a code with 3 uppercase letters and 3 digits in random order.
  const generateCode = () => {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    let codeArr = [];
    for (let i = 0; i < 3; i++) {
      codeArr.push(letters.charAt(Math.floor(Math.random() * letters.length)));
    }
    for (let i = 0; i < 3; i++) {
      codeArr.push(digits.charAt(Math.floor(Math.random() * digits.length)));
    }
    // Shuffle array using Fisher-Yates algorithm.
    for (let i = codeArr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [codeArr[i], codeArr[j]] = [codeArr[j], codeArr[i]];
    }
    return codeArr.join('');
  };

  // Open modal and generate new code if not already in a session.
  const openModal = () => {
    setModalError('');
    if (collabMode === null) {
      setGeneratedCode(generateCode());
    }
    setIsModalOpen(true);
  };

  // Close modal and clear input/error.
  const closeModal = () => {
    setIsModalOpen(false);
    setModalError('');
    setInputCode('');
    setCopied(false);
  };

  // Copy the generated code to clipboard.
  const handleCopy = () => {
    navigator.clipboard.writeText(generatedCode)
      .then(() => setCopied(true))
      .catch(() => setCopied(false));
  };

  // Host: start collaboration.
  const handleStart = async () => {
    setModalError('');
    try {
      // Replace with your backend endpoint.
      await apiClient.post('/api/start-collaboration', { code: generatedCode });
      setCollabMode('host');
      closeModal();
    } catch (err) {
      setModalError(err.response?.data?.message || 'Failed to start collaboration');
    }
  };

  // Guest: join collaboration.
  const handleJoin = async () => {
    setModalError('');
    if (inputCode === generatedCode) {
      setModalError('Entered code cannot be the same as your code.');
      return;
    }
    try {
      // Replace with your backend endpoint.
      await apiClient.post('/api/join-collaboration', { code: inputCode });
      setCollabMode('guest');
      closeModal();
    } catch (err) {
      setModalError(err.response?.data?.message || 'Failed to join collaboration');
    }
  };

  // Toggle collaboration when clicking the main button.
  // If not in session, open modal.
  // If host, clicking "End" will end the session.
  // If guest, clicking "Leave" will end the session.
  const handleCollabToggle = async () => {
    if (collabMode === null) {
      openModal();
    } else if (collabMode === 'host') {
      try {
        await apiClient.post('/api/end-collaboration', { mode: 'host' });
        setCollabMode(null);
      } catch (err) {
        // Optionally handle errors.
      }
    } else if (collabMode === 'guest') {
      try {
        await apiClient.post('/api/leave-collaboration', { mode: 'guest' });
        setCollabMode(null);
      } catch (err) {
        // Optionally handle errors.
      }
    }
  };

  // Logout: remove the JWT cookie and navigate to the login page.
  const handleLogout = () => {
    Cookies.remove('jwt');
    navigate('/login');
  };

  // Determine the label for the collaboration button.
  let collabButtonLabel = 'Collaborate';
  if (collabMode === 'host') collabButtonLabel = 'End';
  if (collabMode === 'guest') collabButtonLabel = 'Leave';

  return (
    <>
      <header className={styles.navbar}>
        <h1 className={styles.title}>{title}</h1>
        <nav className={styles.navItems}>
          <button onClick={handleCollabToggle} className={styles.collabButton}>
            {collabButtonLabel}
          </button>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Logout
          </button>
        </nav>
      </header>

      {isModalOpen && (
        <div className={styles.modalOverlay}>
          <div className={styles.modalContent}>
            <button className={styles.closeButton} onClick={closeModal}>×</button>
            <div className={styles.modalBody}>
              {/* Left Partition (Host) */}
              <div className={styles.leftPane}>
                <h2>Your Code</h2>
                <div className={styles.codeContainer}>
                  <span className={styles.generatedCode}>{generatedCode}</span>
                  <button onClick={handleCopy} className={styles.iconButton}>
                    {copied ? (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="green" width="24px" height="24px">
                        <path d="M0 0h24v24H0z" fill="none"/>
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19l12-12-1.41-1.41z"/>
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px">
                        <path d="M0 0h24v24H0z" fill="none"/>
                        <path d="M16 1H8C6.9 1 6 1.9 6 3v1H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h16
                                 c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-2V3
                                 c0-1.1-.9-2-2-2zM8 3h8v2H8V3zm10
                                 18H6V6h2v2h8V6h2v15z"/>
                      </svg>
                    )}
                  </button>
                </div>
                <button onClick={handleStart} className={styles.startButton}>Start</button>
              </div>
              {/* Vertical Divider */}
              <div className={styles.divider}></div>
              {/* Right Partition (Guest) */}
              <div className={styles.rightPane}>
                <h2>Join Code</h2>
                <input
                  type="text"
                  className={styles.joinInput}
                  placeholder="Enter code to join"
                  value={inputCode}
                  onChange={(e) => setInputCode(e.target.value)}
                />
                <button onClick={handleJoin} className={styles.joinButton}>Join</button>
              </div>
            </div>
            {modalError && <p className={styles.modalError}>{modalError}</p>}
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;
