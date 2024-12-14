import { AppBar, Toolbar, Typography, Box, Container, Divider } from '@mui/material';
import { Groups, EmojiEvents, People } from '@mui/icons-material';

const Header = () => {
  return (
    <AppBar
      position="static"
      color="transparent"
      sx={{
        background: 'linear-gradient(135deg, #1E1E1E, #121212)',
        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.4)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.12)',
      }}
    >
      <Container maxWidth="xl">
        <Toolbar disableGutters sx={{ flexDirection: 'column', textAlign: 'center', py: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <EmojiEvents sx={{ fontSize: 40, color: '#fbc02d' }} />
            <Typography
              variant="h3"
              component="div"
              sx={{ fontWeight: 'bold', color: 'white', letterSpacing: 1.2 }}
            >
              Flipkart GRID 2024
            </Typography>
          </Box>

          <Divider
            sx={{
              width: '20%',
              mb: 1,
              backgroundColor: 'rgba(255, 255, 255, 0.3)',
              height: '2px',
            }}
          />

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Groups sx={{ fontSize: 24, color: 'white' }} />
            <Typography
              variant="subtitle1"
              component="div"
              sx={{ color: 'white', opacity: 0.9 }}
            >
              Team Name: <span style={{ fontWeight: '600' }}>Saatwik.vasishtha</span>
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
            <People sx={{ fontSize: 24, color: 'white' }} />
            <Typography
              variant="subtitle2"
              component="div"
              sx={{ color: 'white', opacity: 0.7 }}
            >
              Team Members: <span style={{ fontWeight: '500' }}>Saatwik Vasishtha, Aansh Basu</span>
            </Typography>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;

