import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box } from '@mui/material';

const DataTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_data');
        console.log('Data fetched successfully', response.data);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data', error);
      }
    };
    fetchData();
  }, []);

  const columns: GridColDef[] = [
    { field: 'Rechnungsnummer', headerName: 'Rechnungsnummer', width: 90 },
    { field: 'Datum', headerName: 'Datum', width: 150 },
    { field: 'Beschreibung', headerName: 'Beschreibung', width: 150 },
    { field: 'Betrag', headerName: 'Betrag', width: 150 },
    { field: 'Bezahlt', headerName: 'Bezahlt', width: 150 },
    { field: 'Fälligkeitsdatum', headerName: 'Fälligkeitsdatum', width: 150 },
    { field: 'Kategorie', headerName: 'Kategorie', width: 150 },
    { field: 'Kunde', headerName: 'Kunde', width: 150 },
    { field: 'Rechnungsnummer', headerName: 'Rechnungsnummer', width: 150 },
    { field: 'Zahlungsmethode', headerName: 'Zahlungsmethode', width: 150 }
  ];

return (
    <Box sx={{ height: '70vh', width: '100%' }}>
        <DataGrid
            rows={data}
            columns={columns}
            pagination={true}
            checkboxSelection
            getRowId={(row) => row.Rechnungsnummer}
        />
    </Box>
);
};

export default DataTable;
