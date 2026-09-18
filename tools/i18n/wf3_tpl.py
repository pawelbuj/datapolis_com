# -*- coding: utf-8 -*-
"""Szablon strony /sharepoint — hub o wyłączeniu przepływów SharePoint 2010/2013.

Jedno źródło prawdy dla EN/PL/DE/ES. Słowniki: wf3_en.py, wf3_pl.py, wf3_de.py, wf3_es.py.
Budowanie: python3 tools/i18n/wf3_build.py

Zasady, których ten plik pilnuje:
  - "Run work. Speed up the flow." nie jest tłumaczone,
  - daty i cytaty z Microsoftu są identyczne we wszystkich językach,
  - polecenia PowerShell nie są tłumaczone.
"""

TPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index,follow">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:type" content="article">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#020617">

    <!-- SEO: canonical / hreflang / open graph -->
    <link rel="canonical" href="https://datapolis.com/{path}">
    <link rel="alternate" hreflang="en" href="https://datapolis.com/sharepoint">
    <link rel="alternate" hreflang="pl" href="https://datapolis.com/pl/sharepoint">
    <link rel="alternate" hreflang="de" href="https://datapolis.com/de/sharepoint">
    <link rel="alternate" hreflang="es" href="https://datapolis.com/es/sharepoint">
    <link rel="alternate" hreflang="x-default" href="https://datapolis.com/sharepoint">
    <meta property="og:url" content="https://datapolis.com/{path}">
    <meta property="og:locale" content="{og_locale}">
    <meta property="og:image" content="https://datapolis.com/assets/img/og-image-1200x630.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta property="article:modified_time" content="{modified}">
    <!-- /SEO -->

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;family=Instrument+Sans:wght@400;500;600;700&amp;display=swap">

    <link rel="stylesheet" href="{a}assets/css/main.min.css?v=0ca3b828">
    <link rel="stylesheet" href="{a}assets/css/async.min.css?v=31662295" media="print" onload="this.media='all'; this.onload=null;">
    <link rel="stylesheet" href="{a}assets/css/dark-theme.css?v=1d664f9e">
    <link rel="stylesheet" href="{a}assets/css/new-homepage.css?v=8f7d4412">
    <link rel="stylesheet" href="{a}assets/css/home-v7.css?v=52eaffbf">
    <link rel="stylesheet" href="{a}assets/css/sharepoint-wf3.css?v=1a0c55e2">

    <script src="{a}includes/loader.js"></script>
</head>
<body>

    <div id="header-placeholder"></div>

    <main>
        <section class="v7-page-hero" aria-labelledby="wf3-title">
            <div class="v7-container v7-page-hero__layout">
                <div>
                    <p class="v7-eyebrow">{eyebrow}</p>
                    <h1 class="v7-page-hero__title" id="wf3-title">
                        {h1}
                        <em>{h1_em}</em>
                    </h1>
                    <p class="v7-page-hero__lead">{lead}</p>
                    <p class="wf3-updated">{updated_label}</p>

                    <ul class="v7-points">
                        <li><span aria-hidden="true">&#10003;</span> {pt1}</li>
                        <li><span aria-hidden="true">&#10003;</span> {pt2}</li>
                        <li><span aria-hidden="true">&#10003;</span> {pt3}</li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="v7-steps-section" aria-labelledby="wf3-timeline">
            <div class="v7-container">
                <div class="v7-steps-section__head">
                    <p class="v7-eyebrow">{tl_eyebrow}</p>
                    <h2 class="v7-steps-section__title" id="wf3-timeline">{tl_title}</h2>
                </div>

                <div class="v7-steps">
                    <div class="v7-step">
                        <span class="v7-step__num">1</span>
                        <h3 class="v7-step__title">{tl1_t}</h3>
                        <p class="v7-step__desc">{tl1_d}</p>
                    </div>
                    <div class="v7-step">
                        <span class="v7-step__num">2</span>
                        <h3 class="v7-step__title">{tl2_t}</h3>
                        <p class="v7-step__desc">{tl2_d}</p>
                    </div>
                    <div class="v7-step">
                        <span class="v7-step__num">3</span>
                        <h3 class="v7-step__title">{tl3_t}</h3>
                        <p class="v7-step__desc">{tl3_d}</p>
                    </div>
                    <div class="v7-step">
                        <span class="v7-step__num">4</span>
                        <h3 class="v7-step__title">{tl4_t}</h3>
                        <p class="v7-step__desc">{tl4_d}</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="v7-band" aria-labelledby="wf3-status">
            <div class="v7-container">
                <div class="v7-band__head">
                    <p class="v7-eyebrow">{st_eyebrow}</p>
                    <h2 class="v7-band__title" id="wf3-status">{st_title}</h2>
                </div>

                <table class="wf3-status">
                    <thead>
                        <tr><th>{st_col1}</th><th>{st_col2}</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>{st_r1c1}</td><td><span class="wf3-yes">{st_r1state}</span> &mdash; {st_r1c2}</td></tr>
                        <tr><td>{st_r2c1}</td><td><span class="wf3-no">{st_r2state}</span> &mdash; {st_r2c2}</td></tr>
                        <tr><td>{st_r3c1}</td><td><span class="wf3-yes">{st_r3state}</span> &mdash; {st_r3c2}</td></tr>
                        <tr><td>{st_r4c1}</td><td><span class="wf3-no">{st_r4state}</span> &mdash; {st_r4c2}</td></tr>
                        <tr><td>{st_r5c1}</td><td><span class="wf3-no">{st_r5state}</span> &mdash; {st_r5c2}</td></tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="v7-steps-section" aria-labelledby="wf3-fix">
            <div class="v7-container">
                <div class="v7-steps-section__head">
                    <p class="v7-eyebrow">{fx_eyebrow}</p>
                    <h2 class="v7-steps-section__title" id="wf3-fix">{fx_title}</h2>
                </div>

                <p class="v7-page-hero__lead">{fx_lead}</p>

                <pre class="wf3-code"><code><span class="wf3-comment"># {fx_c1}</span>
Get-SPLegacyWorkflowEnabledSites
Get-SPWorkflow2013EnabledSites

<span class="wf3-comment"># {fx_c2}</span>
Enable-SPLegacyWorkflow  https://sharepoint.example.com/sites/quality
Enable-SPWorkflow2013    https://sharepoint.example.com/sites/quality

<span class="wf3-comment"># {fx_c3}</span>
Disable-SPLegacyWorkflow https://sharepoint.example.com/sites/quality</code></pre>

                <div class="wf3-warn">
                    <strong>{fx_warn_label}</strong> {fx_warn}
                </div>

                <p class="v7-page-hero__lead">{fx_note}</p>
            </div>
        </section>

        <section class="v7-band" aria-labelledby="wf3-onprem">
            <div class="v7-container">
                <div class="v7-band__head">
                    <p class="v7-eyebrow">{op_eyebrow}</p>
                    <h2 class="v7-band__title" id="wf3-onprem">{op_title}</h2>
                </div>

                <div class="v7-band__list">
                    <p class="v7-band__item"><strong>{op1_t}</strong> {op1_d}</p>
                    <p class="v7-band__item"><strong>{op2_t}</strong> {op2_d}</p>
                    <p class="v7-band__item"><strong>{op3_t}</strong> {op3_d}</p>
                    <p class="v7-band__item"><strong>{op4_t}</strong> {op4_d}</p>
                </div>

                <div class="wf3-warn">
                    <strong>{op_gap_label}</strong> {op_gap}
                </div>
            </div>
        </section>

        <section class="v7-band" aria-labelledby="wf3-myths">
            <div class="v7-container">
                <div class="v7-band__head">
                    <p class="v7-eyebrow">{my_eyebrow}</p>
                    <h2 class="v7-band__title" id="wf3-myths">{my_title}</h2>
                </div>

                <div class="v7-band__list">
                    <p class="v7-band__item"><strong>{my1_t}</strong> {my1_d}</p>
                    <p class="v7-band__item"><strong>{my2_t}</strong> {my2_d}</p>
                    <p class="v7-band__item"><strong>{my3_t}</strong> {my3_d}</p>
                    <p class="v7-band__item"><strong>{my4_t}</strong> {my4_d}</p>
                </div>
            </div>
        </section>

        <section class="v7-steps-section" aria-labelledby="wf3-workbox">
            <div class="v7-container">
                <div class="v7-steps-section__head">
                    <p class="v7-eyebrow">{wb_eyebrow}</p>
                    <h2 class="v7-steps-section__title" id="wf3-workbox">{wb_title}</h2>
                </div>

                <p class="v7-page-hero__lead">{wb_lead}</p>

                <div class="v7-steps">
                    <div class="v7-step">
                        <span class="v7-step__num">1</span>
                        <h3 class="v7-step__title">{wb1_t}</h3>
                        <p class="v7-step__desc">{wb1_d}</p>
                    </div>
                    <div class="v7-step">
                        <span class="v7-step__num">2</span>
                        <h3 class="v7-step__title">{wb2_t}</h3>
                        <p class="v7-step__desc">{wb2_d}</p>
                    </div>
                    <div class="v7-step">
                        <span class="v7-step__num">3</span>
                        <h3 class="v7-step__title">{wb3_t}</h3>
                        <p class="v7-step__desc">{wb3_d}</p>
                    </div>
                </div>

                <div class="wf3-sources">
                    <p>{src_title}</p>
                    <ul>
                        <li><a href="https://support.microsoft.com/en-us/servicing/office/hotfix/sharepoint/5002908" rel="noopener" target="_blank">KB5002908 &mdash; {src1}</a></li>
                        <li><a href="https://learn.microsoft.com/en-us/sharepoint/what-s-new/what-s-deprecated-or-removed-from-sharepoint-server-subscription-edition" rel="noopener" target="_blank">{src2}</a></li>
                        <li><a href="https://support.microsoft.com/en-us/office/sharepoint-2013-workflow-retirement-4613d9cf-69aa-40f7-b6bf-6e7831c9691e" rel="noopener" target="_blank">{src3}</a></li>
                        <li><a href="https://learn.microsoft.com/en-us/lifecycle/products/sharepoint-workflow-manager" rel="noopener" target="_blank">{src4}</a></li>
                        <li><a href="https://blog.stefan-gossner.com/2026/08/14/are-you-using-sp2010-or-sp2013-workflows-in-your-sharepoint-farms-this-post-is-for-you/" rel="noopener" target="_blank">{src5}</a></li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="v7-cta">
            <div class="v7-container v7-cta__inner">
                <h2 class="v7-cta__title">Run work. <span class="accent">Speed up the flow.</span></h2>
                <p class="v7-cta__lead">{cta_lead}</p>
                <div class="v7-cta__actions">
                    <a class="v7-btn v7-btn--primary" href="contact.html">{cta_1} <span aria-hidden="true">&#8594;</span></a>
                    <a class="v7-btn v7-btn--ghost" href="platform-2to2.html">{cta_2}</a>
                </div>
                <p class="v7-cta__note">{cta_mail} <a href="mailto:office@datapolis.com">office@datapolis.com</a></p>
            </div>
        </section>
    </main>

    <div id="footer-placeholder"></div>

</body>
</html>
"""
