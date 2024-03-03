import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import ScienceOutlinedIcon from '@mui/icons-material/ScienceOutlined';
import InstructionsPage from './pages/Instructions';
import RecipesPage from './pages/Recipes';
import IngredientsPage from './pages/Ingredients';
import Stack from '@mui/material/Stack';


const drawerWidth = 240;

const theme = createTheme({
  palette: {
    primary: {
      main: '#fffefb', // This is a shade of dark green.
      contrastText: '#ffffff', // This ensures text is white.
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
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          {/* ... your drawer content */}
          <Toolbar>
          
          <Stack direction="row" alignItems="center" gap={1}>
            
            <Typography variant="h5">CosmeAPI</Typography>
            <ScienceOutlinedIcon style={{ fontSize: '2rem' }}/>
            </Stack>
          
          
        </Toolbar>
          <List>
            <ListItem component={Link} to="/">
              <ListItemText primary="Instructions" />
            </ListItem>
            <ListItem component={Link} to="/recipes">
              <ListItemText primary="Recipes" />
            </ListItem>
            <ListItem component={Link} to="/ingredients">
              <ListItemText primary="Ingredients" />
            </ListItem>
          </List>
        </Drawer>
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
            <Route path="/recipes" element={<RecipesPage />} />
            <Route path="/ingredients" element={<IngredientsPage />} />
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

