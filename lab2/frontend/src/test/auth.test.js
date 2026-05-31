import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    create: vi.fn(() => ({ get: vi.fn(), interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } } })),
  },
}));

import axios from 'axios';
import { isAuthenticated, logout } from '../api/auth';

describe('auth helpers', () => {
  beforeEach(() => localStorage.clear());
  afterEach(() => localStorage.clear());

  it('isAuthenticated returns false when no token', () => {
    expect(isAuthenticated()).toBe(false);
  });

  it('isAuthenticated returns true when token present', () => {
    localStorage.setItem('access_token', 'tok');
    expect(isAuthenticated()).toBe(true);
  });

  it('logout removes tokens', () => {
    localStorage.setItem('access_token', 'tok');
    localStorage.setItem('refresh_token', 'ref');
    logout();
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();
  });

  it('login stores tokens', async () => {
    axios.post.mockResolvedValue({ data: { access: 'acc', refresh: 'ref' } });
    const { login } = await import('../api/auth');
    await login('user', 'pass');
    expect(localStorage.getItem('access_token')).toBe('acc');
    expect(localStorage.getItem('refresh_token')).toBe('ref');
  });
});
