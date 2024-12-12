// src/App.jsx
import Header from './components/Header';
import VideoFeed from './components/VideoFeed';
import SubmitButton from './components/SubmitButton';
import ChatBox from './components/ChatBox';

const App = () => {
  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100">
      <Header />
      <main className="flex flex-col md:flex-row w-full max-w-9xl p-8 space-y-8 md:space-y-0 md:space-x-8">
        <div className="flex flex-col w-full md:w-1/3 gap-8">
          <VideoFeed label="Camera View" videoRefKey="videoFeed1" />

        </div>

        <div className="flex flex-col w-full md:w-1/3">
          <h1 className="text-xl font-bold tracking-wide">Output</h1>
          <ChatBox />
        </div>
        <div className="flex flex-col w-full md:w-1/3 gap-8">
          <SubmitButton />
        </div>
      </main>
    </div>
  );
};

export default App;







