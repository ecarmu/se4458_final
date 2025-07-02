import React, { useState, useEffect, useRef } from 'react';
import './JobSearchHomePage.css';
import { Link, useNavigate } from 'react-router-dom';
import { apiGet, apiPost } from '../../api';
import JobPostingForm from '../../components/JobPostingForm';
import JobAlertModal from '../../components/JobAlertModal';

const popularSearches = [
    'Finans Uzmanı', 'Dijital Pazarlama Uzmanı', 'Yazılım Geliştirme Uzmanı',
    'Proje Yöneticisi', 'İK Uzmanı',
    'İstanbul (Avrupa)', 'İstanbul (Asya)', 'Ankara', 'İzmir', 'Bursa', 'İstanbul'
];

const cityDistricts = {
    "İstanbul": ["Kadıköy", "Beşiktaş", "Şişli", "Üsküdar", "Bakırköy"],
    "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Sincan"],
    "İzmir": ["Balçova", "Bornova", "Karşıyaka", "Konak", "Buca"],
    "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "Mudanya", "Gemlik"]
};

const cityList = [
    "İstanbul", "Ankara", "İzmir", "Bursa", "Adana", "Antalya", "Konya", "Gaziantep", "Kayseri", "Mersin",
    "Eskişehir", "Samsun", "Trabzon", "Erzurum", "Malatya", "Sakarya", "Kocaeli", "Denizli", "Manisa", "Balıkesir"
];
const positionList = [
    "Yazılım Mühendisi", "Öğretmen", "Doktor", "Hemşire", "Avukat", "Mimar", "Mühendis", "Pazarlama Uzmanı", "Satış Temsilcisi",
    "Muhasebeci", "Finans Uzmanı", "İnsan Kaynakları Uzmanı", "Proje Yöneticisi", "Grafik Tasarımcı", "Veri Analisti",
    "İş Analisti", "Web Geliştirici", "Mobil Uygulama Geliştirici", "Sistem Yöneticisi", "Elektrik Mühendisi", "Makine Mühendisi",
    "İnşaat Mühendisi", "Çevirmen", "Editör", "Yönetici Asistanı", "Sekreter", "Müşteri Temsilcisi", "Depo Sorumlusu"
];

export default function JobSearchHomePage() {
    const [query, setQuery] = useState('');
    const [location, setLocation] = useState('');
    const [showJobForm, setShowJobForm] = useState(false);
    
    // Filter states
    const [workPreferences, setWorkPreferences] = useState({
        onsite: false,
        remote: false,
        hybrid: false
    });
    const [dateFilter, setDateFilter] = useState('all'); // all, today, 3hours, 8hours
    const [country, setCountry] = useState('');
    const [city, setCity] = useState('');
    const [district, setDistrict] = useState('');
    
    const navigate = useNavigate();
    const [user] = useState(() => JSON.parse(localStorage.getItem('user') || 'null'));
    const [recentSearches, setRecentSearches] = useState([]);
    const [featuredJobs, setFeaturedJobs] = useState([]);
    const [cityLoading, setCityLoading] = useState(true);
    const [cityError, setCityError] = useState(null);
    const [userCity, setUserCity] = useState('');
    const [citySuggestions, setCitySuggestions] = useState([]);
    const [showCitySuggestions, setShowCitySuggestions] = useState(false);
    const [positionSuggestions, setPositionSuggestions] = useState([]);
    const [showPositionSuggestions, setShowPositionSuggestions] = useState(false);
    const cityInputRef = useRef(null);
    const positionInputRef = useRef(null);
    const [showAIChat, setShowAIChat] = useState(false);
    const [aiMessages, setAIMessages] = useState([]);
    const [aiInput, setAIInput] = useState('');
    const [aiLoading, setAILoading] = useState(false);
    const [showJobAlertModal, setShowJobAlertModal] = useState(false);
    const [alerts, setAlerts] = useState([]);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        if (!user || !user.id) return;
        async function fetchRecentSearches() {
            try {
                const searches = await apiGet(`/jobs/search/history?user_id=${user.id}`);
                setRecentSearches(searches);
            } catch (err) {
                setRecentSearches([]);
            }
        }
        fetchRecentSearches();
    }, [user?.id]);

    // Fetch featured jobs based on user's city
    useEffect(() => {
        async function fetchFeaturedJobs() {
            setCityLoading(true);
            setCityError(null);
            let userCity = '';
            try {
                // 1. Get geolocation
                await new Promise((resolve, reject) => {
                    if (!navigator.geolocation) {
                        reject('Geolocation not supported');
                        return;
                    }
                    navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 10000 });
                }).then(async (position) => {
                    const { latitude, longitude } = position.coords;
                    // 2. Reverse geocode to get city
                    const geoResp = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`);
                    const geoData = await geoResp.json();
                    userCity = geoData.address?.city || geoData.address?.town || geoData.address?.village || geoData.address?.state || '';
                    setUserCity(userCity);
                    console.log('Detected user city:', userCity);
                });
            } catch (err) {
                setCityError('Konum alınamadı, genel ilanlar gösteriliyor.');
                userCity = '';
                setUserCity('');
            }
            // 3. Fetch jobs for the city
            let jobs = [];
            try {
                if (userCity) {
                    jobs = await apiGet(`/jobs/?city=${encodeURIComponent(userCity)}&limit=5`);
                    jobs = jobs.jobs || jobs; // handle both array and {jobs:[]} response
                }
                // 4. If fewer than 5, fetch more jobs (no city filter)
                if (!jobs || jobs.length < 5) {
                    const moreJobs = await apiGet(`/jobs/?limit=5`);
                    const more = moreJobs.jobs || moreJobs;
                    // Avoid duplicates
                    const jobIds = new Set(jobs.map(j => j.id));
                    jobs = jobs.concat(more.filter(j => !jobIds.has(j.id))).slice(0, 5);
                }
            } catch (err) {
                setCityError('İlanlar yüklenemedi.');
                jobs = [];
            }
            setFeaturedJobs(jobs);
            setCityLoading(false);
        }
        fetchFeaturedJobs();
    }, []);

    // Autocomplete for city (only detected city)
    useEffect(() => {
        if (userCity && city && userCity.toLowerCase().includes(city.toLowerCase())) {
            setCitySuggestions([userCity]);
        } else if (userCity && !city) {
            setCitySuggestions([userCity]);
        } else {
            setCitySuggestions([]);
        }
    }, [city, userCity]);

    // Autocomplete for position (max 5, compact)
    useEffect(() => {
        if (query) {
            setPositionSuggestions(positionList.filter(p => p.toLowerCase().includes(query.toLowerCase())).slice(0, 5));
        } else {
            setPositionSuggestions([]);
        }
    }, [query]);

    useEffect(() => {
        // user objesini localStorage'dan çek
        const user = JSON.parse(localStorage.getItem('user') || 'null');

        // user yoksa istek atma!
        if (!user || !user.id) return;

        // Fetch alerts directly from notification service
        fetch(`http://notification_service:8002/api/v1/alerts?user_id=${user.id}`)
            .then(res => res.json())
            .then(setAlerts)
            .catch(() => setAlerts([]));
        apiGet(`/notifications/?user_id=${user.id}`)
            .then(setNotifications)
            .catch(() => setNotifications([]));
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();
        console.log('handleSearch called', { query, location, city, country, district, time: new Date().toISOString() });
        
        // Build filters object
        const filters = {
            query,
            location,
            workPreferences: workPreferences.onsite || workPreferences.remote || workPreferences.hybrid ? workPreferences : null,
            dateFilter: dateFilter !== 'all' ? dateFilter : null,
            country: country || null,
            city: city || null,
            district: district || null,
            user_id: user ? user.id : undefined
        };

        // Only navigate to results with filters (do not make API call here)
        navigate('/results', { state: { filters } });
    };

    const handleApplyFilters = () => {
        handleSearch({ preventDefault: () => {} });
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        window.location.reload();
    };

    const handleJobSuccess = () => {
        // Optionally refresh the page or show success message
        window.location.reload();
    };

    const handleAIClick = () => setShowAIChat(true);
    const handleAIClose = () => setShowAIChat(false);

    const handleAISend = async () => {
        if (!aiInput.trim()) return;
        const userMsg = { sender: 'user', text: aiInput };
        setAIMessages(msgs => [...msgs, userMsg]);
        setAIInput('');
        setAILoading(true);
        try {
            // You may need to adjust the endpoint path depending on your API Gateway
            const res = await apiPost('/ai_agent/chat', { message: userMsg.text, user_id: user?.id });
            setAIMessages(msgs => [...msgs, { sender: 'ai', text: res.response || res.reply || res.answer || JSON.stringify(res) }]);
        } catch (err) {
            setAIMessages(msgs => [...msgs, { sender: 'ai', text: 'Bir hata oluştu.' }]);
        }
        setAILoading(false);
    };

    const handleSaveJobAlert = async (alertData) => {
        try {
            /*
            const payload = { ...alertData, user_id: user.id };
            await apiPost('/notifications/alerts', payload);*/
            const payload = {
                user_id: user.id,
                keywords: alertData.keywords,
                location: alertData.location || "",   // fallback if missing
                salary_min: alertData.salary_min,
                salary_max: alertData.salary_max,
                frequency: alertData.frequency || "daily",
              };
              await apiPost("/notifications/alerts", payload);
            setShowJobAlertModal(false);
            alert('İş alarmı başarıyla kaydedildi!');
        } catch (err) {
            alert('İş alarmı kaydedilemedi.');
        }
    };

    return (
        <div className="container">
            {/* Header */}
            <header className="header">
                <div className="logo">kariyer.net</div>
                {user ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {user && (user.is_admin || user.is_company) && (
                            <button 
                                onClick={() => setShowJobForm(true)}
                                style={{ background: '#28a745', color: '#fff', border: 'none', borderRadius: 16, padding: '6px 14px', fontWeight: 500, cursor: 'pointer' }}
                            >
                                İlan Ekle
                            </button>
                        )}
                        <button 
                            onClick={() => setShowJobAlertModal(true)}
                            style={{ background: '#ff9800', color: '#fff', border: 'none', borderRadius: 16, padding: '6px 14px', fontWeight: 500, cursor: 'pointer' }}
                        >
                            İş Alarmı Oluştur
                        </button>
                        <div style={{ background: '#eee', padding: '6px 14px', borderRadius: 16, fontWeight: 500 }}>{user.first_name}</div>
                        <button onClick={handleLogout} style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer' }}>Çıkış</button>
                    </div>
                ) : (
                    <button className="login-button" onClick={() => navigate('/auth')}>Giriş Yap / Üye Ol</button>
                )}
            </header>

            {/* Hero Section */}
            <section className="hero">
                <h1>Kariyer Fırsatlarını Keşfet</h1>

                <form className="search-bar" onSubmit={handleSearch} autoComplete="off">
                    <div style={{ position: 'relative', width: '100%' }}>
                        <input
                            type="text"
                            placeholder="Pozisyon ara"
                            value={query}
                            ref={positionInputRef}
                            onChange={e => {
                                setQuery(e.target.value);
                                setShowPositionSuggestions(true);
                            }}
                            onFocus={() => setShowPositionSuggestions(true)}
                            onBlur={() => setTimeout(() => setShowPositionSuggestions(false), 100)}
                        />
                        {showPositionSuggestions && positionSuggestions.length > 0 && (
                            <ul className="autocomplete-suggestions compact">
                                {positionSuggestions.map((suggestion, idx) => (
                                    <li
                                        key={idx}
                                        onMouseDown={() => {
                                            setQuery(suggestion);
                                            setShowPositionSuggestions(false);
                                        }}
                                    >
                                        {suggestion}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    <div style={{ position: 'relative', width: '100%' }}>
                        <input
                            type="text"
                            placeholder="Şehir veya ilçe ara"
                            value={city}
                            ref={cityInputRef}
                            onChange={e => {
                                setCity(e.target.value);
                                setShowCitySuggestions(true);
                            }}
                            onFocus={() => setShowCitySuggestions(true)}
                            onBlur={() => setTimeout(() => setShowCitySuggestions(false), 100)}
                        />
                        {showCitySuggestions && citySuggestions.length > 0 && (
                            <ul className="autocomplete-suggestions compact">
                                {citySuggestions.map((suggestion, idx) => (
                                    <li
                                        key={idx}
                                        onMouseDown={() => {
                                            setCity(suggestion);
                                            setShowCitySuggestions(false);
                                        }}
                                    >
                                        {suggestion}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    <button type="submit">İş Bul</button>
                </form>

                <div className="popular-tags">
                    {popularSearches.map(term => (
                        <span key={term} className="tag">{term}</span>
                    ))}
                </div>
            </section>

            {/* Recent Searches */}
            <section className="recent-searches">
                <h2>Son Aramalarım</h2>
                <div className="recent-searches-grid">
                    {recentSearches.length === 0 && <div>Son arama bulunamadı.</div>}
                    {recentSearches.slice(0, 5).map((search, index) => (
                        <Link to="/results" key={index} className="recent-search-card">
                            <div className="search-icon">🔍</div>
                            <div className="search-info">
                                <h3>{search.query || '-'}</h3>
                                <p className="search-location">{search.filters?.location || '-'}</p>
                            </div>
                        </Link>
                    ))}
                </div>
            </section>

            {/* Job Posting Form Modal */}
            {showJobForm && (
                <JobPostingForm
                    onClose={() => setShowJobForm(false)}
                    onSuccess={handleJobSuccess}
                />
            )}

            {/* Featured Jobs */}
            <section className="featured">
                <h2>Öne Çıkan İlanlar</h2>
                {!cityLoading && !cityError && userCity && (
                  <div className="city-info">Konumunuz: {userCity}</div>
                )}
                {cityLoading ? (
                    <div>Yükleniyor...</div>
                ) : cityError ? (
                    <div>{cityError}</div>
                ) : (
                    <div className="job-grid">
                        {featuredJobs.map((job) => (
                            <div className="job-card" key={job.id}>
                                {job.logo && <img className="logo-img" src={job.logo} alt={job.company} />}
                                <h3>{job.title}</h3>
                                <p className="company">{job.company}</p>
                                <p className="location">{job.location}</p>
                            </div>
                        ))}
                    </div>
                )}
            </section>

            {/* AI Agent Floating Button */}
            <button
                className="ai-agent-cta"
                onClick={handleAIClick}
                title="AI Asistan ile konuş"
                style={{
                    position: 'fixed',
                    bottom: 32,
                    right: 32,
                    width: 64,
                    height: 64,
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #007bff 60%, #00c3ff 100%)',
                    color: '#fff',
                    border: 'none',
                    boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
                    fontSize: 32,
                    zIndex: 1000,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                💬
            </button>
            {/* AI Agent Chat Modal */}
            {showAIChat && (
                <div className="ai-agent-modal" style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    width: '100vw',
                    height: '100vh',
                    background: 'rgba(0,0,0,0.35)',
                    zIndex: 2000,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}>
                    <div style={{
                        background: '#fff',
                        borderRadius: 16,
                        width: 360,
                        maxWidth: '90vw',
                        minHeight: 420,
                        boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
                        display: 'flex',
                        flexDirection: 'column',
                        position: 'relative',
                    }}>
                        <button onClick={handleAIClose} style={{ position: 'absolute', top: 12, right: 16, background: 'none', border: 'none', fontSize: 22, color: '#888', cursor: 'pointer' }}>×</button>
                        <div style={{ padding: '24px 24px 12px 24px', fontWeight: 600, fontSize: 20, color: '#007bff' }}>AI Asistan</div>
                        <div style={{ flex: 1, overflowY: 'auto', padding: '0 24px 12px 24px', display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 320 }} ref={el => { if (el) el.scrollTop = el.scrollHeight; }}>
                            {aiMessages.length === 0 && <div style={{ color: '#888', fontSize: 15 }}>Merhaba! Size nasıl yardımcı olabilirim?</div>}
                            {aiMessages.map((msg, i) => (
                                <div key={i} style={{ alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start', background: msg.sender === 'user' ? '#e6f0ff' : '#f1f3f4', color: '#222', borderRadius: 12, padding: '8px 14px', maxWidth: '80%', fontSize: 15, whiteSpace: 'pre-line' }}>{msg.text}</div>
                            ))}
                            {aiLoading && <div style={{ color: '#888', fontSize: 15 }}>Yanıtlanıyor...</div>}
                        </div>
                        <div style={{ display: 'flex', padding: 16, borderTop: '1px solid #eee', gap: 8 }}>
                            <input
                                type="text"
                                value={aiInput}
                                onChange={e => setAIInput(e.target.value)}
                                onKeyDown={e => { if (e.key === 'Enter') handleAISend(); }}
                                placeholder="Sorunuzu yazın..."
                                style={{ flex: 1, borderRadius: 8, border: '1px solid #ccc', padding: '8px 12px', fontSize: 15 }}
                                disabled={aiLoading}
                                autoFocus
                            />
                            <button
                                onClick={handleAISend}
                                disabled={aiLoading || !aiInput.trim()}
                                style={{ background: '#007bff', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 16px', fontWeight: 500, fontSize: 15, cursor: aiLoading || !aiInput.trim() ? 'not-allowed' : 'pointer' }}
                            >Gönder</button>
                        </div>
                    </div>
                </div>
            )}

            {showJobAlertModal && (
                <JobAlertModal
                    onClose={() => setShowJobAlertModal(false)}
                    onSave={handleSaveJobAlert}
                    user={user}
                />
            )}

            {/* Job Alerts Section */}
            <section className="job-alerts">
                <h2>İş Alarmlarım</h2>
                {alerts.length === 0 && <div>Hiç iş alarmınız yok.</div>}
                <ul>
                    {alerts.map(alert => (
                        <li key={alert.id}>
                            <b>{alert.keywords.join(', ')}</b> - {alert.location}
                        </li>
                    ))}
                </ul>
            </section>
            {/* Notifications Section */}
            <section className="notifications">
                <h2>Bildirimler</h2>
                {notifications.length === 0 && <div>Hiç bildiriminiz yok.</div>}
                <ul>
                    {notifications.map(n => (
                        <li key={n.id}>
                            <b>{n.title}</b>: {n.message}
                        </li>
                    ))}
                </ul>
            </section>
        </div>
    );
}

/*


*/