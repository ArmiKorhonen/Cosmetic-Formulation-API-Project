import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, TextField, Paper, Typography, Snackbar, Alert, Chip, Box } from '@mui/material';

const SingleIngredientPage = () => {
  const { cas } = useParams();
  const navigate = useNavigate();
  const [ingredientData, setIngredientData] = useState({});
  const [schema, setSchema] = useState({});
  const [selectedFunctions, setSelectedFunctions] = useState([]);
  const apiUrl = 'http://127.0.0.1:5000/api/ingredients'; // Your API URL

  // Fetch schema and ingredient details if editing
  useEffect(() => {
    fetchSchema();
    if (cas) {
      fetchIngredientDetails(cas);
    }
  }, [cas]);

  // Fetch the schema from the API
  const fetchSchema = async () => {
    try {
      const response = await fetch(`${apiUrl}/schema`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const schemaData = await response.json();
      setSchema(schemaData.properties);
      initializeFormData(schemaData.properties);
    } catch (error) {
      console.error("Could not fetch schema:", error);
    }
  };

  // Initialize form data based on the schema
  const initializeFormData = (schemaProperties) => {
    const initialData = {};
    Object.keys(schemaProperties).forEach(key => {
      const property = schemaProperties[key];
      initialData[key] = property.type === 'number' ? null : '';
    });
    setIngredientData(initialData);
  };

  // Fetch ingredient details for editing
  const fetchIngredientDetails = async (casNumber) => {
      try {
          const response = await fetch(`${apiUrl}/${casNumber}`);
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          let ingredient = await response.json();
          // Exclude non-editable or system fields like @controls
          const { '@controls': _, ...editableFields } = ingredient;
          setIngredientData(editableFields);
          // Handling functions, if needed
          if (ingredient.function) {
              setSelectedFunctions(ingredient.function.split(', '));
          }
      } catch (error) {
          console.error("Could not fetch ingredient details:", error);
      }
  };


  // Handle form submission for both adding and updating ingredients
  const handleSubmit = async (event) => {
    event.preventDefault();
    const method = cas ? 'PUT' : 'POST';
    const url = cas ? `${apiUrl}/${cas}` : apiUrl;
    try {
      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ingredientData),
      });
      if (response.ok) {
        const message = cas ? 'Ingredient updated successfully!' : 'Ingredient added successfully!';
        setSnackbar({ open: true, message: message, severity: 'success' });
        navigate('/ingredients/list'); // Redirect to the ingredients list on success
      } else {
        const error = await response.json();
        setSnackbar({ open: true, message: error.message || 'An error occurred.', severity: 'error' });
      }
    } catch (error) {
      console.error("Could not submit ingredient:", error);
      setSnackbar({ open: true, message: 'An error occurred. Please try again.', severity: 'error' });
    }
  };

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

  //Handling the adding and removing of chips from the ingredient function field
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


  
  

  return (
    
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        {cas ? 'Edit Ingredient' : 'Add New Ingredient'}
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
