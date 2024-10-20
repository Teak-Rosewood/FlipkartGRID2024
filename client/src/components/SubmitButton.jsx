// src/components/SubmitButton.jsx
import { useRecoilState, useRecoilValue } from 'recoil';
import { videoRefsAtom, outputDataState } from '../recoil/atoms';
import axios from 'axios';
import { useEffect } from 'react';

const SubmitButton = () => {
  const videoRefs = useRecoilValue(videoRefsAtom);
  const [outputData, setOutputData] = useRecoilState(outputDataState);

  const handleSubmit = async () => {
    // Access the video elements from Recoil state
    const video1 = videoRefs.videoFeed1?.current;
    // const video2 = videoRefs.videoFeed2?.current;

    // if (!video1 || !video2) {
    if (!video1) {
      console.error('Video feeds are not available');
      return;
    }

    try {
      // Capture images from the video elements
      const canvas1 = document.createElement('canvas');
      // const canvas2 = document.createElement('canvas');
      canvas1.width = video1.videoWidth;
      canvas1.height = video1.videoHeight;
      // canvas2.width = video2.videoWidth;
      // canvas2.height = video2.videoHeight;
      canvas1.getContext('2d').drawImage(video1, 0, 0, canvas1.width, canvas1.height);
      // canvas2.getContext('2d').drawImage(video2, 0, 0, canvas2.width, canvas2.height);
      const image1 = canvas1.toDataURL('image/jpeg');
      // const image2 = canvas2.toDataURL('image/jpeg');

      // Send the images to the backend
      const response = await axios.post('http://localhost:8000/api/v1/pipeline/process_images', {
        image1,
      });
      console.log(response)
      const { productname, price, net_weight, shelf_life, mfg_date, estimates, metadata } = response.data.result;

      // Format the product information
      const productInfo = `
      Product Name: ${productname} <br>
      Price: ${price} <br>
      Net Weight: ${net_weight} <br>
      Shelf Life: ${shelf_life} <br>
      Manufacturing Date: ${mfg_date} <br>
      Estimated Price: ${estimates.price} <br>
      Estimated Shelf Life: ${estimates.shelf_life} <br>
    `.trim();

      // Format the metadata
      const metadataInfo = Object.entries(metadata)
      .map(([key, value]) => `${key}: ${value}`)
      .join('<br>');

      // Adding the output data
      setOutputData((prevData) => [
        // ...prevData,
        { text: response.data.message, sender: 'system' },
        { text: "Product Count", sender: 'User' },
        { text: response.data.count, sender: 'system' },
        { text: "Product Information", sender: 'User' },
        { text: productInfo, sender: 'system' },
        { text: "Product Metadata", sender: 'User' },
        { text: metadataInfo, sender: 'system' },
      ]);
    } catch (error) {
      setOutputData((prevData) => [
        ...prevData,
        { text: `Error processing videos: ${error.response?.data?.detail || error.message}`, sender: 'system' },
      ]);
    }
  };
  // useEffect(() => {
  //   // Set an interval to call handleSubmit every second
  //   const intervalId = setInterval(handleSubmit, 1000);

  //   // Clear the interval when the component is unmounted
  //   return () => clearInterval(intervalId);
  // }, []);
  return (
    <button
      className="mt-8 px-8 py-3 bg-blue-600 text-white text-lg rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 ease-in-out transform hover:scale-105"
      onClick={handleSubmit}
    >
      Scan Images
    </button>
  );
};

export default SubmitButton;


