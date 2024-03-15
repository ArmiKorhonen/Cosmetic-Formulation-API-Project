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
import SingleIngredientPage from './pages/IngredientSingle';
import ViewRecipePage from './pages/ViewRecipe';




const theme = createTheme({
  palette: {
    primary: {
      main: '#05668D',
      //contrastText: '#ffffff',
      color: '#00668c'
    },
    background: {
      default: '#EBF2FA',
    },
  },
  components: {
    // Name of the component
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#05668D', // Drawer paper color.
          color: '#FFFFFF'
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
            <Route path="/recipes/viewrecipe/" element={<ViewRecipePage />} />
            <Route path="/recipes/viewrecipe/:id" element={<ViewRecipePage />} />
            <Route path="/ingredients/list" element={<IngredientsPage />} />
            <Route path="/ingredients/add" element={<SingleIngredientPage />} />
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

