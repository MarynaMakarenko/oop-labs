import { Link, useNavigate } from 'react-router-dom';
import { logout } from '../api/auth';

export default function Navbar({ user }) {
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand fw-bold" to="/dashboard">&#127968; Hotel Booking</Link>
        <div className="navbar-nav ms-auto align-items-center">
          {user?.role === 'admin' && (
            <Link className="nav-link" to="/rooms">Rooms</Link>
          )}
          <Link className="nav-link" to="/bookings">
            {user?.role === 'admin' ? 'Bookings' : 'My Bookings'}
          </Link>
          <Link className="nav-link" to="/invoices">
            {user?.role === 'admin' ? 'Invoices' : 'My Invoices'}
          </Link>
          <span className="nav-link text-secondary">
            {user?.username} ({user?.role})
          </span>
          <button className="btn btn-outline-light btn-sm ms-2" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
