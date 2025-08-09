// Transform backend financial plan data to frontend format
export const transformPlanFromBackend = (backendPlan) => {
  return {
    id: backendPlan.id,
    name: backendPlan.name,
    interestRate: backendPlan.interest_rate,
    term: backendPlan.term,
    minContribution: backendPlan.min_contribution,
    maxContribution: backendPlan.max_contribution,
    benefits: backendPlan.benefits,
    description: backendPlan.description
  };
};

// Transform multiple plans
export const transformPlansFromBackend = (backendPlans) => {
  return backendPlans.map(transformPlanFromBackend);
};

// Transform frontend enrollment data to backend format
export const transformEnrollmentToBackend = (frontendData) => {
  return {
    name: frontendData.name,
    email: frontendData.email,
    phone: frontendData.phone,
    address: frontendData.address,
    selected_plan_id: frontendData.selectedPlan.id,
    monthly_contribution: parseFloat(frontendData.monthlyContribution)
  };
};

// Transform backend enrollment response to frontend format
export const transformEnrollmentFromBackend = (backendData) => {
  return {
    enrollmentId: backendData.enrollment_id,
    name: backendData.name,
    email: backendData.email,
    phone: backendData.phone,
    address: backendData.address,
    selectedPlan: {
      id: backendData.selected_plan.id,
      name: backendData.selected_plan.name,
      interestRate: backendData.selected_plan.interest_rate,
      term: backendData.selected_plan.term
    },
    monthlyContribution: backendData.monthly_contribution,
    enrollmentDate: backendData.enrollment_date,
    status: backendData.status
  };
};
