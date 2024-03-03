// src/pages/AddIngredientPage.js
import React, { useState } from 'react';
import { Button, TextField, Paper, Typography } from '@mui/material';
import { Snackbar, Alert } from '@mui/material';


const AddIngredientPage = () => {
  const [ingredientData, setIngredientData] = useState({
    name: '',
    INCI_name: '',
    CAS: '',
    function: '',
    description: '',
    ph_min: null,
    ph_max: null,
    temp_min: null,
    temp_max: null,
    use_level_min: null,
    use_level_max: null
  });

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info',
  });
  
  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbar({ ...snackbar, open: false });
  };
  

  const handleChange = (event) => {
    const { name, value } = event.target;
    setIngredientData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
  
    try {
      const response = await fetch('http://127.0.0.1:5000/api/ingredients', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(ingredientData),
      });
  
      const result = await response.json();
  
      if (response.status === 201) {
        setSnackbar({ open: true, message: 'Ingredient added successfully!', severity: 'success' });
      } else if (response.status === 400) {
        setSnackbar({ open: true, message: 'Missing fields. Please check your input.', severity: 'warning' });
      } else if (response.status === 409) {
        setSnackbar({ open: true, message: 'Ingredient already exists.', severity: 'error' });
      } else if (response.status === 500) {
        setSnackbar({ open: true, message: 'Server error. Please try again later.', severity: 'error' });
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
    } catch (error) {
      console.error("Could not post ingredient:", error);
      setSnackbar({ open: true, message: 'An error occurred. Please try again.', severity: 'error' });
    }
  };
  

  return (
    
    <Paper style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Add New Ingredient
      </Typography>
      <form onSubmit={handleSubmit}>
        {/* Iterate over each field in ingredientData to create TextField */}
        {Object.keys(ingredientData).map((key) => (
          <TextField
            key={key}
            name={key}
            label={key.replace('_', ' ')}
            value={ingredientData[key]}
            onChange={handleChange}
            margin="normal"
            fullWidth
            required={['name', 'INCI_name', 'CAS'].includes(key)} // Make mandatory fields required
          />
        ))}
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>
            {/* Snackbar for displaying messages */}
            <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default AddIngredientPage;
