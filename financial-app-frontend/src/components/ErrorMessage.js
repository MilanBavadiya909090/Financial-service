import React from 'react';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-container">
      <div className="error-content">
        <div className="error-icon">⚠️</div>
        <h3 className="error-title">Connection Error</h3>
        <p className="error-message">{message}</p>
        <div className="error-actions">
          {onRetry && (
            <button className="retry-btn" onClick={onRetry}>
              🔄 Retry Connection
            </button>
          )}
          <p className="error-help">
            Make sure the backend server is running on port 8000
          </p>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
