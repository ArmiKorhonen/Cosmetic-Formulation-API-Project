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
    setRecipe(prevRecipe => {
      const updatedPhases = prevRecipe.phases.map((phase, index) => {
        if (index === phaseIndex) {
          return {
            ...phase,
            ingredients: [...phase.ingredients, { CAS: '', name: '', quantity: '' }] // Initialize with empty string for quantity
          };
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

  const handleIngredientChange = (phaseIndex, ingredientIndex, value, field) => {
    setRecipe(prevRecipe => {
      const updatedPhases = prevRecipe.phases.map((phase, pIndex) => {
        if (pIndex === phaseIndex) {
          return {
            ...phase,
            ingredients: phase.ingredients.map((ingredient, iIndex) => {
              if (iIndex === ingredientIndex) {
                return { ...ingredient, [field]: value };
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

  const handleSubmitRecipe = async () => {
    // Basic validation
    if (!recipe.title.trim()) {
      alert('Title is required.');
      return;
    }
    if (recipe.phases.length === 0) {
      alert('At least one phase is required.');
      return;
    }
    for (const phase of recipe.phases) {
      if (!phase.name.trim()) {
        alert('All phases must have a name.');
        return;
      }
      for (const ingredient of phase.ingredients) {
        if (!ingredient.name.trim() || !ingredient.quantity) {
          alert('All ingredients must have a name and quantity.');
          return;
        }
      }
    }
  
    const payload = {
      title: recipe.title,
      description: recipe.description,
      instructions: recipe.instructions,
      phases: recipe.phases.map(phase => ({
        name: phase.name,
        note: phase.note,
        ingredients: phase.ingredients.map(ingredient => ({
          CAS: availableIngredients.find(item => item.name === ingredient.name).CAS, // Ensure that the name is unique and exists
          quantity: parseFloat(ingredient.quantity)
        }))
      }))
    };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/api/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
  
      if (!response.ok) throw new Error('Failed to post new recipe');
      alert('Recipe added successfully!');
      // Reset the form here or navigate the user to another page
      setRecipe({
        title: '',
        description: '',
        instructions: '',
        phases: []
      });
    } catch (error) {
      console.error("Failed to post new recipe:", error);
      alert("Failed to post new recipe: " + error.message);
    }
  };
  
  
  

  useEffect(() => {
    const fetchIngredients = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/ingredients');
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        const data = await response.json();
        // Assuming the API returns an object with an array in `items`
        setAvailableIngredients(data.items || []);  // Fallback to an empty array if no items
      } catch (error) {
        console.error("Could not fetch ingredients:", error);
        setAvailableIngredients([]);  // Ensure it's always an array
      }
    };

    fetchIngredients();
}, []);

  


  return (
    <Paper style={{ padding: '20px' }}>
      <TextField
          label="Title"
          value={recipe.title}
          onChange={(e) => setRecipe(prevRecipe => ({ ...prevRecipe, title: e.target.value }))}
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
            <Box key={ingredientIndex}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Ingredient</InputLabel>
                <Select
                  value={ingredient.name}
                  onChange={(e) => handleIngredientChange(phaseIndex, ingredientIndex, e.target.value, 'name')}
                  fullWidth
                >
                  {availableIngredients.map((item) => (
                    <MenuItem key={item.CAS} value={item.name}>{item.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              <TextField
                label="Quantity (%)"
                type="number"
                value={ingredient.quantity}
                onChange={(e) => handleIngredientChange(phaseIndex, ingredientIndex, e.target.value, 'quantity')}
                fullWidth
                margin="normal"
              />
            </Box>
          ))}

        </Box>
      ))}
      <Button onClick={handleAddPhase}>Add Phase</Button>
      <Button onClick={handleSubmitRecipe} color="primary" variant="contained">
        Submit Recipe
      </Button>

    </Paper>
  );
};

export default AddRecipePage;
