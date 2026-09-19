import { get } from 'svelte/store';
import { token, clearSession } from './auth';

export async function api<T = unknown>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  const t = get(token);
  if (t) headers.Authorization = `Bearer ${t}`;

  const res = await fetch(`/api${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    clearSession();
    throw new Error('未登录或登录已过期');
  }

  const text = await res.text();
  let data: unknown = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!res.ok) {
    const body = data as { message?: string; error?: string } | null;
    const msg =
      body?.message ||
      body?.error ||
      `请求失败 (${res.status})`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data as T;
}
