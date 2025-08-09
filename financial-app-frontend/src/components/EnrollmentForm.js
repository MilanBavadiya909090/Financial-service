import React, { useState } from 'react';

const EnrollmentForm = ({ selectedPlan, onSubmit, submitting = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    monthlyContribution: selectedPlan ? selectedPlan.minContribution : 0,
    phone: '',
    address: ''
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    }

    const contribution = parseFloat(formData.monthlyContribution);
    if (!contribution || contribution < selectedPlan.minContribution || contribution > selectedPlan.maxContribution) {
      newErrors.monthlyContribution = `Monthly contribution must be between $${selectedPlan.minContribution} and $${selectedPlan.maxContribution}`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm() && !submitting) {
      onSubmit({
        ...formData,
        selectedPlan: selectedPlan,
        enrollmentDate: new Date().toLocaleDateString()
      });
    }
  };

  if (!selectedPlan) {
    return (
      <div className="enrollment-section">
        <h2>Please select a financial plan first</h2>
        <p style={{ textAlign: 'center', color: '#666' }}>
          Choose one of the plans above to proceed with enrollment.
        </p>
      </div>
    );
  }

  return (
    <div className="enrollment-section">
      <h2>Enroll in {selectedPlan.name}</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="name">Full Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your full name"
              disabled={submitting}
            />
            {errors.name && <span style={{ color: 'red', fontSize: '0.9rem' }}>{errors.name}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email Address *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              disabled={submitting}
            />
            {errors.email && <span style={{ color: 'red', fontSize: '0.9rem' }}>{errors.email}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="phone">Phone Number *</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Enter your phone number"
              disabled={submitting}
            />
            {errors.phone && <span style={{ color: 'red', fontSize: '0.9rem' }}>{errors.phone}</span>}
          </div>
          
          <div className="form-group">
            <label htmlFor="monthlyContribution">Monthly Contribution *</label>
            <input
              type="number"
              id="monthlyContribution"
              name="monthlyContribution"
              value={formData.monthlyContribution}
              onChange={handleChange}
              min={selectedPlan.minContribution}
              max={selectedPlan.maxContribution}
              placeholder={`$${selectedPlan.minContribution} - $${selectedPlan.maxContribution}`}
              disabled={submitting}
            />
            {errors.monthlyContribution && <span style={{ color: 'red', fontSize: '0.9rem' }}>{errors.monthlyContribution}</span>}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="address">Address *</label>
          <input
            type="text"
            id="address"
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="Enter your address"
            disabled={submitting}
          />
          {errors.address && <span style={{ color: 'red', fontSize: '0.9rem' }}>{errors.address}</span>}
        </div>

        <div className="form-group">
          <label>Selected Plan</label>
          <input
            type="text"
            value={`${selectedPlan.name} - ${selectedPlan.interestRate} (${selectedPlan.term})`}
            disabled
            style={{ backgroundColor: '#f8f9fa', color: '#666' }}
          />
        </div>

        <button 
          type="submit" 
          className={`submit-btn ${submitting ? 'submitting' : ''}`}
          disabled={submitting}
        >
          {submitting ? (
            <>
              <span className="spinner-small"></span>
              Submitting to Backend...
            </>
          ) : (
            'Complete Enrollment'
          )}
        </button>
      </form>
    </div>
  );
};

export default EnrollmentForm;
