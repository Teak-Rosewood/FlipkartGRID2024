// src/components/OutputArea.jsx
import { useRecoilValue } from 'recoil';
import { outputDataState } from '../recoil/atoms';
import { Box, Typography, Paper } from '@mui/material';

const OutputArea = () => {
  const outputData = useRecoilValue(outputDataState);

  return (
    <Box className="mt-8 p-6 border rounded-lg bg-paper w-full max-w-2xl shadow-md">
      <Typography variant="h6" className="mb-4">Output Data:</Typography>
      <Paper elevation={3} className="p-4">
        <pre className="whitespace-pre-wrap">{outputData}</pre>
      </Paper>
    </Box>
  );
};

export default OutputArea;