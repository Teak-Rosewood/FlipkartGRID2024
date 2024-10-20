// src/components/OutputArea.jsx
import { useRecoilValue } from 'recoil';
import { outputDataState } from '../recoil/atoms';

const OutputArea = () => {
  const outputData = useRecoilValue(outputDataState);

  return (
    <div className="mt-8 p-6 border rounded-lg bg-gray-100 w-full max-w-2xl shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Output Data:</h3>
      <pre className="whitespace-pre-wrap text-gray-700">{outputData}</pre>
    </div>
  );
};

export default OutputArea;

