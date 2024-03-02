// src/pages/Instructions.js
import React from 'react';
import { Typography, Paper } from '@mui/material';

const InstructionsPage = () => {
  return (
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Instructions
      </Typography>
      {/* Add your instructions content here */}
      <Typography paragraph>
        Here are the instructions for using the cosmetics recipe database...
        {/* Continue with the content */}
      </Typography>
    </Paper>
  );
};

export default InstructionsPage;
