import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getBookings } from '../api/bookings';

const STATUS_BADGE = {
  pending:   'bg-warning text-dark',
  approved:  'bg-success',
  rejected:  'bg-danger',
  completed: 'bg-secondary',
};

export default function Bookings({ user }) {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    getBookings().then(setBookings).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" /></div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>{user?.role === 'admin' ? 'All Bookings' : 'My Bookings'}</h2>
        {user?.role === 'client' && (
          <Link to="/bookings/new" className="btn btn-primary">+ New Booking</Link>
        )}
      </div>

      {bookings.length === 0 ? (
        <div className="alert alert-info">No bookings found.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover bg-white shadow-sm rounded">
            <thead className="table-dark">
              <tr>
                <th>#</th>
                {user?.role === 'admin' && <th>Client</th>}
                <th>Class</th><th>Guests</th><th>Check-in</th><th>Check-out</th>
                <th>Nights</th><th>Room</th><th>Status</th><th></th>
              </tr>
            </thead>
            <tbody>
              {bookings.map(b => (
                <tr key={b.id}>
                  <td>{b.id}</td>
                  {user?.role === 'admin' && <td>{b.client_username}</td>}
                  <td>{b.apartment_class}</td>
                  <td>{b.guests_count}</td>
                  <td>{b.check_in}</td>
                  <td>{b.check_out}</td>
                  <td>{b.nights}</td>
                  <td>{b.room_number ?? '—'}</td>
                  <td><span className={`badge ${STATUS_BADGE[b.status] ?? 'bg-secondary'}`}>{b.status}</span></td>
                  <td><Link to={`/bookings/${b.id}`} className="btn btn-sm btn-outline-primary">Details</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
