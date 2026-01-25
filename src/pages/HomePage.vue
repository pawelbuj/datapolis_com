<script setup>
// HomePage - placeholder for Phase 1
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
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
              People. AI.<br>
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
        </div>
      </div>
    </section>

    <!-- Problem Section -->
    <section class="dp-section dp-section--dark dp-section--problem">
      <div class="dp-container">
        <div class="dp-section__header">
          <span class="dp-label">The reality</span>
          <h2 class="dp-title">Why work is broken</h2>
        </div>
        
        <div class="dp-problems">
          <div class="dp-problem">
            <p class="dp-problem__text">Critical processes are scattered across emails, spreadsheets, and people's heads.</p>
          </div>
          <div class="dp-problem">
            <p class="dp-problem__text">Automation tools don't connect. Work breaks between systems and teams.</p>
          </div>
          <div class="dp-problem">
            <p class="dp-problem__text">AI copilots have no governance: no audit trail, no accountability.</p>
          </div>
        </div>
        
        <div class="dp-thesis">
          <p class="dp-thesis__line">AI won't fix broken work.</p>
          <p class="dp-thesis__line dp-thesis__line--accent">Work needs a <span class="accent">governed process layer</span>.</p>
        </div>
      </div>
    </section>

    <!-- Credibility Section -->
    <section class="dp-section dp-section--credibility">
      <div class="dp-container">
        <div class="dp-credibility">
          <h2 class="dp-credibility__title">
            We've spent <span class="accent">20+ years</span> running mission-critical business processes.
          </h2>
          
          <div class="dp-stats">
            <div class="dp-stat">
              <span class="dp-stat__number">Thousands</span>
              <span class="dp-stat__label">Business-critical workflows running in production</span>
            </div>
            <div class="dp-stat">
              <span class="dp-stat__number">Banks, Energy, Industry, Government</span>
              <span class="dp-stat__label">The most regulated environments in the world</span>
            </div>
            <div class="dp-stat">
              <span class="dp-stat__number">Zero-downtime operations</span>
              <span class="dp-stat__label">Audited. Controlled. Always on.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
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
