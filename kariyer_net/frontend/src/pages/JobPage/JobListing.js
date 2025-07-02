// File: JobListing.jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import './JobListing.css';
import { apiGet, apiPost } from '../../api';

const JobListing = () => {
    const { id } = useParams();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [applyStatus, setApplyStatus] = useState(null);
    const [relatedJobs, setRelatedJobs] = useState([]);
    const [relatedPage, setRelatedPage] = useState(1);
    const [relatedTotal, setRelatedTotal] = useState(0);
    const relatedPageSize = 3;
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || 'null');

    useEffect(() => {
        async function fetchJob() {
            setLoading(true);
            setError(null);
            try {
                // Fetch job details from backend
                const job = await apiGet(`/jobs/${id}`);
                setJob(job);
            } catch (err) {
                setError('Failed to fetch job: ' + err.message);
            }
            setLoading(false);
        }
        fetchJob();
    }, [id]);

    useEffect(() => {
        async function fetchRelated() {
            try {
                const skip = (relatedPage - 1) * relatedPageSize;
                const jobs = await apiGet(`/jobs/${id}/related?skip=${skip}&limit=${relatedPageSize}`);
                setRelatedJobs(jobs);
                // For demo, we don't have total count, so just guess if there are more
                setRelatedTotal(jobs.length < relatedPageSize && relatedPage > 1 ? (relatedPage - 1) * relatedPageSize + jobs.length : relatedPage * relatedPageSize + 1);
            } catch (err) {
                setRelatedJobs([]);
            }
        }
        fetchRelated();
    }, [id, relatedPage]);

    const handleLogout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        window.location.reload();
    };

    const handleApply = async () => {
        if (!user) {
            navigate('/auth');
            return;
        }
        try {
            await apiPost(`/jobs/${id}/apply`, { user_id: user.id });
            setApplyStatus('success');
        } catch (err) {
            if (err.status === 409) {
                setApplyStatus('already');
            } else {
                setApplyStatus('error');
            }
        }
    };

    return (
        <div className="job-listing-container">
            {/* HEADER */}
            <header className="header">
                <div className="logo">kariyer.net</div>
                {user ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div style={{ background: '#eee', padding: '6px 14px', borderRadius: 16, fontWeight: 500 }}>{user.first_name}</div>
                        <button onClick={handleLogout} style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer' }}>Çıkış</button>
                    </div>
                ) : (
                    <button className="login-button" onClick={() => navigate('/auth')}>Giriş Yap / Üye Ol</button>
                )}
            </header>

            {/* LEFT COLUMN */}
            <div className="job-left">
                {/* 1) HEADER */}
                <div className="job-listing-header">
                    <div className="job-header-info-wrapper">
                        <div className="job-header-info">
                            {loading && <p>Loading...</p>}
                            {error && <p style={{color:'red'}}>{error}</p>}
                            {job && <>
                                <p style={{ fontSize: "18px", fontWeight: 500, marginBottom: "8px" }}>{job.title}</p>
                                <p style={{fontSize: "16px"}}>{job.company}</p>
                                <p className="location">{job.location} • {job.work_mode || job.mode}</p>
                            </>}
                        </div>
                        <div className="job-actions">
                            <button className="btn-apply" onClick={handleApply} disabled={applyStatus === 'success' || applyStatus === 'already'}>
                                {applyStatus === 'success' ? 'Başvuruldu' : applyStatus === 'already' ? 'Zaten başvurdunuz' : 'Başvur'}
                            </button>
                            {applyStatus === 'error' && <span style={{color:'red'}}>Başvuru başarısız</span>}
                            <button className="btn-save">Kaydet</button>
                        </div>
                    </div>

                    <div className="job-stats" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        {job && <>
                            <div>
                                <div>Çalışma Şekli:<strong> {job.job_type || 'Bilinmiyor'}</strong></div>
                                <div>Başvuru Sayısı:<strong> {job.application_count !== undefined && job.application_count !== null ? job.application_count : 'Bilinmiyor'}</strong></div>
                            </div>
                            <div style={{ marginLeft: 'auto', textAlign: 'right', color: '#888', fontSize: '0.95em' }}>
                                Son Güncelleme:<br />
                                <strong>{job.last_updated ? new Date(job.last_updated).toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' }) : '-'}</strong>
                            </div>
                        </>}
                    </div>
                </div>

                {/* 2) MAIN CONTENT */}
                <div className="job-content">
                    <section className="description">
                        <p style={{ fontSize: '16px', fontWeight: '500', marginBottom: '8px' }}>GENEL NİTELİKLER VE İŞ TANIMI</p>
                        {job ? (
                            <>
                                <p>{job.description}</p>
                                <p>
                                    {job.requirements && job.requirements.map((req, i) => <span key={i}>{req}<br /></span>)}
                                </p>
                            </>
                        ) : (
                            <p>Yiyecek ve içecek sektöründe hizmet veren işletmemizde…</p>
                        )}
                    </section>
                </div>
            </div>

            {/* RIGHT COLUMN */}
            <aside className="job-sidebar">
                <h4 style={{ fontWeight: '500' }}>İlginizi Çekebilecek İlanlar</h4>
                <div className="job-results">
                    {relatedJobs.length === 0 && <div>İlgili ilan bulunamadı.</div>}
                    {relatedJobs.map((s) => (
                        <Link to={`/job/${s.id}`} key={s.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                            <div className="job-card compact">
                                <div className="logo-container">
                                    {s.logo ? (
                                        <img src={s.logo} alt={s.title} className="company-logo" />
                                    ) : (
                                        <div className="logo-placeholder">
                                            {s.company?.charAt(0) || '?'}
                                        </div>
                                    )}
                                </div>
                                <div className="job-info">
                                    <p className="job-title">{s.title}</p>
                                    <p className="company-name">{s.company}</p>
                                    <p className="job-meta">{s.location}</p>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
                {/* Pagination controls for related jobs */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 12 }}>
                    <button onClick={() => setRelatedPage(p => Math.max(1, p - 1))} disabled={relatedPage === 1}>Önceki</button>
                    <span>Sayfa {relatedPage}</span>
                    <button onClick={() => setRelatedPage(p => p + 1)} disabled={relatedJobs.length < relatedPageSize}>Sonraki</button>
                </div>
            </aside>
        </div>
    );
};

export default JobListing;
