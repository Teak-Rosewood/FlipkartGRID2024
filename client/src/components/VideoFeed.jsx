// src/components/VideoFeed.jsx
import React, { useRef, useEffect, useState } from 'react';
import { useRecoilState } from 'recoil';
import { videoRefsAtom, mainImageState } from '../recoil/atoms';
import { Box, FormControl, InputLabel, MenuItem, Select, Typography, Divider } from '@mui/material';
import { Videocam, PhotoCamera, HighlightAlt } from '@mui/icons-material';
const VideoFeed = ({ label, videoRefKey }) => {
  const videoRef = useRef(null);
  const [mediaDevices, setMediaDevices] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState('');
  const [videoRefs, setVideoRefs] = useRecoilState(videoRefsAtom);
  const [mainImage, setMainImage] = useRecoilState(mainImageState);

  useEffect(() => {
    // Update the Recoil state with the current videoRef
    setVideoRefs((prevRefs) => ({
      ...prevRefs,
      [videoRefKey]: videoRef,
    }));
  }, [videoRef, setVideoRefs, videoRefKey]);

  useEffect(() => {
    // navigator.mediaDevices.getUserMedia({video: true});
    const fetchMediaDevices = async () => {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter((device) => device.kind === 'videoinput');
        setMediaDevices(videoDevices);
        if (videoDevices.length > 0) {
          setSelectedCamera(videoDevices[0].deviceId);
        }
      } catch (error) {
        console.error('Error fetching media devices:', error);
      }
    };

    fetchMediaDevices();
  }, []);

  useEffect(() => {
    const constraints = { video: { deviceId: selectedCamera ? { exact: selectedCamera } : undefined } };
    const getUserMedia = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error('Error accessing media devices.', error);
      }
    };

    // if (selectedCamera) {
      getUserMedia();
    // }
  }, [selectedCamera]);

  return (
    <Box
      sx={{
        backgroundColor: '#1E1E1E',
        borderRadius: 2,
        p: 3,
        boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
        color: 'white',
      }}
    >
      {/* Header Section */}
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Videocam sx={{ fontSize: 32, color: '#29b6f6' }} />
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          {label}
        </Typography>
      </Box>

      {/* Camera Selection */}
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel sx={{ color: 'rgba(255,255,255,0.7)' }}>Camera</InputLabel>
        <Select
          value={selectedCamera}
          onChange={(e) => setSelectedCamera(e.target.value)}
          label="Camera"
          sx={{
            backgroundColor: '#2C2C2C',
            color: 'white',
            '& .MuiSelect-icon': { color: 'white' },
          }}
        >
          {mediaDevices.map((device, index) => (
            <MenuItem key={device.deviceId} value={device.deviceId}>
              {device.label || `Camera ${index + 1}`}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Video Feed */}
      <Box
        sx={{
          border: '2px solid rgba(255,255,255,0.2)',
          borderRadius: 2,
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{ width: '100%', height: '400px', objectFit: 'cover' }}
        />
        {!mediaDevices.length && (
          <Box
            display="flex"
            alignItems="center"
            justifyContent="center"
            position="absolute"
            top={0}
            left={0}
            width="100%"
            height="100%"
            bgcolor="rgba(0,0,0,0.6)"
          >
            <Typography variant="body1" color="white">
              No Camera Detected
            </Typography>
          </Box>
        )}
      </Box>

      {/* Main Image Section */}
      {mainImage.image && (
        <>
          <Divider sx={{ my: 2, backgroundColor: 'rgba(255,255,255,0.2)' }} />
          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <HighlightAlt sx={{ fontSize: 28, color: '#FF7043' }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Detected Objects
            </Typography>
          </Box>
          <Box
            sx={{
              border: '2px solid rgba(255,255,255,0.2)',
              borderRadius: 2,
              overflow: 'hidden',
            }}
          >
            <img
              src={mainImage.image}
              alt="Detected Object"
              style={{
                width: '100%',
                height: '400px',
                objectFit: 'cover',
              }}
            />
          </Box>
        </>
      )}
    </Box>
  );
};

export default VideoFeed;





