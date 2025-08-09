import React from 'react';

const PlanCard = ({ plan, isSelected, onSelect }) => {
  return (
    <div className={`plan-card ${isSelected ? 'selected' : ''}`}>
      <div className="plan-header">
        <h3 className="plan-name">{plan.name}</h3>
        <div className="plan-rate">{plan.interestRate}</div>
        <div className="plan-term">Annual Interest Rate</div>
        <div className="plan-term">Term: {plan.term}</div>
      </div>
      
      <p className="plan-description">{plan.description}</p>
      
      <ul className="plan-benefits">
        {plan.benefits.map((benefit, index) => (
          <li key={index}>{benefit}</li>
        ))}
      </ul>
      
      <div style={{ marginBottom: '1rem', fontSize: '0.9rem', color: '#666' }}>
        <strong>Contribution Range:</strong> ${plan.minContribution} - ${plan.maxContribution} per month
      </div>
      
      <button 
        className={`select-plan-btn ${isSelected ? 'selected' : ''}`}
        onClick={() => onSelect(plan)}
      >
        {isSelected ? 'Selected ✓' : 'Select This Plan'}
      </button>
    </div>
  );
};

export default PlanCard;
