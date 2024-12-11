const IPFeed = ({ label, ip }) => {

  return (
    <div className="flex flex-col items-center p-4 border rounded-lg shadow-lg bg-white">
      <h2 className="text-xl font-semibold mb-2">{label}</h2>
      <img
        src={ip}
        className="w-full h-64 rounded-lg object-cover border-2 border-gray-300"
      />
    </div>
  );
};

export default IPFeed;