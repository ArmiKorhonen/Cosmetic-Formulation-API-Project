import React, { useState, useEffect } from 'react';
import { Snackbar, Alert } from '@mui/material';
import { Button, Paper, Table, Box, TextField, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { useParams } from 'react-router-dom';

const ViewRecipePage = () => {
  const [searchId, setSearchId] = useState('');
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState('');
  const { id } = useParams(); // This hook provides access to the `id` param from the URL


  useEffect(() => {
    // Clear the recipe details if there's no ID in the URL
    if (!id) {
      setRecipe(null);
      setError(''); // Also clear any previous errors
      setSearchId(''); // Optionally clear the search ID as well
    } else {
      // If there's an ID, fetch the corresponding recipe
      fetchRecipe(id);
    }
  }, [id]); // Dependency on `id` so it re-runs the effect when `id` changes
  


  const fetchRecipe = async (recipeId) => {
    setError('');
    if (!recipeId) {
      setError('Please enter a recipe ID to search.');
      return;
    }
    
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/recipes/${recipeId}`);
      if (!response.ok) {
        if(response.status === 404) {
          setError(`Recipe with ID ${recipeId} not found.`);
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        setRecipe(null);
        return;
      }
      const data = await response.json();
      setRecipe(data);
    } catch (error) {
      setError("Could not fetch recipe. Please try again later.");
      console.error("Fetch error: ", error);
    }
  };
  

  const handleSearch = () => {
    if (searchId) {
      fetchRecipe(searchId);
    } else {
      setError('Please enter a recipe ID to search.');
    }
  };
  

  const handleChange = (event) => {
    setSearchId(event.target.value);
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setError('');
  };

  return (
    <Paper style={{ padding: '20px', margin: '20px' }}>
      <Typography variant="h5" gutterBottom>
        Search for a Recipe by ID
      </Typography>
      <Box mb={2}>
        <TextField
          label="Recipe ID"
          variant="outlined"
          value={searchId}
          onChange={handleChange}
          error={Boolean(error)}
          helperText={error}
        />
        <Button variant="contained" color="primary" onClick={handleSearch} style={{ marginLeft: '8px' }}>
          Search
        </Button>
      </Box>
      {recipe && (
        <Box>
        <Typography variant="h6">{recipe.title}</Typography>
        <Typography variant="subtitle1">{recipe.description}</Typography>
        <Typography variant="subtitle1">{`Version of: ${recipe.version_of || 'Original Recipe'}`}</Typography>
        <Typography variant="subtitle1">{`Rating: ${recipe.rating || 'Not rated'}`}</Typography>
        <Typography variant="subtitle2">Instructions:</Typography>
        <Typography paragraph>{recipe.instructions}</Typography>
        
        {recipe.phases.map((phase, index) => (
          <Box key={index} mb={2}>
            <Typography variant="h6">{`${phase.name} (Order: ${phase.order_number})`}</Typography>
            <Typography variant="subtitle1">{phase.note}</Typography>
            
            <TableContainer component={Paper}>
              <Table size="small" aria-label="ingredients">
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>INCI Name</TableCell>
                    <TableCell>CAS</TableCell>
                    <TableCell>Function</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell align="right">Quantity (%)</TableCell>
                    {/* Add more headers if needed */}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {phase.ingredients.map((ingredient, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{ingredient.name}</TableCell>
                      <TableCell>{ingredient.INCI_name}</TableCell>
                      <TableCell>{ingredient.CAS}</TableCell>
                      <TableCell>{ingredient.function}</TableCell>
                      <TableCell>{ingredient.description}</TableCell>
                      <TableCell align="right">{ingredient.quantity}</TableCell>
                      {/* Add more cells if needed */}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        ))}
      </Box>
      
      )}
      <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default ViewRecipePage;