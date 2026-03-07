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
    {"id":1,"yojana_id":1,"title":"PM-KISAN योजना में कैसे करें आवेदन? पूरी जानकारी हिंदी में","slug":"pm-kisan-apply-kaise-kare","icon":"🌾","date":"27 फरवरी 2024","read_time":"8 मिनट","content":"""
<h2>PM-KISAN योजना क्या है?</h2>
<p>प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) भारत सरकार की एक महत्वपूर्ण योजना है जिसे 1 दिसंबर 2018 को शुरू किया गया था। इस योजना के तहत देश के छोटे और सीमांत किसानों को प्रतिवर्ष <strong>₹6,000</strong> की आर्थिक सहायता दी जाती है। यह राशि तीन समान किस्तों में — ₹2,000-₹2,000-₹2,000 — सीधे किसान के बैंक खाते में भेजी जाती है। इस योजना का मुख्य उद्देश्य किसानों की आय बढ़ाना और उन्हें खेती के लिए आर्थिक सहायता प्रदान करना है।</p>

<h2>PM-KISAN की किस्तें कब आती हैं?</h2>
<p>इस योजना के तहत साल में तीन किस्तें मिलती हैं। पहली किस्त अप्रैल से जुलाई के बीच, दूसरी किस्त अगस्त से नवंबर के बीच, और तीसरी किस्त दिसंबर से मार्च के बीच आती है। हर किस्त में ₹2,000 सीधे आपके बैंक खाते में DBT (Direct Benefit Transfer) के माध्यम से भेजे जाते हैं।</p>

<h2>कौन कर सकता है आवेदन?</h2>
<ul>
<li>लघु एवं सीमांत किसान जिनके पास 2 हेक्टेयर तक कृषि योग्य जमीन हो</li>
<li>किसान का नाम भूमि रिकॉर्ड (खसरा/खतौनी) में होना चाहिए</li>
<li>आधार कार्ड होना अनिवार्य है</li>
<li>बैंक खाता आधार से linked होना चाहिए</li>
<li>जमीन किसान के नाम पर registered होनी चाहिए</li>
</ul>

<h2>कौन नहीं कर सकता आवेदन?</h2>
<ul>
<li>सरकारी कर्मचारी (चतुर्थ श्रेणी को छोड़कर)</li>
<li>Income Tax भरने वाले किसान</li>
<li>डॉक्टर, इंजीनियर, वकील जैसे professionals</li>
<li>₹10,000 से अधिक मासिक पेंशन पाने वाले</li>
<li>Constitutional posts पर बैठे लोग</li>
<li>पूर्व और वर्तमान मंत्री, सांसद, विधायक</li>
</ul>

<h2>आवेदन के लिए जरूरी दस्तावेज</h2>
<ul>
<li>📋 आधार कार्ड (अनिवार्य)</li>
<li>🏦 बैंक पासबुक (खाता नंबर और IFSC code)</li>
<li>🌾 खसरा/खतौनी (जमीन के कागज)</li>
<li>📱 आधार से linked मोबाइल नंबर</li>
<li>📸 पासपोर्ट साइज फोटो</li>
</ul>

<h2>Online आवेदन कैसे करें? Step by Step</h2>
<ol>
<li><strong>Step 1:</strong> pmkisan.gov.in वेबसाइट खोलें</li>
<li><strong>Step 2:</strong> होम पेज पर "Farmers Corner" section पर जाएं</li>
<li><strong>Step 3:</strong> "New Farmer Registration" पर click करें</li>
<li><strong>Step 4:</strong> Rural या Urban Farmer select करें</li>
<li><strong>Step 5:</strong> आधार नंबर और मोबाइल नंबर डालें</li>
<li><strong>Step 6:</strong> OTP से verify करें</li>
<li><strong>Step 7:</strong> राज्य, जिला, तहसील, गाँव की जानकारी भरें</li>
<li><strong>Step 8:</strong> बैंक खाते की जानकारी भरें</li>
<li><strong>Step 9:</strong> जमीन की जानकारी (खसरा नंबर) भरें</li>
<li><strong>Step 10:</strong> Form submit करें और Registration number नोट करें</li>
</ol>

<h2>Offline आवेदन कैसे करें?</h2>
<p>अगर online आवेदन नहीं कर सकते तो अपने नजदीकी <strong>CSC (Common Service Center)</strong>, <strong>कृषि विभाग कार्यालय</strong>, या <strong>ग्राम पंचायत</strong> में जाएं। वहाँ से मुफ्त में आवेदन हो जाएगा। बस अपने सभी documents साथ लेकर जाएं।</p>

<h2>Status कैसे चेक करें?</h2>
<ol>
<li>pmkisan.gov.in खोलें</li>
<li>"Farmers Corner" → "Beneficiary Status" click करें</li>
<li>आधार नंबर, बैंक खाता नंबर, या मोबाइल नंबर डालें</li>
<li>"Get Data" click करें — सारी किस्तों की जानकारी दिखेगी</li>
</ol>

<h2>eKYC कैसे करें? (जरूरी!)</h2>
<p>PM-KISAN का लाभ लेने के लिए eKYC करना अनिवार्य है। pmkisan.gov.in पर जाकर "eKYC" option पर click करें और आधार OTP से verify करें। बिना eKYC के किस्त नहीं आएगी।</p>

<h2>हेल्पलाइन नंबर</h2>
<p>📞 <strong>155261</strong> या <strong>011-24300606</strong> पर call करें।<br>
📧 Email: pmkisan-ict@gov.in</p>
"""},
    {"id":2,"yojana_id":2,"title":"PM Awas Yojana: घर के लिए ₹2.5 लाख सब्सिडी कैसे पाएं?","slug":"pmay-awas-yojana-apply","icon":"🏠","date":"26 फरवरी 2024","read_time":"8 मिनट","content":"""
<h2>प्रधानमंत्री आवास योजना क्या है?</h2>
<p>प्रधानमंत्री आवास योजना (PMAY) भारत सरकार की "Housing for All" मिशन के तहत शुरू की गई योजना है। इसके तहत गरीब और मध्यम वर्ग के परिवारों को अपना पक्का घर बनाने के लिए <strong>₹1.2 लाख से ₹2.5 लाख</strong> तक की आर्थिक सहायता दी जाती है। यह योजना 2015 में शुरू हुई थी और इसका लक्ष्य देश के हर परिवार को पक्का घर देना है।</p>

<h2>योजना के दो प्रकार</h2>
<ul>
<li><strong>PMAY-Gramin (PMAY-G):</strong> ग्रामीण क्षेत्र के लोगों के लिए। इसमें ₹1.2 लाख (मैदानी) और ₹1.3 लाख (पहाड़ी/नक्सल) की सहायता मिलती है।</li>
<li><strong>PMAY-Urban (PMAY-U):</strong> शहरी क्षेत्र के लोगों के लिए। इसमें Credit Linked Subsidy Scheme (CLSS) के तहत home loan पर ब्याज में सब्सिडी मिलती है।</li>
</ul>

<h2>पात्रता की शर्तें</h2>
<ul>
<li>EWS (आर्थिक रूप से कमजोर): सालाना आय ₹3 लाख से कम</li>
<li>LIG (निम्न आय वर्ग): सालाना आय ₹3 लाख से ₹6 लाख</li>
<li>MIG-I (मध्यम आय वर्ग-I): सालाना आय ₹6 लाख से ₹12 लाख</li>
<li>MIG-II (मध्यम आय वर्ग-II): सालाना आय ₹12 लाख से ₹18 लाख</li>
<li>परिवार के किसी भी सदस्य के नाम देश में कहीं भी पक्का घर नहीं होना चाहिए</li>
<li>महिला के नाम पर या joint ownership में घर होना अनिवार्य (EWS/LIG के लिए)</li>
</ul>

<h2>जरूरी दस्तावेज</h2>
<ul>
<li>📋 आधार कार्ड (सभी परिवार सदस्यों का)</li>
<li>💰 आय प्रमाण पत्र</li>
<li>🏦 बैंक खाते की जानकारी</li>
<li>📸 पासपोर्ट साइज फोटो</li>
<li>🏠 जमीन के दस्तावेज (ग्रामीण के लिए)</li>
<li>📄 जाति प्रमाण पत्र (SC/ST के लिए)</li>
</ul>

<h2>Online आवेदन — Step by Step</h2>
<ol>
<li><strong>Step 1:</strong> pmaymis.gov.in पर जाएं</li>
<li><strong>Step 2:</strong> "Citizen Assessment" पर click करें</li>
<li><strong>Step 3:</strong> अपनी category चुनें (Slum Dweller/Benefits under 3 components)</li>
<li><strong>Step 4:</strong> आधार नंबर और नाम डालकर verify करें</li>
<li><strong>Step 5:</strong> Application form में सारी जानकारी भरें</li>
<li><strong>Step 6:</strong> Submit करें और Application ID नोट करें</li>
</ol>

<h2>Subsidy कितनी मिलती है?</h2>
<ul>
<li>EWS/LIG: 6.5% ब्याज सब्सिडी (अधिकतम ₹2.67 लाख)</li>
<li>MIG-I: 4% ब्याज सब्सिडी (अधिकतम ₹2.35 लाख)</li>
<li>MIG-II: 3% ब्याज सब्सिडी (अधिकतम ₹2.30 लाख)</li>
</ul>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>1800-11-6163</strong> (Toll Free)<br>📞 <strong>1800-11-3377</strong></p>
"""},
    {"id":3,"yojana_id":3,"title":"Ayushman Bharat Card: मुफ्त ₹5 लाख का इलाज कैसे पाएं?","slug":"ayushman-bharat-card-kaise-banaye","icon":"🏥","date":"25 फरवरी 2024","read_time":"7 मिनट","content":"""
<h2>आयुष्मान भारत योजना क्या है?</h2>
<p>आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना (AB-PMJAY) दुनिया की सबसे बड़ी सरकारी स्वास्थ्य बीमा योजना है। इसे सितंबर 2018 में शुरू किया गया था। इस योजना के तहत देश के गरीब और वंचित परिवारों को प्रति वर्ष <strong>₹5 लाख</strong> तक का मुफ्त स्वास्थ्य बीमा दिया जाता है। इस योजना से देश के लगभग 50 करोड़ लोगों को लाभ मिलता है।</p>

<h2>क्या-क्या मिलता है मुफ्त?</h2>
<ul>
<li>अस्पताल में भर्ती होने का पूरा खर्च</li>
<li>ऑपरेशन का खर्च</li>
<li>ICU का खर्च</li>
<li>दवाइयां और medical tests</li>
<li>Chemotherapy और dialysis</li>
<li>1,393 से अधिक बीमारियों का इलाज</li>
<li>Cashless और paperless treatment</li>
<li>Pre और post hospitalization खर्च (3 दिन पहले और 15 दिन बाद तक)</li>
</ul>

<h2>पात्रता कैसे जांचें?</h2>
<ol>
<li>pmjay.gov.in पर जाएं</li>
<li>"Am I Eligible" button click करें</li>
<li>मोबाइल नंबर डालें और OTP verify करें</li>
<li>राज्य select करें और नाम/राशन कार्ड नंबर से खोजें</li>
</ol>

<h2>Ayushman Card कैसे बनाएं?</h2>
<ol>
<li><strong>Online:</strong> beneficiary.nha.gov.in पर जाएं → मोबाइल से login करें → आधार eKYC करें → Card download करें</li>
<li><strong>CSC Center:</strong> नजदीकी Common Service Center पर जाएं</li>
<li><strong>अस्पताल में:</strong> empanelled अस्पताल के Ayushman Mitra से बनवाएं</li>
</ol>

<h2>कहाँ मिलेगा मुफ्त इलाज?</h2>
<p>देश के 25,000 से अधिक सरकारी और private empanelled अस्पतालों में। अपने नजदीकी अस्पताल की list देखने के लिए pmjay.gov.in पर "Find Hospital" click करें।</p>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>14555</strong> (Toll Free, 24x7)<br>📞 <strong>1800-111-565</strong></p>
"""},
    {"id":4,"yojana_id":5,"title":"मुद्रा लोन: बिना गारंटी ₹10 लाख का व्यवसाय ऋण कैसे लें?","slug":"mudra-loan-kaise-le","icon":"💼","date":"24 फरवरी 2024","read_time":"7 मिनट","content":"""
<h2>मुद्रा योजना क्या है?</h2>
<p>प्रधानमंत्री मुद्रा योजना (PMMY) अप्रैल 2015 में शुरू की गई थी। इस योजना के तहत छोटे और लघु उद्यमियों को <strong>बिना किसी गारंटी के</strong> ₹10 लाख तक का loan दिया जाता है। "MUDRA" का पूरा नाम है — Micro Units Development and Refinance Agency। इस योजना का उद्देश्य देश के छोटे व्यवसायियों को financial support देना है।</p>

<h2>तीन प्रकार के लोन</h2>
<ul>
<li>🐣 <strong>शिशु:</strong> ₹50,000 तक — नया व्यवसाय शुरू करने के लिए</li>
<li>🌱 <strong>किशोर:</strong> ₹50,000 से ₹5 लाख — बढ़ते व्यवसाय के लिए</li>
<li>🌳 <strong>तरुण:</strong> ₹5 लाख से ₹10 लाख — स्थापित व्यवसाय बढ़ाने के लिए</li>
</ul>

<h2>कौन ले सकता है लोन?</h2>
<ul>
<li>दुकानदार और व्यापारी</li>
<li>कारीगर और बुनकर</li>
<li>Street vendor और hawker</li>
<li>छोटे manufacturers</li>
<li>Fruits और vegetable vendor</li>
<li>Hair salon, beauty parlour owner</li>
<li>Repair shop owner</li>
<li>Food processing unit</li>
</ul>

<h2>जरूरी दस्तावेज</h2>
<ul>
<li>📋 आधार कार्ड और PAN Card</li>
<li>🏠 Address proof</li>
<li>📸 2 पासपोर्ट साइज फोटो</li>
<li>💼 व्यवसाय का विवरण और plan</li>
<li>🏦 6 महीने की bank statement</li>
<li>📄 Caste certificate (यदि applicable हो)</li>
</ul>

<h2>आवेदन कैसे करें?</h2>
<ol>
<li><strong>Step 1:</strong> नजदीकी बैंक/NBFC/MFI में जाएं</li>
<li><strong>Step 2:</strong> Mudra loan application form भरें</li>
<li><strong>Step 3:</strong> Business plan और documents जमा करें</li>
<li><strong>Step 4:</strong> Bank verification करेगा (7-10 दिन)</li>
<li><strong>Step 5:</strong> Approve होने पर Mudra Card और loan amount मिलेगा</li>
</ol>

<h2>Online आवेदन</h2>
<p>mudra.org.in या udyamimitra.in पर भी online apply कर सकते हैं।</p>

<h2>ब्याज दर</h2>
<p>Bank के अनुसार अलग-अलग, आमतौर पर <strong>8.5% से 12%</strong> प्रति वर्ष।</p>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>1800-180-1111</strong> (Toll Free)</p>
"""},
    {"id":5,"yojana_id":7,"title":"मनरेगा Job Card: 100 दिन गारंटीड रोजगार कैसे पाएं?","slug":"mgnrega-job-card-kaise-banaye","icon":"⛏️","date":"23 फरवरी 2024","read_time":"6 मिनट","content":"""
<h2>मनरेगा क्या है?</h2>
<p>महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी अधिनियम (MGNREGA) 2005 में पास हुआ और 2006 में लागू हुआ। यह कानून ग्रामीण परिवारों के वयस्क सदस्यों को <strong>एक वित्त वर्ष में 100 दिन का गारंटीड रोजगार</strong> प्रदान करता है। इस योजना का मुख्य उद्देश्य ग्रामीण गरीबी कम करना और लोगों को उनके गाँव में ही रोजगार देना है।</p>

<h2>मुख्य विशेषताएं</h2>
<ul>
<li>100 दिन का कानूनी रूप से गारंटीड रोजगार</li>
<li>काम मांगने के 15 दिन के अंदर काम देना जरूरी</li>
<li>काम नहीं मिला तो Unemployment Allowance मिलेगा</li>
<li>घर से 5 किमी के अंदर काम दिया जाएगा</li>
<li>मजदूरी सीधे बैंक खाते में आएगी</li>
<li>महिलाओं को 33% reservation</li>
</ul>

<h2>Job Card कैसे बनाएं?</h2>
<ol>
<li>अपनी ग्राम पंचायत में जाएं</li>
<li>MGNREGA registration form भरें</li>
<li>आधार कार्ड और फोटो जमा करें</li>
<li>बैंक खाते की जानकारी दें</li>
<li>15 दिन के अंदर Job Card मिल जाएगा</li>
</ol>

<h2>काम की मांग कैसे करें?</h2>
<ol>
<li>ग्राम पंचायत में लिखित application दें</li>
<li>Application की receipt लें (date-stamped)</li>
<li>15 दिन के अंदर काम मिलना जरूरी है</li>
<li>काम न मिले तो Unemployment Allowance का दावा करें</li>
</ol>

<h2>मजदूरी दरें 2024</h2>
<ul>
<li>उत्तर प्रदेश: ₹237/दिन</li>
<li>राजस्थान: ₹266/दिन</li>
<li>मध्य प्रदेश: ₹243/दिन</li>
<li>हरियाणा: ₹374/दिन</li>
<li>बिहार: ₹245/दिन</li>
<li>महाराष्ट्र: ₹323/दिन</li>
</ul>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>1800-111-555</strong> (Toll Free)</p>
"""},
    {"id":6,"yojana_id":6,"title":"सुकन्या समृद्धि: बेटी के लिए खोलें खाता, मिलेगा 8.2% ब्याज","slug":"sukanya-samriddhi-account-kaise-khole","icon":"👧","date":"22 फरवरी 2024","read_time":"6 मिनट","content":"""
<h2>सुकन्या समृद्धि योजना क्या है?</h2>
<p>सुकन्या समृद्धि योजना (SSY) "बेटी बचाओ बेटी पढ़ाओ" अभियान के तहत 2015 में शुरू हुई। यह बेटियों के उज्जवल भविष्य के लिए एक विशेष बचत योजना है जिसमें वर्तमान में <strong>8.2% प्रति वर्ष</strong> की ब्याज दर मिलती है। यह किसी भी सरकारी बचत योजना में सबसे अधिक ब्याज दर है।</p>

<h2>मुख्य फायदे</h2>
<ul>
<li>💰 8.2% सालाना ब्याज (quarterly compounded)</li>
<li>🎯 बेटी की पढ़ाई और शादी के लिए बड़ी रकम</li>
<li>📊 Income Tax में Section 80C के तहत ₹1.5 लाख तक छूट</li>
<li>🔒 ब्याज और maturity amount — दोनों tax free</li>
<li>🏛️ सरकारी गारंटी — पूरी तरह सुरक्षित</li>
</ul>

<h2>खाता कैसे खोलें?</h2>
<ol>
<li>नजदीकी Post Office या authorized बैंक (SBI, PNB, BOB, etc.) जाएं</li>
<li>SSY account opening form भरें</li>
<li>बेटी का birth certificate जमा करें</li>
<li>माता-पिता का आधार और PAN card दें</li>
<li>न्यूनतम ₹250 जमा करें — खाता खुल जाएगा!</li>
</ol>

<h2>कितना जमा करना होगा?</h2>
<ul>
<li>न्यूनतम: ₹250 प्रति वर्ष</li>
<li>अधिकतम: ₹1.5 लाख प्रति वर्ष</li>
<li>15 साल तक जमा करना होगा</li>
<li>21 साल में account mature होगा</li>
</ul>

<h2>Maturity पर कितना मिलेगा?</h2>
<p>अगर हर साल ₹1.5 लाख जमा करें तो 21 साल बाद लगभग <strong>₹70 लाख से ₹74 लाख</strong> मिलेंगे!</p>

<h2>पैसे कब निकाल सकते हैं?</h2>
<ul>
<li>बेटी 18 साल की होने पर 50% निकाल सकते हैं (पढ़ाई के लिए)</li>
<li>21 साल में पूरा पैसा निकाल सकते हैं</li>
<li>शादी होने पर (18 साल बाद) भी निकाल सकते हैं</li>
</ul>
"""},
    {"id":7,"yojana_id":4,"title":"उज्ज्वला योजना: मुफ्त गैस कनेक्शन के लिए ऐसे करें आवेदन","slug":"ujjwala-yojana-free-gas-connection","icon":"🔥","date":"21 फरवरी 2024","read_time":"6 मिनट","content":"""
<h2>उज्ज्वला योजना क्या है?</h2>
<p>प्रधानमंत्री उज्ज्वला योजना (PMUY) मई 2016 में शुरू हुई। इस योजना के तहत BPL परिवारों की महिलाओं को <strong>मुफ्त LPG गैस कनेक्शन</strong> दिया जाता है। इसका उद्देश्य ग्रामीण और गरीब परिवारों को चूल्हे के धुएं से मुक्ति दिलाना है। अब तक 9 करोड़ से अधिक महिलाओं को इस योजना का लाभ मिल चुका है।</p>

<h2>क्या मिलता है मुफ्त?</h2>
<ul>
<li>🔥 LPG Connection (बिल्कुल मुफ्त)</li>
<li>💰 ₹1,600 की financial assistance (deposit और regulator के लिए)</li>
<li>🍳 पहला refill subsidized दर पर</li>
<li>🔧 Regulator, pipe और stove की सुविधा</li>
</ul>

<h2>पात्रता</h2>
<ul>
<li>महिला की उम्र 18 साल या उससे अधिक हो</li>
<li>BPL (गरीबी रेखा से नीचे) परिवार</li>
<li>घर में पहले से कोई LPG connection नहीं होना चाहिए</li>
<li>SECC-2011 डेटा में नाम हो या PM Ujjwala 2.0 में eligible हो</li>
</ul>

<h2>आवेदन कैसे करें?</h2>
<ol>
<li>नजदीकी LPG distributor (Indane, HP, Bharat Gas) पर जाएं</li>
<li>KYC form भरें</li>
<li>BPL card / Ration card जमा करें</li>
<li>आधार कार्ड की copy दें</li>
<li>बैंक account की जानकारी दें</li>
<li>Verification के बाद 15-30 दिन में connection मिलेगा</li>
</ol>

<h2>जरूरी दस्तावेज</h2>
<ul>
<li>📋 आधार कार्ड</li>
<li>🏠 BPL Ration Card या BPL Certificate</li>
<li>🏦 बैंक पासबुक</li>
<li>📸 पासपोर्ट साइज फोटो</li>
</ul>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>1906</strong> (LPG Emergency)<br>📞 <strong>1800-233-3555</strong> (Toll Free)</p>
"""},
    {"id":8,"yojana_id":8,"title":"जन धन खाता: Zero Balance + ₹2 लाख बीमा कैसे पाएं?","slug":"jan-dhan-account-kaise-khole","icon":"🏦","date":"20 फरवरी 2024","read_time":"5 मिनट","content":"""
<h2>जन धन योजना क्या है?</h2>
<p>प्रधानमंत्री जन धन योजना (PMJDY) अगस्त 2014 में शुरू हुई। यह दुनिया का सबसे बड़ा financial inclusion program है। इसके तहत बिना किसी minimum balance के <strong>Zero Balance बैंक खाता</strong> खोला जा सकता है। साथ में ₹2 लाख का दुर्घटना बीमा, ₹10,000 का overdraft और बहुत सारी सुविधाएं मिलती हैं।</p>

<h2>क्या-क्या मिलता है?</h2>
<ul>
<li>🏦 Zero Balance बैंक खाता</li>
<li>💳 RuPay Debit Card (मुफ्त)</li>
<li>☂️ ₹2 लाख दुर्घटना बीमा (RuPay card use करने पर)</li>
<li>🏥 ₹30,000 जीवन बीमा (eligible खाताधारकों को)</li>
<li>💰 ₹10,000 overdraft facility</li>
<li>📱 Mobile banking और Internet banking</li>
<li>💵 Direct Benefit Transfer (सरकारी लाभ सीधे खाते में)</li>
</ul>

<h2>खाता कैसे खोलें?</h2>
<ol>
<li>नजदीकी बैंक शाखा या Bank Mitra के पास जाएं</li>
<li>"Jan Dhan Account" खोलने के लिए कहें</li>
<li>Application form भरें</li>
<li>आधार कार्ड और एक फोटो दें</li>
<li>उसी दिन खाता खुल जाएगा और Passbook मिलेगी!</li>
<li>15-30 दिन में RuPay card भी मिलेगा</li>
</ol>

<h2>Overdraft कैसे मिलेगा?</h2>
<ul>
<li>6 महीने तक खाता सही से चलाएं</li>
<li>DBT (Direct Benefit Transfer) खाते में आता हो</li>
<li>Bank को overdraft के लिए apply करें</li>
<li>₹10,000 तक का overdraft मिल सकता है</li>
</ul>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>1800-11-0001</strong> (Toll Free)</p>
"""},
    {"id":9,"yojana_id":9,"title":"NSP Scholarship 2024: छात्रवृत्ति के लिए Online Apply कैसे करें?","slug":"nsp-scholarship-apply-online","icon":"🎓","date":"19 फरवरी 2024","read_time":"7 मिनट","content":"""
<h2>NSP Scholarship क्या है?</h2>
<p>National Scholarship Portal (NSP) भारत सरकार का एक एकीकृत scholarship portal है जहाँ SC, ST, OBC और अल्पसंख्यक वर्ग के छात्रों को पढ़ाई के लिए <strong>₹1,000 से ₹25,000</strong> तक की छात्रवृत्ति दी जाती है। यह portal 2013 में शुरू हुआ था और अब तक करोड़ों छात्रों को इससे लाभ मिल चुका है।</p>

<h2>कौन-कौन सी Scholarships मिलती हैं?</h2>
<ul>
<li><strong>Pre-Matric Scholarship:</strong> 9th और 10th के छात्रों के लिए</li>
<li><strong>Post-Matric Scholarship:</strong> 11th से ऊपर के छात्रों के लिए</li>
<li><strong>Merit cum Means Scholarship:</strong> Technical/professional courses के लिए</li>
<li><strong>Central Sector Scholarship:</strong> 12th के बाद college students के लिए</li>
<li><strong>Top Class Education Scholarship:</strong> Prestigious institutions के लिए</li>
<li><strong>PM Scholarship for RPF/RPSF:</strong> RPF जवानों के बच्चों के लिए</li>
</ul>

<h2>पात्रता</h2>
<ul>
<li>SC/ST/OBC/Minority वर्ग के छात्र</li>
<li>पिछली कक्षा में 50% से अधिक अंक</li>
<li>परिवार की वार्षिक आय तय सीमा से कम हो</li>
<li>Government या recognised school/college में पढ़ रहे हों</li>
<li>किसी और scholarship का लाभ न ले रहे हों</li>
</ul>

<h2>Online Apply कैसे करें? Step by Step</h2>
<ol>
<li><strong>Step 1:</strong> scholarships.gov.in खोलें</li>
<li><strong>Step 2:</strong> "New Registration" पर click करें</li>
<li><strong>Step 3:</strong> आधार कार्ड से register करें</li>
<li><strong>Step 4:</strong> Login करें और अपनी category की scholarship चुनें</li>
<li><strong>Step 5:</strong> सभी जानकारी carefully भरें</li>
<li><strong>Step 6:</strong> Documents upload करें</li>
<li><strong>Step 7:</strong> Submit करें और Application ID नोट करें</li>
<li><strong>Step 8:</strong> School/Institute से verify करवाएं</li>
</ol>

<h2>जरूरी दस्तावेज</h2>
<ul>
<li>📋 आधार कार्ड</li>
<li>📚 पिछली कक्षा की marksheet</li>
<li>🏷️ Caste Certificate (SC/ST/OBC के लिए)</li>
<li>💰 Income Certificate (परिवार की)</li>
<li>🏦 Bank Passbook (IFSC code सहित)</li>
<li>📸 Passport Size Photo</li>
<li>🏫 Bonafide Certificate from School/College</li>
</ul>

<h2>Application की Last Date</h2>
<p>आमतौर पर <strong>October-November</strong> में होती है। NSP website पर regularly check करते रहें।</p>

<h2>हेल्पलाइन</h2>
<p>📞 <strong>0120-6619540</strong><br>📧 helpdesk@nsp.gov.in</p>
"""},
    {"id":10,"yojana_id":1,"title":"PM-KISAN eKYC कैसे करें? बिना eKYC किस्त नहीं मिलेगी!","slug":"pm-kisan-ekyc-kaise-kare","icon":"🌾","date":"15 फरवरी 2024","read_time":"5 मिनट","content":"<h2>PM-KISAN eKYC क्यों जरूरी है?</h2><p>बिना eKYC के अगली किस्त रुक सकती है।</p><h2>OTP से eKYC Steps</h2><ol><li>pmkisan.gov.in → Farmers Corner → eKYC click करें</li><li>आधार नंबर डालें</li><li>मोबाइल OTP डालें और submit करें</li></ol><h2>Biometric eKYC</h2><p>मोबाइल linked नहीं है तो नजदीकी <strong>CSC Center</strong> पर जाएं — fingerprint से मुफ्त eKYC।</p><h2>Status Check</h2><p>pmkisan.gov.in → Farmers Corner → Know Your Status → आधार नंबर डालें।</p><h2>हेल्पलाइन</h2><p>📞 <strong>155261</strong></p>"},
    {"id":11,"yojana_id":3,"title":"Ayushman Bharat अस्पताल में मुफ्त इलाज कैसे लें?","slug":"ayushman-hospital-ilaj","icon":"🏥","date":"14 फरवरी 2024","read_time":"6 मिनट","content":"<h2>अस्पताल में क्या करें?</h2><ol><li>Reception पर Ayushman Bharat मरीज बताएं</li><li>Ayushman Mitra के पास जाएं</li><li>Card और आधार दिखाएं</li><li>OTP verification होगी</li><li>Cashless treatment शुरू होगा</li></ol><h2>कौन सी बीमारियाँ cover हैं?</h2><ul><li>Heart Surgery, Cancer, Kidney Dialysis</li><li>Knee Replacement, Cataract Surgery</li><li>1,393+ बीमारियाँ</li></ul><h2>Empanelled Hospital खोजें</h2><p>pmjay.gov.in → Find Hospital → राज्य और जिला select करें।</p><h2>हेल्पलाइन</h2><p>📞 <strong>14555</strong> (24x7)</p>"},
    {"id":12,"yojana_id":2,"title":"PMAY Gramin List 2024: अपना नाम कैसे देखें?","slug":"pmay-gramin-list-naam","icon":"🏠","date":"13 फरवरी 2024","read_time":"5 मिनट","content":"<h2>Online List में नाम कैसे देखें?</h2><ol><li>pmayg.nic.in खोलें</li><li>Awaassoft → Report → Social Audit Reports</li><li>Beneficiary details for verification click करें</li><li>राज्य, जिला, Block, ग्राम पंचायत select करें</li><li>Captcha भरें और list देखें</li></ol><h2>नाम नहीं है तो?</h2><ul><li>ग्राम पंचायत में आवेदन करें</li><li>Block Development Office में application दें</li></ul><h2>PMAY-G की राशि</h2><ul><li>मैदानी: ₹1,20,000 — तीन किस्तों में</li><li>पहाड़ी/नक्सल: ₹1,30,000 — तीन किस्तों में</li></ul><h2>हेल्पलाइन</h2><p>📞 <strong>1800-11-6163</strong></p>"},
    {"id":13,"yojana_id":8,"title":"Jan Dhan Overdraft: ₹10,000 बिना गारंटी कैसे लें?","slug":"jan-dhan-overdraft","icon":"🏦","date":"12 फरवरी 2024","read_time":"5 मिनट","content":"<h2>Jan Dhan Overdraft क्या है?</h2><p>Jan Dhan खाते पर <strong>₹10,000 तक का overdraft</strong> — बिना गारंटी, बिना paperwork।</p><h2>पात्रता</h2><ul><li>खाता 6 महीने पुराना हो</li><li>DBT आता हो खाते में</li><li>उम्र 18-60 साल</li></ul><h2>Apply करें</h2><ol><li>बैंक शाखा में जाएं</li><li>Overdraft application form भरें</li><li>आधार और passbook दें</li><li>Approval पर activate होगा</li></ol><h2>वापस कब करना होगा?</h2><p>30 दिन के अंदर।</p><h2>हेल्पलाइन</h2><p>📞 <strong>1800-11-0001</strong></p>"},
    {"id":14,"yojana_id":5,"title":"Mudra Loan SBI से कैसे लें? Online और Offline Process","slug":"mudra-loan-sbi-process","icon":"💼","date":"11 फरवरी 2024","read_time":"6 मिनट","content":"<h2>SBI से Mudra Loan Online</h2><ol><li>emudra.sbi.co.in पर जाएं</li><li>₹1 लाख तक online मिल सकता है</li><li>Login करें और form fill करें</li></ol><h2>udyamimitra.in से Apply करें</h2><ol><li>udyamimitra.in खोलें</li><li>Apply for Mudra Loan click करें</li><li>Register, Login, Bank select करें</li><li>Documents upload करें और submit करें</li></ol><h2>Loan मिलने में समय</h2><ul><li>Shishu (₹50,000): 7-10 दिन</li><li>Kishore: 15-20 दिन</li><li>Tarun (₹10 लाख): 20-30 दिन</li></ul><h2>Mudra Card</h2><p>Loan approve होने पर Mudra Card मिलता है — ATM जैसा use करें।</p><h2>हेल्पलाइन</h2><p>📞 <strong>1800-180-1111</strong></p>"},
    {"id":15,"yojana_id":6,"title":"Sukanya Samriddhi Calculator: ₹500/माह से बनाएं ₹45 लाख","slug":"sukanya-samriddhi-calculator","icon":"👧","date":"10 फरवरी 2024","read_time":"6 मिनट","content":"<h2>8.2% ब्याज पर कितना मिलेगा?</h2><ul><li>₹500/माह → 21 साल बाद ≈ <strong>₹4.5 लाख</strong></li><li>₹1,000/माह → 21 साल बाद ≈ <strong>₹9 लाख</strong></li><li>₹2,000/माह → 21 साल बाद ≈ <strong>₹18 लाख</strong></li><li>₹5,000/माह → 21 साल बाद ≈ <strong>₹45 लाख</strong></li><li>₹12,500/माह → 21 साल बाद ≈ <strong>₹70 लाख</strong></li></ul><h2>SSY vs PPF vs FD</h2><ul><li>SSY: 8.2% — Tax Free — Government Guarantee</li><li>PPF: 7.1% — Tax Free</li><li>FD: 6.5-7.5% — Taxable</li></ul><h2>Section 80C</h2><p>SSY में निवेश पर ₹1.5 लाख तक income tax में छूट मिलती है।</p><h2>खाता कहाँ खुलता है?</h2><p>Post Office, SBI, PNB, BOB, HDFC, ICICI और सभी authorized बैंकों में।</p>"},
    {"id":16,"yojana_id":9,"title":"SC ST Post Matric Scholarship 2024: ₹25,000 कैसे पाएं?","slug":"sc-st-scholarship-2024","icon":"🎓","date":"9 फरवरी 2024","read_time":"6 मिनट","content":"<h2>Post Matric Scholarship राशि</h2><ul><li>Group I (Medical/Engineering): ₹7,000-₹25,000</li><li>Group II (Professional): ₹3,500-₹10,000</li><li>Group III (Graduation): ₹2,500-₹5,000</li><li>Group IV (11th-12th): ₹1,200-₹3,000</li></ul><h2>पात्रता</h2><ul><li>SC/ST वर्ग के छात्र</li><li>SC के लिए: परिवार की आय ₹2.5 लाख से कम</li><li>ST के लिए: कोई income limit नहीं</li></ul><h2>Apply Steps</h2><ol><li>scholarships.gov.in पर जाएं</li><li>Register → Login करें</li><li>Post Matric Scholarship select करें</li><li>Form fill करें, documents upload करें</li><li>Institute से verify कराएं</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>0120-6619540</strong></p>"},
    {"id":17,"yojana_id":7,"title":"MGNREGA शिकायत: काम न मिले तो ये करें","slug":"mgnrega-complaint","icon":"⛏️","date":"8 फरवरी 2024","read_time":"5 मिनट","content":"<h2>शिकायत कब करें?</h2><p>काम नहीं मिला, मजदूरी कम मिली, Job Card नहीं बना, payment नहीं आई।</p><h2>Online शिकायत Steps</h2><ol><li>nrega.nic.in खोलें</li><li>Grievance section जाएं</li><li>राज्य select करें और form भरें</li><li>Complaint number नोट करें</li></ol><h2>Offline शिकायत</h2><ul><li>ग्राम पंचायत — सचिव/प्रधान को लिखित दें</li><li>BDO Office — Block Development Officer से मिलें</li></ul><h2>Unemployment Allowance</h2><p>15 दिन में काम नहीं मिला तो allowance मिलेगा — पहले 30 दिन: 25%, बाद में: 50%।</p><h2>हेल्पलाइन</h2><p>📞 <strong>1800-111-555</strong></p>"},
    {"id":18,"yojana_id":4,"title":"LPG Subsidy 2024: Ujjwala और Regular Subsidy Check करें","slug":"lpg-subsidy-check","icon":"🔥","date":"7 फरवरी 2024","read_time":"5 मिनट","content":"<h2>LPG Subsidy कितनी मिलती है?</h2><p>Ujjwala लाभार्थियों को <strong>₹200 प्रति cylinder</strong> (12 cylinders/वर्ष) subsidy मिलती है।</p><h2>Online Check Steps</h2><ol><li>mylpg.in खोलें</li><li>Gas company select करें</li><li>Consumer number डालें और OTP verify करें</li><li>Subsidy history देखें</li></ol><h2>Subsidy नहीं आई तो?</h2><ul><li>Bank account आधार से linked है?</li><li>LPG connection आधार से linked है?</li><li>Gas agency से संपर्क करें</li></ul><h2>हेल्पलाइन</h2><p>📞 <strong>1906</strong></p>"},
    {"id":19,"yojana_id":1,"title":"Kisan Credit Card: ₹3 लाख सिर्फ 4% ब्याज पर कैसे लें?","slug":"kisan-credit-card","icon":"🌾","date":"6 फरवरी 2024","read_time":"6 मिनट","content":"<h2>Kisan Credit Card (KCC) क्या है?</h2><p>किसानों को खेती के लिए <strong>सिर्फ 4% ब्याज</strong> पर ₹3 लाख तक का loan।</p><h2>KCC के फायदे</h2><ul><li>4% ब्याज पर ₹3 लाख loan</li><li>₹50,000 accident insurance</li><li>Crop insurance की सुविधा</li><li>ATM card मिलेगा</li></ul><h2>KCC कैसे बनवाएं?</h2><ol><li>नजदीकी बैंक में जाएं</li><li>KCC application form भरें</li><li>खसरा/खतौनी, आधार, PAN जमा करें</li><li>7-14 दिन में KCC मिलेगा</li></ol><h2>4% कैसे होता है?</h2><p>सरकार 2% subvention + 3% prompt repayment incentive = कुल 4% ब्याज।</p><h2>हेल्पलाइन</h2><p>📞 <strong>1800-180-1551</strong></p>"},
    {"id":20,"yojana_id":2,"title":"PMAY Urban List: शहर में घर के लिए कैसे करें आवेदन?","slug":"pmay-urban-apply","icon":"🏠","date":"5 फरवरी 2024","read_time":"6 मिनट","content":"""<h2>PMAY Urban क्या है?</h2><p>शहरी गरीबों को पक्का घर देने के लिए PMAY-Urban के तहत <strong>ब्याज सब्सिडी</strong> और direct benefit दिया जाता है।</p><h2>4 Components</h2><ul><li><strong>BLC:</strong> Beneficiary Led Construction — खुद जमीन है, घर बनाओ</li><li><strong>CLSS:</strong> Home loan पर interest subsidy</li><li><strong>AHP:</strong> Affordable Housing in Partnership</li><li><strong>ISSR:</strong> Slum Rehabilitation</li></ul><h2>CLSS Subsidy कितनी मिलती है?</h2><ul><li>EWS/LIG: 6.5% — ₹2.67 लाख तक</li><li>MIG-I: 4% — ₹2.35 लाख तक</li><li>MIG-II: 3% — ₹2.30 लाख तक</li></ul><h2>Online Apply करें</h2><ol><li>pmaymis.gov.in खोलें</li><li>Citizen Assessment click करें</li><li>Category select करें और form भरें</li><li>Application ID note करें</li></ol><h2>हेल्पलाइन</h2><p>📞 <strong>1800-11-3377</strong></p>"""},
    {"id":21,"yojana_id":3,"title":"Ayushman Bharat: नया Card 2024 में कैसे बनाएं? Step by Step","slug":"ayushman-card-banaye-2024","icon":"🏥","date":"4 फरवरी 2024","read_time":"5 मिनट","content":"""<h2>नया Ayushman Card 2024</h2><p>अब Ayushman Card बनाना और भी आसान हो गया है। <strong>घर बैठे mobile से</strong> card बना सकते हैं।</p><h2>Mobile से Card कैसे बनाएं?</h2><ol><li>beneficiary.nha.gov.in खोलें</li><li>मोबाइल नंबर डालें और OTP verify करें</li><li>आधार नंबर डालें</li><li>Face authentication या OTP से verify करें</li><li>Card download करें — PDF format में</li></ol><h2>PM-JAY App से Card बनाएं</h2><ol><li>Play Store से PMJAY app download करें</li><li>Register करें और login करें</li><li>आधार से verify करें</li><li>Card generate होगा</li></ol><h2>CSC Center से Card बनाएं</h2><p>नजदीकी CSC Center पर जाएं — वहाँ <strong>मुफ्त में</strong> card बनेगा। आधार card साथ लाएं।</p><h2>Card खो गया तो?</h2><p>beneficiary.nha.gov.in पर जाकर दोबारा download करें। Card unlimited बार download हो सकता है।</p><h2>हेल्पलाइन</h2><p>📞 <strong>14555</strong></p>"""},
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
.static-page{max-width:780px;margin:0 auto;background:white;border-radius:16px;padding:36px;border:1px solid #e0d5c0;box-shadow:0 4px 15px rgba(0,0,128,.07)}
.static-page h1{font-size:1.6rem;font-weight:800;color:#000080;margin-bottom:20px;padding-bottom:12px;border-bottom:3px solid #FF9933}
.static-page h2{font-size:1.1rem;font-weight:700;color:#000080;margin:20px 0 10px}
.static-page p{font-size:.9rem;line-height:1.8;color:#444;margin-bottom:12px}
.static-page ul{padding-left:20px;margin-bottom:14px}
.static-page li{font-size:.88rem;line-height:1.8;color:#444;margin-bottom:4px}
footer{background:#000080;color:rgba(255,255,255,.7);text-align:center;padding:18px;font-size:.8rem;margin-top:40px}
footer strong{color:#FF9933}
footer a{color:#FF9933;text-decoration:none}
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
<li><a href="/about">ℹ️ About</a></li>
<li><a href="/contact">📞 Contact</a></li>
</ul></nav>
</header>"""

FOOTER = """<footer>
<p>© 2024 <strong>भारत सरकार योजना पोर्टल</strong> | 
<a href="/about">About Us</a> | 
<a href="/contact">Contact</a> | 
<a href="/privacy-policy">Privacy Policy</a> | 
जानकारी के लिए आधिकारिक वेबसाइट देखें।</p>
</footer>"""

def render_page(title, body, desc="सरकारी योजना पोर्टल — भारत की सभी सरकारी योजनाएं एक जगह"):
    return f"""<!DOCTYPE html><html lang="hi"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="सरकारी योजना,PM-KISAN,PMAY,आयुष्मान भारत,sarkari yojana,government scheme india hindi">
<meta name="google-adsense-account" content="ca-pub-1709475506645918">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1709475506645918" crossorigin="anonymous"></script>
{STYLE}</head><body>{HEADER}<main>{body}</main>{FOOTER}</body></html>"""

@app.route('/')
def index():
    yojana_json = json.dumps(yojanas, ensure_ascii=False)
    body = f"""
    <div class="search-box">
    <h2>🇮🇳 सरकारी योजनाएं खोजें</h2>
    <p>भारत सरकार की सभी योजनाओं की जानकारी हिंदी में</p>
    <div class="search-row"><input type="text" id="si" placeholder="योजना खोजें... जैसे किसान, आवास, स्वास्थ्य"><button onclick="window.location='/search?q='+document.getElementById('si').value">🔍 खोजें</button></div>
    <div class="filters">
    <a href="/" class="filter-btn">सभी</a>
    <a href="/search?category=कृषि" class="filter-btn">🌾 कृषि</a>
    <a href="/search?category=स्वास्थ्य" class="filter-btn">🏥 स्वास्थ्य</a>
    <a href="/search?category=आवास" class="filter-btn">🏠 आवास</a>
    <a href="/search?category=महिला" class="filter-btn">👩 महिला</a>
    <a href="/search?category=रोजगार" class="filter-btn">💼 रोजगार</a>
    <a href="/search?category=शिक्षा" class="filter-btn">🎓 शिक्षा</a>
    <a href="/search?category=बैंकिंग" class="filter-btn">🏦 बैंकिंग</a>
    </div></div>
    <div class="stats">
    <div class="stat"><div class="num">9+</div><div class="lbl">सरकारी योजनाएं</div></div>
    <div class="stat"><div class="num">9</div><div class="lbl">विस्तृत Articles</div></div>
    <div class="stat"><div class="num">100Cr+</div><div class="lbl">लाभार्थी</div></div>
    </div>
    <div class="section-title">📋 सभी सरकारी योजनाएं</div>
    <div class="grid" id="grid"></div>
    <script>
    const y={yojana_json};
    document.getElementById('grid').innerHTML=y.map(x=>`<a href="/yojana/${{x.id}}" class="card"><div class="card-head"><div class="card-icon">${{x.icon}}</div><div><div class="card-name">${{x.name}}</div><div class="card-cat">${{x.category}}</div></div></div><p class="card-desc">${{x.description}}</p><div class="card-benefit"><div class="benefit-lbl">💰 लाभ</div><div class="benefit-val">${{x.benefit}}</div></div><div class="card-elig">👥 ${{x.eligibility}}</div><span class="card-btn">विवरण देखें →</span></a>`).join('');
    document.getElementById('si').addEventListener('keyup',e=>{{if(e.key==='Enter')window.location='/search?q='+e.target.value}});
    </script>"""
    return render_page("सरकारी योजना पोर्टल 🇮🇳 | भारत की सभी योजनाएं हिंदी में", body)

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
    <a href="{y['link']}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg,#FF9933,#e07a1a);color:white;text-align:center;border-radius:12px;text-decoration:none;font-weight:700">🚀 अभी आवेदन करें</a>
    {art_btn}</div>"""
    return render_page(f"{y['name']} | सरकारी योजना पोर्टल", body, y['description'])

@app.route('/blog')
def blog():
    cards = ''.join([f'<a href="/blog/{a["slug"]}" class="blog-card"><div class="blog-icon">{a["icon"]}</div><div class="blog-title">{a["title"]}</div><div class="blog-meta"><span>📅 {a["date"]}</span><span>⏱️ {a["read_time"]}</span></div><span class="read-more">पूरा पढ़ें →</span></a>' for a in articles])
    body = f'<div class="section-title">📰 सरकारी योजनाओं पर Articles ({len(articles)})</div><div class="blog-grid">{cards}</div>'
    return render_page("Articles | सरकारी योजना पोर्टल", body, "सरकारी योजनाओं पर विस्तृत लेख — कैसे करें आवेदन, पात्रता, दस्तावेज")

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

@app.route('/about')
def about():
    body = """<a href="/" class="back-btn">← होम</a>
    <div class="static-page">
    <h1>ℹ️ हमारे बारे में (About Us)</h1>
    <p><strong>सरकारी योजना पोर्टल</strong> एक informational website है जो भारत के नागरिकों को सरकारी योजनाओं की जानकारी हिंदी में प्रदान करती है।</p>
    <h2>हमारा उद्देश्य</h2>
    <p>हमारा मुख्य उद्देश्य भारत के आम नागरिकों तक सरकारी योजनाओं की सही और सरल जानकारी पहुंचाना है। बहुत से लोग सरकारी योजनाओं के बारे में नहीं जानते और उनका लाभ नहीं उठा पाते। हम उन्हें सही जानकारी देकर उनकी मदद करना चाहते हैं।</p>
    <h2>हम क्या करते हैं?</h2>
    <ul>
    <li>सरकारी योजनाओं की विस्तृत जानकारी हिंदी में देते हैं</li>
    <li>योजनाओं में आवेदन करने की Step-by-Step guide देते हैं</li>
    <li>पात्रता और जरूरी दस्तावेजों की जानकारी देते हैं</li>
    <li>हेल्पलाइन नंबर और official websites की जानकारी देते हैं</li>
    </ul>
    <h2>महत्वपूर्ण सूचना</h2>
    <p>यह एक informational portal है। हम किसी भी सरकारी संस्था से directly affiliated नहीं हैं। योजनाओं की official जानकारी के लिए हमेशा संबंधित मंत्रालय की official website देखें।</p>
    <h2>संपर्क करें</h2>
    <p>किसी भी सुझाव या जानकारी के लिए हमारे <a href="/contact" style="color:#000080">Contact page</a> पर जाएं।</p>
    </div>"""
    return render_page("About Us | सरकारी योजना पोर्टल", body, "सरकारी योजना पोर्टल के बारे में जानकारी")

@app.route('/contact')
def contact():
    body = """<a href="/" class="back-btn">← होम</a>
    <div class="static-page">
    <h1>📞 संपर्क करें (Contact Us)</h1>
    <p>हम आपकी सेवा में सदैव तत्पर हैं। किसी भी सवाल, सुझाव या जानकारी के लिए नीचे दिए गए माध्यमों से संपर्क करें।</p>
    <h2>सामान्य सरकारी हेल्पलाइन नंबर</h2>
    <ul>
    <li>📞 <strong>PM-KISAN हेल्पलाइन:</strong> 155261</li>
    <li>📞 <strong>आयुष्मान भारत:</strong> 14555</li>
    <li>📞 <strong>PM Awas Yojana:</strong> 1800-11-6163</li>
    <li>📞 <strong>मुद्रा योजना:</strong> 1800-180-1111</li>
    <li>📞 <strong>मनरेगा:</strong> 1800-111-555</li>
    <li>📞 <strong>जन धन योजना:</strong> 1800-11-0001</li>
    <li>📞 <strong>उज्ज्वला योजना:</strong> 1906</li>
    </ul>
    <h2>राष्ट्रीय हेल्पलाइन</h2>
    <ul>
    <li>📞 <strong>PM Helpline:</strong> 1800-11-7800</li>
    <li>📞 <strong>National Helpline:</strong> 1076</li>
    <li>📞 <strong>CSC Helpline:</strong> 1800-3000-3468</li>
    </ul>
    <h2>वेबसाइट के बारे में सुझाव</h2>
    <p>अगर आप इस website के बारे में कोई सुझाव देना चाहते हैं तो कृपया हमें email करें।</p>
    <p>📧 <strong>Email:</strong> sarkari.yojana.portal@gmail.com</p>
    </div>"""
    return render_page("Contact Us | सरकारी योजना पोर्टल", body, "सरकारी योजना पोर्टल से संपर्क करें")

@app.route('/privacy-policy')
def privacy_policy():
    body = """<a href="/" class="back-btn">← होम</a>
    <div class="static-page">
    <h1>🔒 Privacy Policy (गोपनीयता नीति)</h1>
    <p>यह Privacy Policy सरकारी योजना पोर्टल (sarkari-yojana.onrender.com) के लिए है। इस website का उपयोग करके आप इस policy से सहमत होते हैं।</p>
    <h2>हम क्या जानकारी collect करते हैं?</h2>
    <p>हम कोई personal जानकारी collect नहीं करते। यह एक informational website है।</p>
    <h2>Cookies</h2>
    <p>यह website Google AdSense के लिए cookies का उपयोग करती है। Google AdSense आपकी browsing habits के आधार पर relevant ads दिखाता है।</p>
    <h2>Third Party Advertising</h2>
    <p>हम Google AdSense का उपयोग करते हैं जो आपकी browsing information के आधार पर ads दिखाता है। Google की privacy policy के लिए google.com/privacy पर जाएं।</p>
    <h2>External Links</h2>
    <p>इस website पर सरकारी websites के links हैं। उन websites की privacy policy हमारी जिम्मेदारी नहीं है।</p>
    <h2>Changes to Privacy Policy</h2>
    <p>हम समय-समय पर इस policy को update कर सकते हैं।</p>
    <h2>Contact</h2>
    <p>किसी भी प्रश्न के लिए <a href="/contact" style="color:#000080">Contact page</a> पर जाएं।</p>
    <p style="color:#888;font-size:.8rem;margin-top:20px">Last Updated: फरवरी 2024</p>
    </div>"""
    return render_page("Privacy Policy | सरकारी योजना पोर्टल", body, "सरकारी योजना पोर्टल की गोपनीयता नीति")

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-1709475506645918, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

@app.route('/api/yojanas')
def api_yojanas():
    return jsonify(yojanas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
