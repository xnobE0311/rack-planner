import React from 'react';

/**
 * Visual representation of the rack and device placements.
 *
 * For each rack unit, a grid row is created. If a device starts at that
 * position, a block spans multiple rows equal to the device's U height and
 * displays the device name. Empty slots show the U index. This simple view
 * provides immediate feedback on space usage and will later evolve into a
 * 3D visualisation using Three.js.
 */
function RackView({ rackSpec, placements, devices }) {
  const rows = [];
  // We build the rack from the top down so the first row represents the highest U
  for (let u = rackSpec.height_u - 1; u >= 0; u--) {
    const placement = placements.find((p) => p.u_start === u);
    if (placement) {
      const device = devices.find((d) => d.id === placement.device_id);
      rows.push(
        <div
          key={u}
          style={{
            background: '#4caf50',
            color: '#fff',
            gridRow: `span ${placement.u_height}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderBottom: '1px solid #333',
            boxSizing: 'border-box',
          }}
        >
          {device ? device.name : placement.device_id}
        </div>,
      );
      // Skip the rows consumed by this device
      u -= placement.u_height - 1;
    } else {
      rows.push(
        <div
          key={u}
          style={{
            borderBottom: '1px solid #999',
            background: '#f7f7f7',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxSizing: 'border-box',
          }}
        >
          {u + 1}U
        </div>,
      );
    }
  }

  return (
    <div>
      <h2>Rack View</h2>
      <div
        style={{
          display: 'grid',
          gridTemplateRows: `repeat(${rackSpec.height_u}, 40px)`,
          width: '200px',
          border: '1px solid #333',
        }}
      >
        {rows}
      </div>
    </div>
  );
}

export default RackView;