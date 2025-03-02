import React, { useState,useEffect } from 'react';
import MonacoEditor from '@monaco-editor/react';
import Navbar from './Navbar';
import styles from './CodeEditor.module.css';

/**
 * CodeEditor component integrates Monaco Editor for code editing.
 * It displays a Navbar, a participants list (with avatar circles), and the Monaco Editor.
 */
const CodeEditor = () => {
  const [code, setCode] = useState(`# Start coding in Python...
  
def hello():
    print("Hello, World!")
`);

useEffect(() => {
  const newSocket = new WebSocket("ws://localhost:8000/api/v1/ws" + "/6TG6CK"); // Replace "myroom" with a dynamic room ID if needed

  newSocket.onopen = () => {
    console.log('WebSocket connected');
    setSocket(newSocket);
  };

  newSocket.onmessage = (event) => {
    const receivedCode = event.data;
    setCode(receivedCode); // Update code with received data
  };

  // newSocket.onclose = () => {
  //   console.log('WebSocket disconnected');
  //   setSocket(null);
  // };

  return () => {
    if (newSocket) {
      newSocket.close();
    }
  };
}, []); // Run only once on mount
//rest of the code


  const handleEditorChange = (value, event) => {
    setCode(value);
  };

  // Sample participants data with first and last names
  const participants = [
    { firstName: "John", lastName: "Doe" },
    { firstName: "Alice", lastName: "Smith" },
    { firstName: "Bob", lastName: "Brown" },
  ];

  // Get initials from a participant's first and last name.
  const getInitials = (participant) =>
    (participant.firstName.charAt(0) + participant.lastName.charAt(0)).toUpperCase();

  // Define a set of colors for the avatar backgrounds.
  const avatarColors = [
    "#F44336", "#E91E63", "#9C27B0", "#3F51B5",
    "#2196F3", "#009688", "#4CAF50", "#FF9800", "#795548"
  ];
  const getAvatarColor = (index) => avatarColors[index % avatarColors.length];

  return (
    <div className={styles.editorContainer}>
      <Navbar title="Collab Code Editor" onLogout={() => { /* logout logic here */ }} />
      <div className={styles.mainArea}>
        <aside className={styles.participants}>
          <h3>Participants</h3>
          <ul className={styles.participantsList}>
            {participants.map((p, index) => (
              <li key={index} className={styles.participantItem}>
                <div
                  className={styles.avatar}
                  style={{ backgroundColor: getAvatarColor(index) }}
                >
                  {getInitials(p)}
                </div>
                <span className={styles.participantName}>
                  {p.firstName} {p.lastName}
                </span>
              </li>
            ))}
          </ul>
        </aside>
        <main className={styles.editorArea}>
          <MonacoEditor
            height="850px"
            width="100%"
            language="python"
            theme="vs-dark"
            value={code}
            onChange={handleEditorChange}
            options={{
              automaticLayout: true, // Adjusts the layout on container resize
            }}
          />
        </main>
      </div>
    </div>
  );
};

export default CodeEditor;
