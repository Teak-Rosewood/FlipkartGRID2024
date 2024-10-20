// src/components/SubmitButton.jsx
import { useRecoilState } from 'recoil';
import { outputDataState } from '../recoil/atoms';

const SubmitButton = () => {
  const [outputData, setOutputData] = useRecoilState(outputDataState);

  const handleSubmit = async () => {
    setOutputData((prevData) => [
      ...prevData,
      { text: 'Processing video feeds...', sender: 'system' },
    ]);
    setTimeout(() => {
      setOutputData((prevData) => [
        ...prevData,
        { text: 'New output data from backend. (Simulation)', sender: 'system' },
      ]);
    }, 2000);
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


