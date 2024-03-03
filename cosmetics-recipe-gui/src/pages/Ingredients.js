// src/pages/IngredientsPage.js
import React, { useState } from 'react';
import { Button, Paper, Typography } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

const IngredientsPage = () => {
  const [ingredients, setIngredients] = useState([]);

  const columns = [
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'INCI_name', headerName: 'INCI Name', width: 170 },
    { field: 'CAS', headerName: 'CAS Number', width: 110 },
    { field: 'function', headerName: 'Function', width: 180 },
    //{ field: 'description', headerName: 'Description', width: 250, sortable: false },
    { field: 'ph_min', headerName: 'pH, min', width: 70 },
    { field: 'ph_max', headerName: 'pH, max', width: 70 },
    { field: 'temp_min', headerName: 'Temp., min', width: 90 },
    { field: 'temp_min', headerName: 'Temp., max', width: 90 },
    { field: 'use_level_min', headerName: '%, min', width: 70 },
    { field: 'use_level_max', headerName: '%, max', width: 70 },
  ];

  const fetchIngredients = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/ingredients');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      // Transform data here if necessary to fit DataGrid requirements
      setIngredients(data);
    } catch (error) {
      console.error("Could not fetch ingredients:", error);
    }
  };

  return (
    <Paper elevation={0} style={{ height: 650, width: '95%', padding: '10px', margin: '10px', backgroundColor: '#fff' }}>
      <Typography variant="h4" gutterBottom>
        Ingredients
      </Typography>
      <Button variant="contained" onClick={fetchIngredients} style={{ marginBottom: '20px' }}>
        Load Ingredients
      </Button>
      <div style={{ height: '100%', width: '100%' }}>
        <DataGrid
          rows={ingredients.map((ingredient, index) => ({ id: index, ...ingredient }))}
          columns={columns}
          pageSize={15}
          checkboxSelection={false}
          disableRowSelectionOnClick
          disableSelectionOnClick

        />
      </div>
    </Paper>
  );
};

export default IngredientsPage;
