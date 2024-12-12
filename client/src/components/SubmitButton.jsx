// src/components/SubmitButton.jsx
import { useRecoilState, useRecoilValue } from 'recoil';
import { videoRefsAtom, outputDataState, mainImageState } from '../recoil/atoms';
import axios from 'axios';
import { useState } from 'react';
import { URL } from '../constants';
const SubmitButton = () => {
  const videoRefs = useRecoilValue(videoRefsAtom);
  const [outputData, setOutputData] = useRecoilState(outputDataState);
  const [mainImage, setMainImage] = useRecoilState(mainImageState);
  const [images, setImages] = useState([]);
  const [scan_id, setScanId] = useState('');
  
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
      console.log(response)
      const { count, scan_id, classes, bounding_boxes, __ } = response.data;
      setScanId(scan_id);
      setOutputData((prevData) => [
        ...prevData,
        { text: `count: ${count}, classes: ${classes}`, sender: 'user' },
        { text: `Advanced Image Processing...`, sender: 'system' },
      ]);
      // Draw bounding boxes and label the image
      drawBoundingBoxes(canvas1, bounding_boxes, classes);

      const edited_image = canvas1.toDataURL('image/jpeg');
      setMainImage({ image: edited_image});
      if (count === 1 && classes[0] !== "fruit") {
        // Ask user to take more images
        setImages([image1]);
      } else {
        // Handle multiple products
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
      const response = await axios.post(`${URL}/api/v1/pipeline/single_image_info`, { images: images, scan_id: scan_id });
      console.log(JSON.stringify(response.data, null, 2));
      pingImageInfo(scan_id);
    } catch (error) {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Error processing multiple images: ${error.response?.data?.detail || error.message}`, sender: 'system' },
      ]);
    }
  };

  const drawBoundingBoxes = (canvas, bounding_boxes, classes) => {
    console.log(bounding_boxes, classes);
    const ctx = canvas.getContext('2d');
    bounding_boxes.forEach((box, index) => {
      ctx.strokeStyle = 'red';
      ctx.lineWidth = 2;
      ctx.strokeRect(box[0], box[1], box[2]-box[0], box[3]-box[1]);
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
          // product_id: item.product_id,
          // scan_id: item.scan_id,
          brand: item.brand,
          expiry_date: item.expiry_date,
          // expired: item.expired,
          // shelf_life: item.shelf_life,
          summary: item.summary
        }));

        // Combine the data
        const combinedData = {
          fresh_data: freshData,
          product_data: productData
        };

        // Handle the final response
        console.log(combinedData);
        setOutputData((prevData) => [
          ...prevData,
          { text: `Processing complete: ${JSON.stringify(combinedData, null, 2)}`, sender: 'system' },
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
    <div className='flex flex-col w-full md:w-1/1'>
      <button
        className="mt-8 px-8 py-3 bg-green-600 text-white text-lg rounded-full shadow-lg hover:bg-green-700 transition-all duration-300 ease-in-out transform hover:scale-105"
        onClick={handleSubmit}
      >
        New Scan
      </button>
      
      {images.length > 0 && (
        <div>
          <h3>Preview of Clicked Images:</h3>
          {images.map((img, index) => (
            <img key={index} src={img} alt={`Captured ${index}`} className="w-70 h-60 m-2" />
          ))}
          <button
            className="mt-8 px-8 py-3 text-lg rounded-full shadow-lg hover:bg-green-700 transition-all duration-300 ease-in-out transform hover:scale-105 bg-green-600 text-white"
            onClick={handleAddImage}
          >
            Add More Images
          </button>
          <button
            className="mt-8 px-8 py-3 text-lg rounded-full shadow-lg hover:bg-orange-700 transition-all duration-300 ease-in-out transform hover:scale-105 bg-orange-600 text-white"
            onClick={handleMultipleImages}
          >
            Scan Captured Images
          </button>
        </div>
      )}
    </div>
  );
};

export default SubmitButton;


