import React, { useState, useEffect } from 'react';

interface StreamViewProps {
    streamUrl: string;
    fps?: number;
}

const StreamView: React.FC<StreamViewProps> = ({ streamUrl, fps }) => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const formattedFps = fps && fps > 0 ? `${fps.toFixed(0)} FPS` : 'Syncing…';

    useEffect(() => {
        const img = new Image();
        img.src = streamUrl;
        img.onload = () => setLoading(false);
        img.onerror = () => {
            setLoading(false);
            setError(true);
        };
    }, [streamUrl]);

    return (
        <div className="glass-panel video-section">
            {loading && <div className="loading-spinner">Connecting to Camera...</div>}
            {error ? (
                <div style={{ color: 'white' }}>
                    <h3>Signal Lost</h3>
                    <p>Check camera connection</p>
                </div>
            ) : (
                <img
                    src={streamUrl}
                    alt="RealSense Stream"
                    className="video-stream"
                    onError={() => setError(true)}
                />
            )}
            <div style={{
                position: 'absolute',
                bottom: '10px',
                left: '10px',
                background: 'rgba(0,0,0,0.5)',
                color: 'white',
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '0.8rem'
            }}>
                LIVE | RGB + Depth @ {formattedFps}
            </div>
        </div>
    );
};

export default StreamView;
