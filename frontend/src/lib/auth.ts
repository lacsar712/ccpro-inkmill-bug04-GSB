import { writable } from 'svelte/store';
import type { AuthUser } from './types';

const TOKEN_KEY = 'inkmill01_token';
const USER_KEY = 'inkmill01_user';

function readUser(): AuthUser | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  } catch {
    return null;
  }
}

export const token = writable<string | null>(localStorage.getItem(TOKEN_KEY));
export const user = writable<AuthUser | null>(readUser());

export function setSession(accessToken: string, authUser: AuthUser): void {
  localStorage.setItem(TOKEN_KEY, accessToken);
  localStorage.setItem(USER_KEY, JSON.stringify(authUser));
  token.set(accessToken);
  user.set(authUser);
}

export function clearSession(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  token.set(null);
  user.set(null);
}
