import React, { useState, useEffect } from 'react';
import { Button, Paper, Box, TextField, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

const AddRecipePage = () => {
  const [recipe, setRecipe] = useState({
    title: '',
    description: '',
    instructions: '',
    phases: []
  });
  const [availableIngredients, setAvailableIngredients] = useState([]);


  // Your existing useEffect for fetching ingredients remains unchanged

  const handleAddPhase = () => {
    setRecipe((prevRecipe) => ({
      ...prevRecipe,
      phases: [...prevRecipe.phases, { name: '', note: '', order_number: prevRecipe.phases.length + 1, ingredients: [] }]
    }));
  };

  const handleAddIngredientToPhase = (phaseIndex) => {
    setRecipe((prevRecipe) => {
      const updatedPhases = prevRecipe.phases.map((phase, index) => {
        if (index === phaseIndex) {
          return { ...phase, ingredients: [...phase.ingredients, { name: '', quantity: 0 }] };
        }
        return phase;
      });
      return { ...prevRecipe, phases: updatedPhases };
    });
  };

  const handlePhaseChange = (phaseIndex, field, value) => {
    setRecipe((prevRecipe) => {
      const updatedPhases = prevRecipe.phases.map((phase, index) => {
        if (index === phaseIndex) {
          return { ...phase, [field]: value };
        }
        return phase;
      });
      return { ...prevRecipe, phases: updatedPhases };
    });
  };

  const handleIngredientChange = (phaseIndex, ingredientIndex, value) => {
    setRecipe((prevRecipe) => {
      const updatedPhases = prevRecipe.phases.map((phase, pIndex) => {
        if (pIndex === phaseIndex) {
          return {
            ...phase,
            ingredients: phase.ingredients.map((ingredient, iIndex) => {
              if (iIndex === ingredientIndex) {
                return { ...ingredient, name: value };
              }
              return ingredient;
            })
          };
        }
        return phase;
      });
      return { ...prevRecipe, phases: updatedPhases };
    });
  };

  useEffect(() => {
    const fetchIngredients = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/ingredients');
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        const data = await response.json();
        setAvailableIngredients(data); // Assuming the API returns an array of ingredients
      } catch (error) {
        console.error("Could not fetch ingredients:", error);
        // Handle the error appropriately
      }
    };
  
    fetchIngredients();
  }, []);
  


  return (
    <Paper style={{ padding: '20px' }}>
      <TextField
        label="Title"
        value={recipe.title}
        onChange={(e) => setRecipe({ title: e.target.value })}
        fullWidth
        margin="normal"
      />
      {/* Additional fields for description and instructions */}
      {/* Phases and ingredients rendering */}
      {recipe.phases.map((phase, phaseIndex) => (
        <Box key={phaseIndex} sx={{ marginBottom: 2 }}>
          <TextField
            label="Phase Name"
            value={phase.name}
            onChange={(e) => handlePhaseChange(phaseIndex, 'name', e.target.value)}
            fullWidth
            margin="normal"
          />
          {/* TextField for note */}
          {/* Button to add ingredients to this phase */}
          <Button onClick={() => handleAddIngredientToPhase(phaseIndex)}>Add Ingredient</Button>

          {phase.ingredients.map((ingredient, ingredientIndex) => (
            <FormControl fullWidth key={ingredientIndex} margin="normal">
              <InputLabel>Ingredient</InputLabel>
              <Select
                value={ingredient.name}
                onChange={(e) => handleIngredientChange(phaseIndex, ingredientIndex, e.target.value)}
                fullWidth
              >
                {availableIngredients.map((ingredient) => (
                  <MenuItem key={ingredient.CAS} value={ingredient.name}>
                    {ingredient.name}
                  </MenuItem>
                ))}
              </Select>

            </FormControl>
          ))}
        </Box>
      ))}
      <Button onClick={handleAddPhase}>Add Phase</Button>
    </Paper>
  );
};

export default AddRecipePage;
