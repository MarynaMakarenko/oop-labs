import api from './client';

export const getRooms    = ()      => api.get('/rooms/').then(r => r.data);
export const getRoom     = (id)    => api.get(`/rooms/${id}/`).then(r => r.data);
export const createRoom  = (data)  => api.post('/rooms/', data).then(r => r.data);
export const updateRoom  = (id, d) => api.put(`/rooms/${id}/`, d).then(r => r.data);
export const deleteRoom  = (id)    => api.delete(`/rooms/${id}/`);
