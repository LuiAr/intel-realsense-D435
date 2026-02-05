import React from 'react';

interface CameraData {
    status: string;
    temp: string;
    fps: number;
    depth_resolution: string;
    color_resolution: string;
    stream_mode: string;
    device_name: string;
}

interface DataPanelProps {
    data: CameraData;
}

const DataPanel: React.FC<DataPanelProps> = ({ data }) => {
    const isConnected = data.status === 'connected';
    const fpsLabel = data.fps && data.fps > 0 ? `${data.fps.toFixed(1)} FPS` : '0.0 FPS';

    return (
        <div className="data-grid">
            <div className="glass-panel">
                <h3 style={{ marginTop: 0, color: 'var(--accent-color)' }}>System Status</h3>
                <div className="data-card">
                    <span className="data-label">Connection</span>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                        <span className={`status-indicator ${isConnected ? 'status-connected' : 'status-disconnected'}`}></span>
                        <span style={{ fontWeight: 600, color: isConnected ? '#2e7d32' : '#d32f2f' }}>
                            {data.status.toUpperCase()}
                        </span>
                    </div>
                </div>
                <div className="data-card" style={{ marginTop: '1rem' }}>
                    <span className="data-label">Device</span>
                    <span style={{ fontWeight: 600 }}>{data.device_name}</span>
                </div>
                <div className="data-card" style={{ marginTop: '1rem' }}>
                    <span className="data-label">Stream Mode</span>
                    <span className="data-value">{data.stream_mode}</span>
                </div>
            </div>

            <div className="glass-panel">
                <h3 style={{ marginTop: 0, color: 'var(--accent-color)' }}>Sensor Metrics</h3>
                <div className="data-card">
                    <span className="data-label">ASIC Temp</span>
                    <span className="data-value">{data.temp}</span>
                </div>
                <div className="data-card" style={{ marginTop: '1rem' }}>
                    <span className="data-label">Depth Res</span>
                    <span className="data-value">{data.depth_resolution}</span>
                </div>
                <div className="data-card" style={{ marginTop: '1rem' }}>
                    <span className="data-label">Color Res</span>
                    <span className="data-value">{data.color_resolution}</span>
                </div>
                <div className="data-card" style={{ marginTop: '1rem' }}>
                    <span className="data-label">Measured FPS</span>
                    <span className="data-value">{fpsLabel}</span>
                </div>
            </div>

            <div className="glass-panel">
                <h3 style={{ marginTop: 0, color: 'var(--accent-color)' }}>Controls</h3>
                <p style={{ color: '#9aa0a6', marginTop: 0 }}>
                    Capture frames while the viewer streams at peak throughput.
                </p>
                <button className="btn btn-primary" onClick={() => alert('High-speed capture trigger placeholder')}>
                    Capture High-Speed Burst
                </button>
            </div>
        </div>
    );
};

export default DataPanel;
