import { useEffect, useState } from 'react';
import { createRoom, deleteRoom, getRooms, updateRoom } from '../api/rooms';

const CLASSES = ['economy', 'standard', 'luxury'];
const EMPTY = { number: '', capacity: 1, apartment_class: 'standard', price_per_day: '', description: '' };

export default function Rooms({ user }) {
  const [rooms, setRooms]     = useState([]);
  const [form, setForm]       = useState(EMPTY);
  const [editing, setEditing] = useState(null);
  const [error, setError]     = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => { getRooms().then(setRooms).finally(() => setLoading(false)); }, []);

  function set(k, v) { setForm(f => ({ ...f, [k]: v })); }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      const payload = { ...form, capacity: Number(form.capacity), price_per_day: parseFloat(form.price_per_day) };
      if (editing) {
        const updated = await updateRoom(editing, payload);
        setRooms(rs => rs.map(r => r.id === editing ? updated : r));
        setEditing(null);
      } else {
        const created = await createRoom(payload);
        setRooms(rs => [...rs, created]);
      }
      setForm(EMPTY);
    } catch (err) {
      setError(err.response?.data?.number?.[0] ?? 'Error saving room');
    }
  }

  function startEdit(r) {
    setForm({ number: r.number, capacity: r.capacity, apartment_class: r.apartment_class, price_per_day: r.price_per_day, description: r.description });
    setEditing(r.id);
  }

  async function handleDelete(id) {
    if (!confirm('Delete this room?')) return;
    await deleteRoom(id);
    setRooms(rs => rs.filter(r => r.id !== id));
  }

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" /></div>;

  return (
    <div>
      <h2 className="mb-4">Rooms</h2>

      {user?.role === 'admin' && (
        <div className="card shadow-sm mb-4">
          <div className="card-header bg-dark text-white">{editing ? 'Edit Room' : 'Add Room'}</div>
          <div className="card-body">
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-md-3">
                  <label className="form-label">Number</label>
                  <input className="form-control" value={form.number} onChange={e => set('number', e.target.value)} required />
                </div>
                <div className="col-md-2">
                  <label className="form-label">Capacity</label>
                  <input type="number" className="form-control" min="1" value={form.capacity} onChange={e => set('capacity', e.target.value)} required />
                </div>
                <div className="col-md-3">
                  <label className="form-label">Class</label>
                  <select className="form-select" value={form.apartment_class} onChange={e => set('apartment_class', e.target.value)}>
                    {CLASSES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
                  </select>
                </div>
                <div className="col-md-2">
                  <label className="form-label">Price/night</label>
                  <input type="number" className="form-control" step="0.01" min="0.01" value={form.price_per_day} onChange={e => set('price_per_day', e.target.value)} required />
                </div>
                <div className="col-md-2 d-flex align-items-end">
                  <button type="submit" className="btn btn-primary me-2">{editing ? 'Save' : 'Add'}</button>
                  {editing && <button type="button" className="btn btn-secondary" onClick={() => { setEditing(null); setForm(EMPTY); }}>Cancel</button>}
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-hover bg-white shadow-sm rounded">
          <thead className="table-dark">
            <tr><th>Number</th><th>Class</th><th>Capacity</th><th>Price/night</th><th>Status</th>{user?.role === 'admin' && <th>Actions</th>}</tr>
          </thead>
          <tbody>
            {rooms.map(r => (
              <tr key={r.id}>
                <td className="fw-bold">{r.number}</td>
                <td>{r.apartment_class}</td>
                <td>{r.capacity}</td>
                <td>${parseFloat(r.price_per_day).toFixed(2)}</td>
                <td><span className={`badge ${r.is_available ? 'bg-success' : 'bg-secondary'}`}>{r.is_available ? 'Available' : 'Occupied'}</span></td>
                {user?.role === 'admin' && (
                  <td>
                    <button className="btn btn-sm btn-warning me-1" onClick={() => startEdit(r)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(r.id)}>Delete</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
