import os
import json
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

articles = [
    {"id":1,"yojana_id":1,"title":"PM-KISAN योजना में कैसे करें आवेदन? पूरी जानकारी हिंदी में","slug":"pm-kisan-apply-kaise-kare","icon":"🌾","date":"27 फरवरी 2024","read_time":"5 मिनट","content":"<h2>PM-KISAN योजना क्या है?</h2><p>प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) के तहत किसानों को प्रतिवर्ष <strong>₹6,000</strong> की सहायता तीन किस्तों में दी जाती है।</p><h2>पात्रता</h2><ul><li>लघु एवं सीमांत किसान (2 हेक्टेयर तक जमीन)</li><li>आधार कार्ड अनिवार्य</li><li>बैंक खाता आधार से linked हो</li></ul><h2>जरूरी दस्तावेज</h2><ul><li>📋 आधार कार्ड</li><li>🏦 बैंक पासबुक</li><li>🌾 खसरा/खतौनी</li><li>📱 मोबाइल नंबर</li></ul><h2>Online आवेदन - Step by Step</h2><ol><li>pmkisan.gov.in खोलें</li><li>Farmers Corner → New Farmer Registration</li><li>आधार नंबर डालें और OTP verify करें</li><li>सभी जानकारी भरें और submit करें</li></ol><h2>Status कैसे चेक करें?</h2><p>pmkisan.gov.in → Farmers Corner → Beneficiary Status पर जाएं।</p><h2>हेल्पलाइन</h2><p>📞 <strong>155261</strong> या <strong>011-24300606</strong></p>"},
    {"id":2,"yojana_id":2,"title":"PM Awas Yojana: घर के लिए ₹2.5 लाख सब्सिडी कैसे पाएं?","slug":"pmay-awas-yojana-apply","icon":"🏠","date":"26 फरवरी 2024","read_time":"6 मिनट","content":"<h2>प्रधानमंत्री आवास योजना क्या है?</h2><p>PMAY के तहत गरीब परिवारों को पक्का घर बनाने के लिए <strong>₹1.2 लाख से ₹2.5 लाख</strong> तक की सब्सिडी मिलती है।</p><h2>योजना के प्रकार</h2><ul><li><strong>PMAY-Gramin:</strong> ग्रामीण क्षेत्र के लिए</li><li><strong>PMAY-Urban:</strong> शहरी क्षेत्र के लिए</li></ul><h2>पात्रता</h2><ul><li>EWS: सालाना आय ₹3 लाख से कम</li><li>LIG: सालाना आय ₹3-6 लाख</li><li>परिवार के नाम पहले से पक्का घर न हो</li></ul><h2>जरूरी दस्तावेज</h2><ul><li>📋 आधार कार्ड</li><li>💰 आय प्रमाण पत्र</li><li>🏦 बैंक पासबुक</li><li>📸 पासपोर्ट साइज फोटो</li></ul><h2>Online आवेदन</h2><ol><li>pmaymis.gov.in पर जाएं</li><li>Citizen Assessment click करें</li><li>आधार verify करें और form भरें</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>1800-11-6163</strong> (Toll Free)</p>"},
    {"id":3,"yojana_id":3,"title":"Ayushman Bharat Card: मुफ्त ₹5 लाख का इलाज कैसे पाएं?","slug":"ayushman-bharat-card-kaise-banaye","icon":"🏥","date":"25 फरवरी 2024","read_time":"5 मिनट","content":"<h2>आयुष्मान भारत योजना क्या है?</h2><p>AB-PMJAY के तहत गरीब परिवारों को प्रति वर्ष <strong>₹5 लाख</strong> तक का मुफ्त इलाज मिलता है।</p><h2>क्या मिलता है?</h2><ul><li>अस्पताल में भर्ती का खर्च</li><li>ऑपरेशन और दवाइयां</li><li>ICU का खर्च</li><li>1,393 बीमारियों का इलाज</li></ul><h2>Card कैसे बनाएं?</h2><ol><li>beneficiary.nha.gov.in खोलें</li><li>मोबाइल नंबर से login करें</li><li>आधार से eKYC करें</li><li>Card download करें</li></ol><p>या नजदीकी <strong>CSC Center</strong> पर जाएं।</p><h2>हेल्पलाइन</h2><p>📞 <strong>14555</strong> (Toll Free, 24x7)</p>"},
    {"id":4,"yojana_id":5,"title":"मुद्रा लोन: बिना गारंटी ₹10 लाख का व्यवसाय ऋण कैसे लें?","slug":"mudra-loan-kaise-le","icon":"💼","date":"24 फरवरी 2024","read_time":"6 मिनट","content":"<h2>मुद्रा योजना क्या है?</h2><p>PMMY के तहत छोटे व्यवसायियों को <strong>बिना किसी गारंटी के</strong> ₹10 लाख तक का लोन मिलता है।</p><h2>तीन प्रकार के लोन</h2><ul><li>🐣 <strong>शिशु:</strong> ₹50,000 तक</li><li>🌱 <strong>किशोर:</strong> ₹50,000 से ₹5 लाख</li><li>🌳 <strong>तरुण:</strong> ₹5 लाख से ₹10 लाख</li></ul><h2>जरूरी दस्तावेज</h2><ul><li>📋 आधार + PAN Card</li><li>🏠 Address proof</li><li>💼 व्यवसाय का विवरण</li><li>🏦 6 महीने की bank statement</li></ul><h2>आवेदन कैसे करें?</h2><ol><li>नजदीकी बैंक में जाएं</li><li>मुद्रा लोन form भरें</li><li>Documents जमा करें</li><li>Approval पर Mudra Card मिलेगा</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>1800-180-1111</strong></p>"},
    {"id":5,"yojana_id":7,"title":"मनरेगा Job Card: 100 दिन गारंटीड रोजगार कैसे पाएं?","slug":"mgnrega-job-card-kaise-banaye","icon":"⛏️","date":"23 फरवरी 2024","read_time":"4 मिनट","content":"<h2>मनरेगा क्या है?</h2><p>MGNREGA के तहत ग्रामीण परिवारों को <strong>100 दिन का गारंटीड रोजगार</strong> मिलता है।</p><h2>पात्रता</h2><ul><li>ग्रामीण क्षेत्र में रहने वाले 18+ वयस्क</li><li>स्थानीय ग्राम पंचायत के निवासी</li></ul><h2>Job Card कैसे बनाएं?</h2><ol><li>ग्राम पंचायत में जाएं</li><li>Registration form भरें</li><li>आधार और फोटो जमा करें</li><li>15 दिन में Job Card मिलेगा</li></ol><h2>मजदूरी दरें 2024</h2><ul><li>UP: ₹237/दिन | राजस्थान: ₹266/दिन</li><li>MP: ₹243/दिन | हरियाणा: ₹374/दिन</li></ul><h2>हेल्पलाइन</h2><p>📞 <strong>1800-111-555</strong></p>"},
    {"id":6,"yojana_id":6,"title":"सुकन्या समृद्धि: बेटी के लिए खोलें खाता, मिलेगा 8.2% ब्याज","slug":"sukanya-samriddhi-account-kaise-khole","icon":"👧","date":"22 फरवरी 2024","read_time":"5 मिनट","content":"<h2>सुकन्या समृद्धि योजना क्या है?</h2><p>बेटियों के लिए विशेष बचत योजना जिसमें <strong>8.2% प्रति वर्ष</strong> ब्याज मिलता है।</p><h2>मुख्य फायदे</h2><ul><li>8.2% सालाना ब्याज (tax free)</li><li>Income Tax में 80C छूट</li><li>सरकारी गारंटी</li></ul><h2>खाता कैसे खोलें?</h2><ol><li>Post Office या SBI/PNB/BOB में जाएं</li><li>SSY form भरें</li><li>बेटी का birth certificate और माता-पिता का आधार दें</li><li>₹250 जमा करके खाता खुलेगा</li></ol><h2>Maturity पर कितना मिलेगा?</h2><p>₹1.5 लाख/वर्ष जमा करने पर 21 साल बाद लगभग <strong>₹70 लाख</strong>!</p>"},
    {"id":7,"yojana_id":4,"title":"उज्ज्वला योजना: मुफ्त गैस कनेक्शन के लिए ऐसे करें आवेदन","slug":"ujjwala-yojana-free-gas-connection","icon":"🔥","date":"21 फरवरी 2024","read_time":"4 मिनट","content":"<h2>उज्ज्वला योजना क्या है?</h2><p>BPL परिवारों की महिलाओं को <strong>मुफ्त LPG गैस कनेक्शन</strong> + ₹1,600 सहायता दी जाती है।</p><h2>पात्रता</h2><ul><li>महिला की उम्र 18+ हो</li><li>BPL परिवार</li><li>घर में पहले से LPG connection न हो</li></ul><h2>आवेदन कैसे करें?</h2><ol><li>नजदीकी LPG distributor के पास जाएं</li><li>KYC form भरें</li><li>BPL card और आधार जमा करें</li><li>Verification के बाद connection मिलेगा</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>1906</strong> | <strong>1800-233-3555</strong></p>"},
    {"id":8,"yojana_id":8,"title":"जन धन खाता: Zero Balance + ₹2 लाख बीमा कैसे पाएं?","slug":"jan-dhan-account-kaise-khole","icon":"🏦","date":"20 फरवरी 2024","read_time":"4 मिनट","content":"<h2>जन धन योजना क्या है?</h2><p>PMJDY के तहत <strong>Zero Balance बैंक खाता</strong> खोला जा सकता है। साथ में ₹2 लाख बीमा और ₹10,000 overdraft भी मिलता है।</p><h2>क्या मिलता है?</h2><ul><li>Zero Balance खाता</li><li>RuPay Debit Card</li><li>₹2 लाख दुर्घटना बीमा</li><li>₹10,000 overdraft</li></ul><h2>खाता कैसे खोलें?</h2><ol><li>नजदीकी बैंक में जाएं</li><li>Jan Dhan form भरें</li><li>आधार और फोटो दें</li><li>उसी दिन खाता खुलेगा!</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>1800-11-0001</strong></p>"},
    {"id":9,"yojana_id":9,"title":"NSP Scholarship 2024: छात्रवृत्ति के लिए Online Apply कैसे करें?","slug":"nsp-scholarship-apply-online","icon":"🎓","date":"19 फरवरी 2024","read_time":"5 मिनट","content":"<h2>NSP Scholarship क्या है?</h2><p>SC, ST, OBC और अल्पसंख्यक छात्रों को <strong>₹1,000 से ₹25,000</strong> तक की छात्रवृत्ति मिलती है।</p><h2>पात्रता</h2><ul><li>SC/ST/OBC/Minority वर्ग के छात्र</li><li>पिछली कक्षा में 50%+ अंक</li><li>Government/recognised school/college में पढ़ रहे हों</li></ul><h2>Online Apply कैसे करें?</h2><ol><li>scholarships.gov.in खोलें</li><li>New Registration → आधार से register करें</li><li>Scholarship चुनें और form भरें</li><li>Documents upload करें और submit करें</li></ol><h2>जरूरी दस्तावेज</h2><ul><li>📋 आधार, Marksheet, Caste Certificate</li><li>💰 Income Certificate, Bank Passbook</li></ul><h2>हेल्पलाइन</h2><p>📞 <strong>0120-6619540</strong></p>"},
]

STYLE = """<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans Devanagari',sans-serif;background:#f5f0e8;color:#1a1a2e}
.tricolor{height:5px;background:linear-gradient(to right,#FF9933 33%,white 33%,white 66%,#138808 66%)}
header{background:linear-gradient(135deg,#000080,#1a1a8e);color:white;position:sticky;top:0;z-index:100;box-shadow:0 2px 20px rgba(0,0,0,.3)}
.header-inner{max-width:1200px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px}
.header-inner h1{font-size:1.4rem;font-weight:800;color:#FFD700}
.header-inner p{font-size:.75rem;color:rgba(255,255,255,.7)}
nav{background:rgba(255,255,255,.08);border-top:1px solid rgba(255,255,255,.1)}
nav ul{list-style:none;max-width:1200px;margin:0 auto;padding:0 20px;display:flex;overflow-x:auto}
nav ul li a{display:block;padding:10px 16px;color:rgba(255,255,255,.85);text-decoration:none;font-size:.85rem;font-weight:600;transition:all .2s;border-bottom:3px solid transparent;white-space:nowrap}
nav ul li a:hover{color:#FF9933;border-bottom-color:#FF9933}
main{max-width:1200px;margin:0 auto;padding:24px 20px}
.search-box{background:linear-gradient(135deg,#000080,#1a1a8e);border-radius:16px;padding:28px;margin-bottom:24px;text-align:center}
.search-box h2{color:white;font-size:1.5rem;margin-bottom:6px}
.search-box p{color:rgba(255,255,255,.7);margin-bottom:18px;font-size:.9rem}
.search-row{display:flex;gap:10px;max-width:560px;margin:0 auto 16px}
.search-row input{flex:1;padding:12px 18px;border:none;border-radius:50px;font-size:.95rem;font-family:inherit;outline:none}
.search-row button{padding:12px 22px;background:#FF9933;color:white;border:none;border-radius:50px;font-weight:700;cursor:pointer;font-family:inherit}
.filters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.filter-btn{padding:6px 16px;border-radius:50px;border:2px solid rgba(255,255,255,.35);background:transparent;color:white;font-size:.8rem;cursor:pointer;font-family:inherit;transition:all .2s;text-decoration:none;display:inline-block}
.filter-btn:hover{background:#FF9933;border-color:#FF9933}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
.stat{background:white;border-radius:12px;padding:18px;text-align:center;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07)}
.stat .num{font-size:1.8rem;font-weight:800;color:#000080}
.stat .lbl{font-size:.75rem;color:#888;margin-top:4px}
.section-title{font-size:1.2rem;font-weight:800;color:#000080;margin-bottom:18px;padding-bottom:10px;border-bottom:3px solid #FF9933}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{background:white;border-radius:14px;padding:22px;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07);transition:all .25s;position:relative;overflow:hidden;text-decoration:none;color:inherit;display:block}
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
.card-btn{display:inline-block;margin-top:12px;padding:7px 18px;background:#000080;color:white;border-radius:50px;font-size:.78rem;font-weight:600}
.blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}
.blog-card{background:white;border-radius:14px;padding:24px;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07);text-decoration:none;color:inherit;display:block;transition:all .25s;position:relative;overflow:hidden}
.blog-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(to right,#FF9933,#138808)}
.blog-card:hover{transform:translateY(-4px);box-shadow:0 12px 35px rgba(0,0,128,.13)}
.blog-icon{font-size:2.5rem;margin-bottom:12px}
.blog-title{font-size:1rem;font-weight:700;color:#000080;line-height:1.5;margin-bottom:10px}
.blog-meta{font-size:.75rem;color:#888;display:flex;gap:12px;margin-bottom:10px}
.blog-excerpt{font-size:.83rem;color:#666;line-height:1.6}
.read-more{display:inline-block;margin-top:14px;padding:7px 18px;background:#FF9933;color:white;border-radius:50px;font-size:.78rem;font-weight:600;text-decoration:none}
.article-container{max-width:780px;margin:0 auto}
.article-hero{background:linear-gradient(135deg,#000080,#1a1a8e);color:white;border-radius:16px;padding:32px;margin-bottom:28px}
.article-hero h1{font-size:1.6rem;font-weight:800;line-height:1.4;margin-bottom:12px}
.article-meta{font-size:.8rem;color:rgba(255,255,255,.7);display:flex;gap:16px;flex-wrap:wrap}
.article-body{background:white;border-radius:16px;padding:32px;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07)}
.article-body h2{font-size:1.15rem;font-weight:700;color:#000080;margin:24px 0 12px;padding-bottom:6px;border-bottom:2px solid #FF9933}
.article-body h2:first-child{margin-top:0}
.article-body p{font-size:.9rem;line-height:1.8;color:#333;margin-bottom:12px}
.article-body ul,.article-body ol{padding-left:20px;margin-bottom:14px}
.article-body li{font-size:.88rem;line-height:1.8;color:#444;margin-bottom:4px}
.article-body strong{color:#000080}
.back-btn{display:inline-flex;align-items:center;gap:6px;color:#000080;text-decoration:none;font-size:.85rem;font-weight:600;margin-bottom:20px;padding:8px 16px;background:white;border-radius:50px;border:1px solid #e0d5c0}
footer{background:#000080;color:rgba(255,255,255,.7);text-align:center;padding:18px;font-size:.8rem;margin-top:40px}
footer strong{color:#FF9933}
@media(max-width:600px){.stats{gap:8px}.stat .num{font-size:1.4rem}.search-row{flex-direction:column}.grid{grid-template-columns:1fr}.blog-grid{grid-template-columns:1fr}}
</style>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">"""

HEADER = """<div class="tricolor"></div>
<header>
<div class="header-inner"><div><h1>🏛️ भारत सरकार योजना पोर्टल</h1><p>Government of India — Scheme Portal</p></div></div>
<nav><ul>
<li><a href="/">🏠 होम</a></li>
<li><a href="/blog">📰 Articles</a></li>
<li><a href="/search?category=कृषि">🌾 कृषि</a></li>
<li><a href="/search?category=स्वास्थ्य">🏥 स्वास्थ्य</a></li>
<li><a href="/search?category=शिक्षा">🎓 शिक्षा</a></li>
<li><a href="/search?category=आवास">🏠 आवास</a></li>
<li><a href="/search?category=महिला">👩 महिला</a></li>
<li><a href="/search?category=रोजगार">💼 रोजगार</a></li>
</ul></nav>
</header>"""

FOOTER = """<footer><p>© 2024 <strong>भारत सरकार योजना पोर्टल</strong> | Demo Project | जानकारी के लिए आधिकारिक वेबसाइट देखें।</p></footer>"""

def render_page(title, body, desc="सरकारी योजना पोर्टल"):
    return f"""<!DOCTYPE html><html lang="hi"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="सरकारी योजना,PM-KISAN,PMAY,आयुष्मान भारत,sarkari yojana">
{STYLE}</head><body>{HEADER}<main>{body}</main>{FOOTER}</body></html>"""

@app.route('/')
def index():
    yojana_json = json.dumps(yojanas, ensure_ascii=False)
    body = f"""
    <div class="search-box">
    <h2>🇮🇳 सरकारी योजनाएं खोजें</h2>
    <p>अपनी योजना आसानी से ढूंढें</p>
    <div class="search-row"><input type="text" id="si" placeholder="योजना खोजें... जैसे किसान, आवास"><button onclick="window.location='/search?q='+document.getElementById('si').value">🔍 खोजें</button></div>
    <div class="filters">
    <a href="/" class="filter-btn">सभी</a>
    <a href="/search?category=कृषि" class="filter-btn">कृषि</a>
    <a href="/search?category=स्वास्थ्य" class="filter-btn">स्वास्थ्य</a>
    <a href="/search?category=आवास" class="filter-btn">आवास</a>
    <a href="/search?category=महिला" class="filter-btn">महिला</a>
    <a href="/search?category=रोजगार" class="filter-btn">रोजगार</a>
    <a href="/search?category=शिक्षा" class="filter-btn">शिक्षा</a>
    </div></div>
    <div class="stats">
    <div class="stat"><div class="num">9+</div><div class="lbl">सरकारी योजनाएं</div></div>
    <div class="stat"><div class="num">9</div><div class="lbl">Articles</div></div>
    <div class="stat"><div class="num">100Cr+</div><div class="lbl">लाभार्थी</div></div>
    </div>
    <div class="section-title">📋 सभी सरकारी योजनाएं</div>
    <div class="grid" id="grid"></div>
    <script>
    const y={yojana_json};
    document.getElementById('grid').innerHTML=y.map(x=>`<a href="/yojana/${{x.id}}" class="card"><div class="card-head"><div class="card-icon">${{x.icon}}</div><div><div class="card-name">${{x.name}}</div><div class="card-cat">${{x.category}}</div></div></div><p class="card-desc">${{x.description}}</p><div class="card-benefit"><div class="benefit-lbl">💰 लाभ</div><div class="benefit-val">${{x.benefit}}</div></div><div class="card-elig">👥 ${{x.eligibility}}</div><span class="card-btn">विवरण देखें →</span></a>`).join('');
    document.getElementById('si').addEventListener('keyup',e=>{{if(e.key==='Enter')window.location='/search?q='+e.target.value}});
    </script>"""
    return render_page("सरकारी योजना पोर्टल 🇮🇳", body)

@app.route('/search')
def search():
    q = request.args.get('q','').lower()
    cat = request.args.get('category','')
    res = yojanas
    if q: res = [y for y in res if q in y['name'].lower() or q in y['description'].lower()]
    if cat and cat != 'सभी': res = [y for y in res if y['category'] == cat]
    cards = ''.join([f'<a href="/yojana/{y["id"]}" class="card"><div class="card-head"><div class="card-icon">{y["icon"]}</div><div><div class="card-name">{y["name"]}</div><div class="card-cat">{y["category"]}</div></div></div><p class="card-desc">{y["description"]}</p><div class="card-benefit"><div class="benefit-lbl">💰 लाभ</div><div class="benefit-val">{y["benefit"]}</div></div><div class="card-elig">👥 {y["eligibility"]}</div><span class="card-btn">विवरण देखें →</span></a>' for y in res])
    title = f'🔍 "{q}" — {len(res)} परिणाम' if q else f'📋 {cat} योजनाएं ({len(res)})'
    body = f'<div class="section-title">{title}</div><div class="grid">{cards or "<p style=padding:40px;text-align:center;color:#888>कोई योजना नहीं मिली</p>"}</div>'
    return render_page(f"{title} | सरकारी योजना पोर्टल", body)

@app.route('/yojana/<int:yid>')
def yojana_detail(yid):
    y = next((x for x in yojanas if x['id'] == yid), None)
    if not y: return "योजना नहीं मिली", 404
    art = next((a for a in articles if a['yojana_id'] == yid), None)
    art_btn = f'<a href="/blog/{art["slug"]}" style="display:block;margin-top:10px;padding:12px;background:#138808;color:white;text-align:center;border-radius:12px;text-decoration:none;font-weight:700">📰 विस्तृत Article पढ़ें →</a>' if art else ''
    body = f"""<a href="/" class="back-btn">← वापस जाएं</a>
    <div style="max-width:700px;margin:0 auto">
    <div style="background:linear-gradient(135deg,#000080,#1a1a8e);color:white;border-radius:16px;padding:32px;margin-bottom:20px">
    <span style="background:#FF9933;padding:4px 14px;border-radius:50px;font-size:.72rem;font-weight:700">{y['category']}</span>
    <h1 style="font-size:1.5rem;font-weight:800;margin:12px 0 8px">{y['icon']} {y['name']}</h1>
    <p style="color:rgba(255,255,255,.8)">{y['description']}</p></div>
    <div style="background:linear-gradient(135deg,#FFF8E1,#E8F5E9);border:2px solid #4CAF50;border-radius:12px;padding:20px;text-align:center;margin-bottom:16px">
    <div style="font-size:.72rem;color:#888;font-weight:600;text-transform:uppercase">मुख्य लाभ</div>
    <div style="font-size:1.5rem;font-weight:800;color:#138808">{y['benefit']}</div></div>
    <div style="background:white;border-radius:12px;padding:20px;border:1px solid #e0d5c0;margin-bottom:16px">
    <p>🏛️ <strong>मंत्रालय:</strong> {y['ministry']}</p><br>
    <p>👥 <strong>पात्रता:</strong> {y['eligibility']}</p><br>
    <p>📞 <strong>हेल्पलाइन:</strong> 1800-11-0001</p></div>
    <a href="{y['link']}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg,#FF9933,#e07a1a);color:white;text-align:center;border-radius:12px;text-decoration:none;font-weight:700;font-size:1rem">🚀 अभी आवेदन करें</a>
    {art_btn}</div>"""
    return render_page(f"{y['name']} | सरकारी योजना पोर्टल", body)

@app.route('/blog')
def blog():
    cards = ''.join([f'<a href="/blog/{a["slug"]}" class="blog-card"><div class="blog-icon">{a["icon"]}</div><div class="blog-title">{a["title"]}</div><div class="blog-meta"><span>📅 {a["date"]}</span><span>⏱️ {a["read_time"]}</span></div><span class="read-more">पूरा पढ़ें →</span></a>' for a in articles])
    body = f'<div class="section-title">📰 सरकारी योजनाओं पर Articles ({len(articles)})</div><div class="blog-grid">{cards}</div>'
    return render_page("Articles | सरकारी योजना पोर्टल", body, "सरकारी योजनाओं पर विस्तृत लेख")

@app.route('/blog/<slug>')
def blog_article(slug):
    a = next((x for x in articles if x['slug'] == slug), None)
    if not a: return "Article नहीं मिला", 404
    body = f"""<a href="/blog" class="back-btn">← सभी Articles</a>
    <div class="article-container">
    <div class="article-hero">
    <div style="font-size:2.5rem;margin-bottom:12px">{a['icon']}</div>
    <h1>{a['title']}</h1>
    <div class="article-meta"><span>📅 {a['date']}</span><span>⏱️ {a['read_time']}</span></div>
    </div>
    <div class="article-body">{a['content']}</div>
    </div>"""
    return render_page(f"{a['title']} | सरकारी योजना पोर्टल", body, a['title'])

@app.route('/api/yojanas')
def api_yojanas():
    return jsonify(yojanas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
