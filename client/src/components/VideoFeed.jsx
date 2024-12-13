// src/components/VideoFeed.jsx
import React, { useRef, useEffect, useState } from 'react';
import { useRecoilState } from 'recoil';
import { videoRefsAtom, mainImageState } from '../recoil/atoms';

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
        console.log('Video devices:', videoDevices);
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
    <>
      <div className="flex flex-col items-center p-4 border rounded-lg shadow-lg bg-white">
        <h2 className="text-xl font-semibold mb-2">{label}</h2>
        <select
          onChange={(e) => setSelectedCamera(e.target.value)}
          className="mb-4 p-2 border border-gray-300 rounded-md"
          value={selectedCamera}
        >
          {mediaDevices.map((device, index) => (
            <option key={device.deviceId} value={device.deviceId}>
              {device.label || `Camera ${index + 1}`} ({index + 1})
            </option>
          ))}
        </select>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full h-96 rounded-lg object-cover border-2 border-gray-300"
        />
      </div>
      <div>
        {mainImage.image && (
          <div className="mt-4">
            <h2 className="text-xl font-semibold mb-2">Detected Objects</h2>
            <img
              src={mainImage.image}
              alt="Main"
              className="w-full h-96 rounded-lg object-cover border-2 border-gray-300"
            />
          </div>
        )}
      </div>
    </>
  );
};

export default VideoFeed;





