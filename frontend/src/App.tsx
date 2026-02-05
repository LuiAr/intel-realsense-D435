import { useState, useEffect } from 'react';
import StreamView from './components/StreamView';
import DataPanel from './components/DataPanel';
import './index.css';

const initialCameraData = {
  status: 'disconnected',
  temp: 'N/A',
  fps: 0,
  depth_resolution: '0x0',
  color_resolution: '0x0',
  stream_mode: 'offline',
  device_name: 'Intel RealSense D435',
};

function App() {
  const [data, setData] = useState(initialCameraData);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/data');
        const json = await response.json();
        setData(json);
      } catch (e) {
        console.error("Failed to fetch data", e);
        setData(initialCameraData);
      }
    };

    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>RealSense<span style={{ fontWeight: 300 }}>Viewer</span></h1>
        <div style={{ fontSize: '0.9rem', color: '#666' }}>
          Master Thesis RISE
        </div>
      </header>

      <main className="main-content">
        <StreamView streamUrl="http://localhost:8000/video_feed" fps={data.fps} />
        <DataPanel data={data} />
      </main>
    </div>
  );
}

export default App;
