// src/pages/Ingredients.js
import React from 'react';
import { Typography, Paper } from '@mui/material';

const IngredientsPage = () => {
  return (
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Ingredients
      </Typography>
      {/* Add your instructions content here */}
      <Typography paragraph>
        Here are ingredients
        {/* Continue with the content */}
      </Typography>
    </Paper>
  );
};

export default IngredientsPage;