
// import  { createContext, useState, useEffect } from 'react';

// export const AuthContext = createContext(null);

// export function AuthProvider({ children }) {

//   const [token, setToken] = useState(localStorage.getItem('token'));

//   // Use an effect to keep localStorage in sync with the state
//   useEffect(() => {
//     if (token) {
//       localStorage.setItem('token', token);
//     } else {
//       localStorage.removeItem('token');
//     }
//   }, [token]);

//   const login = (newToken) => {
//     setToken(newToken);
//   };

//   const logout = () => {
//     setToken(null);
//   };

//   const value = { token, login, logout };

//   return <AuthContext.Provider value={value}>
//       {children}
//     </AuthContext.Provider>;
// }
// frontend/src/context/AuthContext.jsx
import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const STORAGE_KEY = "cp_token";

  const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEY));

  useEffect(() => {
    if (token) localStorage.setItem(STORAGE_KEY, token);
    else localStorage.removeItem(STORAGE_KEY);
  }, [token]);

  const login = (newToken) => {
    setToken(newToken);
  };

  const logout = () => {
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
