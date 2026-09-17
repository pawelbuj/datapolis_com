# -*- coding: utf-8 -*-
"""Szablon <main> strony glownej ver7 — jeden dla wszystkich jezykow.
   H1 i "Apps that run work." zostaja po angielsku (decyzja z 17.09)."""

TPL = """    <main>
        <!-- 1. HERO -->
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
                            {hero_people}<br>
                            <strong>{hero_layer}</strong>
                        </p>

                        <p class="dp-hero__subtitle">{hero_sub}</p>

                        <div class="dp-hero__actions">
                            <a href="#app-creator" class="dp-btn">{hero_cta1}</a>
                            <a href="contact.html" class="dp-btn dp-btn-outline">{hero_cta2}</a>
                        </div>

                        <div class="v7-trust">
                            <span class="v7-trust__item"><span class="v7-trust__num">20+</span> {t_years}</span>
                            <span class="v7-trust__item"><span class="v7-trust__num">500+</span> {t_orgs}</span>
                            <span class="v7-trust__item"><span class="v7-trust__num">40+</span> {t_countries}</span>
                            <span class="v7-trust__names">Airbus · Orlen · thyssenkrupp · PKO Bank Polski · Nestlé · Hexagon</span>
                        </div>
                    </div>

                    <div class="dp-hero__visual">
                        <div class="dp-workflow-map" data-home-workflow-map data-step="0" data-role="human" role="img" aria-label="{map_aria}">
                            <div class="dp-workflow-map__head">
                                <span>
                                    <small>{map_kicker}</small>
                                    <strong>{map_case}</strong>
                                </span>
                                <em><i></i> {map_running}</em>
                            </div>

                            <div class="dp-workflow-map__canvas">
                                <svg class="dp-workflow-map__lines" viewBox="0 0 640 390" preserveAspectRatio="none" aria-hidden="true">
                                    <path data-home-edge-index="0" d="M79 196 C125 196 138 114 188 114"></path>
                                    <path data-home-edge-index="1" d="M252 114 C294 114 288 196 328 196"></path>
                                    <path data-home-edge-index="2" d="M392 196 C433 196 429 106 474 106"></path>
                                    <path class="dp-workflow-map__branch" d="M392 196 C433 196 429 286 474 286"></path>
                                    <path data-home-edge-index="3" d="M506 138 C506 186 506 220 506 254"></path>
                                    <path data-home-edge-index="4" d="M538 286 C574 286 575 196 607 196"></path>
                                </svg>

                                <div class="dp-workflow-state dp-workflow-state--0" data-home-state-index="0" data-role-label="{s0_role}" data-task="{s0_task}">
                                    <span class="dp-workflow-role dp-workflow-role--human"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7.5" r="3.5"></circle><path d="M5.2 20c.6-4.2 2.9-6.3 6.8-6.3s6.2 2.1 6.8 6.3"></path></svg></span>
                                    <strong>{s0_name}</strong><small>{s0_small}</small>
                                </div>
                                <div class="dp-workflow-state dp-workflow-state--1" data-home-state-index="1" data-role-label="{s1_role}" data-task="{s1_task}">
                                    <span class="dp-workflow-role dp-workflow-role--digital"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="6" width="15" height="13" rx="3"></rect><circle cx="9.2" cy="12" r="1"></circle><circle cx="14.8" cy="12" r="1"></circle><path d="M9 16h6M12 3v3M9.5 3h5"></path></svg></span>
                                    <strong>{s1_name}</strong><small>{s1_small}</small>
                                </div>
                                <div class="dp-workflow-state dp-workflow-state--2" data-home-state-index="2" data-role-label="{s2_role}" data-task="{s2_task}">
                                    <span class="dp-workflow-role dp-workflow-role--human"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7.5" r="3.5"></circle><path d="M5.2 20c.6-4.2 2.9-6.3 6.8-6.3s6.2 2.1 6.8 6.3"></path></svg></span>
                                    <strong>{s2_name}</strong><small>{s2_small}</small>
                                </div>
                                <div class="dp-workflow-state dp-workflow-state--3" data-home-state-index="3" data-role-label="{s3_role}" data-task="{s3_task}">
                                    <span class="dp-workflow-role dp-workflow-role--digital"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="6" width="15" height="13" rx="3"></rect><circle cx="9.2" cy="12" r="1"></circle><circle cx="14.8" cy="12" r="1"></circle><path d="M9 16h6M12 3v3M9.5 3h5"></path></svg></span>
                                    <strong>{s3_name}</strong><small>{s3_small}</small>
                                </div>
                                <div class="dp-workflow-state dp-workflow-state--4" data-home-state-index="4" data-role-label="{s4_role}" data-task="{s4_task}">
                                    <span class="dp-workflow-role dp-workflow-role--human"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7.5" r="3.5"></circle><path d="M5.2 20c.6-4.2 2.9-6.3 6.8-6.3s6.2 2.1 6.8 6.3"></path></svg></span>
                                    <strong>{s4_name}</strong><small>{s4_small}</small>
                                </div>
                                <div class="dp-workflow-state dp-workflow-state--5" data-home-state-index="5" data-role-label="{s5_role}" data-task="{s5_task}">
                                    <span class="dp-workflow-role dp-workflow-role--digital"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="6" width="15" height="13" rx="3"></rect><circle cx="9.2" cy="12" r="1"></circle><circle cx="14.8" cy="12" r="1"></circle><path d="M9 16h6M12 3v3M9.5 3h5"></path></svg></span>
                                    <strong>{s5_name}</strong><small>{s5_small}</small>
                                </div>

                                <span class="dp-workflow-map__route-label">{route_missing}</span>
                                <span class="dp-workflow-map__route-label dp-workflow-map__route-label--fast">{route_fast}</span>
                                <span class="dp-workflow-map__token" aria-hidden="true"><i></i></span>
                            </div>

                            <div class="dp-workflow-map__current">
                                <span>{cur_label}</span>
                                <strong data-home-current-state>{cur_state}</strong>
                                <i></i>
                                <small data-home-current-role>{s0_role}</small>
                                <b data-home-current-task>{s0_task}</b>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 2. PROBLEM -->
        <section class="v7-band">
            <div class="v7-container">
                <div class="v7-band__head">
                    <p class="v7-eyebrow">{band_eyebrow}</p>
                    <h2 class="v7-band__title">{band_title}</h2>
                </div>

                <div class="v7-band__list">
                    <p class="v7-band__item"><strong>{p1_t}</strong>{p1_d}</p>
                    <p class="v7-band__item"><strong>{p2_t}</strong>{p2_d}</p>
                    <p class="v7-band__item"><strong>{p3_t}</strong>{p3_d}</p>
                    <p class="v7-band__item"><strong>{p4_t}</strong>{p4_d}</p>
                </div>

                <p class="v7-band__thesis">
                    {thesis_a}
                    <strong>{thesis_b1}<span class="accent">{thesis_layer}</span>{thesis_b2}</strong>
                </p>
            </div>
        </section>

        <!-- 3. EKSPONAT: specyfikacja <-> aplikacja -->
        <section class="v7-exhibit" id="app-creator" aria-labelledby="app-creator-title" data-spec-app-exhibit>
            <div class="v7-container">
                <div class="v7-exhibit__head">
                    <p class="v7-eyebrow">2to2 App Creator</p>
                    <h2 class="v7-exhibit__title" id="app-creator-title">
                        {ex_title}
                        <em>{ex_title_em}</em>
                    </h2>
                    <p class="v7-exhibit__lead">{ex_lead}</p>
                </div>

                <div class="v7-stage__bar">
                    <span class="v7-sync">
                        <span class="v7-sync__dot"></span>
                        <span data-sync-text data-sync-idle="{sync_ok}" data-sync-drifted="{sync_bad}">{sync_ok}</span>
                    </span>

                    <button class="v7-toggle" type="button"
                            data-exhibit-toggle
                            data-label-idle="{tg_idle}"
                            data-label-drifted="{tg_drifted}"
                            data-label-synced="{tg_synced}">
                        <span class="v7-toggle__icon" aria-hidden="true">↻</span>
                        <span data-toggle-label>{tg_idle}</span>
                    </button>

                    <p class="v7-hint" data-exhibit-hint
                       data-hint-idle="{hint_idle}"
                       data-hint-drifted="{hint_drifted}"
                       data-hint-synced="{hint_synced}">{hint_idle}</p>
                </div>

                <div class="v7-stage">
                    <div class="v7-pane">
                        <div class="v7-pane__head">
                            <span class="v7-pane__label">{pane_spec}</span>
                            <span class="v7-pane__meta">{pane_spec_meta}</span>
                        </div>
                        <div class="v7-pane__body">
                            <p class="v7-spec__doc">{doc_title}</p>
                            <ul class="v7-spec__list">
                                <li><button type="button" class="v7-spec__line" data-link="intake">{sent1}</button></li>
                                <li><button type="button" class="v7-spec__line" data-link="flow">{sent2}</button></li>
                                <li><button type="button" class="v7-spec__line" data-link="audit">{sent3}</button></li>
                                <li><button type="button" class="v7-spec__line" data-link="wire">{sent4}</button></li>
                                <li><button type="button" class="v7-spec__line v7-spec__line--added" data-link="flow">{sent5}</button></li>
                            </ul>
                            <p class="v7-spec__foot">{spec_foot}</p>
                        </div>
                    </div>

                    <div class="v7-stage__divider" aria-hidden="true"></div>

                    <div class="v7-pane">
                        <div class="v7-pane__head">
                            <span class="v7-pane__label">{pane_app}</span>
                            <span class="v7-pane__meta">{pane_app_meta}</span>
                        </div>
                        <div class="v7-pane__body">
                            <div class="v7-app__topbar">
                                <span class="v7-app__name">{doc_title}</span>
                                <span class="v7-app__role">{role_name}</span>
                            </div>

                            <div class="v7-part" data-link="flow" tabindex="0">
                                <div class="v7-part__head">
                                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">
                                        <circle cx="2.6" cy="6" r="1.8"/><path d="M4.6 6h2.8"/><circle cx="9.2" cy="6" r="1.8"/>
                                    </svg>
                                    {part_flow}
                                </div>
                                <div class="v7-flow">
                                    <span class="v7-state">{st_draft}</span>
                                    <span class="v7-arrow" aria-hidden="true">→</span>
                                    <span class="v7-state v7-state--active">{st_review}</span>
                                    <span class="v7-arrow v7-arrow--added" aria-hidden="true">→</span>
                                    <span class="v7-state v7-state--added">{st_approval}</span>
                                    <span class="v7-arrow" aria-hidden="true">→</span>
                                    <span class="v7-state">{st_active}</span>
                                </div>
                            </div>

                            <div class="v7-part" data-link="intake" tabindex="0">
                                <div class="v7-part__head">
                                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">
                                        <rect x="1.2" y="1.6" width="9.6" height="8.8" rx="1.6"/><path d="M1.2 4.4h9.6M4.2 4.4v6"/>
                                    </svg>
                                    {part_pages}
                                </div>
                                <div class="v7-form">
                                    <div class="v7-field v7-field--wide">
                                        <span class="v7-field__label">{f_company}</span>
                                        <span class="v7-field__value">{company_name}</span>
                                    </div>
                                    <div class="v7-field">
                                        <span class="v7-field__label">{f_contact}</span>
                                        <span class="v7-field__value">{contact_name}</span>
                                    </div>
                                    <div class="v7-field">
                                        <span class="v7-field__label">{f_risk}</span>
                                        <span class="v7-field__value v7-field__value--pick">
                                            <span class="v7-pill">{risk_value}</span>
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div class="v7-part" data-link="audit" tabindex="0">
                                <div class="v7-part__head">
                                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">
                                        <circle cx="6" cy="6" r="4.6"/><path d="M6 3.4V6l1.8 1.1"/>
                                    </svg>
                                    {part_audit}
                                </div>
                                <div class="v7-audit">
                                    <div class="v7-audit__row">
                                        <span class="v7-audit__mark" aria-hidden="true">✓</span>
                                        <span class="v7-audit__who">{audit1}</span>
                                        <span class="v7-audit__time">{audit1_time}</span>
                                    </div>
                                    <div class="v7-audit__row">
                                        <span class="v7-audit__mark" aria-hidden="true">✓</span>
                                        <span class="v7-audit__who">{audit2}</span>
                                        <span class="v7-audit__time">{audit2_time}</span>
                                    </div>
                                </div>
                            </div>

                            <div class="v7-part" data-link="wire" tabindex="0">
                                <div class="v7-part__head">
                                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">
                                        <path d="M7.4 1.8 9.9 4.3 6.6 7.6 4.1 5.1z"/><path d="M4.1 5.1 1.8 7.4l2.5 2.5 2.3-2.3"/>
                                    </svg>
                                    {part_wire}
                                </div>
                                <div class="v7-wire">
                                    <span class="v7-wire__target">{wire_record}</span>
                                    <span class="v7-wire__dash" aria-hidden="true"></span>
                                    <span class="v7-wire__target">ERP</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="v7-exhibit__foot">
                    <p class="v7-claim">
                        {claim_a}
                        <strong>{claim_b1}<span class="accent">{claim_years}</span>{claim_b2}</strong>
                        {claim_c}
                    </p>
                    <div class="v7-exhibit__actions">
                        <a class="v7-btn v7-btn--primary" href="{ac_href}">{ac_label} <span aria-hidden="true">→</span></a>
                        <a class="v7-btn v7-btn--ghost" href="contact.html">{show_docs}</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- 4. PLATFORMA -->
        <section class="dp-section dp-section--platform">
            <div class="dp-container">
                <div class="dp-section__header">
                    <span class="dp-label">{pf_label}</span>
                </div>

                <h2 class="dp-platform__headline">
                    <span class="dp-platform__logo">2to2</span> {pf_headline}
                </h2>

                <p class="dp-platform__support">{pf_support}</p>

                <div class="dp-features">
                    <div class="dp-feature">
                        <div class="dp-feature__icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 12h6M9 15h4"/>
                            </svg>
                        </div>
                        <h3 class="dp-feature__title">{pf1_t}</h3>
                        <p class="dp-feature__desc">{pf1_d}</p>
                    </div>

                    <div class="dp-feature">
                        <div class="dp-feature__icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M16 18L22 12L16 6"/><path d="M8 6L2 12L8 18"/><rect x="9" y="9" width="6" height="6" rx="1"/>
                            </svg>
                        </div>
                        <h3 class="dp-feature__title">{pf2_t}</h3>
                        <p class="dp-feature__desc">{pf2_d}</p>
                    </div>

                    <div class="dp-feature">
                        <div class="dp-feature__icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>
                            </svg>
                        </div>
                        <h3 class="dp-feature__title">{pf3_t}</h3>
                        <p class="dp-feature__desc">{pf3_d}</p>
                    </div>
                </div>

                <p class="dp-platform__tagline">Apps that run work.</p>

                <div class="dp-platform__cta">
                    <a href="platform-2to2.html" class="dp-btn dp-btn--large">{pf_cta1} →</a>
                    <a href="https://2to2.ai" target="_blank" rel="noopener" class="dp-link">{pf_cta2}</a>
                </div>
            </div>
        </section>

        <!-- 5. AI WEWNATRZ PROCESOW -->
        <section class="dp-section dp-section--manifesto">
            <div class="dp-container">
                <div class="dp-section__header">
                    <span class="dp-label">{mf_label}</span>
                </div>

                <h2 class="dp-manifesto__headline">
                    <span class="dp-manifesto__line1">{mf_line1}</span>
                    <span class="dp-manifesto__line2">{mf_line2}</span>
                </h2>

                <p class="dp-manifesto__subheadline">{mf_sub}</p>

                <div class="dp-orchestration">
                    <div class="dp-orchestration__node">
                        <div class="dp-orchestration__card">
                            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="8" r="4"/><path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2"/>
                            </svg>
                        </div>
                        <span class="dp-orchestration__label">{n_human}</span>
                    </div>

                    <div class="dp-orchestration__connector">
                        <svg width="60" height="2" viewBox="0 0 60 2"><line x1="0" y1="1" x2="60" y2="1" stroke="#334155" stroke-width="2" stroke-dasharray="6 4"/></svg>
                    </div>

                    <div class="dp-orchestration__node dp-orchestration__node--center">
                        <div class="dp-orchestration__card dp-orchestration__card--process">
                            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="6" cy="12" r="3"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="12" r="3"/>
                                <line x1="9" y1="12" x2="8" y2="12"/><line x1="16" y1="12" x2="15" y2="12"/>
                            </svg>
                        </div>
                        <span class="dp-orchestration__label dp-orchestration__label--process">{n_process}</span>
                    </div>

                    <div class="dp-orchestration__connector">
                        <svg width="60" height="2" viewBox="0 0 60 2"><line x1="0" y1="1" x2="60" y2="1" stroke="#334155" stroke-width="2" stroke-dasharray="6 4"/></svg>
                    </div>

                    <div class="dp-orchestration__node">
                        <div class="dp-orchestration__card">
                            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
                                <line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/>
                                <line x1="6" y1="12" x2="2" y2="12"/><line x1="22" y1="12" x2="18" y2="12"/>
                            </svg>
                        </div>
                        <span class="dp-orchestration__label">Digital Worker</span>
                    </div>
                </div>

                <p class="dp-orchestration__caption">{mf_caption}</p>

                <div class="dp-outcomes">
                    <div class="dp-outcome">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                        <span>{oc1}</span>
                    </div>
                    <div class="dp-outcome">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9M16.5 3.5a2.12 2.12 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                        <span>{oc2}</span>
                    </div>
                    <div class="dp-outcome">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        <span>{oc3}</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- 6. DOWOD -->
        <section class="v7-proof">
            <div class="v7-container">
                <div class="v7-proof__head">
                    <p class="v7-eyebrow">{pr_eyebrow}</p>
                    <h2 class="v7-proof__title">{pr_title1}<span class="accent">{pr_title_years}</span>{pr_title2}</h2>
                </div>

                <div class="v7-figures">
                    <div class="v7-figure"><span class="v7-figure__num">20+</span><span class="v7-figure__label">{fg1}</span></div>
                    <div class="v7-figure"><span class="v7-figure__num">500+</span><span class="v7-figure__label">{fg2}</span></div>
                    <div class="v7-figure"><span class="v7-figure__num">40+</span><span class="v7-figure__label">{fg3}</span></div>
                    <div class="v7-figure"><span class="v7-figure__num">{fg4_num}</span><span class="v7-figure__label">{fg4}</span></div>
                </div>

                <div class="v7-logos">
                    <img class="v7-logo--airbus" src="../storage/files/klienci/logo-airbus.png" alt="Airbus" loading="lazy">
                    <img class="v7-logo--orlen" src="../logos/orlen.png" alt="Orlen" loading="lazy">
                    <img class="v7-logo--thyssen" src="../storage/files/klienci/logo-thyssenkrupp.png" alt="thyssenkrupp" loading="lazy">
                    <img class="v7-logo--nestle" src="../logos/NESN.SW_BIG.svg" alt="Nestlé" loading="lazy">
                    <img class="v7-logo--pko" src="../logos/PKO.WA_BIG.svg" alt="PKO Bank Polski" loading="lazy">
                    <img class="v7-logo--hexagon" src="../logos/hexagon.png" alt="Hexagon" loading="lazy">
                </div>

                <div class="v7-deployments">
                    <div class="v7-deployment">
                        <h3 class="v7-deployment__title">
                            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>
                            </svg>
                            Microsoft 365
                        </h3>
                        <p class="v7-deployment__desc">{dep1}</p>
                    </div>
                    <div class="v7-deployment">
                        <h3 class="v7-deployment__title">
                            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M12 8v4M12 16h.01"/>
                            </svg>
                            {dep2_t}
                        </h3>
                        <p class="v7-deployment__desc">{dep2}</p>
                    </div>
                </div>

                <p class="v7-proof__contrast">
                    {contrast_a}
                    <strong>{contrast_b}</strong>
                </p>
            </div>
        </section>

        <!-- 7. PRZYPADKI UZYCIA -->
        <section class="dp-section dp-section--usecases">
            <div class="dp-container">
                <div class="dp-section__header">
                    <span class="dp-label">{uc_label}</span>
                    <h2 class="dp-title">{uc_title}</h2>
                </div>

                <div class="dp-usecases">
                    <div class="dp-usecase">
                        <span class="dp-usecase__title">{uc1_t}</span>
                        <p class="dp-usecase__desc">{uc1_d}</p>
                        <span class="dp-usecase__badge">{uc_badge}</span>
                    </div>
                    <div class="dp-usecase">
                        <span class="dp-usecase__title">{uc2_t}</span>
                        <p class="dp-usecase__desc">{uc2_d}</p>
                        <span class="dp-usecase__badge">{uc_badge}</span>
                    </div>
                    <div class="dp-usecase">
                        <span class="dp-usecase__title">{uc3_t}</span>
                        <p class="dp-usecase__desc">{uc3_d}</p>
                        <span class="dp-usecase__badge">{uc_badge}</span>
                    </div>
                    <div class="dp-usecase">
                        <span class="dp-usecase__title">{uc4_t}</span>
                        <p class="dp-usecase__desc">{uc4_d}</p>
                        <span class="dp-usecase__badge">{uc_badge}</span>
                    </div>
                    <div class="dp-usecase">
                        <span class="dp-usecase__title">{uc5_t}</span>
                        <p class="dp-usecase__desc">{uc5_d}</p>
                        <span class="dp-usecase__badge">{uc_badge}</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- 8. FINALNE CTA -->
        <section class="v7-final" id="start">
            <div class="v7-container">
                <div class="v7-final__layout">
                    <div>
                        <p class="v7-eyebrow">{fin_eyebrow}</p>
                        <h2 class="v7-final__title">{fin_title1}<span class="accent">{fin_title_accent}</span>{fin_title2}</h2>
                        <p class="v7-final__lead">{fin_lead}</p>
                        <ul class="v7-final__list">
                            <li><span aria-hidden="true">✓</span> {fin_l1}</li>
                            <li><span aria-hidden="true">✓</span> {fin_l2}</li>
                            <li><span aria-hidden="true">✓</span> {fin_l3}</li>
                        </ul>
                        <p class="v7-final__mail">{fin_mail} <a href="mailto:office@datapolis.com">office@datapolis.com</a></p>
                    </div>

                    <div class="v7-formcard">
                        <p class="v7-formcard__title">{fc_title}</p>
                        <p class="v7-formcard__helper">{fc_helper}</p>

                        <!-- Workflow Form Embed -->
                        <div id="workflow-form-www-contacts-home"></div>
                        <script src="https://2to2.ai/embed-workflow.js"
                          data-workflow="www-contacts"
                          data-container="workflow-form-www-contacts-home"
                          data-base-url="https://2to2.ai">
                        </script>

                        <p class="v7-formcard__note">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>
                            </svg>
                            {fc_note}
                        </p>
                    </div>
                </div>
            </div>
        </section>
    </main>"""
