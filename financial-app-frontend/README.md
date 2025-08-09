# SecureBank Financial Services - Frontend

A React-based frontend application for a three-tier financial/banking web application. This is the first tier (presentation layer) that provides a user interface for selecting financial plans and enrolling in them.

## Features

- **Financial Plans Display**: Shows 4 different financial plans (Savings, Premium, Retirement, Education) with details like interest rates, terms, and benefits
- **Plan Selection**: Interactive plan cards that allow users to select their preferred financial plan
- **Enrollment Form**: Comprehensive form for user enrollment with validation
- **Success Confirmation**: Displays enrollment confirmation with all submitted details
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Mock Data**: All data is hardcoded/simulated within the frontend (no backend integration)

## Project Structure

```
src/
├── components/
│   ├── PlanCard.js          # Individual financial plan card component
│   ├── EnrollmentForm.js    # User enrollment form with validation
│   └── SuccessMessage.js    # Success confirmation screen
├── data/
│   └── financialPlans.js    # Mock data for financial plans
├── styles/
│   └── App.css             # Main stylesheet
├── App.js                  # Main application component
└── index.js               # Application entry point
```

## Available Financial Plans

1. **Savings Plan** - 3.5% interest, 12 months, flexible contributions
2. **Premium Plan** - 5.2% interest, 24 months, enhanced benefits
3. **Retirement Plan** - 6.8% interest, 60 months, long-term growth
4. **Education Plan** - 4.7% interest, 36 months, education-focused

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm or yarn

### Installation & Running

1. Navigate to the project directory:
   ```bash
   cd financial-app-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and visit: `http://localhost:3000`

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

## Usage

1. **View Plans**: Browse through the 4 available financial plans displayed in a grid layout
2. **Select Plan**: Click "Select This Plan" on your preferred option
3. **Fill Form**: Complete the enrollment form with your details:
   - Full Name (required)
   - Email Address (required)
   - Phone Number (required)
   - Address (required)
   - Monthly Contribution (within plan limits)
4. **Submit**: Click "Complete Enrollment" to submit the form
5. **Confirmation**: View your enrollment confirmation with all details

## Form Validation

The enrollment form includes client-side validation for:
- Required fields (name, email, phone, address)
- Email format validation
- Monthly contribution amount within plan limits
- Real-time error display and clearing

## Styling

- Clean, modern design with gradient headers
- Responsive grid layout for plan cards
- Hover effects and smooth transitions
- Form styling with focus states
- Success screen with enrollment details
- Mobile-friendly responsive design

## Next Steps (Future Development)

This frontend is designed to be part of a three-tier architecture:

1. **Frontend** (Current) - React application for user interface
2. **Backend** (Future) - API server to handle business logic and form submissions
3. **Database** (Future) - Data persistence layer for storing user enrollments

## Technical Details

- Built with React 18+ using functional components and hooks
- Uses CSS modules for styling (no external CSS frameworks)
- State management with React useState hooks
- Form handling with controlled components
- Client-side routing ready for future expansion
- No external dependencies beyond React ecosystem

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- All data is currently mocked and stored in `src/data/financialPlans.js`
- No HTTP requests or API calls are made
- Form submissions are handled locally with state management
- Ready for backend integration when the API layer is developed
