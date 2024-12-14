// src/components/ChatBox.jsx
import { useRecoilValue } from 'recoil';
import { outputDataState } from '../recoil/atoms';
import { Box, Paper, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const CustomPaper = styled(Paper)(({ theme, sender }) => ({
  padding: theme.spacing(2),
  borderRadius: theme.shape.borderRadius,
  transition: 'all 0.3s ease-in-out',
  boxShadow: theme.shadows[3],
  backgroundColor:
    sender === 'system'
      ? theme.palette.mode === 'dark'
        ? '#2B2B2B' // Sleek dark gray for system in dark mode
        : '#E3F2FD' // Light blue for system in light mode
      : theme.palette.mode === 'dark'
      ? '#1B5E20' // Deep green for user in dark mode
      : '#C8E6C9', // Light green for user in light mode
  color:
    sender === 'system'
      ? theme.palette.mode === 'dark'
        ? '#FFFFFF' // White text for system in dark mode
        : '#0D47A1' // Dark blue text for system in light mode
      : theme.palette.mode === 'dark'
      ? '#FFFFFF' // White text for user in dark mode
      : '#1B5E20', // Dark green text for user in light mode
}));

const ChatBox = () => {
  const outputData = useRecoilValue(outputDataState);

  return (
    <Box className="mt-8 p-4 border rounded-lg bg-gray-100 dark:bg-gray-800 w-full max-w-2xl h-[35rem] overflow-y-auto shadow-inner">
      <div className="space-y-4">
        {outputData.map((entry, index) => (
          <CustomPaper key={index} elevation={3} sender={entry.sender}>
            <Typography
              variant="body2"
              dangerouslySetInnerHTML={{ __html: entry.text }}
              // className="whitespace-pre-wrap break-words"
            />
          </CustomPaper>
        ))}
      </div>
    </Box>
  );
};

export default ChatBox;

