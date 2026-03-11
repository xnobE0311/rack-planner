import React from 'react';

function RackDesigner({ rackSpec, setRackSpec }) {
  const update = (field, value) => {
    if (field === 'height_u') {
      const n = parseInt(value, 10);
      setRackSpec({ ...rackSpec, [field]: Number.isNaN(n) ? 1 : n });
      return;
    }
    setRackSpec({ ...rackSpec, [field]: parseFloat(value) });
  };

  return (
    <div style={{ marginBottom: '1rem' }}>
      <h2>Rack Configuration</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Height (U):
          <input
            type="number"
            min="1"
            max="20"
            step="1"
            value={rackSpec.height_u}
            onChange={(e) => update('height_u', e.target.value)}
          />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Width (mm):
          <input type="number" value={rackSpec.width_mm} onChange={(e) => update('width_mm', e.target.value)} />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Depth (mm):
          <input type="number" value={rackSpec.depth_mm} onChange={(e) => update('depth_mm', e.target.value)} />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Rear Clearance (mm):
          <input
            type="number"
            value={rackSpec.rear_clearance_mm}
            onChange={(e) => update('rear_clearance_mm', e.target.value)}
          />
        </label>
      </div>
    </div>
  );
}

export default RackDesigner;
