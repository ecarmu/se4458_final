// File: JobSearchResultPage.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './JobSearchResultPage.css';
import { apiGet, apiPost } from '../../api';
import JobPostingForm from '../../components/JobPostingForm';

const allFilters = [
    { label: 'Yazılım Uzmanı', type: 'Pozisyon' },
    { label: 'İzmir', type: 'Şehir' },
    { label: 'Türkiye', type: 'Ülke' },
];

const cityDistricts = {
  "İstanbul": ["Kadıköy", "Beşiktaş", "Şişli", "Üsküdar", "Bakırköy"],
  "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Sincan"],
  "İzmir": ["Balçova", "Bornova", "Karşıyaka", "Konak", "Buca"],
  "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "Mudanya", "Gemlik"]
};

export default function JobSearchResultPage() {
    const [selectedFilters, setSelectedFilters] = useState(allFilters);
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [applyStatus, setApplyStatus] = useState({});
    const [showJobForm, setShowJobForm] = useState(false);
    const [editingJob, setEditingJob] = useState(null);
    
    // Two sets of filter state
    const [pendingFilters, setPendingFilters] = useState({
        query: '',
        location: '',
        workPreferences: { onsite: false, remote: false, hybrid: false },
        dateFilter: 'all',
        country: '',
        city: '',
        district: ''
    });
    const [activeFilters, setActiveFilters] = useState({
        query: '',
        location: '',
        workPreferences: { onsite: false, remote: false, hybrid: false },
        dateFilter: 'all',
        country: '',
        city: '',
        district: ''
    });
    
    // Pagination
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalResults, setTotalResults] = useState(0);
    const itemsPerPage = 10;
    
    const navigate = useNavigate();
    const location = useLocation();
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    
    // On initial load, set both pendingFilters and activeFilters from navigation state
    useEffect(() => {
        const initialFilters = location.state?.filters || {};
        setPendingFilters({
            query: initialFilters.query || '',
            location: initialFilters.location || '',
            workPreferences: initialFilters.workPreferences || { onsite: false, remote: false, hybrid: false },
            dateFilter: initialFilters.dateFilter || 'all',
            country: initialFilters.country || '',
            city: initialFilters.city || '',
            district: initialFilters.district || ''
        });
        setActiveFilters({
            query: initialFilters.query || '',
            location: initialFilters.location || '',
            workPreferences: initialFilters.workPreferences || { onsite: false, remote: false, hybrid: false },
            dateFilter: initialFilters.dateFilter || 'all',
            country: initialFilters.country || '',
            city: initialFilters.city || '',
            district: initialFilters.district || ''
        });
        console.log('setActiveFilters called with:', {
            query: initialFilters.query || '',
            location: initialFilters.location || '',
            workPreferences: initialFilters.workPreferences || { onsite: false, remote: false, hybrid: false },
            dateFilter: initialFilters.dateFilter || 'all',
            country: initialFilters.country || '',
            city: initialFilters.city || '',
            district: initialFilters.district || ''
        });
        // If no filters, stop loading
        if (
            !initialFilters.query &&
            !initialFilters.location &&
            !initialFilters.city &&
            !initialFilters.country &&
            !initialFilters.district
        ) {
            setLoading(false);
        }
    }, []);

    // Fetch jobs only when activeFilters or currentPage changes
    useEffect(() => {
        fetchJobs();
        // eslint-disable-next-line
    }, [activeFilters, currentPage]);

    async function fetchJobs() {
        setLoading(true);
        setError(null);
        try {
            // Build query parameters from activeFilters
            const params = new URLSearchParams();
            params.append('query', activeFilters.query || '');
            params.append('location', activeFilters.location || '');
            params.append('page', currentPage.toString());
            params.append('limit', itemsPerPage.toString());
            if (activeFilters.workPreferences.onsite || activeFilters.workPreferences.remote || activeFilters.workPreferences.hybrid) {
                const modes = [];
                if (activeFilters.workPreferences.onsite) modes.push('onsite');
                if (activeFilters.workPreferences.remote) modes.push('remote');
                if (activeFilters.workPreferences.hybrid) modes.push('hybrid');
                params.append('work_mode', modes.join(','));
            }
            if (activeFilters.dateFilter !== 'all') {
                params.append('date_filter', activeFilters.dateFilter);
            }
            if (activeFilters.country) params.append('country', activeFilters.country);
            if (activeFilters.city) params.append('city', activeFilters.city);
            if (activeFilters.district) params.append('district', activeFilters.district);
            if (user && user.id) params.append('user_id', user.id);
            // Debug log
            console.log('fetchJobs called with:', { activeFilters, query: `/jobs/?${params.toString()}` });
            const response = await apiGet(`/jobs/?${params.toString()}`);
            if (response.jobs) {
                setJobs(response.jobs);
                setTotalPages(response.total_pages || 1);
                setTotalResults(response.total_results || response.jobs.length);
            } else {
                setJobs(response);
                setTotalPages(1);
                setTotalResults(response.length);
            }
        } catch (err) {
            setError('Failed to fetch jobs: ' + err.message);
        }
        setLoading(false);
    }

    const clearFilters = () => setSelectedFilters([]);

    // Handlers for pendingFilters (search bar and filters)
    const handlePendingChange = (field, value) => {
        setPendingFilters(prev => ({ ...prev, [field]: value }));
    };
    const handlePendingWorkPref = (key, value) => {
        setPendingFilters(prev => ({ ...prev, workPreferences: { ...prev.workPreferences, [key]: value } }));
    };

    // When İş Bul is clicked, set activeFilters to pendingFilters and reset page
    const handleSearch = (e) => {
        e.preventDefault();
        setActiveFilters({ ...pendingFilters });
        setCurrentPage(1);
    };

    // Remove a tag (from activeFilters and pendingFilters)
    const removeFilter = (field, value) => {
        if (field === 'workPreferences') {
            setActiveFilters(prev => ({ ...prev, workPreferences: { ...prev.workPreferences, [value]: false } }));
            setPendingFilters(prev => ({ ...prev, workPreferences: { ...prev.workPreferences, [value]: false } }));
        } else if (field === 'dateFilter') {
            setActiveFilters(prev => ({ ...prev, dateFilter: 'all' }));
            setPendingFilters(prev => ({ ...prev, dateFilter: 'all' }));
        } else {
            setActiveFilters(prev => ({ ...prev, [field]: '' }));
            setPendingFilters(prev => ({ ...prev, [field]: '' }));
        }
        setCurrentPage(1);
    };
    // Clear all filters
    const clearAllFilters = () => {
        setActiveFilters({
            query: '',
            location: '',
            workPreferences: { onsite: false, remote: false, hybrid: false },
            dateFilter: 'all',
            country: '',
            city: '',
            district: ''
        });
        setPendingFilters({
            query: '',
            location: '',
            workPreferences: { onsite: false, remote: false, hybrid: false },
            dateFilter: 'all',
            country: '',
            city: '',
            district: ''
        });
        setCurrentPage(1);
    };

    const handleApplyFilters = () => {
        setActiveFilters({ ...pendingFilters });
        setCurrentPage(1);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const handleApply = async (jobId) => {
        // Check if user is logged in
        const user = JSON.parse(localStorage.getItem('user') || 'null');
        if (!user) {
            navigate('/auth');
            return;
        }
        try {
            await apiPost(`/jobs/${jobId}/apply`, { user_id: user.id });
            setApplyStatus((prev) => ({ ...prev, [jobId]: 'success' }));
        } catch (err) {
            if (err.status === 409) {
                setApplyStatus((prev) => ({ ...prev, [jobId]: 'already' }));
            } else {
                setApplyStatus((prev) => ({ ...prev, [jobId]: 'error' }));
            }
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        window.location.reload();
    };

    const handleEditJob = (job) => {
        setEditingJob(job);
        setShowJobForm(true);
    };

    const handleJobSuccess = () => {
        // Refresh the jobs list
        window.location.reload();
    };

    return (
        <div style={{ backgroundColor: '#f8f9fa' }}>
            {/* Header */}
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

            <div className="job-search-bar">
                <section
                    className="hero"
                    style={{ backgroundColor: '#fff', paddingTop: '20px', paddingBottom: '1px' }}
                >
                    <form className="search-bar" onSubmit={handleSearch}>
                        <input 
                            type="text" 
                            placeholder="Pozisyon ara" 
                            value={pendingFilters.query}
                            onChange={e => handlePendingChange('query', e.target.value)}
                        />
                        <input 
                            type="text" 
                            placeholder="Şehir veya ilçe ara" 
                            value={pendingFilters.location}
                            onChange={e => handlePendingChange('location', e.target.value)}
                        />
                        <button type="submit">İş Bul</button>
                    </form>
                </section>
            </div>

            {(activeFilters.query || activeFilters.location || activeFilters.country || activeFilters.city || activeFilters.district || activeFilters.workPreferences.onsite || activeFilters.workPreferences.remote || activeFilters.workPreferences.hybrid || activeFilters.dateFilter !== 'all') && (
                <div style={{ margin: '16px 0', display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
                    <span style={{ fontWeight: 600 }}>Seçili Filtreler ({
                        [
                            activeFilters.query && 1,
                            activeFilters.location && 1,
                            activeFilters.country && 1,
                            activeFilters.city && 1,
                            activeFilters.district && 1,
                            activeFilters.workPreferences.onsite && 1,
                            activeFilters.workPreferences.remote && 1,
                            activeFilters.workPreferences.hybrid && 1,
                            activeFilters.dateFilter !== 'all' && 1
                        ].filter(Boolean).length
                    })</span>
                    <button
                        style={{ color: '#a259c6', background: 'none', border: 'none', cursor: 'pointer', marginLeft: 8 }}
                        onClick={clearAllFilters}
                    >
                        Filtreleri Temizle
                    </button>
                    {activeFilters.query && (
                        <span className="tag">
                            {activeFilters.query} <span onClick={() => removeFilter('query')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.location && (
                        <span className="tag">
                            {activeFilters.location} <span onClick={() => removeFilter('location')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.country && (
                        <span className="tag">
                            {activeFilters.country} <span onClick={() => removeFilter('country')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.city && (
                        <span className="tag">
                            {activeFilters.city} <span onClick={() => removeFilter('city')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.district && (
                        <span className="tag">
                            {activeFilters.district} <span onClick={() => removeFilter('district')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.workPreferences.onsite && (
                        <span className="tag">
                            İş Yerinde <span onClick={() => removeFilter('workPreferences', 'onsite')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.workPreferences.remote && (
                        <span className="tag">
                            Uzaktan <span onClick={() => removeFilter('workPreferences', 'remote')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.workPreferences.hybrid && (
                        <span className="tag">
                            Hibrit <span onClick={() => removeFilter('workPreferences', 'hybrid')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                    {activeFilters.dateFilter !== 'all' && (
                        <span className="tag">
                            {activeFilters.dateFilter === 'today' ? 'Bugünün ilanları' : activeFilters.dateFilter === '3hours' ? 'Son 3 saat' : 'Son 8 saat'}
                            <span onClick={() => removeFilter('dateFilter')} style={{ cursor: 'pointer', marginLeft: 4 }}>×</span>
                        </span>
                    )}
                </div>
            )}

            <div className="job-page-container">
                {/* Sidebar */}
                <aside className="sidebar">
                    <h3>Ülke / Şehir / İlçe</h3>
                    <select value={pendingFilters.country} onChange={e => handlePendingChange('country', e.target.value)}>
                        <option value="">Tümü</option>
                        <option value="Türkiye">Türkiye</option>
                    </select>
                    <select value={pendingFilters.city} onChange={e => handlePendingChange('city', e.target.value)}>
                        <option value="" disabled selected={pendingFilters.city === ""}>Şehir seçin</option>
                        <option value="İstanbul">İstanbul</option>
                        <option value="Ankara">Ankara</option>
                        <option value="İzmir">İzmir</option>
                        <option value="Bursa">Bursa</option>
                    </select>
                    <select value={pendingFilters.district} onChange={e => handlePendingChange('district', e.target.value)}>
                        <option value="">İlçe seçin</option>
                        {(cityDistricts[pendingFilters.city] || []).map(d => (
                            <option key={d} value={d}>{d}</option>
                        ))}
                    </select>

                    <h3>Çalışma Tercihi</h3>
                    <label>
                        <input 
                            type="checkbox" 
                            checked={pendingFilters.workPreferences.onsite}
                            onChange={e => handlePendingWorkPref('onsite', e.target.checked)}
                        /> İş Yerinde
                    </label>
                    <label>
                        <input 
                            type="checkbox" 
                            checked={pendingFilters.workPreferences.remote}
                            onChange={e => handlePendingWorkPref('remote', e.target.checked)}
                        /> Uzaktan / Remote
                    </label>
                    <label>
                        <input 
                            type="checkbox" 
                            checked={pendingFilters.workPreferences.hybrid}
                            onChange={e => handlePendingWorkPref('hybrid', e.target.checked)}
                        /> Hibrit
                    </label>

                    <h3>Tarih</h3>
                    <label>
                        <input 
                            type="radio" 
                            name="date" 
                            checked={pendingFilters.dateFilter === 'all'}
                            onChange={() => handlePendingChange('dateFilter', 'all')}
                        /> Tümü
                    </label>
                    <label>
                        <input 
                            type="radio" 
                            name="date" 
                            checked={pendingFilters.dateFilter === 'today'}
                            onChange={() => handlePendingChange('dateFilter', 'today')}
                        /> Bugünün ilanları
                    </label>
                    <label>
                        <input 
                            type="radio" 
                            name="date" 
                            checked={pendingFilters.dateFilter === '3hours'}
                            onChange={() => handlePendingChange('dateFilter', '3hours')}
                        /> Son 3 saat
                    </label>
                    <label>
                        <input 
                            type="radio" 
                            name="date" 
                            checked={pendingFilters.dateFilter === '8hours'}
                            onChange={() => handlePendingChange('dateFilter', '8hours')}
                        /> Son 8 saat
                    </label>

                    <button className="apply-btn" onClick={handleApplyFilters}>Uygula</button>
                </aside>

                {/* Middle column: results */}
                <section className="results-column">
                    {loading && <div>Loading jobs...</div>}
                    {error && <div style={{color:'red'}}>{error}</div>}
                    
                    {/* Results count and pagination info */}
                    {!loading && !error && (
                        <div style={{ marginBottom: '20px', padding: '10px', background: '#fff', borderRadius: '4px' }}>
                            <p><strong>{totalResults}</strong> sonuç bulundu</p>
                            {totalPages > 1 && (
                                <p>Sayfa {currentPage} / {totalPages}</p>
                            )}
                        </div>
                    )}
                    
                    <div className="job-results">
                        {jobs.map((job) => (
                            <Link to={`/job/${job.id}`} key={job.id} style={{ textDecoration: 'none', color: 'inherit' }}>
                                <div className="job-card compact">
                                    <div className="logo-container">
                                        {job.logo ? (
                                            <img src={job.logo} alt={job.company} className="company-logo" />
                                        ) : (
                                            <div className="logo-placeholder">
                                                {job.company?.charAt(0) || '?'}
                                            </div>
                                        )}
                                    </div>
                                    <div className="job-info">
                                        <h4 className="job-title">{job.title}</h4>
                                        <p className="company-name">{job.company}</p>
                                        <p className="job-meta">{job.location} • {job.mode || job.work_mode}</p>
                                        <p className="job-type">{job.type || job.job_type}</p>
                                                                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                            <button className="apply-btn" onClick={e => { e.preventDefault(); handleApply(job.id); }} disabled={applyStatus[job.id] === 'success' || applyStatus[job.id] === 'already'}>
                                {applyStatus[job.id] === 'success' ? 'Başvuruldu' : applyStatus[job.id] === 'already' ? 'Zaten başvurdunuz' : 'Başvur'}
                            </button>
                            {user && (user.is_admin || user.is_company) && (
                                <button 
                                    onClick={e => { e.preventDefault(); handleEditJob(job); }}
                                    style={{
                                        background: 'none',
                                        border: 'none',
                                        cursor: 'pointer',
                                        padding: '4px',
                                        color: '#666'
                                    }}
                                    title="İlanı Düzenle"
                                >
                                    ✏️
                                </button>
                            )}
                        </div>
                        {applyStatus[job.id] === 'error' && <span style={{color:'red'}}>Başvuru başarısız</span>}
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                    
                    {/* Pagination Controls */}
                    {!loading && !error && totalPages > 1 && (
                        <div style={{ 
                            display: 'flex', 
                            justifyContent: 'center', 
                            alignItems: 'center', 
                            gap: '10px', 
                            marginTop: '30px',
                            padding: '20px'
                        }}>
                            <button 
                                onClick={() => handlePageChange(currentPage - 1)}
                                disabled={currentPage === 1}
                                style={{
                                    padding: '8px 16px',
                                    border: '1px solid #ddd',
                                    background: currentPage === 1 ? '#f5f5f5' : '#fff',
                                    cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
                                    borderRadius: '4px'
                                }}
                            >
                                Önceki
                            </button>
                            
                            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                                let pageNum;
                                if (totalPages <= 5) {
                                    pageNum = i + 1;
                                } else if (currentPage <= 3) {
                                    pageNum = i + 1;
                                } else if (currentPage >= totalPages - 2) {
                                    pageNum = totalPages - 4 + i;
                                } else {
                                    pageNum = currentPage - 2 + i;
                                }
                                
                                return (
                                    <button
                                        key={pageNum}
                                        onClick={() => handlePageChange(pageNum)}
                                        style={{
                                            padding: '8px 12px',
                                            border: '1px solid #ddd',
                                            background: currentPage === pageNum ? '#007bff' : '#fff',
                                            color: currentPage === pageNum ? '#fff' : '#333',
                                            cursor: 'pointer',
                                            borderRadius: '4px'
                                        }}
                                    >
                                        {pageNum}
                                    </button>
                                );
                            })}
                            
                            <button 
                                onClick={() => handlePageChange(currentPage + 1)}
                                disabled={currentPage === totalPages}
                                style={{
                                    padding: '8px 16px',
                                    border: '1px solid #ddd',
                                    background: currentPage === totalPages ? '#f5f5f5' : '#fff',
                                    cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
                                    borderRadius: '4px'
                                }}
                            >
                                Sonraki
                            </button>
                        </div>
                    )}
                </section>
            </div>

            {/* Job Posting Form Modal */}
            {showJobForm && (
                <JobPostingForm
                    job={editingJob}
                    onClose={() => {
                        setShowJobForm(false);
                        setEditingJob(null);
                    }}
                    onSuccess={handleJobSuccess}
                />
            )}
        </div>
    );
}
