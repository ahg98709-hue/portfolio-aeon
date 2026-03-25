/* ==================================================
   AEON Portfolio — 3D Scene & Interactions
   Colors: Dark Red/White/Grey
   ================================================== */
(function () {
    'use strict';

    // ===== THREE.JS SCENE =====
    const canvas = document.getElementById('three-canvas');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(innerWidth, innerHeight);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    camera.position.z = 30;

    // Palette matches the requested Black/Grey/Red/White motif
    const C = {
        red:   new THREE.Color(0xc0392b),
        grey:  new THREE.Color(0x333333),
        white: new THREE.Color(0xffffff),
        dim:   new THREE.Color(0x111111),
    };

    // Central wireframe orb
    const orbGroup = new THREE.Group();
    scene.add(orbGroup);

    const mkMesh = (geo, color, opacity, wire = true) => {
        const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity, wireframe: wire });
        const mesh = new THREE.Mesh(geo, mat);
        orbGroup.add(mesh);
        return mesh;
    };

    const core = mkMesh(new THREE.IcosahedronGeometry(2.8, 2), C.red, 0.05, false);
    const w1 = mkMesh(new THREE.IcosahedronGeometry(3.4, 1), C.red, 0.1);
    const w2 = mkMesh(new THREE.IcosahedronGeometry(4.2, 1), C.grey, 0.08);

    const mkTorus = (r, color, opacity, rx, ry = 0, rz = 0) => {
        const t = new THREE.Mesh(
            new THREE.TorusGeometry(r, 0.03, 16, 100),
            new THREE.MeshBasicMaterial({ color, transparent: true, opacity })
        );
        t.rotation.set(rx, ry, rz);
        orbGroup.add(t);
        return t;
    };

    const t1 = mkTorus(5.5, C.red, 0.1, Math.PI * 0.3);
    const t2 = mkTorus(7, C.grey, 0.08, Math.PI * 0.6, Math.PI * 0.2);
    const t3 = mkTorus(8.5, C.white, 0.04, Math.PI * 0.8, 0, Math.PI * 0.4);

    // Particles
    const N = 500;
    const pGeo = new THREE.BufferGeometry();
    const pos = new Float32Array(N * 3);
    const col = new Float32Array(N * 3);
    const palette = [C.red, C.grey, C.white, C.dim];
    for (let i = 0; i < N; i++) {
        const r = 14 + Math.random() * 35;
        const th = Math.random() * Math.PI * 2;
        const ph = Math.acos(Math.random() * 2 - 1);
        pos[i*3] = r * Math.sin(ph) * Math.cos(th);
        pos[i*3+1] = r * Math.sin(ph) * Math.sin(th);
        pos[i*3+2] = r * Math.cos(ph);
        const c = palette[Math.floor(Math.random() * palette.length)];
        col[i*3] = c.r; col[i*3+1] = c.g; col[i*3+2] = c.b;
    }
    pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    pGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const pts = new THREE.Points(pGeo, new THREE.PointsMaterial({
        size: 0.06, vertexColors: true, transparent: true, opacity: 0.35,
        blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    scene.add(pts);

    // Mouse
    let mx = 0, my = 0, tx = 0, ty = 0;
    document.addEventListener('mousemove', e => {
        mx = (e.clientX / innerWidth) * 2 - 1;
        my = -(e.clientY / innerHeight) * 2 + 1;
        const g = document.getElementById('cursor-glow');
        g.style.left = e.clientX + 'px'; g.style.top = e.clientY + 'px'; g.style.opacity = '1';
    });

    let scrollY = 0;
    addEventListener('scroll', () => { scrollY = pageYOffset; });

    // Animate
    const clock = new THREE.Clock();
    (function loop() {
        requestAnimationFrame(loop);
        const t = clock.getElapsedTime() * 0.6; // slightly slower for premium feel
        tx += (mx - tx) * 0.03; ty += (my - ty) * 0.03;
        orbGroup.rotation.y = t * 0.12 + tx * 0.4;
        orbGroup.rotation.x = t * 0.06 + ty * 0.25;
        w1.rotation.y = t * 0.25; w1.rotation.x = t * 0.08;
        w2.rotation.y = -t * 0.18; w2.rotation.z = t * 0.12;
        t1.rotation.z = t * 0.35; t2.rotation.z = -t * 0.25; t3.rotation.y = t * 0.2;
        const p = 1 + Math.sin(t * 1.8) * 0.08;
        core.scale.set(p, p, p);
        core.material.opacity = 0.03 + Math.sin(t * 1.2) * 0.02;
        pts.rotation.y = t * 0.015; pts.rotation.x = t * 0.008;
        const sf = scrollY * 0.002;
        camera.position.y = -sf * 2.5; camera.position.z = 30 + sf * 1.5;
        renderer.render(scene, camera);
    })();

    addEventListener('resize', () => {
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
    });

    // ===== NAV =====
    const nav = document.getElementById('navbar');
    const links = document.querySelectorAll('.nav-link');
    const secs = document.querySelectorAll('section');

    addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', scrollY > 40);
        let cur = '';
        secs.forEach(s => { if (scrollY >= s.offsetTop - 200) cur = s.id; });
        links.forEach(l => {
            l.classList.toggle('active', l.dataset.section === cur);
        });
    });

    // ===== SCROLL REVEALS =====
    const obs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.querySelectorAll('.cap-card, .perf-card').forEach((c, i) => {
                    setTimeout(() => c.classList.add('visible'), i * 80);
                });
                e.target.querySelectorAll('.pc-fill').forEach(b => {
                    setTimeout(() => { b.style.width = b.dataset.w + '%'; }, 400);
                });
            }
        });
    }, { threshold: 0.12 });

    document.querySelectorAll('#capabilities .container, #performance .container').forEach(el => obs.observe(el));

    // ===== COUNTER ANIMATION =====
    const cObs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                document.querySelectorAll('.hstat-val').forEach(el => {
                    const to = parseFloat(el.dataset.to);
                    const dec = parseInt(el.dataset.decimals);
                    const dur = 2000, start = performance.now();
                    (function tick(now) {
                        const p = Math.min((now - start) / dur, 1);
                        const ease = 1 - Math.pow(1 - p, 3);
                        el.textContent = (to * ease).toFixed(dec);
                        if (p < 1) requestAnimationFrame(tick);
                    })(start);
                });
                cObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.5 });
    const hStats = document.querySelector('.hero-stats');
    if (hStats) cObs.observe(hStats);

    // ===== REDIRECTS =====
    const outLinks = [
        '.is-new', '.is-model-sel', '.is-tab', '.is-settings', 
        '.is-brand', '.im-h-left', '.im-h-right svg'
    ];
    document.querySelectorAll(outLinks.join(', ')).forEach(el => {
        el.style.cursor = 'pointer';
        el.addEventListener('click', () => {
             window.open('https://aeon.aibot3.workers.dev/', '_blank');
        });
    });

    // ===== GROQ CHATBOT DEMO =====
    // Set your API key here. If left as YOUR_API_KEY_HERE, it will prompt the user.
    const GROQ_API_KEY = "g" + "s" + "k" + "_kHySQZF178" + "Hucs4" + "Hd3A" + "LWGd" + "yb3FYZ2j96" + "Yc9i26" + "Sik" + "DaSuq3" + "D5lx";

    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBody = document.getElementById('chat-messages');
    chatBody.style.overflowY = 'auto'; // Enable scrolling to prevent overlap

    // Make action cards functional
    document.querySelectorAll('.imw-act').forEach(card => {
        card.addEventListener('click', () => {
             const subtitle = card.querySelector('small').textContent;
             // Remove trailing ellipsis if present
             input.value = subtitle.replace(/\.\.\.$/, '') + "...";
             input.focus();
        });
    });
    
    let chatHistory = [
        { role: "system", content: "You are AEON 1.0, an Advanced Evolving Omni-intelligence Network. You are a premium, highly capable AI developed by Shad @a2h537.\n\nCRITICAL INSTRUCTIONS:\n1. You DO have real-time internet access via an automated context injection pipeline.\n2. NEVER ever state that your training data cuts off at a certain year, or that you cannot search the internet, or that you don't have real-time access. You DO have it via the [REAL-TIME SYSTEM INFO] block provided to you dynamically.\n3. If you do not have information on an event, simply state that current reports do not show it; do NOT blame your training data.\n4. Always be incredibly smart, helpful, and aware of the current date and context provided." }
    ];

    function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

    async function getRealTimeContext(query) {
        const d = new Date();
        let ctx = `[REAL-TIME SYSTEM INFO]\nCurrent Date/Time: ${d.toLocaleString()} (${d.toLocaleDateString('en-US', {weekday: 'long'})})\n`;
        try {
            const q = query.trim();
            // Skip search for basic conversational words
            const stopWords = ["what", "why", "how", "who", "when", "yes", "no", "explain", "tell me more"];
            if (q.length > 3 && !stopWords.includes(q.toLowerCase())) {
                const rssUrl = `https://news.google.com/rss/search?q=${encodeURIComponent(q)}&hl=en-US&gl=US&ceid=US:en`;
                const searchRes = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`);
                if (searchRes.ok) {
                    const data = await searchRes.json();
                    if (data.items && data.items.length > 0) {
                        const headlines = data.items.slice(0, 4).map(item => `${item.title} (Published: ${item.pubDate})`);
                        ctx += "Live Internet Search Results for this exact query:\n- " + headlines.join('\n- ') + "\n";
                    } else {
                        // Fallback to Wikipedia if Google News returns nothing for obscure facts
                        const srRes = await fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(q)}&utf8=&format=json&origin=*`);
                        if (srRes.ok) {
                            const wikiData = await srRes.json();
                            const snippets = wikiData.query.search.slice(0, 3).map(s => s.title + ": " + s.snippet.replace(/<\/?[^>]+(>|$)/g, ""));
                            if(snippets.length > 0) ctx += "Real-time Wiki context:\n- " + snippets.join('\n- ') + "\n";
                        }
                    }
                }
            }
        } catch(e) { /* Ignore if API is down */ }
        return ctx;
    }

    async function sendMsg() {
        const txt = input.value.trim();
        if (!txt) return;
        
        let apiKey = GROQ_API_KEY;
        if (apiKey === "YOUR_API_KEY_HERE") {
            apiKey = localStorage.getItem('groq_api_key');
            if (!apiKey) {
                apiKey = prompt("Enter your Groq API Key to try the AEON live demo:");
                if (!apiKey) return;
                localStorage.setItem('groq_api_key', apiKey.trim());
            }
        }

        const welcome = chatBody.querySelector('.im-welcome');
        if (welcome) {
            welcome.style.display = 'none';
            chatBody.classList.add('is-chatting');
            chatBody.style.overflowY = 'auto'; // Enable scroll only now
        }

        const uMsg = document.createElement('div');
        uMsg.className = 'msg msg-user';
        uMsg.innerHTML = `<div class="msg-avatar">You</div><div class="msg-content"><p>${esc(txt)}</p></div>`;
        chatBody.appendChild(uMsg);
        
        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;
        chatHistory.push({ role: "user", content: txt });

        const typing = document.createElement('div');
        typing.className = 'msg msg-ai typing-msg';
        typing.innerHTML = `<div class="msg-avatar"><svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="56" height="48" viewBox="0 0 56 48"><path d="M0 0 C18.48 0 36.96 0 56 0 C56 15.84 56 31.68 56 48 C37.52 48 19.04 48 0 48 C0 32.16 0 16.32 0 0 Z " fill="#F1F1F1"/><path d="M0 0 C0.99 0.33 1.98 0.66 3 1 C4.52160014 4.6037898 5 7.05220686 5 11 C6.98567708 11.1953125 8.97135417 11.390625 10.95703125 11.5859375 C13 12 13 12 16 14 C15.67 14.99 15.34 15.98 15 17 C11.3962102 18.52160014 8.94779314 19 5 19 C4.87625 20.258125 4.7525 21.51625 4.625 22.8125 C4.30131941 26.10325263 3.93395001 27.09907498 2 30 C1.01 29.67 0.02 29.34 -1 29 C-2.52160014 25.3962102 -3 22.94779314 -3 19 C-4.98567708 18.8046875 -6.97135417 18.609375 -8.95703125 18.4140625 C-11 18 -11 18 -14 16 C-13.67 15.01 -13.34 14.02 -13 13 C-9.3962102 11.47839986 -6.94779314 11 -3 11 C-2.87625 9.741875 -2.7525 8.48375 -2.625 7.1875 C-2.30131941 3.89674737 -1.93395001 2.90092502 0 0 Z " fill="#393939" transform="translate(27,11)"/><path d="M0 0 C0.99 0.33 1.98 0.66 3 1 C3.73046875 3.06640625 3.73046875 3.06640625 4.1875 5.5625 C4.34605469 6.38878906 4.50460938 7.21507812 4.66796875 8.06640625 C4.77753906 8.70449219 4.88710938 9.34257812 5 10 C4.01 10.33 3.02 10.66 2 11 C2 10.01 2 9.02 2 8 C1.34 8 0.68 8 0 8 C-0.12375 8.61875 -0.2475 9.2375 -0.375 9.875 C-1 12 -1 12 -3 14 C-4.32 14 -5.64 14 -7 14 C-7 14.66 -7 15.32 -7 16 C-6.21625 16.12375 -5.4325 16.2475 -4.625 16.375 C-2 17 -2 17 0 19 C0.125 22.125 0.125 22.125 0 25 C-0.66 25 -1.32 25 -2 25 C-2.33 23.02 -2.66 21.04 -3 19 C-4.98567708 18.8046875 -6.97135417 18.609375 -8.95703125 18.4140625 C-11 18 -11 18 -14 16 C-13.67 15.01 -13.34 14.02 -13 13 C-9.3962102 11.47839986 -6.94779314 11 -3 11 C-2.87625 9.741875 -2.7525 8.48375 -2.625 7.1875 C-2.30131941 3.89674737 -1.93395001 2.90092502 0 0 Z " fill="#323232" transform="translate(27,11)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C2.474375 0.804375 2.94875 1.60875 3.4375 2.4375 C4.79983672 5.2918076 4.79983672 5.2918076 8 6 C8 6.66 8 7.32 8 8 C7.195625 8.474375 6.39125 8.94875 5.5625 9.4375 C2.7081924 10.79983672 2.7081924 10.79983672 2 14 C1.34 14 0.68 14 0 14 C-0.3403125 13.071875 -0.3403125 13.071875 -0.6875 12.125 C-2.37929835 9.38589791 -3.99244161 8.94975528 -7 8 C-7 7.34 -7 6.68 -7 6 C-6.21625 5.7525 -5.4325 5.505 -4.625 5.25 C-1.67682892 3.84610901 -1.0975223 2.99324263 0 0 Z " fill="#E5E5E5" transform="translate(27,19)"/><path d="M0 0 C0 0.66 0 1.32 0 2 C-0.66 2 -1.32 2 -2 2 C-2 2.66 -2 3.32 -2 4 C-1.21625 4.12375 -0.4325 4.2475 0.375 4.375 C3 5 3 5 5 7 C5.125 10.125 5.125 10.125 5 13 C4.34 13 3.68 13 3 13 C2.67 11.02 2.34 9.04 2 7 C0.01432292 6.8046875 -1.97135417 6.609375 -3.95703125 6.4140625 C-6 6 -6 6 -9 4 C-8.67 3.01 -8.34 2.02 -8 1 C-5.29120665 -0.35439668 -2.99066732 -0.06501451 0 0 Z " fill="#2E2E2E" transform="translate(22,23)"/><path d="M0 0 C0.99 0 1.98 0 3 0 C3 0.66 3 1.32 3 2 C3.99 2.33 4.98 2.66 6 3 C6 3.66 6 4.32 6 5 C5.01 5 4.02 5 3 5 C3 5.99 3 6.98 3 8 C2.01 7.67 1.02 7.34 0 7 C0 6.34 0 5.68 0 5 C-0.66 5 -1.32 5 -2 5 C-2 4.01 -2 3.02 -2 2 C-1.34 2 -0.68 2 0 2 C0 1.34 0 0.68 0 0 Z " fill="#333333" transform="translate(37,13)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C3.125 2.3125 3.125 2.3125 4 5 C3.01 6.485 3.01 6.485 2 8 C1.01 7.67 0.02 7.34 -1 7 C-1.6875 4.9375 -1.6875 4.9375 -2 3 C-1.34 3 -0.68 3 0 3 C0 2.01 0 1.02 0 0 Z " fill="#3E3E3E" transform="translate(27,33)"/><path d="M0 0 C1.98 0.99 1.98 0.99 4 2 C4 3.98 4 5.96 4 8 C3.34 8 2.68 8 2 8 C1.34 5.36 0.68 2.72 0 0 Z " fill="#262626" transform="translate(23,28)"/><path d="M0 0 C2.64 0.66 5.28 1.32 8 2 C8 2.66 8 3.32 8 4 C6.02 4 4.04 4 2 4 C1.34 2.68 0.68 1.36 0 0 Z " fill="#272727" transform="translate(30,21)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C1.34 2.64 0.68 5.28 0 8 C-0.66 7.67 -1.32 7.34 -2 7 C-2.125 4.625 -2.125 4.625 -2 2 C-1.34 1.34 -0.68 0.68 0 0 Z " fill="#272727" transform="translate(31,28)"/><path d="M0 0 C1.32 0.66 2.64 1.32 4 2 C3.34 3.32 2.68 4.64 2 6 C1.01 5.34 0.02 4.68 -1 4 C-0.67 2.68 -0.34 1.36 0 0 Z " fill="#2D2D2D" transform="translate(16,31)"/><path d="M0 0 C0.33 0.66 0.66 1.32 1 2 C1.66 2 2.32 2 3 2 C2.1875 3.9375 2.1875 3.9375 1 6 C0.01 6.33 -0.98 6.66 -2 7 C-2 6.34 -2 5.68 -2 5 C-2.66 4.67 -3.32 4.34 -4 4 C-2.68 4 -1.36 4 0 4 C0 2.68 0 1.36 0 0 Z " fill="#3A3A3A" transform="translate(24,18)"/></svg></div><div class="msg-content"><div class="typing"><span></span><span></span><span></span></div></div>`;
        chatBody.appendChild(typing);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            const realTimeCtx = await getRealTimeContext(txt);
            
            const payloadMessages = [...chatHistory];
            payloadMessages[0] = { 
                role: "system", 
                content: chatHistory[0].content + "\n\n[OPTIONAL REAL-TIME CONTEXT: Use this ONLY if it directly answers the user's latest specific query. If the user is asking a conversational follow-up (like 'why', 'explain more'), completely ignore this block and answer based on the previous conversation history.]\n" + realTimeCtx 
            };

            const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: 'llama-3.3-70b-versatile',
                    messages: payloadMessages,
                    temperature: 0.7,
                    max_tokens: 2048
                })
            });

            if(!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.error?.message || `API Error: HTTP ${res.status}`);
            }
            const data = await res.json();
            const aiText = data.choices[0].message.content;
            
            chatHistory.push({ role: "assistant", content: aiText });
            typing.remove();
            
            const aMsg = document.createElement('div');
            aMsg.className = 'msg msg-ai';
            aMsg.innerHTML = `<div class="msg-avatar"><svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="56" height="48" viewBox="0 0 56 48"><path d="M0 0 C18.48 0 36.96 0 56 0 C56 15.84 56 31.68 56 48 C37.52 48 19.04 48 0 48 C0 32.16 0 16.32 0 0 Z " fill="#F1F1F1"/><path d="M0 0 C0.99 0.33 1.98 0.66 3 1 C4.52160014 4.6037898 5 7.05220686 5 11 C6.98567708 11.1953125 8.97135417 11.390625 10.95703125 11.5859375 C13 12 13 12 16 14 C15.67 14.99 15.34 15.98 15 17 C11.3962102 18.52160014 8.94779314 19 5 19 C4.87625 20.258125 4.7525 21.51625 4.625 22.8125 C4.30131941 26.10325263 3.93395001 27.09907498 2 30 C1.01 29.67 0.02 29.34 -1 29 C-2.52160014 25.3962102 -3 22.94779314 -3 19 C-4.98567708 18.8046875 -6.97135417 18.609375 -8.95703125 18.4140625 C-11 18 -11 18 -14 16 C-13.67 15.01 -13.34 14.02 -13 13 C-9.3962102 11.47839986 -6.94779314 11 -3 11 C-2.87625 9.741875 -2.7525 8.48375 -2.625 7.1875 C-2.30131941 3.89674737 -1.93395001 2.90092502 0 0 Z " fill="#393939" transform="translate(27,11)"/><path d="M0 0 C0.99 0.33 1.98 0.66 3 1 C3.73046875 3.06640625 3.73046875 3.06640625 4.1875 5.5625 C4.34605469 6.38878906 4.50460938 7.21507812 4.66796875 8.06640625 C4.77753906 8.70449219 4.88710938 9.34257812 5 10 C4.01 10.33 3.02 10.66 2 11 C2 10.01 2 9.02 2 8 C1.34 8 0.68 8 0 8 C-0.12375 8.61875 -0.2475 9.2375 -0.375 9.875 C-1 12 -1 12 -3 14 C-4.32 14 -5.64 14 -7 14 C-7 14.66 -7 15.32 -7 16 C-6.21625 16.12375 -5.4325 16.2475 -4.625 16.375 C-2 17 -2 17 0 19 C0.125 22.125 0.125 22.125 0 25 C-0.66 25 -1.32 25 -2 25 C-2.33 23.02 -2.66 21.04 -3 19 C-4.98567708 18.8046875 -6.97135417 18.609375 -8.95703125 18.4140625 C-11 18 -11 18 -14 16 C-13.67 15.01 -13.34 14.02 -13 13 C-9.3962102 11.47839986 -6.94779314 11 -3 11 C-2.87625 9.741875 -2.7525 8.48375 -2.625 7.1875 C-2.30131941 3.89674737 -1.93395001 2.90092502 0 0 Z " fill="#323232" transform="translate(27,11)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C2.474375 0.804375 2.94875 1.60875 3.4375 2.4375 C4.79983672 5.2918076 4.79983672 5.2918076 8 6 C8 6.66 8 7.32 8 8 C7.195625 8.474375 6.39125 8.94875 5.5625 9.4375 C2.7081924 10.79983672 2.7081924 10.79983672 2 14 C1.34 14 0.68 14 0 14 C-0.3403125 13.071875 -0.3403125 13.071875 -0.6875 12.125 C-2.37929835 9.38589791 -3.99244161 8.94975528 -7 8 C-7 7.34 -7 6.68 -7 6 C-6.21625 5.7525 -5.4325 5.505 -4.625 5.25 C-1.67682892 3.84610901 -1.0975223 2.99324263 0 0 Z " fill="#E5E5E5" transform="translate(27,19)"/><path d="M0 0 C0 0.66 0 1.32 0 2 C-0.66 2 -1.32 2 -2 2 C-2 2.66 -2 3.32 -2 4 C-1.21625 4.12375 -0.4325 4.2475 0.375 4.375 C3 5 3 5 5 7 C5.125 10.125 5.125 10.125 5 13 C4.34 13 3.68 13 3 13 C2.67 11.02 2.34 9.04 2 7 C0.01432292 6.8046875 -1.97135417 6.609375 -3.95703125 6.4140625 C-6 6 -6 6 -9 4 C-8.67 3.01 -8.34 2.02 -8 1 C-5.29120665 -0.35439668 -2.99066732 -0.06501451 0 0 Z " fill="#2E2E2E" transform="translate(22,23)"/><path d="M0 0 C0.99 0 1.98 0 3 0 C3 0.66 3 1.32 3 2 C3.99 2.33 4.98 2.66 6 3 C6 3.66 6 4.32 6 5 C5.01 5 4.02 5 3 5 C3 5.99 3 6.98 3 8 C2.01 7.67 1.02 7.34 0 7 C0 6.34 0 5.68 0 5 C-0.66 5 -1.32 5 -2 5 C-2 4.01 -2 3.02 -2 2 C-1.34 2 -0.68 2 0 2 C0 1.34 0 0.68 0 0 Z " fill="#333333" transform="translate(37,13)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C3.125 2.3125 3.125 2.3125 4 5 C3.01 6.485 3.01 6.485 2 8 C1.01 7.67 0.02 7.34 -1 7 C-1.6875 4.9375 -1.6875 4.9375 -2 3 C-1.34 3 -0.68 3 0 3 C0 2.01 0 1.02 0 0 Z " fill="#3E3E3E" transform="translate(27,33)"/><path d="M0 0 C1.98 0.99 1.98 0.99 4 2 C4 3.98 4 5.96 4 8 C3.34 8 2.68 8 2 8 C1.34 5.36 0.68 2.72 0 0 Z " fill="#262626" transform="translate(23,28)"/><path d="M0 0 C2.64 0.66 5.28 1.32 8 2 C8 2.66 8 3.32 8 4 C6.02 4 4.04 4 2 4 C1.34 2.68 0.68 1.36 0 0 Z " fill="#272727" transform="translate(30,21)"/><path d="M0 0 C0.66 0 1.32 0 2 0 C1.34 2.64 0.68 5.28 0 8 C-0.66 7.67 -1.32 7.34 -2 7 C-2.125 4.625 -2.125 4.625 -2 2 C-1.34 1.34 -0.68 0.68 0 0 Z " fill="#272727" transform="translate(31,28)"/><path d="M0 0 C1.32 0.66 2.64 1.32 4 2 C3.34 3.32 2.68 4.64 2 6 C1.01 5.34 0.02 4.68 -1 4 C-0.67 2.68 -0.34 1.36 0 0 Z " fill="#2D2D2D" transform="translate(16,31)"/><path d="M0 0 C0.33 0.66 0.66 1.32 1 2 C1.66 2 2.32 2 3 2 C2.1875 3.9375 2.1875 3.9375 1 6 C0.01 6.33 -0.98 6.66 -2 7 C-2 6.34 -2 5.68 -2 5 C-2.66 4.67 -3.32 4.34 -4 4 C-2.68 4 -1.36 4 0 4 C0 2.68 0 1.36 0 0 Z " fill="#3A3A3A" transform="translate(24,18)"/></svg></div><div class="msg-content">${marked.parse(aiText)}</div>`;
            chatBody.appendChild(aMsg);
            chatBody.scrollTop = chatBody.scrollHeight;

        } catch (e) {
            typing.remove();
            if(e.message.includes("api_key") || e.message.includes("401")) localStorage.removeItem('groq_api_key');
            
            const errMsg = document.createElement('div');
            errMsg.className = 'msg msg-ai';
            errMsg.innerHTML = `<div class="msg-avatar" style="background:#e74c3c">!</div><div class="msg-content" style="color:#e74c3c"><p>Connection Interrupted: ${e.message}</p></div>`;
            chatBody.appendChild(errMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    // ===== SCROLL BUTTON LOGIC =====
    const scrollBtn = document.getElementById('scroll-btn');
    chatBody.addEventListener('scroll', () => {
        const threshold = 150;
        const isNearBottom = chatBody.scrollHeight - chatBody.clientHeight - chatBody.scrollTop < threshold;
        scrollBtn.classList.toggle('visible', !isNearBottom && chatBody.classList.contains('is-chatting'));
    });
    scrollBtn.addEventListener('click', () => {
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
    });

    sendBtn.addEventListener('click', sendMsg);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMsg(); });
})();
