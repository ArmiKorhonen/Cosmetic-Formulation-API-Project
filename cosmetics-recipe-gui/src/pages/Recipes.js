// src/pages/RecipesPage.js
import React, { useState } from 'react';
import { Button, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

const RecipesPage = () => {
  const [recipes, setRecipes] = useState([]);

  const fetchRecipes = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/recipes');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error("Could not fetch recipes:", error);
    }
  };

  return (
    <Paper elevation={0} style={{ padding: '20px', margin: '20px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Recipes
      </Typography>
      <Button variant="contained" onClick={fetchRecipes}>
        Load All Recipes
      </Button>
      <TableContainer component={Paper} style={{ marginTop: '20px' }}>
        <Table aria-label="recipes table">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Version of</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Rating</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {recipes.map((recipe) => (
              <TableRow key={recipe.id}>
                <TableCell>{recipe.id}</TableCell>
                <TableCell component="th" scope="row">
                  {recipe.title}
                </TableCell>
                <TableCell>{recipe.version_of}</TableCell>
                <TableCell>{recipe.description}</TableCell>
                <TableCell align="right">{recipe.rating || 'Not rated'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default RecipesPage;
