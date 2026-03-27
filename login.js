import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const autofillStyles = `
  input:-webkit-autofill,
  input:-webkit-autofill:hover,
  input:-webkit-autofill:focus,
  input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #111a28 inset !important;
    -webkit-text-fill-color: white !important;
    transition: background-color 5000s ease-in-out 0s;
  }
`;

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      setSuccessMessage('Login successful! Redirecting...');
    }, 1500);
  };

  return (
    <div
      className="h-screen w-screen flex flex-col items-center justify-center font-sans antialiased relative overflow-hidden text-white"
      style={{
        background: 'linear-gradient(to bottom right, #0f1b2d, #1a3552)',
        fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
      }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
        <div
          className="absolute rounded-full"
          style={{
            top: '-15%',
            left: '-10%',
            width: '50%',
            height: '60%',
            background: 'rgba(0, 120, 212, 0.10)',
            filter: 'blur(120px)',
          }}
        />
        <div
          className="absolute rounded-full"
          style={{
            bottom: '-15%',
            right: '-10%',
            width: '40%',
            height: '50%',
            background: 'rgba(6, 182, 212, 0.05)',
            filter: 'blur(100px)',
          }}
        />
      </div>

      {/* Main card */}
      <main
        className="relative z-10 w-full px-10 py-12 rounded-2xl flex flex-col items-center"
        style={{
          maxWidth: '420px',
          background: 'rgba(255,255,255,0.02)',
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          border: '1px solid rgba(255,255,255,0.12)',
          boxShadow: '0 16px 40px -12px rgba(0,0,0,0.5)',
        }}
      >
        {/* Header */}
        <header className="flex flex-col items-center w-full mb-8">
          {/* Badge */}
          <div
            className="flex items-center gap-1.5 px-3 py-1 mb-5 rounded-full text-xs font-bold tracking-widest uppercase"
            style={{
              background: 'rgba(0, 120, 212, 0.15)',
              border: '1px solid rgba(0, 120, 212, 0.30)',
              color: '#0078d4',
              boxShadow: '0 0 15px rgba(0,120,212,0.15)',
              fontSize: '11px',
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="14"
              height="14"
              fill="#0078d4"
              viewBox="0 0 256 256"
            >
              <path d="M208,40H48A16,16,0,0,0,32,56V200a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V56A16,16,0,0,0,208,40Zm0,160H48V56H208V200ZM82.34,141.66a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32l-56,56a8,8,0,0,1-11.32,0Z" />
            </svg>
            HaDEA
          </div>

          <h1
            className="text-white mb-1.5 tracking-tight font-semibold"
            style={{ fontSize: '28px' }}
          >
            Back Office
          </h1>
          <p
            className="text-gray-400 font-medium tracking-wide"
            style={{ fontSize: '13px' }}
          >
            Power BI Monitoring Dashboard
          </p>
        </header>

        {/* Form */}
        <form className="w-full flex flex-col gap-5" onSubmit={handleSubmit}>
          {/* Username field */}
          <div className="flex flex-col gap-1.5 relative group">
            <label
              htmlFor="username"
              className="text-gray-300 ml-1 uppercase tracking-wider font-semibold"
              style={{ fontSize: '11px' }}
            >
              Username
            </label>
            <div className="relative flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                fill="currentColor"
                viewBox="0 0 256 256"
                className="absolute left-3.5 pointer-events-none transition-colors"
                style={{ color: username ? '#0078d4' : '#6b7280' }}
              >
                <path d="M230.93,220a8,8,0,0,1-6.93,4H32a8,8,0,0,1-6.92-12c15.23-26.33,38.7-45.21,66.09-54.16a72,72,0,1,1,73.66,0c27.39,8.95,50.86,27.83,66.09,54.16A8,8,0,0,1,230.93,220Z" />
              </svg>
              <input
                type="text"
                id="username"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full rounded-lg py-2.5 pl-11 pr-4 text-sm text-white placeholder-gray-500 outline-none transition-all duration-300 shadow-inner"
                placeholder="first.last@ec.europa.eu"
                required
                style={{
                  background: 'rgba(0,0,0,0.25)',
                  border: username
                    ? '1px solid #0078d4'
                    : '1px solid rgba(255,255,255,0.10)',
                  boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3)',
                }}
                onFocus={(e) => {
                  e.target.style.border = '1px solid #0078d4';
                  e.target.style.background = 'rgba(0,0,0,0.40)';
                }}
                onBlur={(e) => {
                  if (!username) {
                    e.target.style.border = '1px solid rgba(255,255,255,0.10)';
                    e.target.style.background = 'rgba(0,0,0,0.25)';
                  }
                }}
              />
            </div>
          </div>

          {/* Password field */}
          <div className="flex flex-col gap-1.5 relative group">
            <div className="flex justify-between items-center ml-1">
              <label
                htmlFor="password"
                className="text-gray-300 uppercase tracking-wider font-semibold"
                style={{ fontSize: '11px' }}
              >
                Password
              </label>
              <button
                type="button"
                className="transition-colors font-medium"
                style={{
                  fontSize: '11px',
                  color: '#0078d4',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: 0,
                }}
                onMouseEnter={(e) => (e.target.style.color = '#60a5fa')}
                onMouseLeave={(e) => (e.target.style.color = '#0078d4')}
              >
                Forgot?
              </button>
            </div>
            <div className="relative flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                fill="currentColor"
                viewBox="0 0 256 256"
                className="absolute left-3.5 pointer-events-none transition-colors"
                style={{ color: password ? '#0078d4' : '#6b7280' }}
              >
                <path d="M208,80H176V56a48,48,0,0,0-96,0V80H48A16,16,0,0,0,32,96V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V96A16,16,0,0,0,208,80ZM96,56a32,32,0,0,1,64,0V80H96ZM208,208H48V96H208V208Zm-68-56a12,12,0,1,1-12-12A12,12,0,0,1,140,152Z" />
              </svg>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg py-2.5 pl-11 pr-11 text-sm text-white placeholder-gray-500 outline-none transition-all duration-300 shadow-inner"
                placeholder="••••••••••••"
                required
                style={{
                  background: 'rgba(0,0,0,0.25)',
                  border: password
                    ? '1px solid #0078d4'
                    : '1px solid rgba(255,255,255,0.10)',
                  boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3)',
                }}
                onFocus={(e) => {
                  e.target.style.border = '1px solid #0078d4';
                  e.target.style.background = 'rgba(0,0,0,0.40)';
                }}
                onBlur={(e) => {
                  if (!password) {
                    e.target.style.border = '1px solid rgba(255,255,255,0.10)';
                    e.target.style.background = 'rgba(0,0,0,0.25)';
                  }
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 transition-colors focus:outline-none flex items-center justify-center p-1 rounded-md"
                style={{ color: '#6b7280', background: 'none', border: 'none', cursor: 'pointer' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = '#d1d5db';
                  e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = '#6b7280';
                  e.currentTarget.style.background = 'none';
                }}
              >
                {showPassword ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256">
                    <path d="M53.92,34.62A8,8,0,1,0,42.08,45.38L61.32,66.55C25,88.84,9.38,123.2,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208a127.11,127.11,0,0,0,52.07-10.83l22,24.21a8,8,0,1,0,11.84-10.76Zm47.33,75.84,41.67,45.85a32,32,0,0,1-41.67-45.85ZM128,192c-30.78,0-57.67-11.19-80-33.22A133.16,133.16,0,0,1,25.28,128c4.69-8.79,19.66-33.37,47.35-49.38l18,19.75a48,48,0,0,0,63.66,70l14.73,16.2A112,112,0,0,1,128,192Zm6-95.43a8,8,0,0,1,3-15.72,48.16,48.16,0,0,1,38.77,42.64,8,8,0,0,1-7.22,8.71,6.39,6.39,0,0,1-.76,0,8,8,0,0,1-8-7.26A32.09,32.09,0,0,0,134,96.57Zm113.28,34.69c-.42.94-10.55,23.37-33.36,43.8a8,8,0,1,1-10.67-11.91A132.77,132.77,0,0,0,230.57,128a133.15,133.15,0,0,0-22.7-30.77C185.67,75.19,158.78,64,128,64a118.37,118.37,0,0,0-19.36,1.57A8,8,0,0,1,106.1,49.85,134,134,0,0,1,128,48c34.88,0,66.57,13.26,91.66,38.35,18.83,18.83,27.3,37.62,27.65,38.41A8,8,0,0,1,247.31,131.26Z" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256">
                    <path d="M247.31,124.76c-.35-.79-8.82-19.58-27.65-38.41C194.57,61.26,162.88,48,128,48S61.43,61.26,36.34,86.35C17.51,105.18,9,124,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208s66.57-13.26,91.66-38.34c18.83-18.83,27.3-37.61,27.65-38.4A8,8,0,0,0,247.31,124.76ZM128,192c-30.78,0-57.67-11.19-80-33.22a133.47,133.47,0,0,1-23-30.78,133.33,133.33,0,0,1,23-30.78C70.33,75.19,97.22,64,128,64s57.67,11.19,80,33.22a133.46,133.46,0,0,1,23,30.78A133.33,133.33,0,0,1,208,158.78C185.67,180.81,158.78,192,128,192Zm0-112a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* Success message */}
          {successMessage && (
            <div
              className="text-sm text-center py-2 px-4 rounded-lg font-medium"
              style={{
                background: 'rgba(0, 120, 212, 0.15)',
                border: '1px solid rgba(0, 120, 212, 0.30)',
                color: '#60a5fa',
              }}
            >
              {successMessage}
            </div>
          )}

          {/* Submit button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-4 text-white font-semibold text-sm py-2.5 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
            style={{
              background: 'linear-gradient(to right, #0078d4, #005a9e)',
              boxShadow: '0 4px 14px 0 rgba(0,120,212,0.39)',
              border: '1px solid #005a9e',
              cursor: isSubmitting ? 'not-allowed' : 'pointer',
              opacity: isSubmitting ? 0.8 : 1,
            }}
            onMouseEnter={(e) => {
              if (!isSubmitting) {
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(0,120,212,0.5)';
                e.currentTarget.style.transform = 'translateY(-1px)';
                e.currentTarget.style.background = 'linear-gradient(to right, #0078d4, #004c87)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = '0 4px 14px 0 rgba(0,120,212,0.39)';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.background = 'linear-gradient(to right, #0078d4, #005a9e)';
            }}
          >
            {isSubmitting ? 'Signing In...' : 'Sign In'}
            {!isSubmitting && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                viewBox="0 0 256 256"
              >
                <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z" />
              </svg>
            )}
            {isSubmitting && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                viewBox="0 0 256 256"
                className="animate-spin"
              >
                <path d="M232,128a104,104,0,0,1-208,0c0-41,23.81-78.36,60.66-95.27a8,8,0,0,1,6.68,14.54C60.15,61.59,40,93.27,40,128a88,88,0,0,0,176,0c0-34.73-20.15-66.41-51.34-80.73a8,8,0,0,1,6.68-14.54C208.19,49.64,232,87,232,128Z" />
              </svg>
            )}
          </button>
        </form>

        {/* Footer note */}
        <div className="mt-8 text-center text-gray-400" style={{ fontSize: '11px' }}>
          Having trouble logging in? <br />
          <button
            type="button"
            className="text-white transition-colors mt-1 inline-block pb-0.5"
            style={{
              background: 'none',
              border: 'none',
              borderBottom: '1px solid rgba(255,255,255,0.2)',
              cursor: 'pointer',
              fontSize: '11px',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#0078d4';
              e.currentTarget.style.borderBottomColor = '#0078d4';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = 'white';
              e.currentTarget.style.borderBottomColor = 'rgba(255,255,255,0.2)';
            }}
          >
            Contact IT Support
          </button>
        </div>
      </main>

      {/* Page footer */}
      <footer className="absolute bottom-6 w-full text-center z-10">
        <p
          className="tracking-widest uppercase font-medium"
          style={{ fontSize: '10px', color: 'rgba(255,255,255,0.30)' }}
        >
          © 2024 European Health and Digital Executive Agency
        </p>
      </footer>
    </div>
  );
};

const App = () => {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = autofillStyles;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  return (
    <Router basename="/">
      <Routes>
        <Route path="/" element={<LoginPage />} />
      </Routes>
    </Router>
  );
};

export default App;