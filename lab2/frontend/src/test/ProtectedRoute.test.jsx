import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import ProtectedRoute from '../components/ProtectedRoute';

vi.mock('../api/auth', () => ({ isAuthenticated: vi.fn() }));
import { isAuthenticated } from '../api/auth';

function renderRoute(authenticated) {
  isAuthenticated.mockReturnValue(authenticated);
  render(
    <MemoryRouter initialEntries={['/secret']}>
      <Routes>
        <Route path="/login" element={<div>Login Page</div>} />
        <Route path="/secret" element={
          <ProtectedRoute><div>Secret Content</div></ProtectedRoute>
        } />
      </Routes>
    </MemoryRouter>
  );
}

describe('ProtectedRoute', () => {
  afterEach(() => vi.clearAllMocks());

  it('renders children when authenticated', () => {
    renderRoute(true);
    expect(screen.getByText('Secret Content')).toBeInTheDocument();
  });

  it('redirects to /login when not authenticated', () => {
    renderRoute(false);
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });
});
