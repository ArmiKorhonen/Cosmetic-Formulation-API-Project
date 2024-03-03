// src/pages/Recipes.js
import React from 'react';
import { Typography, Paper } from '@mui/material';

const RecipesPage = () => {
  return (
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Recipes
      </Typography>
      {/* Add your instructions content here */}
      <Typography paragraph>
        Here are recipes
        {/* Continue with the content */}
      </Typography>
    </Paper>
  );
};

export default RecipesPage;