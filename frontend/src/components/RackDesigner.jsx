import React from 'react';

/**
 * Form for configuring rack parameters.
 *
 * Provides numeric inputs for height, width, depth and rear clearance. When the
 * user updates a value, the parent `rackSpec` state is updated via
 * `setRackSpec`. Unit conversions (e.g. between mm/inches) can be added in
 * future iterations.
 */
function RackDesigner({ rackSpec, setRackSpec }) {
  const update = (field, value) => {
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
            value={rackSpec.height_u}
            onChange={(e) => update('height_u', e.target.value)}
          />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Width (mm):
          <input
            type="number"
            value={rackSpec.width_mm}
            onChange={(e) => update('width_mm', e.target.value)}
          />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column' }}>
          Depth (mm):
          <input
            type="number"
            value={rackSpec.depth_mm}
            onChange={(e) => update('depth_mm', e.target.value)}
          />
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