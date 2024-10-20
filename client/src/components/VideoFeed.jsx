// src/components/VideoFeed.jsx
import { useRef, useEffect, useState } from 'react';

const VideoFeed = ({ label }) => {
  const videoRef = useRef(null);
  const [mediaDevices, setMediaDevices] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState('');

  useEffect(() => {
    // Function to fetch media devices
    const fetchMediaDevices = async () => {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === 'videoinput');
      setMediaDevices(videoDevices);
      if (videoDevices.length > 0) {
        setSelectedCamera(videoDevices[0].deviceId); // Set the default camera
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

    if (selectedCamera) {
      getUserMedia();
    }
  }, [selectedCamera]);

  return (
    <div className="flex flex-col items-center p-4 border rounded-lg shadow-lg bg-white">
      <h2 className="text-xl font-semibold mb-2">{label}</h2>
      <select
        onChange={(e) => setSelectedCamera(e.target.value)}
        className="mb-4 p-2 border border-gray-300 rounded-md"
        value={selectedCamera}
      >
        {mediaDevices.map((device) => (
          <option key={device.deviceId} value={device.deviceId}>
            {device.label || `Camera ${mediaDevices.indexOf(device) + 1}`}
          </option>
        ))}
      </select>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className="w-full h-64 rounded-lg object-cover border-2 border-gray-300"
      />
    </div>
  );
};

export default VideoFeed;




