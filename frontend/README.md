# Rental Project Frontend

React + TypeScript frontend for the Rental Project.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (optional):
```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

3. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Build

```bash
npm run build
```

## Project Structure

```
src/
├── components/     # Reusable components
├── pages/         # Page components
├── services/      # API clients
├── store/         # State management (Zustand)
├── types/         # TypeScript types
└── App.tsx        # Main app component
```

## Features

- React 18 with TypeScript
- React Router for navigation
- TanStack Query for data fetching
- Zustand for state management
- Axios for API calls
- Vite for fast development

