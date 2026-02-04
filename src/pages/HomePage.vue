<template>
  <div class="home-page">
    <!-- ========================================
                 1. HERO
                 ======================================== -->
            <section class="dp-hero">
                <div class="dp-hero__grid"></div>
                <div class="dp-hero__glow"></div>
                
                <div class="dp-container">
                    <div class="dp-hero__content">
                        <div>
                            <h1 class="dp-hero__title">
                                <span>We run the work</span>
                                <span class="accent">of modern companies.</span>
                            </h1>
                            
                            <p class="dp-hero__tagline">
                                People.  AI.<br>
                                <strong>One governed process layer.</strong>
                            </p>
                            
                            <p class="dp-hero__subtitle">
                                We design and run the process layer where people and AI get real work done.
                            </p>
                            
                            <div class="dp-hero__actions">
                                <a href="https://2to2.ai" target="_blank" class="dp-btn">
                                    See the platform
                                </a>
                                <router-link to="/contact" class="dp-btn dp-btn-outline">
                                    Talk to an expert
                                </router-link>
                            </div>
                        </div>
                        
                        <div class="dp-hero__visual">
                            <svg viewBox="0 0 400 340" fill="none" xmlns="http://www.w3.org/2000/svg" class="process-diagram">
                                <defs>
                                    <linearGradient id="processGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="#14b8a6"/>
                                        <stop offset="100%" stop-color="#0d9488"/>
                                    </linearGradient>
                                    <filter id="processGlow" x="-50%" y="-50%" width="200%" height="200%">
                                        <feGaussianBlur stdDeviation="12" result="coloredBlur"/>
                                        <feMerge>
                                            <feMergeNode in="coloredBlur"/>
                                            <feMergeNode in="SourceGraphic"/>
                                        </feMerge>
                                    </filter>
                                </defs>
                                
                                <!-- Connection lines from Process to Workers -->
                                <path d="M200 165 L100 95" stroke="#475569" stroke-width="2" stroke-dasharray="8 5">
                                    <animate attributeName="stroke-dashoffset" from="13" to="0" dur="1.2s" repeatCount="indefinite"/>
                                </path>
                                <path d="M200 165 L300 95" stroke="#475569" stroke-width="2" stroke-dasharray="8 5">
                                    <animate attributeName="stroke-dashoffset" from="13" to="0" dur="1.2s" repeatCount="indefinite"/>
                                </path>
                                
                                <!-- Human node (left) -->
                                <g transform="translate(55, 20)">
                                    <rect width="90" height="90" rx="16" fill="#0f172a" stroke="#334155" stroke-width="2"/>
                                    <circle cx="45" cy="35" r="14" stroke="#94a3b8" stroke-width="2" fill="none"/>
                                    <path d="M24 72 Q45 55 66 72" stroke="#94a3b8" stroke-width="2" fill="none"/>
                                    <text x="45" y="118" text-anchor="middle" fill="#94a3b8" font-size="13" font-weight="500" font-family="system-ui, sans-serif">Human</text>
                                </g>
                                
                                <!-- Digital Worker node (right) - visually equal to Human -->
                                <g transform="translate(255, 20)">
                                    <rect width="90" height="90" rx="16" fill="#0f172a" stroke="#334155" stroke-width="2"/>
                                    <!-- Neutral circuit/node icon -->
                                    <circle cx="45" cy="45" r="18" stroke="#94a3b8" stroke-width="2" fill="none"/>
                                    <circle cx="45" cy="45" r="7" fill="#94a3b8"/>
                                    <path d="M45 27 V19 M45 63 V71 M27 45 H19 M63 45 H71" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
                                    <text x="45" y="118" text-anchor="middle" fill="#94a3b8" font-size="13" font-weight="500" font-family="system-ui, sans-serif">Digital Worker</text>
                                </g>
                                
                                <!-- PROCESS node (center, bottom) - The Control Plane / Main Authority -->
                                <g transform="translate(80, 175)" filter="url(#processGlow)">
                                    <rect width="240" height="100" rx="20" fill="url(#processGrad)"/>
                                    <!-- Orchestration symbol: flow with central hub -->
                                    <circle cx="70" cy="50" r="10" fill="white" opacity="0.85"/>
                                    <circle cx="120" cy="50" r="14" fill="white"/>
                                    <circle cx="170" cy="50" r="10" fill="white" opacity="0.85"/>
                                    <path d="M80 50 H106 M134 50 H160" stroke="rgba(2,6,23,0.35)" stroke-width="3" stroke-linecap="round"/>
                                    <text x="120" y="130" text-anchor="middle" fill="#f8fafc" font-size="16" font-weight="600" font-family="system-ui, sans-serif">Process</text>
                                </g>
                                
                                <!-- Subtle caption -->
                                <text x="200" y="328" text-anchor="middle" fill="#475569" font-size="11" font-family="system-ui, sans-serif">Connected to enterprise systems. Producing real business outcomes.</text>
                            </svg>
                        </div>
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 2. PROBLEM - Why work is broken
                 ======================================== -->
            <section class="dp-section dp-section--dark dp-section--problem">
                <div class="dp-container">
                    <div class="dp-section__header">
                        <span class="dp-label">The reality</span>
                        <h2 class="dp-title">Why work is broken</h2>
                    </div>
                    
                    <div class="dp-problems">
                        <div class="dp-problem">
                            <div class="dp-problem__icon">
                                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="3" width="7" height="9" rx="1"/>
                                    <rect x="14" y="3" width="7" height="5" rx="1"/>
                                    <rect x="14" y="12" width="7" height="9" rx="1"/>
                                    <rect x="3" y="16" width="7" height="5" rx="1"/>
                                    <path d="M10 7h4M10 17h4" stroke-dasharray="2 2"/>
                                </svg>
                            </div>
                            <p class="dp-problem__text">Critical processes are scattered across emails, spreadsheets, and people's heads.</p>
                        </div>
                        
                        <div class="dp-problem">
                            <div class="dp-problem__icon">
                                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="6" cy="12" r="3"/>
                                    <circle cx="18" cy="12" r="3"/>
                                    <path d="M9 12h2" stroke-dasharray="2 2"/>
                                    <path d="M13 12h2" stroke-dasharray="2 2"/>
                                    <path d="M11 10l2 4M13 10l-2 4" stroke-width="1.5"/>
                                </svg>
                            </div>
                            <p class="dp-problem__text">Automation tools don't connect. Work breaks between systems and teams.</p>
                        </div>
                        
                        <div class="dp-problem">
                            <div class="dp-problem__icon">
                                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                    <path d="M12 8v4M12 16h.01"/>
                                </svg>
                            </div>
                            <p class="dp-problem__text">AI copilots have no governance: no audit trail, no accountability.</p>
                        </div>
                        
                        <div class="dp-problem">
                            <div class="dp-problem__icon">
                                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="7" width="18" height="14" rx="2"/>
                                    <path d="M7 7V5a2 2 0 012-2h6a2 2 0 012 2v2"/>
                                    <path d="M8 12h8M8 16h5"/>
                                    <circle cx="18" cy="18" r="4" fill="#0f172a" stroke="currentColor"/>
                                    <path d="M18 16v2h2"/>
                                </svg>
                            </div>
                            <p class="dp-problem__text">Enterprises can't let AI act freely—security, compliance, and risk demand control.</p>
                        </div>
                    </div>
                    
                    <div class="dp-thesis">
                        <p class="dp-thesis__line">AI won’t fix broken work.</p>
                        <p class="dp-thesis__line dp-thesis__line--accent">Work needs a <span class="accent">governed process layer</span>.</p>
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 3. CREDIBILITY - 20+ years
                 ======================================== -->
            <section class="dp-section dp-section--credibility">
                <div class="dp-container">
                    <div class="dp-credibility">
                        <h2 class="dp-credibility__title">
                            We've spent <span class="accent">20+ years</span> running mission-critical business processes.
                        </h2>
                        
                        <div class="dp-stats">
                            <div class="dp-stat">
                                <div class="dp-stat__icon">
                                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M3 3h18v18H3z"/>
                                        <path d="M3 9h18M9 3v18"/>
                                    </svg>
                                </div>
                                <span class="dp-stat__number">Thousands</span>
                                <span class="dp-stat__label">Business-critical workflows running in production</span>
                            </div>
                            <div class="dp-stat">
                                <div class="dp-stat__icon">
                                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M3 7l6-4 6 4 6-4v14l-6 4-6-4-6 4V7z"/>
                                        <path d="M9 3v14M15 7v14"/>
                                    </svg>
                                </div>
                                <span class="dp-stat__number">Banks, Energy, Industry, Government</span>
                                <span class="dp-stat__label">The most regulated environments in the world</span>
                            </div>
                            <div class="dp-stat">
                                <div class="dp-stat__icon">
                                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                        <path d="M9 12l2 2 4-4"/>
                                    </svg>
                                </div>
                                <span class="dp-stat__number">Zero-downtime operations</span>
                                <span class="dp-stat__label">Audited. Controlled. Always on.</span>
                            </div>
                        </div>
                        
                        <p class="dp-contrast">
                            AI startups promise the future. 
                            
                        </p>
                        <p class="dp-contrast">
                           
                            <strong>We run the systems companies depend on today.</strong>
                        </p>
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 4. THE NEW ERA - AI Inside Processes (CLIMAX)
                 ======================================== -->
            <section class="dp-section dp-section--manifesto">
                <div class="dp-container">
                    <!-- A) Label pill -->
                    <div class="dp-section__header">
                        <span class="dp-label">The new era</span>
                    </div>
                    
                    <!-- B) Big manifesto headline -->
                    <h2 class="dp-manifesto__headline">
                        <span class="dp-manifesto__line1">AI should not replace processes.</span>
                        <span class="dp-manifesto__line2">It should work inside them.</span>
                    </h2>
                    
                    <!-- C) Subheadline -->
                    <p class="dp-manifesto__subheadline">
                        Digital workers act. Processes govern. Businesses stay in control.
                    </p>
                    
                    <!-- D) Core visual: Orchestration diagram -->
                    <div class="dp-orchestration">
                        <!-- Human node (left) -->
                        <div class="dp-orchestration__node">
                            <div class="dp-orchestration__card">
                                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="12" cy="8" r="4"/>
                                    <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2"/>
                                </svg>
                            </div>
                            <span class="dp-orchestration__label">Human</span>
                        </div>
                        
                        <!-- Connector line -->
                        <div class="dp-orchestration__connector">
                            <svg width="60" height="2" viewBox="0 0 60 2">
                                <line x1="0" y1="1" x2="60" y2="1" stroke="#334155" stroke-width="2" stroke-dasharray="6 4"/>
                            </svg>
                        </div>
                        
                        <!-- Process node (center) - Control Plane -->
                        <div class="dp-orchestration__node dp-orchestration__node--center">
                            <div class="dp-orchestration__card dp-orchestration__card--process">
                                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="6" cy="12" r="3"/>
                                    <circle cx="12" cy="12" r="4"/>
                                    <circle cx="18" cy="12" r="3"/>
                                    <line x1="9" y1="12" x2="8" y2="12"/>
                                    <line x1="16" y1="12" x2="15" y2="12"/>
                                </svg>
                            </div>
                            <span class="dp-orchestration__label dp-orchestration__label--process">Process</span>
                        </div>
                        
                        <!-- Connector line -->
                        <div class="dp-orchestration__connector">
                            <svg width="60" height="2" viewBox="0 0 60 2">
                                <line x1="0" y1="1" x2="60" y2="1" stroke="#334155" stroke-width="2" stroke-dasharray="6 4"/>
                            </svg>
                        </div>
                        
                        <!-- Digital Worker node (right) -->
                        <div class="dp-orchestration__node">
                            <div class="dp-orchestration__card">
                                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="12" cy="12" r="6"/>
                                    <circle cx="12" cy="12" r="2"/>
                                    <line x1="12" y1="6" x2="12" y2="2"/>
                                    <line x1="12" y1="22" x2="12" y2="18"/>
                                    <line x1="6" y1="12" x2="2" y2="12"/>
                                    <line x1="22" y1="12" x2="18" y2="12"/>
                                </svg>
                            </div>
                            <span class="dp-orchestration__label">Digital Worker</span>
                        </div>
                    </div>
                    
                    <!-- Small label under diagram -->
                    <p class="dp-orchestration__caption">Governed. Audited. Approved.</p>
                    
                    <!-- E) Outcome statements (not features) -->
                    <div class="dp-outcomes">
                        <div class="dp-outcome">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M5 12h14M12 5l7 7-7 7"/>
                            </svg>
                            <span>Work moves automatically — with approvals when needed.</span>
                        </div>
                        <div class="dp-outcome">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 20h9M16.5 3.5a2.12 2.12 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
                            </svg>
                            <span>Every action is logged and traceable.</span>
                        </div>
                        <div class="dp-outcome">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            </svg>
                            <span>AI operates inside your policies and permissions.</span>
                        </div>
                    </div>
                    
                    <!-- F) Final thesis line -->
                    <p class="dp-manifesto__thesis">
                        One governed process layer — for humans and digital workers.
                    </p>
                </div>
            </section>
    
            <!-- ========================================
                 5. PLATFORM: 2to2
                 ======================================== -->
            <section class="dp-section dp-section--platform">
                <div class="dp-container">
                    <div class="dp-section__header">
                        <span class="dp-label">The platform</span>
                    </div>
                    
                    <!-- 1) Section headline - decisive positioning -->
                    <h2 class="dp-platform__headline">
                        <span class="dp-platform__logo">2to2</span> is the operating layer for creating, running, and controlling business processes.
                    </h2>
                    
                    <!-- 2) Supporting sentence -->
                    <p class="dp-platform__support">
                        Build apps that run work. Embed them anywhere. Govern every action.
                    </p>
                    
                    <!-- 3) Three cards - outcomes + differentiation -->
                    <div class="dp-features">
                        <div class="dp-feature">
                            <div class="dp-feature__icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                                    <path d="M9 9h6M9 12h6M9 15h4"/>
                                </svg>
                            </div>
                            <h3 class="dp-feature__title">Build process apps</h3>
                            <p class="dp-feature__desc">Design and deploy apps that orchestrate real work — across teams, tools, and AI.</p>
                        </div>
                        
                        <div class="dp-feature">
                            <div class="dp-feature__icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M16 18L22 12L16 6"/>
                                    <path d="M8 6L2 12L8 18"/>
                                    <rect x="9" y="9" width="6" height="6" rx="1"/>
                                </svg>
                            </div>
                            <h3 class="dp-feature__title">Embed anywhere</h3>
                            <p class="dp-feature__desc">Drop process apps into portals, intranets, Teams, or your own products — without rewrites.</p>
                        </div>
                        
                        <div class="dp-feature">
                            <div class="dp-feature__icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                    <path d="M9 12l2 2 4-4"/>
                                </svg>
                            </div>
                            <h3 class="dp-feature__title">Run with control</h3>
                            <p class="dp-feature__desc">Humans and digital workers execute steps inside one governed layer — logged, approved, auditable.</p>
                        </div>
                    </div>
                    
                    <!-- 4) Tagline + CTA -->
                    <p class="dp-platform__tagline">Apps that run work.</p>
                    
                    <div class="dp-platform__cta">
                        <a href="https://2to2.ai" target="_blank" class="dp-btn dp-btn--large">
                            Explore 2to2 →
                        </a>
                        <a href="https://2to2.ai/how-it-works" target="_blank" class="dp-link">
                            See how it works
                        </a>
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 6. ENTERPRISE PROOF - Where Datapolis Runs Today
                 ======================================== -->
            <section class="dp-section dp-section--proof">
                <div class="dp-container">
                    <div class="dp-section__header">
                        <span class="dp-label">Enterprise-grade by design</span>
                        <h2 class="dp-proof__title">Where our process DNA runs in production today</h2>
                        <p class="dp-proof__context">The same governed process layer — deployed in different environments.</p>
                    </div>
                    
                    <div class="dp-deployments">
                        <!-- Microsoft 365 deployment -->
                        <div class="dp-deployment">
                            <div class="dp-deployment__icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                                    <path d="M3 9h18M9 21V9"/>
                                </svg>
                            </div>
                            <h3 class="dp-deployment__title">Microsoft 365 enterprises</h3>
                            <p class="dp-deployment__desc">Datapolis processes running  inside SharePoint and Microsoft 365 — powering real teams at scale.</p>
                        </div>
                        
                        <!-- Regulated on-premise deployment -->
                        <div class="dp-deployment">
                            <div class="dp-deployment__icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                    <path d="M12 8v4M12 16h.01"/>
                                </svg>
                            </div>
                            <h3 class="dp-deployment__title">Regulated SharePoint on-premise environments</h3>
                            <p class="dp-deployment__desc">Datapolis Process System deployed inside the most regulated industries — energy, government, critical infrastructure.</p>
                        </div>
                    </div>
                    
                    <p class="dp-dna">The same process DNA. Different deployments.</p>
                </div>
            </section>
    
            <!-- ========================================
                 7. USE CASES - What Actually Runs Here
                 ======================================== -->
            <section class="dp-section dp-section--usecases">
                <div class="dp-container">
                    <div class="dp-section__header">
                        <span class="dp-label">Use cases</span>
                        <h2 class="dp-title">What runs on Datapolis</h2>
                    </div>
                    
                    <div class="dp-usecases">
                        <div class="dp-usecase">
                            <span class="dp-usecase__title">Invoice processing</span>
                            <p class="dp-usecase__desc">AI reads and classifies invoices. Processes route approvals and post to ERP.</p>
                            <span class="dp-usecase__badge">Powered by 2to2</span>
                        </div>
                        
                        <div class="dp-usecase">
                            <span class="dp-usecase__title">Customer onboarding</span>
                            <p class="dp-usecase__desc">Digital workers collect data. Processes verify and activate new customers.</p>
                            <span class="dp-usecase__badge">Powered by 2to2</span>
                        </div>
                        
                        <div class="dp-usecase">
                            <span class="dp-usecase__title">IT service desk</span>
                            <p class="dp-usecase__desc">AI triages requests. Processes assign, escalate, and close tickets.</p>
                            <span class="dp-usecase__badge">Powered by 2to2</span>
                        </div>
                        
                        <div class="dp-usecase">
                            <span class="dp-usecase__title">Contract lifecycle</span>
                            <p class="dp-usecase__desc">AI extracts terms. Processes route reviews, approvals, and signatures.</p>
                            <span class="dp-usecase__badge">Powered by 2to2</span>
                        </div>
                        
                        <div class="dp-usecase">
                            <span class="dp-usecase__title">HR processes</span>
                            <p class="dp-usecase__desc">Digital workers handle forms. Processes onboard, change, and offboard employees.</p>
                            <span class="dp-usecase__badge">Powered by 2to2</span>
                        </div>
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 8. CUSTOMERS
                 ======================================== -->
            <section class="dp-section dp-section--dark">
                <div class="dp-container">
                    <p class="dp-customers__statement">They run real companies.</p>
                    
                    <div class="dp-logos">
                        <img src="/storage/files/klienci/logo-airbus.png" alt="Airbus">
                        <img src="/storage/files/klienci/logo-pgnig.png" alt="PGNiG">
                        <img src="/storage/files/klienci/logo-thyssenkrup.png" alt="ThyssenKrupp">
                        <img src="/storage/files/klienci/logo-polskie-radio.png" alt="Polskie Radio">
                        <img src="/storage/files/klienci/logo-nexia.png" alt="Nexia">
                    </div>
                </div>
            </section>
    
            <!-- ========================================
                 9. FINAL CTA - Conversion Moment
                 ======================================== -->
            <section class="dp-section dp-final">
                <div class="dp-final__glow"></div>
                <div class="dp-container">
                    <h2 class="dp-final__title">See how governed work runs on <span class="accent">2to2</span></h2>
                    <p class="dp-final__subtitle">Watch humans and digital workers execute real processes — with approvals, audit trails, and full control.</p>
                    
                    <div class="dp-final__cta">
                        <router-link to="/contact" class="dp-btn dp-btn--primary dp-btn--xl">
                            Book a demo →
                        </router-link>
                        <p class="dp-final__trust">See a real workflow, not a mockup.</p>
                    </div>
                </div>
            </section>
  </div>
</template>
