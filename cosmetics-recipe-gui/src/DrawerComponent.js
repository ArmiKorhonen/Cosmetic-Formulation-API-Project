// src/components/YourDrawerComponent.js (or wherever your Drawer component is)
import React, { useState } from 'react';
import {
  List, ListItem, ListItemText, Collapse, ListItemButton,
  IconButton, Drawer, Toolbar, Typography
} from '@mui/material';
import { Link } from 'react-router-dom';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Stack from '@mui/material/Stack';
import ScienceOutlinedIcon from '@mui/icons-material/ScienceOutlined';

const drawerWidth = 240;

const DrawerComponent = () => {
  const [open, setOpen] = useState(false);

  const handleClick = (section) => {
    setOpen(prevOpen => ({
      ...prevOpen,
      [section]: !prevOpen[section],
    }));
  };

  return (
    <Drawer
    variant="permanent"
    sx={{
      width: drawerWidth,
      flexShrink: 0,
      [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
    }}
    >
                <Toolbar>
          
          <Stack direction="row" alignItems="center" gap={1}>
            
            <Typography variant="h5">CosmeAPI</Typography>
            <ScienceOutlinedIcon style={{ fontSize: '2rem' }}/>
            </Stack>
          
          
        </Toolbar>
      <List>
        {/* Non-collapsible Item */}
        <ListItemButton component={Link} to="/instructions">
          <ListItemText primaryTypographyProps={{fontSize: '20px'}} primary="Instructions" />
        </ListItemButton>
        {/* Collapsible Items */}
        <ListItemButton onClick={() => handleClick('ingredients')}>
          <ListItemText primaryTypographyProps={{fontSize: '20px'}} primary="Ingredients" />
          {open ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={open.ingredients} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={Link} to="/ingredients/list">
              <ListItemText primary="All Ingredients" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={Link} to="/ingredients/add">
              <ListItemText primary="Add New Ingredients" />
            </ListItemButton>
          </List>
        </Collapse>
        <ListItemButton onClick={() => handleClick('recipes')}>
          <ListItemText primaryTypographyProps={{fontSize: '20px'}} primary="Recipes" />
          {open ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={open.recipes} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItemButton sx={{ pl: 4 }} component={Link} to="/recipes/list">
              <ListItemText primary="All Recipes" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={Link} to="/recipes/viewrecipe">
              <ListItemText primary="View Recipe" />
            </ListItemButton>
            <ListItemButton sx={{ pl: 4 }} component={Link} to="/recipes/add">
              <ListItemText primary="Create New Recipe" />
            </ListItemButton>
          </List>
        </Collapse>
      </List>
    </Drawer>
  );
};

export default DrawerComponent;
