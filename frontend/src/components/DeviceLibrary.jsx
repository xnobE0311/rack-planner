import React from 'react';

/**
 * Sidebar listing available devices.
 *
 * Each entry displays basic information (name, U height, dimensions) and
 * is clickable. When clicked, it triggers `onAdd` to place the device into
 * the rack. As the project evolves, this component could include search,
 * filtering and category tabs.
 */
function DeviceLibrary({ devices, onAdd }) {
  return (
    <div style={{ width: '220px', flexShrink: 0 }}>
      <h2 style={{ marginTop: 0 }}>Device Library</h2>
      {devices.map((device) => (
        <div
          key={device.id}
          style={{
            border: '1px solid #ddd',
            marginBottom: '0.5rem',
            padding: '0.5rem',
            cursor: 'pointer',
            borderRadius: '4px',
            backgroundColor: '#fff',
          }}
          onClick={() => onAdd(device)}
        >
          <strong>{device.name}</strong>
          <div>{device.u_height}U</div>
          <div>
            {device.width_mm} mm × {device.depth_mm} mm
          </div>
        </div>
      ))}
    </div>
  );
}

export default DeviceLibrary;