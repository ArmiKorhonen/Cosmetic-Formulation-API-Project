import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Box, Snackbar, Alert } from '@mui/material';

const ViewRecipePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState('');
  const apiUrl = process.env.REACT_APP_API_URL; // Ensure this is correctly set in your environment variables

  useEffect(() => {
    if (id) {
      fetchRecipe(id);
    }
  }, [id]);

  const fetchRecipe = async (recipeId) => {
    try {
      const response = await fetch(`${apiUrl}/api/recipes/${recipeId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setRecipe(data);
    } catch (error) {
      setError("Could not fetch recipe: " + error.message);
      console.error("Fetch error:", error);
    }
  };

  const handleDelete = async () => {
    const confirmDelete = window.confirm('Are you sure you want to delete this recipe?');
    if (confirmDelete && recipe && recipe['@controls'].delete) {
      try {
        const response = await fetch(recipe['@controls'].delete.href, { method: 'DELETE' });
        if (response.ok) {
          navigate('/recipes'); // Redirect to the recipes listing page
        } else {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      } catch (error) {
        setError("Failed to delete recipe: " + error.message);
        console.error("Delete error:", error);
      }
    }
  };

  if (!recipe) {
    return (
      <Paper style={{ padding: '20px' }}>
        <Typography>Loading recipe details...</Typography>
        {error && <Alert severity="error">{error}</Alert>}
      </Paper>
    );
  }

  return (
    <Paper style={{ padding: '20px', margin: '20px' }}>
      <Typography variant="h4">{recipe.title}</Typography>
      <Typography variant="subtitle1">{recipe.description}</Typography>
      {recipe.phases.map((phase, index) => (
        <Box key={index} mb={2}>
          <Typography variant="h6">{`${phase.name} (Order: ${phase.order_number})`}</Typography>
          {phase.note && <Typography>{phase.note}</Typography>}
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Ingredient</TableCell>
                  <TableCell>CAS</TableCell>
                  <TableCell>Function</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell align="right">Quantity (%)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {phase.ingredients.map((ingredient, idx) => (
                  <TableRow key={idx}>
                    <TableCell>{ingredient.name}</TableCell>
                    <TableCell>{ingredient.CAS}</TableCell>
                    <TableCell>{ingredient.function}</TableCell>
                    <TableCell>{ingredient.description}</TableCell>
                    <TableCell align="right">{ingredient.quantity}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      ))}
      <Button variant="contained" color="secondary" onClick={handleDelete}>Delete Recipe</Button>
      <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={() => setError('')}>
        <Alert onClose={() => setError('')} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default ViewRecipePage;
