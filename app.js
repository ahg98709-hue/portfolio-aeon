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
    const GROQ_API_KEY = "YOUR_API_KEY_HERE";

    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBody = document.getElementById('chat-messages');

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
        if (welcome) welcome.style.display = 'none';

        const uMsg = document.createElement('div');
        uMsg.className = 'msg msg-user';
        uMsg.innerHTML = `<div class="msg-avatar">You</div><div class="msg-content"><p>${esc(txt)}</p></div>`;
        chatBody.appendChild(uMsg);
        
        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;
        chatHistory.push({ role: "user", content: txt });

        const typing = document.createElement('div');
        typing.className = 'msg msg-ai typing-msg';
        typing.innerHTML = `<div class="msg-avatar"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/></svg></div><div class="msg-content"><div class="typing"><span></span><span></span><span></span></div></div>`;
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
            aMsg.innerHTML = `<div class="msg-avatar"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/></svg></div><div class="msg-content">${marked.parse(aiText)}</div>`;
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

    sendBtn.addEventListener('click', sendMsg);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMsg(); });
})();
