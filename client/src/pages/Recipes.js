import React, { useState, useEffect } from 'react';
import { Paper, Typography, List, ListItem } from '@mui/material';

const RecipesPage = () => {
  const [recipes, setRecipes] = useState([]);
  const [controls, setControls] = useState({});
  const apiUrl = process.env.REACT_APP_API_URL; // Ensure this is set in your environment

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/recipes`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRecipes(data.items);  // Assuming the 'items' key holds the array of recipes
        setControls(data['@controls']);  // If there are any controls sent by the server
      } catch (error) {
        console.error("Could not fetch recipes:", error);
      }
    };

    fetchRecipes();
  }, [apiUrl]);

  return (
    <Paper style={{ padding: '20px', margin: '20px' }}>
      <Typography variant="h5" gutterBottom>Recipes List</Typography>
      <List>
        {recipes.map((recipe, index) => (
          <ListItem key={index}>
            {recipe.title} - {recipe.description}
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default RecipesPage;
