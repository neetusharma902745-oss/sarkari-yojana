import os
from flask import Flask, request, jsonify

app = Flask(__name__)

yojanas = [
    {"id":1,"name":"प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)","category":"कृषि","description":"किसानों को प्रतिवर्ष ₹6,000 की आर्थिक सहायता तीन किस्तों में दी जाती है।","benefit":"₹6,000 प्रति वर्ष","eligibility":"लघु एवं सीमांत किसान","ministry":"कृषि मंत्रालय","link":"https://pmkisan.gov.in","icon":"🌾"},
    {"id":2,"name":"प्रधानमंत्री आवास योजना (PMAY)","category":"आवास","description":"गरीब परिवारों को पक्का घर बनाने के लिए वित्तीय सहायता प्रदान की जाती है।","benefit":"₹1.2 लाख - ₹2.5 लाख तक","eligibility":"BPL परिवार, EWS, LIG श्रेणी","ministry":"आवास मंत्रालय","link":"https://pmaymis.gov.in","icon":"🏠"},
    {"id":3,"name":"आयुष्मान भारत योजना","category":"स्वास्थ्य","description":"गरीब परिवारों को ₹5 लाख तक का मुफ्त स्वास्थ्य बीमा प्रदान किया जाता है।","benefit":"₹5 लाख स्वास्थ्य बीमा","eligibility":"SECC डेटाबेस में शामिल परिवार","ministry":"स्वास्थ्य मंत्रालय","link":"https://pmjay.gov.in","icon":"🏥"},
    {"id":4,"name":"उज्ज्वला योजना (PMUY)","category":"महिला","description":"BPL परिवारों की महिलाओं को मुफ्त LPG गैस कनेक्शन दिया जाता है।","benefit":"मुफ्त LPG + ₹1600","eligibility":"BPL परिवार की महिलाएं","ministry":"पेट्रोलियम मंत्रालय","link":"https://pmuy.gov.in","icon":"🔥"},
    {"id":5,"name":"प्रधानमंत्री मुद्रा योजना (PMMY)","category":"व्यवसाय","description":"छोटे व्यवसायियों को बिना गारंटी के ₹10 लाख तक का ऋण दिया जाता है।","benefit":"₹50,000 से ₹10 लाख ऋण","eligibility":"छोटे व्यापारी, कारीगर","ministry":"वित्त मंत्रालय","link":"https://mudra.org.in","icon":"💼"},
    {"id":6,"name":"सुकन्या समृद्धि योजना","category":"महिला","description":"बेटियों के भविष्य के लिए उच्च ब्याज दर पर बचत खाता खोला जाता है।","benefit":"8.2% ब्याज + टैक्स लाभ","eligibility":"10 वर्ष से कम की बेटियां","ministry":"महिला एवं बाल विकास","link":"https://www.india.gov.in","icon":"👧"},
    {"id":7,"name":"मनरेगा (MGNREGA)","category":"रोजगार","description":"ग्रामीण परिवारों को 100 दिन का गारंटीड रोजगार प्रदान किया जाता है।","benefit":"100 दिन गारंटीड रोजगार","eligibility":"ग्रामीण वयस्क नागरिक","ministry":"ग्रामीण विकास मंत्रालय","link":"https://nrega.nic.in","icon":"⛏️"},
    {"id":8,"name":"प्रधानमंत्री जन धन योजना","category":"बैंकिंग","description":"जीरो बैलेंस पर बैंक खाता, बीमा और ओवरड्राफ्ट सुविधा मिलती है।","benefit":"₹2 लाख बीमा + ओवरड्राफ्ट","eligibility":"बिना बैंक खाते वाले नागरिक","ministry":"वित्त मंत्रालय","link":"https://pmjdy.gov.in","icon":"🏦"},
    {"id":9,"name":"NSP छात्रवृत्ति योजना","category":"शिक्षा","description":"SC/ST/OBC और अल्पसंख्यक छात्रों को पढ़ाई के लिए छात्रवृत्ति दी जाती है।","benefit":"₹1,000 से ₹25,000/वर्ष","eligibility":"SC/ST/OBC छात्र","ministry":"सामाजिक न्याय मंत्रालय","link":"https://scholarships.gov.in","icon":"🎓"},
]

HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>सरकारी योजना पोर्टल 🇮🇳</title>
<meta name="description" content="भारत सरकार की सभी योजनाएं एक जगह — PM-KISAN, PMAY, आयुष्मान भारत और बहुत कुछ।">
<meta name="keywords" content="सरकारी योजना, PM-KISAN, PMAY, आयुष्मान भारत, government scheme, sarkari yojana">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans Devanagari',sans-serif;background:#f5f0e8;color:#1a1a2e}
.tricolor{height:5px;background:linear-gradient(to right,#FF9933 33%,white 33%,white 66%,#138808 66%)}
header{background:linear-gradient(135deg,#000080,#1a1a8e);color:white;position:sticky;top:0;z-index:100;box-shadow:0 2px 20px rgba(0,0,0,.3)}
.header-inner{max-width:1200px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px}
.header-inner h1{font-size:1.4rem;font-weight:800;color:#FFD700}
.header-inner p{font-size:.75rem;color:rgba(255,255,255,.7)}
main{max-width:1200px;margin:0 auto;padding:24px 20px}
.search-box{background:linear-gradient(135deg,#000080,#1a1a8e);border-radius:16px;padding:28px;margin-bottom:24px;text-align:center}
.search-box h2{color:white;font-size:1.5rem;margin-bottom:6px}
.search-box p{color:rgba(255,255,255,.7);margin-bottom:18px;font-size:.9rem}
.search-row{display:flex;gap:10px;max-width:560px;margin:0 auto 16px}
.search-row input{flex:1;padding:12px 18px;border:none;border-radius:50px;font-size:.95rem;font-family:inherit;outline:none}
.search-row button{padding:12px 22px;background:#FF9933;color:white;border:none;border-radius:50px;font-weight:700;cursor:pointer;font-family:inherit}
.search-row button:hover{background:#e07a1a}
.filters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.filter-btn{padding:6px 16px;border-radius:50px;border:2px solid rgba(255,255,255,.35);background:transparent;color:white;font-size:.8rem;cursor:pointer;font-family:inherit;transition:all .2s}
.filter-btn:hover,.filter-btn.active{background:#FF9933;border-color:#FF9933}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
.stat{background:white;border-radius:12px;padding:18px;text-align:center;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07)}
.stat .num{font-size:1.8rem;font-weight:800;color:#000080}
.stat .lbl{font-size:.75rem;color:#888;margin-top:4px}
.section-title{font-size:1.2rem;font-weight:800;color:#000080;margin-bottom:18px;padding-bottom:10px;border-bottom:3px solid #FF9933}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{background:white;border-radius:14px;padding:22px;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07);transition:all .25s;cursor:pointer;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(to right,#FF9933,#138808)}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 35px rgba(0,0,128,.13)}
.card-head{display:flex;gap:12px;align-items:flex-start;margin-bottom:12px}
.card-icon{font-size:2rem;width:48px;height:48px;border-radius:10px;background:linear-gradient(135deg,#FFF3E0,#E8F5E9);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.card-name{font-size:.92rem;font-weight:700;color:#000080;line-height:1.4}
.card-cat{font-size:.7rem;color:#138808;font-weight:600;margin-top:3px}
.card-desc{font-size:.82rem;color:#666;line-height:1.6;margin-bottom:12px}
.card-benefit{background:linear-gradient(135deg,#FFF8E1,#E8F5E9);border-radius:8px;padding:10px 12px;margin-bottom:10px}
.benefit-lbl{font-size:.65rem;color:#888;font-weight:600;text-transform:uppercase}
.benefit-val{font-size:.88rem;font-weight:700;color:#138808}
.card-elig{font-size:.76rem;color:#888}
.card-btn{display:inline-block;margin-top:12px;padding:7px 18px;background:#000080;color:white;border-radius:50px;font-size:.78rem;font-weight:600;border:none;cursor:pointer;font-family:inherit}
.card-btn:hover{background:#0047AB}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:999;align-items:center;justify-content:center;padding:20px}
.modal-overlay.show{display:flex}
.modal{background:white;border-radius:20px;max-width:580px;width:100%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.modal-hero{background:linear-gradient(135deg,#000080,#1a1a8e);color:white;padding:28px;border-radius:20px 20px 0 0}
.modal-hero .cat-tag{background:#FF9933;color:white;padding:4px 14px;border-radius:50px;font-size:.72rem;font-weight:700;display:inline-block;margin-bottom:10px}
.modal-hero h2{font-size:1.4rem;font-weight:800;margin-bottom:8px}
.modal-hero p{color:rgba(255,255,255,.8);font-size:.88rem;line-height:1.6}
.modal-body{padding:24px}
.info-row{display:flex;gap:10px;margin-bottom:14px;align-items:flex-start}
.info-icon{font-size:1.2rem;flex-shrink:0}
.info-lbl{font-size:.68rem;color:#888;font-weight:600;text-transform:uppercase}
.info-val{font-size:.88rem;color:#1a1a2e;font-weight:500;margin-top:2px}
.big-benefit{background:linear-gradient(135deg,#FFF8E1,#E8F5E9);border:2px solid #4CAF50;border-radius:12px;padding:18px;text-align:center;margin-bottom:18px}
.big-benefit .val{font-size:1.4rem;font-weight:800;color:#138808}
.big-benefit .lbl{font-size:.72rem;color:#888;text-transform:uppercase;font-weight:600}
.apply-big{display:block;width:100%;padding:13px;background:linear-gradient(135deg,#FF9933,#e07a1a);color:white;text-align:center;border-radius:12px;text-decoration:none;font-weight:700;font-size:.95rem;border:none;cursor:pointer;font-family:inherit;margin-bottom:10px}
.close-btn{display:block;width:100%;padding:11px;background:#f0f0f0;color:#333;border-radius:12px;border:none;cursor:pointer;font-family:inherit;font-size:.88rem;font-weight:600}
.no-results{text-align:center;padding:50px;color:#888;grid-column:1/-1}
.no-results .icon{font-size:3.5rem;margin-bottom:14px}
.no-results h3{color:#000080;font-size:1.1rem;margin-bottom:8px}
footer{background:#000080;color:rgba(255,255,255,.7);text-align:center;padding:18px;font-size:.8rem;margin-top:40px}
footer strong{color:#FF9933}
@media(max-width:600px){.stats{gap:8px}.stat .num{font-size:1.4rem}.search-row{flex-direction:column}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="tricolor"></div>
<header>
<div class="header-inner">
<div>
<h1>🏛️ भारत सरकार योजना पोर्टल</h1>
<p>Government of India — Scheme Portal</p>
</div>
</div>
</header>
<main>
<div class="search-box">
<h2>🇮🇳 सरकारी योजनाएं खोजें</h2>
<p>अपनी योजना आसानी से ढूंढें</p>
<div class="search-row">
<input type="text" id="searchInput" placeholder="योजना खोजें... जैसे किसान, आवास, स्वास्थ्य">
<button onclick="doSearch()">🔍 खोजें</button>
</div>
<div class="filters" id="filters"></div>
</div>
<div class="stats">
<div class="stat"><div class="num">9+</div><div class="lbl">सरकारी योजनाएं</div></div>
<div class="stat"><div class="num">6</div><div class="lbl">श्रेणियां</div></div>
<div class="stat"><div class="num">100Cr+</div><div class="lbl">लाभार्थी</div></div>
</div>
<div class="section-title" id="sectionTitle">📋 सभी सरकारी योजनाएं</div>
<div class="grid" id="grid"></div>
</main>
<footer><p>© 2024 <strong>भारत सरकार योजना पोर्टल</strong> | Demo Project</p></footer>
<div class="modal-overlay" id="modal" onclick="closeModal(event)">
<div class="modal" id="modalBox"></div>
</div>
<script>
const yojanas = YOJANA_DATA;
let activeFilter='सभी';
function getCategories(){return['सभी',...new Set(yojanas.map(y=>y.category))]}
function renderFilters(){document.getElementById('filters').innerHTML=getCategories().map(cat=>`<button class="filter-btn ${cat===activeFilter?'active':''}" onclick="setFilter('${cat}')">${cat}</button>`).join('')}
function setFilter(cat){activeFilter=cat;renderFilters();renderGrid()}
function doSearch(){activeFilter='सभी';renderFilters();renderGrid()}
function renderGrid(){
const query=document.getElementById('searchInput').value.toLowerCase();
let filtered=yojanas;
if(activeFilter!=='सभी')filtered=filtered.filter(y=>y.category===activeFilter);
if(query)filtered=filtered.filter(y=>y.name.toLowerCase().includes(query)||y.description.toLowerCase().includes(query));
const titleEl=document.getElementById('sectionTitle');
if(query)titleEl.textContent=`🔍 "${query}" के लिए ${filtered.length} परिणाम`;
else if(activeFilter!=='सभी')titleEl.textContent=`📋 ${activeFilter} योजनाएं (${filtered.length})`;
else titleEl.textContent='📋 सभी सरकारी योजनाएं';
const grid=document.getElementById('grid');
if(!filtered.length){grid.innerHTML=`<div class="no-results"><div class="icon">🔍</div><h3>कोई योजना नहीं मिली</h3><p>अलग शब्दों से खोजें।</p></div>`;return}
grid.innerHTML=filtered.map(y=>`<div class="card" onclick="openModal(${y.id})"><div class="card-head"><div class="card-icon">${y.icon}</div><div><div class="card-name">${y.name}</div><div class="card-cat">${y.category} • ${y.ministry}</div></div></div><p class="card-desc">${y.description}</p><div class="card-benefit"><div class="benefit-lbl">💰 लाभ</div><div class="benefit-val">${y.benefit}</div></div><div class="card-elig">👥 <strong>पात्रता:</strong> ${y.eligibility}</div><button class="card-btn">विवरण देखें →</button></div>`).join('')}
function openModal(id){
const y=yojanas.find(x=>x.id===id);
document.getElementById('modalBox').innerHTML=`<div class="modal-hero"><span class="cat-tag">${y.category}</span><h2>${y.icon} ${y.name}</h2><p>${y.description}</p></div><div class="modal-body"><div class="big-benefit"><div class="lbl">मुख्य लाभ</div><div class="val">${y.benefit}</div></div><div class="info-row"><span class="info-icon">🏛️</span><div><div class="info-lbl">मंत्रालय</div><div class="info-val">${y.ministry}</div></div></div><div class="info-row"><span class="info-icon">👥</span><div><div class="info-lbl">पात्रता</div><div class="info-val">${y.eligibility}</div></div></div><div class="info-row"><span class="info-icon">📞</span><div><div class="info-lbl">हेल्पलाइन</div><div class="info-val">1800-11-0001 (Toll Free)</div></div></div><br><a href="${y.link}" target="_blank" class="apply-big">🚀 अभी आवेदन करें</a><button class="close-btn" onclick="document.getElementById('modal').classList.remove('show')">✕ बंद करें</button></div>`;
document.getElementById('modal').classList.add('show')}
function closeModal(e){if(e.target===document.getElementById('modal'))document.getElementById('modal').classList.remove('show')}
document.getElementById('searchInput').addEventListener('keyup',e=>{if(e.key==='Enter')doSearch()});
renderFilters();renderGrid();
</script>
</body>
</html>"""

@app.route('/')
def index():
    import json
    html = HTML.replace('YOJANA_DATA', json.dumps(yojanas, ensure_ascii=False))
    return html

@app.route('/api/yojanas')
def api_yojanas():
    return jsonify(yojanas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
