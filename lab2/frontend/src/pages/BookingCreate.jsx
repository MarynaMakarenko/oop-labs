import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createBooking } from '../api/bookings';

const CLASSES = ['economy', 'standard', 'luxury'];

export default function BookingCreate() {
  const [form, setForm]   = useState({
    guests_count: 1, apartment_class: 'standard',
    check_in: '', check_out: '', notes: '',
  });
  const [error, setError]     = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function set(field, value) {
    setForm(f => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (new Date(form.check_out) <= new Date(form.check_in)) {
      setError('Check-out must be after check-in');
      return;
    }
    setLoading(true);
    try {
      await createBooking({ ...form, guests_count: Number(form.guests_count) });
      navigate('/bookings');
    } catch (err) {
      const msg = err.response?.data;
      setError(typeof msg === 'object' ? JSON.stringify(msg) : 'Failed to create booking');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2 className="mb-4">New Booking Request</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="card shadow-sm">
        <div className="card-body p-4">
          <form onSubmit={handleSubmit}>
            <div className="row g-3">
              <div className="col-md-6">
                <label className="form-label">Guests Count</label>
                <input type="number" className="form-control" min="1" max="10"
                  value={form.guests_count} onChange={e => set('guests_count', e.target.value)} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Apartment Class</label>
                <select className="form-select" value={form.apartment_class}
                  onChange={e => set('apartment_class', e.target.value)}>
                  {CLASSES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
                </select>
              </div>
              <div className="col-md-6">
                <label className="form-label">Check-in</label>
                <input type="date" className="form-control" value={form.check_in}
                  onChange={e => set('check_in', e.target.value)} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Check-out</label>
                <input type="date" className="form-control" value={form.check_out}
                  onChange={e => set('check_out', e.target.value)} required />
              </div>
              <div className="col-12">
                <label className="form-label">Notes (optional)</label>
                <textarea className="form-control" rows="2" value={form.notes}
                  onChange={e => set('notes', e.target.value)} />
              </div>
            </div>
            <div className="mt-4">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Submitting…' : 'Submit Request'}
              </button>
              <button type="button" className="btn btn-secondary ms-2"
                onClick={() => navigate('/bookings')}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
