// src/components/SubmitButton.jsx
import { useRecoilState, useRecoilValue } from 'recoil';
import { videoRefsAtom, outputDataState, mainImageState } from '../recoil/atoms';
import axios from 'axios';
import { useState } from 'react';
import { URL } from '../constants';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Typography } from '@mui/material';
import EnhancedDialog from './Tables';

const SubmitButton = () => {
  const videoRefs = useRecoilValue(videoRefsAtom);
  const [outputData, setOutputData] = useRecoilState(outputDataState);
  const [mainImage, setMainImage] = useRecoilState(mainImageState);
  const [images, setImages] = useState([]);
  const [scan_id, setScanId] = useState('');
  const [expandedImage, setExpandedImage] = useState(null);
  const [allData, setAllData] = useState(null);
  const [isDataExpanded, setIsDataExpanded] = useState(false);

  const handleImageClick = (img) => {
    setExpandedImage(img);
  };

  const handleOutsideClick = (e) => {
    setExpandedImage(null);
  };
  const handleFetchData = async () => {
    try {
      const response = await axios.get(`${URL}/api/v1/pipeline/all_data`);
      setAllData(response.data);
      setIsDataExpanded(true);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleCloseData = () => {
    setIsDataExpanded(false);
  };


  const handleSubmit = async () => {
    setOutputData((prevData) => [
      { text: `Image Processing...`, sender: 'system' },
    ]);
    const video1 = videoRefs.videoFeed1?.current;

    if (!video1) {
      console.error('Video feed is not available');
      return;
    }

    try {
      const canvas1 = document.createElement('canvas');
      canvas1.width = video1.videoWidth;
      canvas1.height = video1.videoHeight;
      canvas1.getContext('2d').drawImage(video1, 0, 0, canvas1.width, canvas1.height);
      const image1 = canvas1.toDataURL('image/jpeg');
      // const image1 = await loadImageAsDataURL('/testing.jpeg'); 
      setImages([image1]);
      const response = await axios.post(`${URL}/api/v1/pipeline/initial_image_info`, { images: [image1] });
      const { count, scan_id, classes, bounding_boxes, __ } = response.data;
      setScanId(scan_id);

      setOutputData((prevData) => [
        ...prevData,
        { text: `count: ${count}, classes: ${classes}`, sender: 'user' },
      ]);
      // Draw bounding boxes and label the image
      drawBoundingBoxes(canvas1, bounding_boxes, classes);

      const edited_image = canvas1.toDataURL('image/jpeg');
      setMainImage({ image: edited_image });
      if (count === 0) {
        setOutputData((prevData) => [
          ...prevData,
          { text: `Please try again...`, sender: 'system' },
        ]);
      }
      else if (count === 1 && classes[0] !== "fruit") {
        // Ask user to take more images
        setOutputData((prevData) => [
          ...prevData,
          { text: `Add more images to process...`, sender: 'system' }
        ]);
        setImages([image1]);
      } else {
        // Handle multiple products
        setOutputData((prevData) => [
          ...prevData,
          { text: `Advanced Image Processing...`, sender: 'system' }
        ]);
        setImages([]);
        pingImageInfo(scan_id);
      }
    } catch (error) {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Error processing images: ${error.response?.data?.detail || error.message}`, sender: 'system' },
      ]);
    }
  };
  const handleAddImage = () => {
    const video1 = videoRefs.videoFeed1?.current;

    if (!video1) {
      console.error('Video feed is not available');
      return;
    }

    const canvas1 = document.createElement('canvas');
    canvas1.width = video1.videoWidth;
    canvas1.height = video1.videoHeight;
    canvas1.getContext('2d').drawImage(video1, 0, 0, canvas1.width, canvas1.height);
    const image1 = canvas1.toDataURL('image/jpeg');

    setImages([...images, image1]);
  };

  const handleMultipleImages = async () => {
    try {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Advanced Image Processing...`, sender: 'system' },
      ]);
      const response = await axios.post(`${URL}/api/v1/pipeline/single_image_info`, { images: images, scan_id: scan_id });
      pingImageInfo(scan_id);
    } catch (error) {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Error processing multiple images: ${error.response?.data?.detail || error.message}`, sender: 'system' },
      ]);
    }
  };

  const drawBoundingBoxes = (canvas, bounding_boxes, classes) => {
    const ctx = canvas.getContext('2d');
    bounding_boxes.forEach((box, index) => {
      ctx.strokeStyle = 'red';
      ctx.lineWidth = 2;
      ctx.strokeRect(box[0], box[1], box[2] - box[0], box[3] - box[1]);
      ctx.fillStyle = 'red';
      ctx.fillText(classes[index], box[0], box[1] - 10);
    });
  };

  const pingImageInfo = async (scan_id) => {
    try {
      const response = await axios.get(`${URL}/api/v1/pipeline/image_info/${scan_id}`);
      if (response.data.message) {
        setTimeout(() => pingImageInfo(scan_id), 1000);
      } else {
        const freshData = response.data.fresh_data.map(item => ({
          summary: item.summary
        }));

        const productData = response.data.product_data.map(item => ({
          brand: item.brand,
          expiry_date: item.expiry_date,
          price: item.price,
          summary: item.summary
        }));
        const formattedData = `
          <strong>Processing complete:</strong><br/>
          <strong>Fresh Data:</strong><br/>
          ${freshData.length > 0 ? freshData.map(item => item.summary).join('<br/><br/>') : 'No fresh data available.'}<br/><br/>
          <strong>Product Data:</strong><br/>
          ${productData.length > 0 ? productData.map(item => `
            <strong>Brand:</strong> ${item.brand}<br/>
            <strong>Expiry Date:</strong> ${item.expiry_date}<br/>
            <strong>Price:</strong> ${item.price}<br/>
            <strong>Summary:</strong> ${item.summary}<br/><br/>
          `).join('') : 'No product data available.'}
        `;

        setOutputData((prevData) => [
          ...prevData,
          { text: formattedData, sender: 'system' },
        ]);
      }
    } catch (error) {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Error fetching image info: ${error.response?.data?.detail || error.message}`, sender: 'system' },
      ]);
    }
  };

  return (
    <Box className='flex flex-col w-full md:w-1/1'>
      <Button
        variant="contained"
        color="primary"
        className="mt-8"
        onClick={handleSubmit}
      >
        New Scan
      </Button>
      <div className='mt-4'></div>
      {images.length > 0 && (
        <Box>
          <Box className='flex flex-col'>
            <Button
              variant="contained"
              color="secondary"
              onClick={handleAddImage}
            >
              Add More Images
            </Button>
            <div className='mt-4'></div>
            <Button
              variant="contained"
              color="warning"
              onClick={handleMultipleImages}
            >
              Scan Captured Images
            </Button>
            <div className='mt-4'></div>
          </Box>
          <Typography variant="body2" className="mt-4">Click to preview image</Typography>
          <Box className="flex flex-wrap">
            {images.map((img, index) => (
              <img
                key={index}
                src={img}
                alt={`Captured ${index}`}
                className="w-32 h-24 m-2 cursor-pointer"
                onClick={() => handleImageClick(img)}
              />
            ))}
          </Box>
        </Box>
      )}

      <div className="mt-8" />
      <Button
        variant="contained"
        color="info"
        onClick={handleFetchData}
      >
        View Database
      </Button>

      <EnhancedDialog isOpen={isDataExpanded} handleClose={handleCloseData} allData={allData} />

      {expandedImage && (
        <div
          id="expanded-image-overlay"
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
          onClick={handleOutsideClick}
        >
          <img src={expandedImage} alt="Expanded" className="max-w-full max-h-full" />
        </div>
      )}
    </Box>
  );
};

export default SubmitButton;


