import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getBookings } from '../api/bookings';
import { getInvoices } from '../api/invoices';
import { getRooms } from '../api/rooms';

export default function Dashboard({ user }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!user) return;
    if (user.role === 'admin') {
      Promise.all([getBookings(), getRooms()]).then(([bookings, rooms]) =>
        setData({ bookings, rooms })
      );
    } else {
      Promise.all([getBookings(), getInvoices()]).then(([bookings, invoices]) =>
        setData({ bookings, invoices })
      );
    }
  }, [user]);

  if (!user || !data) return <div className="text-center mt-5"><div className="spinner-border" /></div>;

  const pending = data.bookings?.filter(b => b.status === 'pending') ?? [];

  return (
    <div>
      <h2 className="mb-4">Welcome, <strong>{user.username}</strong>!</h2>

      {user.role === 'admin' ? (
        <>
          <div className="row g-3 mb-4">
            <div className="col-md-4">
              <div className="card text-bg-warning h-100">
                <div className="card-body">
                  <h6>Pending Bookings</h6>
                  <h1 className="display-4 fw-bold">{pending.length}</h1>
                  <Link to="/bookings" className="btn btn-dark btn-sm">View All</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-bg-info h-100">
                <div className="card-body">
                  <h6>Total Rooms</h6>
                  <h1 className="display-4 fw-bold">{data.rooms?.length ?? 0}</h1>
                  <Link to="/rooms" className="btn btn-dark btn-sm">Manage</Link>
                </div>
              </div>
            </div>
          </div>

          {pending.length > 0 && (
            <>
              <h5>Pending Requests</h5>
              <table className="table table-hover bg-white shadow-sm rounded">
                <thead className="table-dark">
                  <tr><th>#</th><th>Client</th><th>Class</th><th>Guests</th><th>Check-in</th><th>Check-out</th><th></th></tr>
                </thead>
                <tbody>
                  {pending.map(b => (
                    <tr key={b.id}>
                      <td>{b.id}</td>
                      <td>{b.client_username}</td>
                      <td>{b.apartment_class}</td>
                      <td>{b.guests_count}</td>
                      <td>{b.check_in}</td>
                      <td>{b.check_out}</td>
                      <td><Link to={`/bookings/${b.id}`} className="btn btn-sm btn-primary">Review</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </>
      ) : (
        <>
          <div className="row g-3 mb-4">
            <div className="col-md-4">
              <div className="card text-bg-primary h-100">
                <div className="card-body text-white">
                  <h6>My Bookings</h6>
                  <h1 className="display-4 fw-bold">{data.bookings?.length ?? 0}</h1>
                  <Link to="/bookings" className="btn btn-light btn-sm">View</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-bg-success h-100">
                <div className="card-body text-white">
                  <h6>My Invoices</h6>
                  <h1 className="display-4 fw-bold">{data.invoices?.length ?? 0}</h1>
                  <Link to="/invoices" className="btn btn-light btn-sm">View</Link>
                </div>
              </div>
            </div>
          </div>
          <Link to="/bookings/new" className="btn btn-primary">+ New Booking</Link>
        </>
      )}
    </div>
  );
}
