const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface RequestOptions {
  headers?: Record<string, string>;
  body?: unknown;
}

interface ApiError {
  status: number;
  message: string;
  detail?: unknown;
}

function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

function buildHeaders(custom?: Record<string, string>): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...custom,
  };

  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = {
      status: response.status,
      message: response.statusText,
    };

    try {
      error.detail = await response.json();
    } catch {
      // response body is not JSON
    }

    throw error;
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

async function request<T>(method: string, path: string, options?: RequestOptions): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const headers = buildHeaders(options?.headers);

  const config: RequestInit = {
    method,
    headers,
  };

  if (options?.body !== undefined) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, config);
  return handleResponse<T>(response);
}

export const api = {
  get<T>(path: string, options?: RequestOptions): Promise<T> {
    return request<T>('GET', path, options);
  },

  post<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return request<T>('POST', path, {...options, body});
  },

  put<T>(path: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return request<T>('PUT', path, {...options, body});
  },

  delete<T>(path: string, options?: RequestOptions): Promise<T> {
    return request<T>('DELETE', path, options);
  },
};
