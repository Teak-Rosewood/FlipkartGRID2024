// src/components/SubmitButton.jsx
import { useRecoilValue } from 'recoil';
import { videoRefsAtom } from '../recoil/atoms';
import axios from 'axios';

const SubmitButton = () => {
  const videoRefs = useRecoilValue(videoRefsAtom);

  const handleSubmit = async () => {
    // Access the video elements from Recoil state
    const video1 = videoRefs.videoFeed1?.current;
    const video2 = videoRefs.videoFeed2?.current;

    if (!video1 || !video2) {
      console.error('Video feeds are not available');
      return;
    }

    try {
      // Capture images from the video elements
      const canvas1 = document.createElement('canvas');
      const canvas2 = document.createElement('canvas');
      canvas1.width = video1.videoWidth;
      canvas1.height = video1.videoHeight;
      canvas2.width = video2.videoWidth;
      canvas2.height = video2.videoHeight;
      canvas1.getContext('2d').drawImage(video1, 0, 0, canvas1.width, canvas1.height);
      canvas2.getContext('2d').drawImage(video2, 0, 0, canvas2.width, canvas2.height);
      const image1 = canvas1.toDataURL('image/jpeg');
      const image2 = canvas2.toDataURL('image/jpeg');

      // Send the images to the backend
      const response = await axios.post('http://localhost:8000/api/v1/pipeline/process_images', {
        image1,
        image2,
      });

      console.log('Backend response:', response.data);
    } catch (error) {
      console.error('Error submitting videos:', error);
    }
  };

  return (
    <button
      className="mt-8 px-8 py-3 bg-blue-600 text-white text-lg rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 ease-in-out transform hover:scale-105"
      onClick={handleSubmit}
    >
      Submit Videos
    </button>
  );
};

export default SubmitButton;


