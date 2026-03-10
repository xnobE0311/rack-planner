import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RackDesigner from './components/RackDesigner.jsx';
import DeviceLibrary from './components/DeviceLibrary.jsx';
import RackView from './components/RackView.jsx';

// Base URL of the backend API. During development the backend runs on port 8000.
const API_BASE = 'http://localhost:8000';

/**
 * Main application component.
 *
 * This component orchestrates the rack planner by fetching the device library
 * from the backend, storing the current rack specification and maintaining
 * device placements. Child components handle rendering and user input.
 */
function App() {
  const [devices, setDevices] = useState([]);
  const [rackSpec, setRackSpec] = useState({
    height_u: 10,
    width_mm: 236.525,
    depth_mm: 310,
    rear_clearance_mm: 150,
  });
  const [placements, setPlacements] = useState([]);

  // Load device library on first render
  useEffect(() => {
    axios
      .get(`${API_BASE}/devices`)
      .then((res) => setDevices(res.data))
      .catch((err) => console.error('Failed to load devices', err));
  }, []);

  /**
   * Add a device to the rack at the first available position.
   *
   * The planner scans used slots from the bottom up and inserts the device
   * wherever it fits. If there is no room, it notifies the user. This logic
   * could be improved to support dragging, editing and overlap detection.
   */
  const addDeviceToRack = (device) => {
    // Determine which U indices are occupied
    const used = placements
      .reduce((acc, p) => acc.concat([...Array(p.u_height).keys()].map((i) => i + p.u_start)), []);
    let start = 0;
    // Find the first free slot large enough for the device
    while (used.includes(start) && start < rackSpec.height_u) {
      start += 1;
    }
    if (start + device.u_height <= rackSpec.height_u) {
      setPlacements([
        ...placements,
        { device_id: device.id, u_start: start, u_height: device.u_height },
      ]);
    } else {
      alert('No space in rack for this device.');
    }
  };

  return (
    <div
      style={{ display: 'flex', padding: '1rem', fontFamily: 'Arial, sans-serif', height: '100vh' }}
    >
      <DeviceLibrary devices={devices} onAdd={addDeviceToRack} />
      <div style={{ flexGrow: 1, marginLeft: '1rem', overflowY: 'auto' }}>
        <RackDesigner rackSpec={rackSpec} setRackSpec={setRackSpec} />
        <RackView rackSpec={rackSpec} placements={placements} devices={devices} />
      </div>
    </div>
  );
}

export default App;