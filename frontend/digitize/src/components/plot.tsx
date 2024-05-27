import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Plot = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_plot');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching plot data', error);
      }
    };
    fetchData();
  }, []);

  return (
    <BarChart
      width={500}
      height={300}
      data={data}
      margin={{
        top: 5, right: 30, left: 20, bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="Kategorie" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="Betrag" fill="#8884d8" />
    </BarChart>
  );
};

export default Plot;
