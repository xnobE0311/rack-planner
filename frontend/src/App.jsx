import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RackDesigner from './components/RackDesigner.jsx';
import DeviceLibrary from './components/DeviceLibrary.jsx';
import RackView from './components/RackView.jsx';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const API_V1 = `${API_BASE}/api/v1`;

function firstFitU(placements, deviceUHeight, rackHeightU) {
  const occupied = new Set();
  placements.forEach((p) => {
    for (let u = p.u_start; u < p.u_start + p.u_height; u += 1) occupied.add(u);
  });

  for (let start = 0; start <= rackHeightU - deviceUHeight; start += 1) {
    let ok = true;
    for (let u = start; u < start + deviceUHeight; u += 1) {
      if (occupied.has(u)) {
        ok = false;
        break;
      }
    }
    if (ok) return start;
  }
  return null;
}

function App() {
  const [devices, setDevices] = useState([]);
  const [rackSpec, setRackSpec] = useState({
    height_u: 10,
    width_mm: 236.525,
    depth_mm: 310,
    rear_clearance_mm: 150,
  });
  const [placements, setPlacements] = useState([]);

  useEffect(() => {
    axios
      .get(`${API_V1}/devices`)
      .then((res) => setDevices(res.data))
      .catch((err) => console.error('Failed to load devices', err));
  }, []);

  const addDeviceToRack = (device) => {
    const start = firstFitU(placements, device.u_height, rackSpec.height_u);
    if (start === null) {
      alert('No contiguous space in rack for this device.');
      return;
    }
    setPlacements([
      ...placements,
      { device_id: device.id, u_start: start, u_height: device.u_height },
    ]);
  };

  return (
    <div style={{ display: 'flex', padding: '1rem', fontFamily: 'Arial, sans-serif', height: '100vh' }}>
      <DeviceLibrary devices={devices} onAdd={addDeviceToRack} />
      <div style={{ flexGrow: 1, marginLeft: '1rem', overflowY: 'auto' }}>
        <RackDesigner rackSpec={rackSpec} setRackSpec={setRackSpec} />
        <RackView rackSpec={rackSpec} placements={placements} devices={devices} />
      </div>
    </div>
  );
}

export default App;
