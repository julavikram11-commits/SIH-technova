/**
 * app.js - Main Application Orchestrator for SIH26063 Polar Portal
 * Pure Light Institutional Theme (MoES / NCPOR).
 * Handles tab navigation, mobile drawer, live telemetry ticker, GIGW accessibility, and dynamic stats.
 */

const App = {
  activeTab: 'outreach',
  language: 'en',
  isHighContrast: false,

  init() {
    this.bindNavigation();
    this.bindMobileNav();
    this.bindAccessibility();
    this.startTelemetryTicker();
    this.loadDynamicStats();
    this.startLiveStationWidget();
    
    // Initialize module controllers
    if (window.OutreachModule) OutreachModule.init();
    if (window.RepoModule) RepoModule.init();
    if (window.MediaModule) MediaModule.init();
    if (window.AIChatModule) AIChatModule.init();
    if (window.AdminModule) AdminModule.init();

    // Check URL path or hash for deep linking (e.g. /resources, /repository, /media, /stations, /about, /admin)
    const validTabs = ['outreach', 'repository', 'stations', 'media', 'resources', 'about', 'admin'];
    let initialTab = 'outreach';
    const pathSegment = window.location.pathname.replace(/^\/+/, '').split('/')[0].toLowerCase();
    if (validTabs.includes(pathSegment)) {
      initialTab = pathSegment;
    } else if (window.location.hash) {
      const hashTab = window.location.hash.replace('#', '').replace('view-', '').toLowerCase();
      if (validTabs.includes(hashTab)) {
        initialTab = hashTab;
      }
    }

    if (initialTab !== 'outreach') {
      this.switchTab(initialTab, false);
    }

    console.log("NCPOR Polar Science Portal Initialized (SIH26063 - Light Institutional Theme)");
  },

  bindNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        if (!tab) return;
        this.switchTab(tab);
        const navLinks = document.querySelector('.nav-links');
        if (navLinks) navLinks.classList.remove('open');
      });
    });

    // Handle browser back and forward history buttons
    window.addEventListener('popstate', () => {
      const validTabs = ['outreach', 'repository', 'stations', 'media', 'resources', 'about', 'admin'];
      const pathSegment = window.location.pathname.replace(/^\/+/, '').split('/')[0].toLowerCase();
      const tab = validTabs.includes(pathSegment) ? pathSegment : 'outreach';
      this.switchTab(tab, false);
    });
  },

  bindMobileNav() {
    const toggleBtn = document.getElementById('mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (toggleBtn && navLinks) {
      toggleBtn.addEventListener('click', () => {
        navLinks.classList.toggle('open');
      });
    }
  },

  switchTab(tabId, updateHistory = true) {
    const validTabs = ['outreach', 'repository', 'stations', 'media', 'resources', 'about', 'admin'];
    if (!validTabs.includes(tabId)) tabId = 'outreach';
    this.activeTab = tabId;

    // Update browser URL history if supported
    if (updateHistory && window.history && window.history.pushState) {
      const targetPath = tabId === 'outreach' ? '/' : `/${tabId}`;
      if (window.location.pathname !== targetPath) {
        window.history.pushState({ tab: tabId }, '', targetPath);
      }
    }

    // Update Nav Buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    // Update Views
    document.querySelectorAll('.portal-view').forEach(view => {
      const isTarget = view.id === `view-${tabId}`;
      view.style.display = isTarget ? 'block' : 'none';
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Module hooks on activate
    if (tabId === 'outreach' && window.OutreachModule) OutreachModule.onActivate();
    if (tabId === 'repository' && window.RepoModule) RepoModule.loadPublications();
    if (tabId === 'stations' && window.OutreachModule) {
      if (OutreachModule.stations.length === 0) {
        OutreachModule.loadStations();
      } else {
        OutreachModule.renderStationTabs();
        OutreachModule.renderStationDetails(OutreachModule.selectedStationId);
      }
    }
    if (tabId === 'media' && window.MediaModule) { 
      MediaModule.loadAssets(); 
      MediaModule.renderVideos(); 
      MediaModule.renderAudios(); 
    }
    if (tabId === 'resources') {
      if (window.OutreachModule) {
        OutreachModule.loadToolkits();
        OutreachModule.loadQuiz();
      }
      if (window.RepoModule) {
        RepoModule.loadDatasets();
      }
    }
    if (tabId === 'admin' && window.AdminModule) AdminModule.onActivate();
  },

  openAIChat(starterPrompt = '') {
    if (window.AIChatModule) {
      AIChatModule.openWithPrompt(starterPrompt);
    }
  },

  async loadDynamicStats() {
    try {
      const res = await fetch('/api/stats');
      if (!res.ok) return;
      const stats = await res.json();
      
      const elAntarctic = document.getElementById('hero-stat-antarctic');
      const elArctic = document.getElementById('hero-stat-arctic');
      const elOcean = document.getElementById('hero-stat-ocean');
      const elHimalaya = document.getElementById('hero-stat-himalaya');

      if (elAntarctic && stats.antarctic_expeditions) elAntarctic.textContent = stats.antarctic_expeditions;
      if (elArctic && stats.arctic_campaigns) elArctic.textContent = stats.arctic_campaigns;
      if (elOcean && stats.southern_ocean_cruises) elOcean.textContent = stats.southern_ocean_cruises;
      if (elHimalaya && stats.third_pole_altitude) elHimalaya.textContent = stats.third_pole_altitude;
    } catch (err) {
      console.warn("Dynamic /api/stats fallback active", err);
    }
  },

  async startLiveStationWidget() {
    const updateWidget = async () => {
      try {
        const res = await fetch('/api/stations/live');
        if (!res.ok) return;
        const data = await res.json();
        if (data.stations && data.stations.length > 0) {
          data.stations.forEach(s => {
            const tempEl = document.getElementById(`hero-temp-${s.id}`);
            if (tempEl) {
              tempEl.textContent = s.temp_display;
            }
          });
        }
      } catch (err) {
        console.warn("Station widget sync fallback", err);
      }
    };

    await updateWidget();
    setInterval(updateWidget, 10000);
  },

  bindAccessibility() {
    // High Contrast Toggle (GIGW standard)
    const contrastBtn = document.getElementById('btn-high-contrast');
    if (contrastBtn) {
      contrastBtn.addEventListener('click', () => {
        this.isHighContrast = !this.isHighContrast;
        document.body.classList.toggle('high-contrast', this.isHighContrast);
        contrastBtn.classList.toggle('active', this.isHighContrast);
        this.showToast(this.isHighContrast ? "High Contrast Mode Enabled (GIGW Standard)" : "High Contrast Mode Disabled");
      });
    }

    // Font Sizing (GIGW 3.0 standard)
    const fontPlusBtn = document.getElementById('btn-font-plus');
    const fontNormalBtn = document.getElementById('btn-font-normal');
    const fontMinusBtn = document.getElementById('btn-font-minus');

    if (fontPlusBtn) {
      fontPlusBtn.addEventListener('click', () => {
        document.body.classList.remove('font-large', 'font-xlarge');
        document.body.classList.add('font-large');
        this.showToast("Font size increased (GIGW standard)");
      });
    }

    if (fontNormalBtn) {
      fontNormalBtn.addEventListener('click', () => {
        document.body.classList.remove('font-large', 'font-xlarge');
        this.showToast("Font size reset to normal");
      });
    }

    if (fontMinusBtn) {
      fontMinusBtn.addEventListener('click', () => {
        document.body.classList.remove('font-large', 'font-xlarge');
        this.showToast("Standard font scale active");
      });
    }

    // Language Toggle (English / Hindi)
    const langBtn = document.getElementById('btn-lang-toggle');
    if (langBtn) {
      langBtn.addEventListener('click', () => {
        this.language = this.language === 'en' ? 'hi' : 'en';
        langBtn.textContent = this.language === 'en' ? 'English | हिंदी' : 'हिंदी | English';
        this.showToast(this.language === 'en' ? "Language: English" : "भाषा: हिंदी (MoES द्विभाषी पोर्टल)");
      });
    }

    // Text to Speech Narrator
    const ttsBtn = document.getElementById('btn-tts-reader');
    if (ttsBtn) {
      ttsBtn.addEventListener('click', () => {
        const textToRead = document.querySelector('.carousel-slide-title')?.innerText || "National Centre for Polar and Ocean Research";
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(textToRead);
          utterance.rate = 0.95;
          window.speechSynthesis.speak(utterance);
          this.showToast("Reading aloud screen header (GIGW Audio Assist)");
        } else {
          this.showToast("Speech synthesis not supported on this browser.");
        }
      });
    }
  },

  async startTelemetryTicker() {
    const updateTicker = async () => {
      try {
        const res = await fetch('/api/outreach/telemetry/live');
        if (!res.ok) return;
        const data = await res.json();
        this.renderTicker(data.data);
      } catch (err) {
        console.warn("Telemetry stream retry", err);
      }
    };

    await updateTicker();
    setInterval(updateTicker, 8000);
  },

  renderTicker(stations) {
    const container = document.getElementById('ticker-items-container');
    if (!container) return;

    container.innerHTML = stations.map(s => `
      <div class="station-ticker-pill" onclick="App.switchTab('outreach'); OutreachModule.selectStation('${s.station_id}')" role="button" tabindex="0" aria-label="Inspect ${s.name} telemetry">
        <span class="station-ticker-name">${s.name.replace(' Research Station', '').replace(' High-Altitude Station', '')}:</span>
        <span class="station-ticker-temp">${s.temp_c > 0 ? '+' : ''}${s.temp_c}°C</span>
        <span class="station-ticker-wind">${s.wind_knots} kts ${s.wind_direction}</span>
        <span style="font-size: 0.7rem; color: var(--text-muted); font-family: var(--font-mono);">(${s.daylight_hours})</span>
      </div>
    `).join('');
  },

  showToast(message, duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.2s ease';
      setTimeout(() => toast.remove(), 200);
    }, duration);
  }
};

window.App = App;
document.addEventListener('DOMContentLoaded', () => App.init());
