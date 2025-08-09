import React from 'react';

const SuccessMessage = ({ enrollmentData, onBackToPlans }) => {
  return (
    <div className="success-message">
      <div className="success-icon">🎉</div>
      <h2>Enrollment Successful!</h2>
      <p>Thank you for choosing our financial services. Your enrollment has been processed successfully.</p>
      
      <div className="enrollment-details">
        <h3>Enrollment Details</h3>
        <div className="detail-row">
          <span className="detail-label">Name:</span>
          <span className="detail-value">{enrollmentData.name}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Email:</span>
          <span className="detail-value">{enrollmentData.email}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Phone:</span>
          <span className="detail-value">{enrollmentData.phone}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Selected Plan:</span>
          <span className="detail-value">{enrollmentData.selectedPlan.name}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Interest Rate:</span>
          <span className="detail-value">{enrollmentData.selectedPlan.interestRate}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Term:</span>
          <span className="detail-value">{enrollmentData.selectedPlan.term}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Monthly Contribution:</span>
          <span className="detail-value">${enrollmentData.monthlyContribution}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Enrollment Date:</span>
          <span className="detail-value">{enrollmentData.enrollmentDate}</span>
        </div>
      </div>
      
      <div style={{ marginTop: '2rem' }}>
        <p style={{ marginBottom: '1rem', color: '#666' }}>
          You will receive a confirmation email shortly with your account details and next steps.
        </p>
        <button className="back-btn" onClick={onBackToPlans}>
          Explore Other Plans
        </button>
      </div>
    </div>
  );
};

export default SuccessMessage;
