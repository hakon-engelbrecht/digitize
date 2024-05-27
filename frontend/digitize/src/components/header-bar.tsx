import React from 'react';
import { Box } from '@mui/material';

const HeaderBar = () => {
  return (
    <Box 
        display="flex"
        justifyContent="center"
        alignItems="center"
        height='10vh'
        sx={{ 
            bgcolor: 'primary.main', 
            color: 'primary.contrastText', 
            p: 2,
            boxShadow: 3
            }}>
      <h1>Digitize</h1>
    </Box>
  );
}

export default HeaderBar;
