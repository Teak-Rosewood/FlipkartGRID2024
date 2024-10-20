// src/App.jsx
import { RecoilRoot } from 'recoil';
import Header from './components/Header';
import VideoFeed from './components/VideoFeed';
import SubmitButton from './components/SubmitButton';
import ChatBox from './components/ChatBox';

const App = () => {
  return (
      <div className="min-h-screen flex flex-col items-center bg-gray-100">
        <Header />
        <main className="flex flex-col md:flex-row w-full max-w-7xl p-8 space-y-8 md:space-y-0 md:space-x-8">
          <div className="flex flex-col w-full md:w-1/2 gap-8">
            <VideoFeed label="Top View" />
            <VideoFeed label="Side View" />
          </div>
          
          <div className="flex flex-col w-full md:w-1/2 gap-8">
            <SubmitButton />
            <ChatBox />
          </div>
        </main>
      </div>
  );
};

export default App;







