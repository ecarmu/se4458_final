import React, { useState } from 'react';
import { apiPost } from '../api';

export default function LoginRegisterPage() {
    const [mode, setMode] = useState('login'); // 'login' or 'register'
    const [form, setForm] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        phone: '',
        is_company: false,
        is_admin: false
    });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleChange = e => {
        const { name, value, type, checked } = e.target;
        if (type === 'checkbox') {
            if (name === 'is_company') {
                setForm(f => ({ ...f, is_company: checked, is_admin: false }));
            } else if (name === 'is_admin') {
                setForm(f => ({ ...f, is_admin: checked, is_company: false }));
            } else {
                setForm(f => ({ ...f, [name]: checked }));
            }
        } else {
            setForm(f => ({ ...f, [name]: value }));
        }
    };

    const handleSubmit = async e => {
        e.preventDefault();
        setError(null);
        setSuccess(null);
        try {
            if (mode === 'login') {
                const data = await apiPost('/auth/login', { email: form.email, password: form.password });
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('token', data.access_token);
                setSuccess('Giriş başarılı!');
                window.location.href = '/';
            } else {
                const data = await apiPost('/auth/register', form);
                setSuccess('Kayıt başarılı! Şimdi giriş yapabilirsiniz.');
                setMode('login');
            }
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ maxWidth: 400, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px #eee' }}>
            <h2 style={{ textAlign: 'center' }}>{mode === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}</h2>
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
                {mode === 'login' ? (
                    <span>Hesabınız yok mu? <button onClick={() => setMode('register')}>Kayıt Ol</button></span>
                ) : (
                    <span>Zaten hesabınız var mı? <button onClick={() => setMode('login')}>Giriş Yap</button></span>
                )}
            </div>
            <form onSubmit={handleSubmit}>
                <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
                <input name="password" type="password" placeholder="Şifre" value={form.password} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
                {mode === 'register' && (
                    <>
                        <input name="first_name" placeholder="Ad" value={form.first_name} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
                        <input name="last_name" placeholder="Soyad" value={form.last_name} onChange={handleChange} required style={{ width: '100%', marginBottom: 8 }} />
                        <input name="phone" placeholder="Telefon" value={form.phone} onChange={handleChange} style={{ width: '100%', marginBottom: 8 }} />
                        <div style={{ marginBottom: 8 }}>
                            <label style={{ display: 'block', marginBottom: 4 }}>
                                <input name="is_company" type="checkbox" checked={form.is_company} onChange={handleChange} /> Şirket olarak kayıt ol
                            </label>
                            <label style={{ display: 'block', marginBottom: 4 }}>
                                <input name="is_admin" type="checkbox" checked={form.is_admin} onChange={handleChange} /> Admin olarak kayıt ol
                            </label>
                        </div>
                    </>
                )}
                <button type="submit" style={{ width: '100%', padding: 8, background: '#007bff', color: '#fff', border: 'none', borderRadius: 4 }}>
                    {mode === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}
                </button>
                {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
                {success && <div style={{ color: 'green', marginTop: 8 }}>{success}</div>}
            </form>
        </div>
    );
} 