// src/components/ChatBox.jsx
import { useRecoilValue } from 'recoil';
import { outputDataState } from '../recoil/atoms';

const ChatBox = () => {
  const outputData = useRecoilValue(outputDataState);

  return (
    <div className="mt-8 p-4 border rounded-lg bg-gray-50 w-full max-w-2xl h-[35rem] overflow-y-auto shadow-inner">
      <div className="space-y-4">
        {outputData.map((entry, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg ${
              entry.sender === 'system'
                ? 'bg-blue-100 text-blue-800 self-start'
                : 'bg-green-200 text-gray-800 self-end'
            }`}
            dangerouslySetInnerHTML={{ __html: entry.text }}
          />
        ))}
      </div>
    </div>
  );
};

export default ChatBox;
