// src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { RecoilRoot } from 'recoil';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RecoilRoot>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </RecoilRoot>
  </StrictMode>,
);