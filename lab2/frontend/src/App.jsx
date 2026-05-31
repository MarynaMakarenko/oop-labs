import { useEffect, useState } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { getMe, isAuthenticated } from './api/auth';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import BookingCreate from './pages/BookingCreate';
import BookingDetail from './pages/BookingDetail';
import Bookings from './pages/Bookings';
import Dashboard from './pages/Dashboard';
import Invoices from './pages/Invoices';
import Login from './pages/Login';
import Rooms from './pages/Rooms';

export default function App() {
  const [user, setUser] = useState(null);
  const location = useLocation();

  useEffect(() => {
    if (isAuthenticated()) {
      getMe().then(setUser).catch(() => setUser(null));
    } else {
      setUser(null);
    }
  }, [location.pathname]);

  const showNav = isAuthenticated() && location.pathname !== '/login';

  return (
    <>
      {showNav && <Navbar user={user} />}
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Dashboard user={user} /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard user={user} /></ProtectedRoute>} />
          <Route path="/bookings" element={<ProtectedRoute><Bookings user={user} /></ProtectedRoute>} />
          <Route path="/bookings/new" element={<ProtectedRoute><BookingCreate /></ProtectedRoute>} />
          <Route path="/bookings/:id" element={<ProtectedRoute><BookingDetail user={user} /></ProtectedRoute>} />
          <Route path="/rooms" element={<ProtectedRoute><Rooms user={user} /></ProtectedRoute>} />
          <Route path="/invoices" element={<ProtectedRoute><Invoices user={user} /></ProtectedRoute>} />
        </Routes>
      </div>
    </>
  );
}
