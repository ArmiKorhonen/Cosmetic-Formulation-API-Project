import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

import InstructionsPage from './pages/Instructions';
import RecipesPage from './pages/Recipes';
import IngredientsPage from './pages/Ingredients';

import DrawerComponent from './DrawerComponent';
import AddIngredientPage from './pages/IngredientAdd';




const theme = createTheme({
  palette: {
    primary: {
      main: '#fffefb', // This is a shade of dark green.
      //contrastText: '#ffffff', // This ensures text is white.
      color: '#00668c'
    },
    background: {
      default: '#fffefb', // Change the default background to dark green.
    },
  },
  components: {
    // Name of the component
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#f5f4f1', // Drawer paper color.
          color: '#00668c'
        },
      },
    },
  },
});

const App = () => {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <DrawerComponent />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3      
          }}
        >
          <Toolbar />
          <Routes>
            <Route path="/" element={<InstructionsPage />} />
            <Route path="/recipes/list" element={<RecipesPage />} />
            <Route path="/recipes/add" element={<RecipesPage />} />
            <Route path="/ingredients/list" element={<IngredientsPage />} />
            <Route path="/ingredients/add" element={<AddIngredientPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

const ThemedApp = () => {
  return (
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  );
};

export default ThemedApp;

