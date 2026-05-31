import { useEffect, useState } from 'react';
import { getInvoices, payInvoice } from '../api/invoices';

export default function Invoices({ user }) {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => { getInvoices().then(setInvoices).finally(() => setLoading(false)); }, []);

  async function handlePay(id) {
    const updated = await payInvoice(id);
    setInvoices(list => list.map(inv => inv.id === id ? updated : inv));
  }

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" /></div>;

  return (
    <div>
      <h2 className="mb-4">{user?.role === 'admin' ? 'All Invoices' : 'My Invoices'}</h2>
      {invoices.length === 0 ? (
        <div className="alert alert-info">No invoices found.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover bg-white shadow-sm rounded">
            <thead className="table-dark">
              <tr><th>#</th><th>Booking</th><th>Amount</th><th>Status</th><th>Issued</th>{user?.role === 'client' && <th></th>}</tr>
            </thead>
            <tbody>
              {invoices.map(inv => (
                <tr key={inv.id}>
                  <td>{inv.id}</td>
                  <td>#{inv.booking}</td>
                  <td className="fw-bold">${parseFloat(inv.amount).toFixed(2)}</td>
                  <td><span className={`badge ${inv.status === 'paid' ? 'bg-success' : 'bg-danger'}`}>{inv.status}</span></td>
                  <td className="text-muted small">{new Date(inv.issued_at).toLocaleDateString()}</td>
                  {user?.role === 'client' && (
                    <td>
                      {inv.status === 'unpaid' && (
                        <button className="btn btn-sm btn-success" onClick={() => handlePay(inv.id)}>Pay</button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
