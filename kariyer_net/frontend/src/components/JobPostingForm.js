import React, { useState, useEffect } from 'react';
import { apiPost, apiPut } from '../api';

export default function JobPostingForm({ job = null, onClose, onSuccess }) {
    const [form, setForm] = useState({
        title: '',
        description: '',
        company_id: 1, // Default company ID
        location: '',
        salary_min: '',
        salary_max: '',
        work_mode: 'on-site', // on-site, remote, hybrid
        job_type: 'full-time' // full-time, part-time, contract
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (job) {
            setForm({
                title: job.title || '',
                description: job.description || '',
                company_id: job.company_id || 1,
                location: job.location || '',
                salary_min: job.salary_min || '',
                salary_max: job.salary_max || '',
                work_mode: job.work_mode || 'on-site',
                job_type: job.job_type || 'full-time'
            });
        }
    }, [job]);

    const handleChange = e => {
        const { name, value } = e.target;
        setForm(f => ({ ...f, [name]: value }));
    };

    const handleSubmit = async e => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Client-side validation
        if (form.description.length < 10) {
            setError('İş tanımı en az 10 karakter olmalıdır.');
            setLoading(false);
            return;
        }

        try {
            if (job) {
                // Edit existing job
                await apiPut(`/jobs/${job.id}`, form);
            } else {
                // Create new job
                await apiPost('/jobs/', form);
            }
            onSuccess();
            onClose();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
        }}>
            <div style={{
                backgroundColor: 'white',
                padding: '24px',
                borderRadius: '8px',
                width: '90%',
                maxWidth: '600px',
                maxHeight: '90vh',
                overflowY: 'auto'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h2>{job ? 'İlanı Düzenle' : 'Yeni İlan Ekle'}</h2>
                    <button 
                        onClick={onClose}
                        style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '24px',
                            cursor: 'pointer',
                            color: '#666'
                        }}
                    >
                        ×
                    </button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                            İlan Başlığı *
                        </label>
                        <input
                            name="title"
                            type="text"
                            value={form.title}
                            onChange={handleChange}
                            required
                            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                            placeholder="Örn: Senior Software Engineer"
                        />
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                            İş Tanımı *
                        </label>
                        <textarea
                            name="description"
                            value={form.description}
                            onChange={handleChange}
                            required
                            rows="6"
                            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', resize: 'vertical' }}
                            placeholder="İş tanımını ve gereksinimleri detaylı olarak açıklayın..."
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                                Lokasyon *
                            </label>
                            <input
                                name="location"
                                type="text"
                                value={form.location}
                                onChange={handleChange}
                                required
                                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                                placeholder="Örn: İstanbul, Türkiye"
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                                Çalışma Şekli *
                            </label>
                            <select
                                name="work_mode"
                                value={form.work_mode}
                                onChange={handleChange}
                                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                            >
                                <option value="on-site">Ofiste</option>
                                <option value="remote">Uzaktan</option>
                                <option value="hybrid">Hibrit</option>
                            </select>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                                Minimum Maaş (TL)
                            </label>
                            <input
                                name="salary_min"
                                type="number"
                                value={form.salary_min}
                                onChange={handleChange}
                                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                                placeholder="15000"
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                                Maksimum Maaş (TL)
                            </label>
                            <input
                                name="salary_max"
                                type="number"
                                value={form.salary_max}
                                onChange={handleChange}
                                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                                placeholder="25000"
                            />
                        </div>
                    </div>

                    <div style={{ marginBottom: '24px' }}>
                        <label style={{ display: 'block', marginBottom: '4px', fontWeight: '500' }}>
                            İstihdam Türü *
                        </label>
                        <select
                            name="job_type"
                            value={form.job_type}
                            onChange={handleChange}
                            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                        >
                            <option value="full-time">Tam Zamanlı</option>
                            <option value="part-time">Yarı Zamanlı</option>
                            <option value="contract">Sözleşmeli</option>
                            <option value="internship">Staj</option>
                        </select>
                    </div>

                    {error && (
                        <div style={{ color: 'red', marginBottom: '16px', padding: '8px', backgroundColor: '#ffe6e6', borderRadius: '4px' }}>
                            {error}
                        </div>
                    )}

                    <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                        <button
                            type="button"
                            onClick={onClose}
                            style={{
                                padding: '10px 20px',
                                border: '1px solid #ddd',
                                borderRadius: '4px',
                                background: 'white',
                                cursor: 'pointer'
                            }}
                        >
                            İptal
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                padding: '10px 20px',
                                border: 'none',
                                borderRadius: '4px',
                                background: '#007bff',
                                color: 'white',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.7 : 1
                            }}
                        >
                            {loading ? 'Kaydediliyor...' : (job ? 'Güncelle' : 'İlan Ekle')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
} 