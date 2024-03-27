// src/pages/AddIngredientPage.js
import React, { useState } from 'react';
import { Button, TextField, Paper, Typography } from '@mui/material';
import { Snackbar, Alert } from '@mui/material';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';

const SingleIngredientPage = () => {
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

  const [selectedFunctions, setSelectedFunctions] = useState([]);
  const functionOptions = ["Solvent", "Surfactant", "Emulsifier", "Preservative", "Humectant", "Emollient", "Moisturizer", "Antioxidant", "Thickener/Viscosity Modifier", "Skin-Conditioning Agent", "Hair Conditioning Agent", "UV Filter/Sunscreen Agent", "Exfoliant", "Fragrance", "Colorant", "pH Adjusters", "Film Formers", "Antimicrobial/Preservative Booster", "Sequestrant", "Opacifying Agent"].sort();

  // Define a constant array of color values
  const chipColors = {
    "Antimicrobial/Preservative Booster": "rgba(233, 30, 99, 0.1)",
    "Antioxidant": "rgba(156, 39, 176, 0.1)",
    "Colorant": "rgba(103, 58, 183, 0.1)",
    "Emollient": "rgba(63, 81, 181, 0.1)",
    "Emulsifier": "rgba(33, 150, 243, 0.1)",
    "Exfoliant": "rgba(3, 169, 244, 0.1)",
    "Film Formers": "rgba(0, 188, 212, 0.1)",
    "Fragrance": "rgba(0, 150, 136, 0.1)",
    "Hair Conditioning Agent": "rgba(76, 175, 80, 0.1)",
    "Humectant": "rgba(139, 195, 74, 0.1)",
    "Moisturizer": "rgba(205, 220, 57, 0.1)",
    "Opacifying Agent": "rgba(255, 235, 59, 0.1)",
    "Preservative": "rgba(255, 193, 7, 0.1)",
    "Sequestrant": "rgba(255, 152, 0, 0.1)",
    "Skin-Conditioning Agent": "rgba(255, 87, 34, 0.1)",
    "Solvent": "rgba(121, 85, 72, 0.1)",
    "Surfactant": "rgba(158, 158, 158, 0.1)",
    "Thickener/Viscosity Modifier": "rgba(96, 125, 139, 0.1)",
    "UV Filter/Sunscreen Agent": "rgba(120, 144, 156, 0.1)",
    "pH Adjusters": "rgba(244, 67, 54, 0.1)",
    };


  
  // Function to get the color for a function
  const getChipColor = (func) => {
    return chipColors[func] || '#999999'; // Default color if not found
  };

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

  const handleAddFunction = (func) => {
    setSelectedFunctions((prevSelected) => {
      if (!prevSelected.includes(func)) {
        const updatedSelected = [...prevSelected, func];
        // Update ingredientData for the function field
        setIngredientData((prevData) => ({
          ...prevData,
          function: updatedSelected.join(', '),
        }));
        return updatedSelected;
      }
      return prevSelected;
    });
  };
  
  
  const handleDeleteFunction = (func) => {
    setSelectedFunctions((prevSelected) => {
      const updatedSelected = prevSelected.filter((f) => f !== func);
      // Update ingredientData for the function field
      setIngredientData((prevData) => ({
        ...prevData,
        function: updatedSelected.join(', '),
      }));
      return updatedSelected;
    });
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
    
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Add New Ingredient
      </Typography>
      <form onSubmit={handleSubmit}>
        {Object.keys(ingredientData).map((key) => {
          // Separate rendering for the "function" field to include chips
          if (key === 'function') {
            return (
              <Box key={key}>
                <TextField
                  name={key}
                  label={key.replace('_', ' ')}
                  value={''}
                  onChange={handleChange}
                  margin="dense"
                  size="small"
                  fullWidth
                  InputProps={{
                    startAdornment: selectedFunctions.map((func, index) => (
                      <Chip
                        key={index}
                        label={func}
                        size="small"
                        onDelete={() => handleDeleteFunction(func)}
                        style={{ marginRight: '5px', backgroundColor: getChipColor(func) }} // random color
                      />
                    )),
                  }}
                />
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 2 }}>
  {functionOptions.map((func) => (
    <Chip
      key={func}
      label={func}
      onClick={() => handleAddFunction(func)}
      style={{ backgroundColor: getChipColor(func) }} // Use the function to get the color
    />
  ))}
</Box>

              </Box>
            );
          } else {
            // Render all other fields as normal
            return (
              <TextField
                key={key}
                name={key}
                label={key.replace('_', ' ')}
                value={ingredientData[key]}
                onChange={handleChange}
                margin="dense"
                size="small"
                fullWidth
                variant="outlined"
                required={['name', 'INCI_name', 'CAS'].includes(key)} // Make mandatory fields required
              />
            );
          }
        })}
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

export default SingleIngredientPage;
