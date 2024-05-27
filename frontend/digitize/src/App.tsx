import React from 'react';
import logo from './logo.svg';
import './App.css';
import FileUpload from './components/file-upload';
import Plot from './components/plot';
import DataTable from './components/database-table';
import HeaderBar from './components/header-bar';

function App() {
  return (
    <div>
      <HeaderBar />
      <FileUpload />
      <DataTable />
      <Plot />
    </div>
  );
}

export default App;
