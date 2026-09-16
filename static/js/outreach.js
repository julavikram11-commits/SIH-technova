/**
 * outreach.js - Science Outreach & Smart Education Module (Pillar 1)
 * Enhanced for Pure Light Institutional Theme (MoES / NCPOR).
 * Features:
 *  - 2-Column Hero: Featured Carousel (70%) + Live News & Bulletins Sidebar (30%)
 *  - Automated Carousel rotation with manual dot/button controls
 *  - Auto-scrolling live news ticker with pause-on-hover & manual toggle
 *  - Polar Station Dossiers with real-time sensory telemetry
 *  - Plain-language Science Articles with audience segmentation
 *  - Open Educational Toolkits with direct download triggers
 *  - Cadet Quiz Assessment with automated scoring & verifiable certificate generation
 */

const OutreachModule = {
  stations: [],
  selectedStationId: 'bharati',
  articles: [],
  toolkits: [],
  events: [],
  selectedAudience: 'all',
  quizQuestions: [],
  userQuizAnswers: {},

  // Featured Carousel State
  currentSlideIndex: 0,
  carouselTimer: null,
  carouselPaused: false,
  featuredSlides: [
    {
      badge: "44th ISEA • Antarctica",
      title: "Bharati Research Station: Continental Cryosphere & Oceanography",
      summary: "Constructed from 134 modular prefabricated containers on stilts in Larsemann Hills, East Antarctica, Bharati serves as India's year-round hub for paleoclimatology, ocean dynamics, and direct satellite telemetry.",
      image: "/assets/images/bharati.jpg",
      alt: "Bharati Research Station, Antarctica",
      station: "bharati"
    },
    {
      badge: "Arctic Expedition • Ny-Ålesund, Svalbard",
      title: "Himadri Station & IndARC Mooring: Arctic Ocean Dynamics & Teleconnections",
      summary: "Located at 79°N in Svalbard, Himadri monitors aerosol radiative forcing and fjord hydrography. The IndARC multi-sensor mooring in Kongsfjorden provides year-round underwater acoustic and biogeochemical measurements.",
      image: "/assets/images/himadri.jpg",
      alt: "Himadri Arctic Station at Ny-Ålesund",
      station: "himadri"
    },
    {
      badge: "Southern Ocean Expedition • ORV Sagar Nidhi",
      title: "11th Indian Southern Ocean Expedition: Planetary Carbon Sinks & Biogeochemistry",
      summary: "Investigating the Southern Ocean's role as a major atmospheric carbon sink. Multi-disciplinary teams deploy bio-optical floats, deep CTD rosettes, and trace-metal clean rosette systems across the Sub-Antarctic Front.",
      image: "/assets/images/sagarnidhi.jpg",
      alt: "ORV Sagar Nidhi Southern Ocean Expedition",
      station: "maitri"
    },
    {
      badge: "Himalayan Glaciology • Spiti Valley (4,050m)",
      title: "Himansh High-Altitude Field Station: Third Pole Freshwater Glaciology",
      summary: "Perched at 4,050 meters above sea level in the Chandra basin, Himachal Pradesh, Himansh conducts continuous mass-balance modeling, ice-thickness radar surveys, and glacial melt telemetry across the Third Pole.",
      image: "/assets/images/himansh.jpg",
      alt: "Himansh High Altitude Station",
      station: "himansh"
    }
  ],

  // Live News Ticker State
  newsTickerTimer: null,
  isNewsAutoScrollActive: true,
  bulletins: [
    {
      tag: "EXPEDITION",
      date: "10 MAR 2026",
      title: "44th Indian Antarctic Expedition Team Arrives at Bharati Station",
      summary: "Scientific crew and logistics convoy successfully completed turnover at Larsemann Hills.",
      source: "MoES Dispatch #26-88"
    },
    {
      tag: "RESEARCH",
      date: "08 MAR 2026",
      title: "IndARC Mooring in Kongsfjorden Successfully Retrieved and Redeployed",
      summary: "Year-long hydrological, acoustic, and nutrient profiles captured across Arctic fjord water column.",
      source: "Arctic Science Cell"
    },
    {
      tag: "DATASET",
      date: "04 MAR 2026",
      title: "New 10-Year High-Resolution Antarctic Ice Surface Velocity Dataset Released",
      summary: "Available under Government Open Data License (GODL-India) with DOI: 10.5061/dryad.ncpor.2026.01.",
      source: "Data Repository Cell"
    },
    {
      tag: "NOTICE",
      date: "28 FEB 2026",
      title: "Call for Research Proposals: 45th Indian Scientific Expedition to Antarctica (ISEA)",
      summary: "MoES invites multidisciplinary research proposals from national institutes and universities.",
      source: "Polar Logistics Division"
    },
    {
      tag: "SEMINAR",
      date: "22 FEB 2026",
      title: "National Seminar on Himalayan Cryosphere & Freshwater Security Announced",
      summary: "Hybrid session focusing on Spiti Valley benchmark glacier mass balance modeling.",
      source: "Centre for Glaciology"
    },
    {
      tag: "PRESS",
      date: "15 FEB 2026",
      title: "ORV Sagar Kanya Concludes Southern Ocean Hydrographic Transect",
      summary: "Over 80 CTD stations completed down to 4,500m depth across the Polar Frontal Zone.",
      source: "Ocean Sciences Group"
    }
  ],

  async init() {
    this.initCarousel();
    this.initNewsTicker();
    await this.loadStations();
    await this.loadArticles();
    await this.loadToolkits();
    await this.loadEvents();
    await this.loadQuiz();
    this.bindAudienceFilters();
    this.bindQuizControls();
  },

  onActivate() {
    // Resume timers if paused during tab switch
    if (this.isNewsAutoScrollActive && !this.newsTickerTimer) {
      this.startNewsAutoScroll();
    }
    if (!this.carouselTimer) {
      this.startCarouselTimer();
    }
  },

  // ================= 1. Featured Expedition Carousel =================
  initCarousel() {
    this.renderCarouselDots();
    this.goToSlide(0);
    this.startCarouselTimer();

    // Pause on hover
    const carouselCard = document.querySelector('.featured-carousel-card');
    if (carouselCard) {
      carouselCard.addEventListener('mouseenter', () => {
        this.carouselPaused = true;
      });
      carouselCard.addEventListener('mouseleave', () => {
        this.carouselPaused = false;
      });
    }
  },

  renderCarouselDots() {
    const dotsContainer = document.getElementById('carousel-dots-container');
    if (!dotsContainer) return;

    dotsContainer.innerHTML = this.featuredSlides.map((slide, idx) => `
      <button type="button" 
              class="carousel-dot ${idx === this.currentSlideIndex ? 'active' : ''}" 
              onclick="OutreachModule.goToSlide(${idx})" 
              aria-label="Go to Slide ${idx + 1}: ${slide.title}">
      </button>
    `).join('');
  },

  goToSlide(index) {
    if (index < 0) index = this.featuredSlides.length - 1;
    if (index >= this.featuredSlides.length) index = 0;
    this.currentSlideIndex = index;

    const slide = this.featuredSlides[this.currentSlideIndex];
    const imgEl = document.getElementById('carousel-slide-img');
    const badgeEl = document.getElementById('carousel-slide-badge');
    const titleEl = document.getElementById('carousel-slide-title');
    const summaryEl = document.getElementById('carousel-slide-summary');

    if (imgEl) {
      imgEl.style.opacity = '0.3';
      setTimeout(() => {
        imgEl.src = slide.image;
        imgEl.alt = slide.alt;
        imgEl.style.opacity = '1';
      }, 150);
    }
    if (badgeEl) badgeEl.textContent = slide.badge;
    if (titleEl) titleEl.textContent = slide.title;
    if (summaryEl) summaryEl.textContent = slide.summary;

    // Update active dot
    const dots = document.querySelectorAll('.carousel-dot');
    dots.forEach((d, idx) => {
      d.classList.toggle('active', idx === this.currentSlideIndex);
    });
  },

  nextSlide() {
    this.goToSlide(this.currentSlideIndex + 1);
  },

  prevSlide() {
    this.goToSlide(this.currentSlideIndex - 1);
  },

  startCarouselTimer() {
    if (this.carouselTimer) clearInterval(this.carouselTimer);
    this.carouselTimer = setInterval(() => {
      if (!this.carouselPaused) {
        this.nextSlide();
      }
    }, 6000);
  },

  // ================= 2. Live News & Bulletins Sidebar =================
  initNewsTicker() {
    this.renderNewsTicker();
    this.startNewsAutoScroll();

    const scrollArea = document.getElementById('news-ticker-scroll-area');
    if (scrollArea) {
      scrollArea.addEventListener('mouseenter', () => {
        if (this.isNewsAutoScrollActive) {
          clearInterval(this.newsTickerTimer);
          this.newsTickerTimer = null;
        }
      });
      scrollArea.addEventListener('mouseleave', () => {
        if (this.isNewsAutoScrollActive && !this.newsTickerTimer) {
          this.startNewsAutoScroll();
        }
      });
    }
  },

  renderNewsTicker() {
    const container = document.getElementById('news-ticker-scroll-area');
    if (!container) return;

    // Duplicate list once to create a seamless infinite loop effect
    const allItems = [...this.bulletins, ...this.bulletins];

    container.innerHTML = allItems.map(item => `
      <div class="news-ticker-item" role="article" tabindex="0">
        <div class="news-ticker-item-meta">
          <span class="news-tag">${item.tag}</span>
          <span class="news-date">${item.date}</span>
        </div>
        <div class="news-ticker-item-title">${item.title}</div>
        <div class="news-ticker-item-desc">${item.summary}</div>
        <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 4px;">
          ${item.source}
        </div>
      </div>
    `).join('');
  },

  startNewsAutoScroll() {
    const scrollArea = document.getElementById('news-ticker-scroll-area');
    if (!scrollArea) return;

    if (this.newsTickerTimer) clearInterval(this.newsTickerTimer);

    this.newsTickerTimer = setInterval(() => {
      if (scrollArea.scrollHeight - scrollArea.scrollTop <= scrollArea.clientHeight + 1) {
        // Halfway point reset for seamless loop
        scrollArea.scrollTop = scrollArea.scrollHeight / 2 - scrollArea.clientHeight;
      } else {
        scrollArea.scrollTop += 1;
      }
    }, 45);
  },

  toggleNewsAutoScroll() {
    const btn = document.getElementById('btn-toggle-news-ticker');
    if (this.isNewsAutoScrollActive) {
      clearInterval(this.newsTickerTimer);
      this.newsTickerTimer = null;
      this.isNewsAutoScrollActive = false;
      if (btn) btn.textContent = 'Resume Stream';
    } else {
      this.isNewsAutoScrollActive = true;
      this.startNewsAutoScroll();
      if (btn) btn.textContent = 'Pause Stream';
    }
  },

  // ================= 3. Field Observatories & Stations =================
  async loadStations() {
    try {
      const res = await fetch('/api/outreach/stations');
      if (!res.ok) return;
      this.stations = await res.json();
      this.renderStationTabs();
      this.renderStationDetails(this.selectedStationId);
    } catch (err) {
      console.error("Failed to load stations", err);
    }
  },

  renderStationTabs() {
    const container = document.getElementById('station-selector-grid');
    if (!container) return;

    container.innerHTML = this.stations.map(s => `
      <div class="station-tab-card ${s.id === this.selectedStationId ? 'active' : ''}" 
           id="tab-${s.id}" 
           onclick="OutreachModule.selectStation('${s.id}')"
           role="button"
           tabindex="0"
           aria-label="Select ${s.name} (${s.region})">
        <div class="station-tab-info">
          <span class="station-region-badge">${s.region.toUpperCase()}</span>
          <h4>${s.name}</h4>
          <p>Commissioned ${s.commissioned} • ${s.status}</p>
        </div>
      </div>
    `).join('');
  },

  selectStation(stationId) {
    this.selectedStationId = stationId;
    document.querySelectorAll('.station-tab-card').forEach(card => {
      card.classList.toggle('active', card.id === `tab-${stationId}`);
    });
    this.renderStationDetails(stationId);
  },

  renderStationDetails(stationId) {
    const station = this.stations.find(s => s.id === stationId);
    if (!station) return;

    const showcase = document.getElementById('station-showcase-container');
    if (!showcase) return;

    const shortName = station.name.split(' ')[0];

    showcase.innerHTML = `
      <div class="station-showcase-media">
        <img src="${station.image}" alt="${station.name} - India's Polar Research Facility" onerror="this.src='/assets/images/bharati.jpg'" />
        <div class="station-badge-overlay">
          ${station.location}
        </div>
      </div>
      <div class="station-showcase-content">
        <div>
          <div class="station-header-meta">
            <div>
              <h3 class="station-name-large">${station.name}</h3>
              <div class="station-coords">${station.lat_display} • ${station.lng_display}</div>
            </div>
            <span style="font-size: 0.75rem; font-family: var(--font-mono); background: var(--status-active-subtle); color: var(--status-active); padding: 4px 10px; border-radius: var(--radius-xs); font-weight: 600; border: 1px solid rgba(22, 101, 52, 0.2);">
              ${station.status}
            </span>
          </div>

          <p class="station-desc">${station.description}</p>

          <div class="station-telemetry-grid">
            <div class="telem-box">
              <span>Ambient Temp</span>
              <strong>${station.telemetry.temp_c > 0 ? '+' : ''}${station.telemetry.temp_c}°C</strong>
            </div>
            <div class="telem-box">
              <span>Wind Velocity</span>
              <strong>${station.telemetry.wind_speed_knots} kts</strong>
            </div>
            <div class="telem-box">
              <span>Solar / Day</span>
              <strong style="font-size: 0.8125rem;">${station.telemetry.daylight_hours.split('(')[0]}</strong>
            </div>
          </div>

          <div style="margin-bottom: 18px;">
            <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; display: block; margin-bottom: 6px;">
              Primary Scientific Disciplines
            </span>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
              ${station.scientific_focus.map(f => `
                <span style="background: var(--bg-surface); border: 1px solid var(--border-subtle); font-size: 0.75rem; padding: 3px 9px; border-radius: var(--radius-xs); color: var(--ocean-navy); font-weight: 500;">
                  ${f}
                </span>
              `).join('')}
            </div>
          </div>

          <div>
            <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; display: block; margin-bottom: 6px;">
              Engineering & Environmental Features
            </span>
            <ul class="station-highlights-list">
              ${station.highlights.map(h => `<li>${h}</li>`).join('')}
            </ul>
          </div>
        </div>

        <div style="margin-top: 24px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; border-top: 1px solid var(--border-subtle); padding-top: 16px;">
          <button type="button" class="btn-hero-primary" onclick="App.switchTab('repository'); RepoModule.filterByStation('${shortName}')">
            Explore ${shortName} Research & Datasets →
          </button>
          <button type="button" class="btn-cite" onclick="App.openAIChat('Tell me about the engineering, history, and scientific mandate of ${station.name}.')">
            Ask AI About ${shortName}
          </button>
        </div>
      </div>
    `;
  },

  // ================= 4. Science Outreach Articles =================
  bindAudienceFilters() {
    const pills = document.querySelectorAll('.audience-pill');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.selectedAudience = pill.dataset.audience;
        this.loadArticles();
      });
    });
  },

  async loadArticles() {
    try {
      const audienceParam = this.selectedAudience === 'all' ? '' : `?audience=${encodeURIComponent(this.selectedAudience)}`;
      const res = await fetch(`/api/outreach/articles${audienceParam}`);
      if (!res.ok) return;
      const data = await res.json();
      this.articles = data.articles;
      this.renderArticles();
    } catch (err) {
      console.error("Failed to load articles", err);
    }
  },

  renderArticles() {
    const container = document.getElementById('articles-grid-container');
    if (!container) return;

    if (this.articles.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted); background: var(--bg-surface); border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          No science briefing articles found matching the selected audience criteria.
        </div>
      `;
      return;
    }

    container.innerHTML = this.articles.map(art => `
      <article class="article-card" onclick="OutreachModule.openArticleModal('${art.id}')" aria-label="${art.title}" tabindex="0" role="button">
        <div class="article-thumb-box">
          <img src="${art.image}" alt="${art.title}" loading="lazy" onerror="this.src='/assets/images/bharati.jpg'" />
          <span class="article-audience-badge">${art.audience}</span>
        </div>
        <div class="article-body">
          <span class="article-topic-tag">${art.topic}</span>
          <h4 class="article-title">${art.title}</h4>
          <p class="article-summary">${art.summary}</p>
          <div class="article-footer-meta">
            <span>Read: ${art.read_time}</span>
            <span>${art.published_date}</span>
          </div>
        </div>
      </article>
    `).join('');
  },

  openArticleModal(artId) {
    const article = this.articles.find(a => a.id === artId);
    if (!article) return;

    const modal = document.getElementById('modal-explain-paper');
    const content = document.getElementById('modal-explain-content');
    if (!modal || !content) return;

    content.innerHTML = `
      <div style="display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap;">
        <span class="pub-badge station">Audience: ${article.audience}</span>
        <span class="pub-badge expedition">Topic: ${article.topic}</span>
      </div>
      <h2 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--ocean-navy); margin-bottom: 8px; line-height: 1.3;">
        ${article.title}
      </h2>
      <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 16px;">
        Published: ${article.published_date} • Reading Duration: ${article.read_time} • MoES Polar Science Dissemination Cell
      </div>

      <div style="max-height: 240px; overflow: hidden; border-radius: var(--radius-sm); margin-bottom: 18px; background: #000; border: 1px solid var(--border-subtle);">
        <img src="${article.image}" style="width: 100%; height: 240px; object-fit: cover;" alt="${article.title}" onerror="this.src='/assets/images/bharati.jpg'" />
      </div>

      <div style="background: var(--bg-surface); border-left: 3px solid var(--polar-cyan); padding: 14px 16px; border-radius: var(--radius-sm); margin-bottom: 18px; line-height: 1.6; border: 1px solid var(--border-subtle); border-left-width: 3px;">
        <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--polar-cyan); text-transform: uppercase; margin-bottom: 4px; font-weight: 700;">Executive Briefing</h4>
        <p style="font-size: 0.875rem; color: var(--ocean-navy); font-weight: 500;">${article.summary}</p>
      </div>

      <div style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: 20px;">
        ${article.content}
      </div>

      <div style="background: var(--bg-surface); border-left: 3px solid var(--status-active); padding: 14px 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); border-left-width: 3px;">
        <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--status-active); text-transform: uppercase; margin-bottom: 6px; font-weight: 700;">Key Insights for Citizens</h4>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; padding-left: 0;">
          ${article.key_takeaways.map(t => `<li style="font-size: 0.8125rem; color: var(--text-primary); display: flex; gap: 6px;"><span style="color: var(--status-active); font-weight: 700;">✓</span> <span>${t}</span></li>`).join('')}
        </ul>
      </div>

      <div style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 16px;">
        <button type="button" class="btn-hero-primary" onclick="App.openAIChat('Explain the key scientific findings of the article: ${article.title.replace(/'/g, "\\'")} in simple terms.')">
          Ask AI to Explain This Article
        </button>
        <button type="button" class="btn-cite" onclick="RepoModule.closeModals()">Close Briefing</button>
      </div>
    `;

    modal.classList.add('open');
  },

  // ================= 5. Educational Toolkits =================
  async loadToolkits() {
    try {
      const res = await fetch('/api/outreach/toolkits');
      if (!res.ok) return;
      this.toolkits = await res.json();
      this.renderToolkits();
    } catch (err) {
      console.error("Failed to load toolkits", err);
    }
  },

  renderToolkits() {
    const container = document.getElementById('toolkits-grid-container');
    if (!container) return;

    container.innerHTML = this.toolkits.map(kit => `
      <div class="toolkit-card">
        <div>
          <span class="toolkit-grade-badge">${kit.grade}</span>
          <h4 style="font-family: var(--font-heading); font-size: 1.0625rem; color: var(--ocean-navy); margin-bottom: 6px;">
            ${kit.title}
          </h4>
          <p style="font-size: 0.8125rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px;">
            ${kit.summary}
          </p>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 12px;">
          <span style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">${kit.file_size} • ${kit.downloads} downloads</span>
          <button type="button" class="btn-cite" onclick="OutreachModule.downloadToolkit('${kit.id}')">
            Download Toolkit (PDF)
          </button>
        </div>
      </div>
    `).join('');
  },

  // ================= 6. Events & Announcements =================
  async loadEvents() {
    try {
      const res = await fetch('/api/outreach/events');
      if (!res.ok) return;
      this.events = await res.json();
      this.renderEvents();
    } catch (err) {
      console.error("Failed to load events", err);
    }
  },

  renderEvents() {
    const container = document.getElementById('events-grid-container');
    if (!container) return;

    container.innerHTML = this.events.map(evt => `
      <div class="event-card">
        <div class="event-date-row">
          <span style="color: var(--polar-cyan); font-weight: 600;">${evt.date}</span>
          <span style="color: var(--status-active); font-weight: 500;">${evt.status}</span>
        </div>
        <h4 style="font-family: var(--font-heading); font-size: 1rem; color: var(--ocean-navy); margin-bottom: 6px;">
          ${evt.title}
        </h4>
        <p style="font-size: 0.8125rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">
          ${evt.summary}
        </p>
        <span style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">Organized by: ${evt.organizer}</span>
      </div>
    `).join('');
  },

  // ================= 7. Cadet Quiz & Certification =================
  async loadQuiz() {
    try {
      const res = await fetch('/api/outreach/quiz');
      if (!res.ok) return;
      this.quizQuestions = await res.json();
      this.renderQuiz();
    } catch (err) {
      console.error("Failed to load quiz", err);
    }
  },

  renderQuiz() {
    const container = document.getElementById('quiz-questions-wrapper');
    if (!container) return;

    container.innerHTML = this.quizQuestions.map((q, idx) => `
      <div class="quiz-question-box" id="quiz-q-${q.id}">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--polar-cyan); font-weight: 600;">QUESTION ${idx + 1} OF ${this.quizQuestions.length}</span>
        </div>
        <h4 class="quiz-question-title">${q.question}</h4>
        <div class="quiz-options-list">
          ${q.options.map((opt, optIdx) => `
            <button type="button" class="quiz-opt-btn" 
                    id="opt-${q.id}-${optIdx}" 
                    onclick="OutreachModule.selectAnswer(${q.id}, ${optIdx})">
              <span style="display: inline-block; width: 20px; height: 20px; border-radius: 2px; border: 1px solid var(--border-subtle); text-align: center; line-height: 18px; font-size: 0.72rem; font-family: var(--font-mono); font-weight: 700;">
                ${String.fromCharCode(65 + optIdx)}
              </span>
              <span>${opt}</span>
            </button>
          `).join('')}
        </div>
        <div class="quiz-explanation-box" id="expl-${q.id}" style="display: none; margin-top: 12px; padding: 12px; background: var(--bg-surface); border-left: 3px solid var(--polar-cyan); font-size: 0.8125rem; border-radius: var(--radius-xs); border: 1px solid var(--border-subtle); border-left-width: 3px;"></div>
      </div>
    `).join('');
  },

  selectAnswer(questionId, optionIndex) {
    this.userQuizAnswers[questionId] = optionIndex;
    document.querySelectorAll(`[id^="opt-${questionId}-"]`).forEach((btn, idx) => {
      btn.classList.toggle('selected', idx === optionIndex);
    });
  },

  bindQuizControls() {
    const submitBtn = document.getElementById('btn-submit-quiz');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.evaluateQuiz());
    }
  },

  async evaluateQuiz() {
    const studentName = document.getElementById('quiz-student-name')?.value.trim() || "Polar Science Candidate";
    const institution = document.getElementById('quiz-student-school')?.value.trim() || "National Polar Explorer Program";

    if (Object.keys(this.userQuizAnswers).length === 0) {
      App.showToast("Please answer the questions before submitting.");
      return;
    }

    try {
      const res = await fetch('/api/outreach/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_name: studentName,
          school_institution: institution,
          answers: this.userQuizAnswers
        })
      });

      if (!res.ok) return;
      const data = await res.json();
      this.displayQuizResults(data);
    } catch (err) {
      console.error("Quiz evaluation failed", err);
    }
  },

  displayQuizResults(evalResult) {
    evalResult.results.forEach(r => {
      const explBox = document.getElementById(`expl-${r.question_id}`);
      if (explBox) {
        explBox.style.display = 'block';
        explBox.innerHTML = `<strong>${r.is_correct ? 'Correct:' : 'Explanation:'}</strong> ${r.explanation}`;
      }

      const userOptIdx = this.userQuizAnswers[r.question_id];
      const correctIdx = this.quizQuestions.find(q => q.id === r.question_id).correct_index;

      const userBtn = document.getElementById(`opt-${r.question_id}-${userOptIdx}`);
      const correctBtn = document.getElementById(`opt-${r.question_id}-${correctIdx}`);

      if (correctBtn) correctBtn.classList.add('correct');
      if (userBtn && !r.is_correct) userBtn.classList.add('wrong');
    });

    const certArea = document.getElementById('certificate-output-area');
    if (certArea) {
      const cert = evalResult.certificate;
      certArea.innerHTML = `
        <div class="certificate-card">
          <div class="cert-title">National Centre for Polar & Ocean Research</div>
          <div class="cert-subtitle">Ministry of Earth Sciences • Government of India</div>
          <p style="font-size: 0.8125rem; color: var(--text-secondary); margin-bottom: 4px;">Certificate of Scientific Achievement</p>
          <div class="cert-recipient">${cert.student_name}</div>
          <p style="font-size: 0.8125rem; color: var(--text-secondary); margin-bottom: 12px;">Representing <strong>${cert.institution}</strong></p>
          <p style="font-size: 0.875rem; color: var(--ocean-navy); margin-bottom: 14px;">Successfully demonstrated proficiency in Indian Polar Cryosphere Expeditions with a score of <strong>${cert.score} (${cert.percentage}%)</strong></p>
          <div>
            <span class="cert-badge">${cert.badge}</span>
          </div>
          <div class="cert-meta">
            <span>Certificate ID: <strong>${cert.certificate_id}</strong></span>
            <span>Issued: <strong>${cert.date}</strong></span>
            <span>Accreditation: <strong>MoES Polar Outreach Cell</strong></span>
          </div>
          <div style="margin-top: 20px;">
            <button type="button" class="btn-hero-primary" onclick="window.print()">Print / Save Certificate PDF</button>
          </div>
        </div>
      `;
      certArea.scrollIntoView({ behavior: 'smooth' });
    }

    App.showToast(`Evaluation complete. Score: ${evalResult.score}/${evalResult.total} (${evalResult.badge})`);
  },

  downloadToolkit(toolkitId) {
    if (!toolkitId) return;
    window.location.href = `/api/outreach/toolkits/download/${encodeURIComponent(toolkitId)}`;
  }
};

window.OutreachModule = OutreachModule;
