import api from './client';

export const getBookings  = ()         => api.get('/bookings/').then(r => r.data);
export const getBooking   = (id)       => api.get(`/bookings/${id}/`).then(r => r.data);
export const createBooking = (data)    => api.post('/bookings/', data).then(r => r.data);
export const approveBooking = (id, roomId) =>
  api.post(`/bookings/${id}/approve/`, { room_id: roomId }).then(r => r.data);
export const rejectBooking  = (id)     => api.post(`/bookings/${id}/reject/`).then(r => r.data);
