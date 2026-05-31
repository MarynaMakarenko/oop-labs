import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { approveBooking, getBooking, rejectBooking } from '../api/bookings';
import { getRooms } from '../api/rooms';
import { payInvoice } from '../api/invoices';

const BADGE = { pending: 'bg-warning text-dark', approved: 'bg-success', rejected: 'bg-danger' };

export default function BookingDetail({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [booking, setBooking]   = useState(null);
  const [rooms, setRooms]       = useState([]);
  const [selectedRoom, setRoom] = useState('');
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    getBooking(id).then(b => {
      setBooking(b);
      if (user?.role === 'admin' && b.status === 'pending') {
        getRooms().then(rs =>
          setRooms(rs.filter(r => r.is_available && r.apartment_class === b.apartment_class && r.capacity >= b.guests_count))
        );
      }
    }).finally(() => setLoading(false));
  }, [id, user]);

  async function handleApprove() {
    const updated = await approveBooking(id, Number(selectedRoom));
    setBooking(updated);
  }

  async function handleReject() {
    if (!confirm('Reject this booking?')) return;
    const updated = await rejectBooking(id);
    setBooking(updated);
  }

  async function handlePay() {
    await payInvoice(booking.invoice.id);
    setBooking(b => ({ ...b, invoice: { ...b.invoice, status: 'paid' } }));
  }

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" /></div>;
  if (!booking) return <div className="alert alert-danger">Booking not found.</div>;

  return (
    <div>
      <h2 className="mb-4">Booking #{booking.id}</h2>
      <div className="row g-4">
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-header bg-dark text-white">Details</div>
            <div className="card-body">
              <dl className="row mb-0">
                {user?.role === 'admin' && <><dt className="col-sm-5">Client</dt><dd className="col-sm-7">{booking.client_username}</dd></>}
                <dt className="col-sm-5">Class</dt><dd className="col-sm-7">{booking.apartment_class}</dd>
                <dt className="col-sm-5">Guests</dt><dd className="col-sm-7">{booking.guests_count}</dd>
                <dt className="col-sm-5">Check-in</dt><dd className="col-sm-7">{booking.check_in}</dd>
                <dt className="col-sm-5">Check-out</dt><dd className="col-sm-7">{booking.check_out}</dd>
                <dt className="col-sm-5">Nights</dt><dd className="col-sm-7">{booking.nights}</dd>
                {booking.notes && <><dt className="col-sm-5">Notes</dt><dd className="col-sm-7">{booking.notes}</dd></>}
                <dt className="col-sm-5">Status</dt>
                <dd className="col-sm-7"><span className={`badge ${BADGE[booking.status] ?? 'bg-secondary'}`}>{booking.status}</span></dd>
                {booking.room_number && <><dt className="col-sm-5">Room</dt><dd className="col-sm-7">{booking.room_number}</dd></>}
              </dl>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          {booking.invoice && (
            <div className="card shadow-sm mb-3">
              <div className="card-header bg-dark text-white">Invoice</div>
              <div className="card-body">
                <p><strong>Amount:</strong> ${parseFloat(booking.invoice.amount).toFixed(2)}</p>
                <p><strong>Status:</strong> <span className={`badge ${booking.invoice.status === 'paid' ? 'bg-success' : 'bg-danger'}`}>{booking.invoice.status}</span></p>
                {user?.role === 'client' && booking.invoice.status === 'unpaid' && (
                  <button className="btn btn-success" onClick={handlePay}>Pay Now</button>
                )}
              </div>
            </div>
          )}

          {user?.role === 'admin' && booking.status === 'pending' && (
            <div className="card shadow-sm">
              <div className="card-header bg-dark text-white">Assign Room & Approve</div>
              <div className="card-body">
                {rooms.length > 0 ? (
                  <div className="mb-3">
                    <label className="form-label">Available rooms</label>
                    <select className="form-select" value={selectedRoom} onChange={e => setRoom(e.target.value)}>
                      <option value="">— select room —</option>
                      {rooms.map(r => (
                        <option key={r.id} value={r.id}>
                          Room {r.number} — ${r.price_per_day}/night — {r.capacity} persons
                        </option>
                      ))}
                    </select>
                  </div>
                ) : (
                  <div className="alert alert-warning">No available rooms match this request.</div>
                )}
                <button className="btn btn-success me-2" onClick={handleApprove} disabled={!selectedRoom}>
                  Approve & Assign
                </button>
                <button className="btn btn-danger" onClick={handleReject}>Reject</button>
              </div>
            </div>
          )}
        </div>
      </div>
      <button className="btn btn-secondary mt-4" onClick={() => navigate('/bookings')}>← Back</button>
    </div>
  );
}
