import api from './client';

export const getInvoices  = ()   => api.get('/invoices/').then(r => r.data);
export const payInvoice   = (id) => api.post(`/invoices/${id}/pay/`).then(r => r.data);
