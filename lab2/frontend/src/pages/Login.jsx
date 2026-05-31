import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

export default function Login() {
  const [form, setForm]     = useState({ username: '', password: '' });
  const [error, setError]   = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form.username, form.password);
      navigate('/dashboard');
    } catch {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="row justify-content-center mt-5">
        <div className="col-md-4">
          <div className="card shadow-sm">
            <div className="card-header bg-dark text-white text-center py-3">
              <h4 className="mb-0">&#127968; Hotel Booking</h4>
            </div>
            <div className="card-body p-4">
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    value={form.username}
                    onChange={e => setForm({ ...form, username: e.target.value })}
                    autoFocus
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={form.password}
                    onChange={e => setForm({ ...form, password: e.target.value })}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-dark w-100" disabled={loading}>
                  {loading ? 'Signing in…' : 'Sign In'}
                </button>
              </form>
            </div>
          </div>
          <p className="text-center text-muted mt-3 small">
            Demo: <code>admin / admin123</code> &nbsp;|&nbsp; <code>client1 / pass123</code>
          </p>
        </div>
      </div>
    </div>
  );
}
