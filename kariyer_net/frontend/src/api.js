const API_URL = process.env.REACT_APP_API_URL;

// Generic GET
export async function apiGet(path) {
  const res = await fetch(`${API_URL}${path}`, { credentials: 'include' });
  if (!res.ok) {
    const text = await res.text();
    const error = new Error(text);
    error.status = res.status;
    throw error;
  }
  return res.json();
}

// Generic POST
export async function apiPost(path, data) {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const headers = { 'Content-Type': 'application/json' };
  
  if (user) {
    headers['X-User-Info'] = JSON.stringify(user);
  }
  
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers,
    credentials: 'include',
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const text = await res.text();
    const error = new Error(text);
    error.status = res.status;
    throw error;
  }
  return res.json();
}

// Generic PUT
export async function apiPut(path, data) {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const headers = { 'Content-Type': 'application/json' };
  
  if (user) {
    headers['X-User-Info'] = JSON.stringify(user);
  }
  
  const res = await fetch(`${API_URL}${path}`, {
    method: 'PUT',
    headers,
    credentials: 'include',
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const text = await res.text();
    const error = new Error(text);
    error.status = res.status;
    throw error;
  }
  return res.json();
}

// Add DELETE as needed