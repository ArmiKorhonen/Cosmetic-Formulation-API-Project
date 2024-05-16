// src/pages/IngredientsPage.js
import React, { useState, useEffect } from 'react';
import { Button, Paper, Typography } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';

const IngredientsPage = () => {
  const [ingredients, setIngredients] = useState([]);
  const [controls, setControls] = useState({});
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL;

  const columns = [
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'INCI_name', headerName: 'INCI Name', width: 170 },
    { field: 'CAS', headerName: 'CAS Number', width: 110 },
    { field: 'function', headerName: 'Function', width: 180 },
    { field: 'ph_min', headerName: 'pH, min', width: 70 },
    { field: 'ph_max', headerName: 'pH, max', width: 70 },
    { field: 'temp_min', headerName: 'Temp., min', width: 90 },
    { field: 'temp_max', headerName: 'Temp., max', width: 90 },
    { field: 'use_level_min', headerName: '%, min', width: 70 },
    { field: 'use_level_max', headerName: '%, max', width: 70 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params) => {
        const ingredientControls = params.row['@controls'];
        return (
          <div>
            {ingredientControls.edit && <Button onClick={() => handleEdit(params.row)}>Edit</Button>}
            {ingredientControls.delete && <Button onClick={() => handleDelete(params.row)}>Delete</Button>}
          </div>
        );
      },
    },
  ];

  useEffect(() => {
    fetchIngredients();
  }, []);

  const fetchIngredients = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/ingredients`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setIngredients(data.items);
      setControls(data['@controls']);
    } catch (error) {
      console.error("Could not fetch ingredients:", error);
    }
  };

  // Handle the edit action
  const handleEdit = (ingredient) => {
    // Navigate to the edit page
    navigate(`/ingredients/${ingredient.CAS}`);
  };

  // Handle the delete action
  const handleDelete = async (ingredient) => {
    const confirmDelete = window.confirm(`Are you sure you want to delete ${ingredient.name}?`);
    if (!confirmDelete) return;
  
    try {
      const response = await fetch(`${apiUrl}/api/ingredients/${ingredient.CAS}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // If the delete was successful, remove the ingredient from the UI
      setIngredients(ingredients.filter((item) => item.CAS !== ingredient.CAS));
      console.log(`Deleted ${ingredient.CAS}`);
    } catch (error) {
      console.error("Could not delete ingredient:", error);
    }
  };
  
    return (
      <Paper elevation={0} style={{ height: 650, width: '95%', padding: '10px', margin: '10px', backgroundColor: '#fff' }}>
        <Typography variant="h4" gutterBottom>
          Ingredients
        </Typography>
        <div style={{ height: '100%', width: '100%' }}>
          <DataGrid
            rows={ingredients.map((ingredient, index) => ({ id: index, ...ingredient }))}
            columns={columns}
            pageSize={10}
            checkboxSelection={false}
            disableSelectionOnClick
          />
        </div>
      </Paper>
    );
};

export default IngredientsPage;
