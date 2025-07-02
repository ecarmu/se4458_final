import React, { useState } from 'react';

const countryList = ["Türkiye"];
const cityList = [
  "İstanbul", "Ankara", "İzmir", "Bursa", "Adana", "Antalya", "Konya", "Gaziantep", "Kayseri", "Mersin"
];
const districtMap = {
  "İstanbul": ["Kadıköy", "Beşiktaş", "Şişli", "Üsküdar", "Bakırköy"],
  "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Sincan"],
  "İzmir": ["Balçova", "Bornova", "Karşıyaka", "Konak", "Buca"],
  "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "Mudanya", "Gemlik"]
};

export default function JobAlertModal({ onClose, onSave, user }) {
  const [keywords, setKeywords] = useState("");
  const [country, setCountry] = useState("Türkiye");
  const [city, setCity] = useState("");
  const [district, setDistrict] = useState("");

  const handleSave = () => {
    if (!keywords || !city) return;
    onSave({
      user_id: user.id,
      keywords: [keywords],
      location: city + (district ? ", " + district : "")
    });
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.25)', zIndex: 3000, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ background: '#fff', borderRadius: 12, width: 380, maxWidth: '95vw', padding: 24, boxShadow: '0 4px 24px rgba(0,0,0,0.18)', position: 'relative' }}>
        <button onClick={onClose} style={{ position: 'absolute', top: 12, right: 16, background: 'none', border: 'none', fontSize: 22, color: '#888', cursor: 'pointer' }}>×</button>
        <h2 style={{ fontSize: 20, marginBottom: 18 }}>İş Alarmı Oluştur</h2>
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontWeight: 500, marginBottom: 6 }}>Anahtar Kelimeler</div>
          <input
            type="text"
            value={keywords}
            onChange={e => setKeywords(e.target.value)}
            placeholder="Örn: Web Tasarım Uzmanı"
            style={{ width: '100%', padding: 8, borderRadius: 6, border: '1px solid #ccc' }}
          />
        </div>
        <div style={{ marginBottom: 18 }}>
          <div style={{ fontWeight: 500, marginBottom: 6 }}>Ülke / Şehir / İlçe</div>
          <select value={country} onChange={e => setCountry(e.target.value)} style={{ width: '100%', marginBottom: 8, padding: 8, borderRadius: 6, border: '1px solid #ccc' }}>
            {countryList.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={city} onChange={e => { setCity(e.target.value); setDistrict(""); }} style={{ width: '100%', marginBottom: 8, padding: 8, borderRadius: 6, border: '1px solid #ccc' }}>
            <option value="">Şehir seçin</option>
            {cityList.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select value={district} onChange={e => setDistrict(e.target.value)} style={{ width: '100%', padding: 8, borderRadius: 6, border: '1px solid #ccc' }} disabled={!city}>
            <option value="">İlçe seçin</option>
            {(districtMap[city] || []).map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
          <button onClick={onClose} style={{ background: '#eee', color: '#333', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 500 }}>İptal</button>
          <button onClick={handleSave} style={{ background: '#007bff', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 500 }} disabled={!keywords || !city}>Kaydet</button>
        </div>
      </div>
    </div>
  );
} 