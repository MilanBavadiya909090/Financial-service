import React, { useState, useEffect } from 'react';
import PlanCard from './components/PlanCard';
import EnrollmentForm from './components/EnrollmentForm';
import SuccessMessage from './components/SuccessMessage';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { apiService } from './services/api';
import { transformPlansFromBackend, transformEnrollmentFromBackend } from './utils/dataTransform';
import './styles/App.css';

function App() {
  const [financialPlans, setFinancialPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [enrollmentData, setEnrollmentData] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  // Fetch financial plans from backend on component mount
  useEffect(() => {
    fetchFinancialPlans();
  }, []);

  const fetchFinancialPlans = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('🔄 Fetching financial plans from backend...');
      const result = await apiService.getFinancialPlans();
      
      if (result.success) {
        const transformedPlans = transformPlansFromBackend(result.data);
        setFinancialPlans(transformedPlans);
        console.log('✅ Successfully loaded plans from backend:', transformedPlans.length);
      } else {
        throw new Error(result.error);
      }
    } catch (err) {
      console.error('❌ Failed to fetch financial plans:', err);
      setError(`Failed to load financial plans: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handlePlanSelect = (plan) => {
    setSelectedPlan(plan);
    setShowSuccess(false);
    setError(null);
  };

  const handleEnrollmentSubmit = async (data) => {
    setSubmitting(true);
    setError(null);
    
    try {
      console.log('🔄 Submitting enrollment to backend...');
      const result = await apiService.createEnrollment(data);
      
      if (result.success) {
        const transformedData = transformEnrollmentFromBackend(result.data.enrollment_data);
        setEnrollmentData(transformedData);
        setShowSuccess(true);
        console.log('✅ Enrollment successful:', result.data.enrollment_id);
        
        // Scroll to top to show success message
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        throw new Error(result.error);
      }
    } catch (err) {
      console.error('❌ Enrollment failed:', err);
      setError(`Enrollment failed: ${err.message || 'Please try again.'}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleBackToPlans = () => {
    setSelectedPlan(null);
    setEnrollmentData(null);
    setShowSuccess(false);
    setError(null);
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleRetry = () => {
    fetchFinancialPlans();
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>AnyBank Updated Financial Services</h1>
          <p>Choose the perfect financial plan to secure your future</p>
          <div className="api-status">
            <span className="status-indicator">
              {loading ? '🔄' : error ? '❌' : '✅'} 
              {loading ? ' Loading...' : error ? ' API Error' : ' Connected to Backend'}
            </span>
          </div>
        </div>
      </header>

      <div className="container">
        {error && !loading && (
          <ErrorMessage 
            message={error} 
            onRetry={handleRetry}
          />
        )}

        {loading ? (
          <LoadingSpinner message="Loading financial plans..." />
        ) : showSuccess ? (
          <SuccessMessage 
            enrollmentData={enrollmentData}
            onBackToPlans={handleBackToPlans}
          />
        ) : (
          <>
            <section>
              <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: '#333' }}>
                Our Financial Plans
                <span style={{ fontSize: '0.8rem', color: '#666', display: 'block', marginTop: '0.5rem' }}>
                  Loaded from Backend API • {financialPlans.length} plans available
                </span>
              </h2>
              
              {financialPlans.length > 0 ? (
                <div className="plans-grid">
                  {financialPlans.map(plan => (
                    <PlanCard
                      key={plan.id}
                      plan={plan}
                      isSelected={selectedPlan && selectedPlan.id === plan.id}
                      onSelect={handlePlanSelect}
                    />
                  ))}
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
                  No financial plans available at the moment.
                </div>
              )}
            </section>

            <section>
              <EnrollmentForm
                selectedPlan={selectedPlan}
                onSubmit={handleEnrollmentSubmit}
                submitting={submitting}
              />
            </section>
          </>
        )}
      </div>

      <footer style={{ 
        textAlign: 'center', 
        padding: '2rem', 
        marginTop: '3rem', 
        backgroundColor: '#333', 
        color: 'white' 
      }}>
        <p>&copy; 2025 SecureBank Financial Services. All rights reserved.</p>
        <p style={{ fontSize: '0.9rem', opacity: '0.8', marginTop: '0.5rem' }}>
          Frontend ↔ Backend Communication Active • Ready for Database Integration
        </p>
      </footer>
    </div>
  );
}

export default App;
