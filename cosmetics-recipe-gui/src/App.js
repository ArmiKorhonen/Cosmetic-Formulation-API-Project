import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import ScienceOutlinedIcon from '@mui/icons-material/ScienceOutlined';
import InstructionsPage from './pages/Instructions';
import Stack from '@mui/material/Stack';


const drawerWidth = 240;

const theme = createTheme({
  palette: {
    primary: {
      main: '#004d40', // This is a shade of dark green.
      contrastText: '#ffffff', // This ensures text is white.
    },
    background: {
      default: '#004d40', // Change the default background to dark green.
    },
  },
  components: {
    // Name of the component
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#004d40', // Drawer paper color.
          color: '#ffffff', // Text color for items in the drawer.
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
            <ListItem button component={Link} to="/">
              <ListItemText primary="Instructions" />
            </ListItem>
            {/* Add other navigation items here */}
          </List>
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3
            //width: `calc(100% - ${drawerWidth}px)`, // Removed the breakpoint to apply for all sizes
            //marginLeft: `${drawerWidth}px`, // Removed the breakpoint to apply for all sizes
        
          }}
        >
          <Toolbar />
          <Routes>
            <Route path="/" element={<InstructionsPage />} />
            {/* Define other routes here */}
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

