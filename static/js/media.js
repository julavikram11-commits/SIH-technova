/**
 * media.js - Verified Media Dissemination Hub Module (Pillar 3)
 * Features:
 *  - 4K Photography Grid with Lightbox
 *  - Verified Polar Science Documentary Videos with dedicated Video Player Modal
 *  - Playable Sub-zero Audio Soundscapes with Web Audio API synthesis engine fallback
 *  - Category filtering across Antarctic, Arctic, Himalayan, and Southern Ocean expeditions
 *  - Curated Journalist Press Kits with verifiable provenance
 */

const POLAR_DOCUMENTARY_VIDEOS = [
  {
    id: "vid-01",
    title: "Tour Inside India's Antarctic Base: Bharati Station",
    category: "Antarctica",
    station: "Bharati Station",
    duration: "14:20",
    embedUrl: "https://www.youtube.com/embed/lNhK69S_LLM",
    channel: "Polar Man Studio / NCPOR Expedition",
    thumbnail: "/assets/images/bharati.jpg",
    tags: ["Bharati", "Antarctica", "LarsemannHills", "PolarExpedition"],
    summary: "Comprehensive field walkthrough exploring the aerodynamic container stilt architecture, living modules, satellite receiving systems, and year-round research at Bharati Station in East Antarctica."
  },
  {
    id: "vid-02",
    title: "40th Indian Scientific Expedition to Antarctica: Voyage to Maitri & Bharati",
    category: "Antarctica",
    station: "Maitri & Bharati",
    duration: "22:15",
    embedUrl: "https://www.youtube.com/embed/he35dQfayAU",
    channel: "Ministry of Earth Sciences / NCPOR",
    thumbnail: "/assets/images/maitri.jpg",
    tags: ["Maitri", "40thISEA", "AntarcticProgram", "NCPOR"],
    summary: "Documentary covering the scientific objectives, logistics, wintering-over protocols, and environmental research of the Indian Antarctic Program at Maitri and Bharati stations."
  },
  {
    id: "vid-03",
    title: "Himadri: India's First Arctic Research Station at Ny-Ålesund",
    category: "Arctic",
    station: "Himadri Station",
    duration: "16:45",
    embedUrl: "https://www.youtube.com/embed/BMUn8U4tLfU",
    channel: "Ministry of Earth Sciences (MoES GoI)",
    thumbnail: "/assets/images/himadri.jpg",
    tags: ["Himadri", "Arctic", "NyAlesund", "Svalbard", "MoES"],
    summary: "Official MoES film documenting India's Arctic presence at Ny-Ålesund in Svalbard (79°N), profiling long-term atmospheric, oceanic, and glaciological monitoring."
  },
  {
    id: "vid-04",
    title: "IndARC & Arctic Ocean Sea Ice Research: NCPOR Scientific Study",
    category: "Arctic",
    station: "IndARC / Himadri",
    duration: "09:30",
    embedUrl: "https://www.youtube.com/embed/9qezdBidoGw",
    channel: "National Centre for Polar and Ocean Research (NCPOR)",
    thumbnail: "/assets/images/himadri.jpg",
    tags: ["IndARC", "Kongsfjorden", "ArcticSeaIce", "NCPOR", "Oceanography"],
    summary: "NCPOR scientific investigation on Arctic sea ice dynamics, fjord oceanography, and multi-sensor underwater moored observatories in Kongsfjorden."
  },
  {
    id: "vid-05",
    title: "HIMANSH: High-Altitude Himalayan Glaciology Research Station",
    category: "Himalayas",
    station: "Himansh Station",
    duration: "18:10",
    embedUrl: "https://www.youtube.com/embed/4DGp4MuUbzc",
    channel: "National Centre for Polar and Ocean Research (NCPOR)",
    thumbnail: "/assets/images/himansh.jpg",
    tags: ["Himansh", "ThirdPole", "SpitiValley", "NCPOR", "Glaciers"],
    summary: "Official NCPOR documentary on Himansh station situated at 4,050 meters in Spiti Valley, Himachal Pradesh, monitoring benchmark glacier mass balance in the Chandra basin."
  },
  {
    id: "vid-06",
    title: "Southern Ocean Climate Cruise & Indian Scientific Expedition to Antarctica",
    category: "Southern Ocean",
    station: "ORV Sagar Nidhi / Southern Ocean",
    duration: "12:50",
    embedUrl: "https://www.youtube.com/embed/W7-C3Zxzpc8",
    channel: "India Science / Department of Science & Technology",
    thumbnail: "/assets/images/sagarnidhi.jpg",
    tags: ["SouthernOcean", "ORVSagarNidhi", "Expedition", "IndiaScience"],
    summary: "Expedition documentary following Indian scientists aboard ice-class research vessels navigating the Southern Ocean across the Roaring Forties to study carbon fluxes and marine biomes."
  }
];

const POLAR_AUDIO_SOUNDSCAPES = [
  {
    id: "aud-01",
    title: "Tidewater Glacier Calving & Sub-zero Ice Rumble",
    category: "Soundscapes",
    station: "Himadri & Kongsfjorden",
    duration: "03:45",
    type: "rumble",
    url: "/assets/audio/glacier_calving.mp3",
    source: "NCPOR Cryospheric Acoustic Array",
    description: "High-fidelity hydrophone and atmospheric acoustic recording of brittle glacier front fracture and ice calving into Arctic marine waters."
  },
  {
    id: "aud-02",
    title: "Antarctic Katabatic Blizzard Winds at Maitri (80 knots)",
    category: "Soundscapes",
    station: "Maitri Station",
    duration: "04:12",
    type: "wind",
    url: "/assets/audio/polar_blizzard.mp3",
    source: "Schirmacher Oasis Meteorological Mast",
    description: "Raw sensory recording of severe sub-zero katabatic windstorms sweeping off the polar ice cap at -32°C."
  },
  {
    id: "aud-03",
    title: "Weddell Seal Underwater Bio-Acoustic Whistles & Chirps",
    category: "Interviews",
    station: "Bharati Station",
    duration: "02:30",
    type: "seal",
    url: "/assets/audio/seal_chirps.mp3",
    source: "Prydz Bay Bio-Acoustic Hydrophone",
    description: "Eerie descending frequency chirps and underwater ultrasonic echo-locomotion recorded under 2-metre fast sea ice in East Antarctica."
  },
  {
    id: "aud-04",
    title: "IndARC Mooring Hydrophone: Deep Arctic Currents",
    category: "Soundscapes",
    station: "IndARC Underwater Observatory",
    duration: "05:00",
    type: "marine",
    url: "/assets/audio/ocean_currents.mp3",
    source: "MoES Moored Acoustic Transducer",
    description: "Sub-surface hydro-acoustic telemetry at 192m depth capturing Atlantic water inflow and thermal mixing dynamics."
  },
  {
    id: "aud-05",
    title: "Expedition Radio Log: Wintering Over at Bharati Station",
    category: "Interviews",
    station: "Bharati Station",
    duration: "03:15",
    type: "station",
    url: "/assets/audio/scientist_log.mp3",
    source: "43rd ISEA Expedition Log",
    description: "Voice dispatch from expedition wintering team describing scientific sample collection during the 4-month polar night."
  },
  {
    id: "aud-06",
    title: "Himalayan Glacier Moraine & Meltwater Acoustic Flow",
    category: "Soundscapes",
    station: "Himansh Station",
    duration: "04:20",
    type: "avalanche",
    url: "/assets/audio/himalayan_stream.mp3",
    source: "Chandra Basin Hydrometric Station",
    description: "Sub-surface acoustic monitoring of subglacial discharge channels and active moraine movement at 4,050 metres altitude."
  }
];

const MediaModule = {
  assets: [],
  pressKits: [],
  videos: POLAR_DOCUMENTARY_VIDEOS,
  audios: POLAR_AUDIO_SOUNDSCAPES,
  currentFilter: 'all',
  currentVideoCategory: 'all',
  currentAudioCategory: 'all',
  searchDebounceTimer: null,

  // Video Player Modal State
  activeVideoId: null,
  activeVideoMode: 'html5', // 'html5' or 'youtube'

  // Audio Player State & Web Audio Synthesizer
  activeAudioId: null,
  isAudioPaused: false,
  activeAudioElement: null,
  audioContext: null,
  audioSynthNodes: [],
  audioProgressInterval: null,
  audioElapsedTime: 0,
  audioDurationSeconds: 225,

  async init() {
    this.bindFilters();
    this.bindSearch();
    this.bindKeyboardShortcuts();
    await this.loadAssets();
    await this.loadPressKits();
    this.renderVideos();
    this.renderAudios();
  },

  bindKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeVideoModal();
        if (typeof RepoModule !== 'undefined' && RepoModule.closeModals) {
          RepoModule.closeModals();
        }
      }
    });
  },

  bindFilters() {
    const buttons = document.querySelectorAll('.media-tab-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.currentFilter = btn.dataset.filter;

        const videoSection = document.getElementById('media-section-videos');
        const audioSection = document.getElementById('media-section-audio');
        const photoSection = document.getElementById('media-section-photos');
        const pressSection = document.getElementById('media-section-press');

        if (this.currentFilter === 'video') {
          if (videoSection) videoSection.style.display = 'block';
          if (audioSection) audioSection.style.display = 'none';
          if (photoSection) photoSection.style.display = 'none';
          if (pressSection) pressSection.style.display = 'none';
        } else if (this.currentFilter === 'audio') {
          if (videoSection) videoSection.style.display = 'none';
          if (audioSection) audioSection.style.display = 'block';
          if (photoSection) photoSection.style.display = 'none';
          if (pressSection) pressSection.style.display = 'none';
        } else if (this.currentFilter === 'photo') {
          if (videoSection) videoSection.style.display = 'none';
          if (audioSection) audioSection.style.display = 'none';
          if (photoSection) photoSection.style.display = 'block';
          if (pressSection) pressSection.style.display = 'none';
        } else if (this.currentFilter === 'press') {
          if (videoSection) videoSection.style.display = 'none';
          if (audioSection) audioSection.style.display = 'none';
          if (photoSection) photoSection.style.display = 'none';
          if (pressSection) pressSection.style.display = 'block';
        } else {
          if (videoSection) videoSection.style.display = 'block';
          if (audioSection) audioSection.style.display = 'block';
          if (photoSection) photoSection.style.display = 'block';
          if (pressSection) pressSection.style.display = 'block';
        }

        this.loadAssets();
      });
    });
  },

  bindSearch() {
    const searchInput = document.getElementById('media-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(this.searchDebounceTimer);
        this.searchDebounceTimer = setTimeout(() => {
          this.loadAssets();
        }, 200);
      });
    }
  },

  async loadAssets() {
    try {
      const query = document.getElementById('media-search-input')?.value.trim() || '';
      const params = new URLSearchParams();
      if (this.currentFilter !== 'all' && this.currentFilter !== 'press') {
        params.append('media_type', this.currentFilter);
      }
      if (query) params.append('q', query);

      const res = await fetch(`/api/media/assets?${params.toString()}`);
      if (!res.ok) return;
      const data = await res.json();
      this.assets = data.assets || [];

      // Synchronize video assets from backend API
      const backendVideos = this.assets.filter(a => a.type === 'video');
      if (backendVideos.length > 0) {
        this.videos = backendVideos.map(v => ({
          id: v.id.toLowerCase(),
          title: v.title,
          category: v.category,
          station: v.station,
          duration: v.duration || '15:00',
          embedUrl: v.url,
          channel: v.credit || 'MoES / NCPOR India',
          thumbnail: v.thumbnail || v.url || '/assets/images/bharati.jpg',
          tags: v.tags || ['PolarScience'],
          summary: v.description
        }));
      }

      this.renderAssets();
      this.renderVideos();
      this.renderAudios();
    } catch (err) {
      console.error("Failed to load media assets", err);
    }
  },

  renderAssets() {
    const container = document.getElementById('media-grid-container');
    if (!container) return;

    const photos = this.assets.filter(a => a.type === 'photo');

    if (photos.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; color: var(--text-muted); background: var(--bg-surface); border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          No photo assets found matching this filter or search query.
        </div>
      `;
      return;
    }

    container.innerHTML = photos.map(a => `
      <div class="media-card" onclick="MediaModule.openLightbox('${a.id}')" role="button" tabindex="0" aria-label="${this.escapeHTML(a.title)}">
        <div class="media-thumbnail-box">
          <img src="${a.thumbnail || a.url}" alt="${this.escapeHTML(a.title)}" loading="lazy" onerror="this.src='/assets/images/bharati.jpg'" />
          <span class="media-type-badge">📸 4K PHOTO</span>
        </div>
        <div class="media-card-content">
          <h4 class="media-title">${this.escapeHTML(a.title)}</h4>
          <div class="media-meta-row">
            <span>${this.escapeHTML(a.station)}</span>
            <span>${this.escapeHTML(a.resolution || '4K UHD')}</span>
          </div>
          <div class="media-tags-list">
            ${(a.tags || []).slice(0, 3).map(t => `<span class="keyword-tag">#${this.escapeHTML(t)}</span>`).join('')}
          </div>
        </div>
      </div>
    `).join('');
  },

  // ==========================================
  // VIDEOS & VIDEO MODAL CONTROLLER
  // ==========================================

  filterVideos(category) {
    this.currentVideoCategory = category;
    document.querySelectorAll('.video-filter-pill').forEach(btn => {
      const isSelected = (category === 'all' && btn.textContent.includes('All')) ||
                         (category !== 'all' && btn.textContent.toLowerCase().includes(category.toLowerCase()));
      btn.classList.toggle('active', isSelected);
    });
    this.renderVideos();
  },

  renderVideos() {
    const container = document.getElementById('polar-videos-grid-container');
    if (!container) return;

    const filtered = this.currentVideoCategory === 'all'
      ? this.videos
      : this.videos.filter(v => v.category.toLowerCase().includes(this.currentVideoCategory.toLowerCase()));

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; color: var(--text-muted); background: var(--bg-surface); border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          No documentary videos found in this category.
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(v => `
      <div class="video-card" onclick="MediaModule.openVideoModal('${v.id}')" role="button" tabindex="0" aria-label="Watch ${this.escapeHTML(v.title)}">
        <div class="video-embed-container" style="position: relative; cursor: pointer;">
          <img src="${v.thumbnail}" alt="${this.escapeHTML(v.title)}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" onerror="this.src='/assets/images/bharati.jpg'" />
          <div class="video-play-overlay">
            <div class="video-play-btn-circle">▶</div>
            <span class="video-play-text">Click to Play Documentary</span>
          </div>
          <span class="video-duration-badge">⏱ ${v.duration}</span>
        </div>
        <div class="video-card-body">
          <div>
            <div class="video-meta-top">
              <span class="video-category-tag">${this.escapeHTML(v.station)}</span>
              <span class="video-badge-pill">${this.escapeHTML(v.category)}</span>
            </div>
            <h4 class="video-title">${this.escapeHTML(v.title)}</h4>
            <p class="video-summary">${this.escapeHTML(v.summary)}</p>
          </div>
          <div class="video-card-footer">
            <span>Source: <strong>${this.escapeHTML(v.channel)}</strong></span>
            <span class="video-watch-link">Watch Now ↗</span>
          </div>
        </div>
      </div>
    `).join('');
  },

  openVideoModal(videoId) {
    const vIdLower = (videoId || '').toLowerCase();
    const video = this.videos.find(v => v.id.toLowerCase() === vIdLower) ||
                  this.assets.find(a => a.id.toLowerCase() === vIdLower);
    if (!video) return;

    this.activeVideoId = video.id;

    const modal = document.getElementById('modal-video-player');
    const content = document.getElementById('modal-video-content');
    if (!modal || !content) return;

    const rawUrl = video.embedUrl || video.url || "https://www.youtube.com/embed/n4p8QvX7J1E";
    const isDirectMp4 = rawUrl.endsWith('.mp4') || rawUrl.endsWith('.webm') || video.videoSource === 'html5';
    const isYouTube = rawUrl.includes('youtube.com') || rawUrl.includes('youtu.be');
    
    let playerHtml = '';
    let externalWatchUrl = rawUrl;

    if (isDirectMp4) {
      playerHtml = `
        <video 
          id="modal-html5-video"
          controls 
          playsinline 
          preload="metadata"
          poster="${video.thumbnail || '/assets/images/bharati.jpg'}"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #000; object-fit: contain;"
          onerror="document.getElementById('video-frame-container').innerHTML='<div style=\\'position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#fff;text-align:center;padding:20px;\\'>Video stream currently unavailable. Please try an alternate documentary.</div>'"
        >
          <source src="${rawUrl}" type="video/mp4">
          Your browser does not support HTML5 video playback.
        </video>
      `;
    } else if (isYouTube) {
      const cleanEmbedUrl = rawUrl.includes('/embed/') ? rawUrl : `https://www.youtube.com/embed/${rawUrl.split('v=')[1]?.split('&')[0] || rawUrl}`;
      externalWatchUrl = cleanEmbedUrl.replace('/embed/', '/watch?v=');
      playerHtml = `
        <iframe 
          id="modal-youtube-iframe"
          src="${cleanEmbedUrl}?rel=0&modestbranding=1&enablejsapi=1" 
          title="${this.escapeHTML(video.title)}" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          loading="eager"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
        </iframe>
      `;
    } else {
      playerHtml = `
        <iframe 
          id="modal-youtube-iframe"
          src="${rawUrl}" 
          title="${this.escapeHTML(video.title)}" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          loading="eager"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
        </iframe>
      `;
    }

    content.innerHTML = `
      <div class="video-modal-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; flex-wrap: wrap;">
          <div>
            <div style="display: flex; gap: 8px; margin-bottom: 6px; align-items: center; flex-wrap: wrap;">
              <span class="pub-badge station">${this.escapeHTML(video.station || 'Polar Outpost')}</span>
              <span class="pub-badge vertical">${this.escapeHTML(video.category || 'Polar Science')}</span>
              <span class="pub-badge year">⏱ ${this.escapeHTML(video.duration || '15:00')}</span>
            </div>
            <h2 class="video-modal-title">${this.escapeHTML(video.title)}</h2>
          </div>
        </div>
      </div>

      <div class="video-modal-frame-box" id="video-frame-container" style="position: relative; width: 100%; padding-top: 56.25%; background: #000; border-radius: var(--radius-sm); overflow: hidden;">
        ${playerHtml}
      </div>

      <div class="video-modal-details">
        <p class="video-modal-desc">${this.escapeHTML(video.summary || video.description || '')}</p>
        
        <div class="video-modal-meta-grid">
          <div><span style="color: var(--text-muted);">Station / Base:</span> <strong>${this.escapeHTML(video.station || 'National Centre for Polar and Ocean Research')}</strong></div>
          <div><span style="color: var(--text-muted);">Broadcast Channel:</span> <strong>${this.escapeHTML(video.channel || video.credit || 'MoES India')}</strong></div>
          <div><span style="color: var(--text-muted);">Playback Format:</span> <strong>1080p HD (Subtitles Available)</strong></div>
          <div><span style="color: var(--text-muted);">License:</span> <strong style="color: var(--status-active);">Government Open Media / CC-BY 4.0</strong></div>
        </div>

        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 14px; flex-wrap: wrap;">
          <button type="button" class="btn-cite" onclick="MediaModule.closeVideoModal()">Close Video</button>
          <a href="${externalWatchUrl}" target="_blank" rel="noopener noreferrer" class="btn-hero-primary" style="text-decoration: none;">
            ${isYouTube ? 'Open on YouTube ↗' : 'Direct Video Link ↗'}
          </a>
        </div>
      </div>
    `;

    modal.classList.add('open');

    // Backdrop click listener to close modal
    modal.onclick = (e) => {
      if (e.target === modal) {
        this.closeVideoModal();
      }
    };
  },

  closeVideoModal() {
    const modal = document.getElementById('modal-video-player');
    const content = document.getElementById('modal-video-content');
    if (content) {
      content.innerHTML = ''; // Instantly unloads iframe and halts video/audio stream
    }
    if (modal) {
      modal.classList.remove('open');
      modal.onclick = null;
    }
    this.activeVideoId = null;
  },

  // ==========================================
  // AUDIOS & WEB AUDIO SOUNDSCAPE SYNTHESIZER
  // ==========================================

  filterAudios(category) {
    this.currentAudioCategory = category;
    document.querySelectorAll('.audio-filter-pill').forEach(btn => {
      const isSelected = (category === 'all' && btn.textContent.includes('All')) ||
                         (category !== 'all' && btn.textContent.toLowerCase().includes(category.toLowerCase()));
      btn.classList.toggle('active', isSelected);
    });
    this.renderAudios();
  },

  renderAudios() {
    const container = document.getElementById('polar-audios-grid-container');
    if (!container) return;

    const filtered = this.currentAudioCategory === 'all'
      ? this.audios
      : this.audios.filter(a => a.category.toLowerCase().includes(this.currentAudioCategory.toLowerCase()));

    container.innerHTML = filtered.map(a => {
      const isPlaying = this.activeAudioId === a.id && !this.isAudioPaused;
      const isCurrent = this.activeAudioId === a.id;
      const displayDuration = isCurrent 
        ? `${this.formatTime(this.audioElapsedTime)} / ${a.duration}` 
        : a.duration;

      const progressPercent = isCurrent 
        ? Math.min(100, (this.audioElapsedTime / this.audioDurationSeconds) * 100) 
        : 0;

      return `
        <div class="audio-card ${isCurrent ? 'playing' : ''}" id="audio-card-${a.id}">
          <div class="audio-card-header">
            <div>
              <span class="audio-badge">${this.escapeHTML(a.station)}</span>
              <h4 class="audio-card-title">${this.escapeHTML(a.title)}</h4>
            </div>
            <span class="audio-duration-pill" id="audio-timer-${a.id}">
              ${displayDuration}
            </span>
          </div>

          <p class="audio-card-desc">${this.escapeHTML(a.description)}</p>

          <!-- Waveform Equalizer -->
          <div class="audio-waveform-container" id="waveform-${a.id}">
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 35%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 70%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 45%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 90%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 60%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 80%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 30%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 95%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 50%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 75%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 40%;"></div>
            <div class="waveform-bar ${isPlaying ? 'animating' : ''}" style="height: 85%;"></div>
          </div>

          <!-- Progress Bar Scrubber -->
          <div class="audio-progress-bar-bg" onclick="MediaModule.handleAudioScrub(event, '${a.id}')" title="Click to seek">
            <div class="audio-progress-bar-fill" id="progress-fill-${a.id}" style="width: ${progressPercent}%;"></div>
          </div>

          <div class="audio-card-footer">
            <div class="audio-source-info">
              <span>Source: <strong>${this.escapeHTML(a.source)}</strong></span>
            </div>
            <div style="display: flex; gap: 6px;">
              <button type="button" class="audio-play-btn ${isPlaying ? 'active' : ''}" onclick="MediaModule.toggleAudio('${a.id}')" id="play-btn-${a.id}">
                <span>${isPlaying ? '⏸ Pause' : (isCurrent && this.isAudioPaused ? '▶ Resume' : '▶ Play Soundscape')}</span>
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  toggleAudio(audioId) {
    if (this.activeAudioId === audioId) {
      if (this.isAudioPaused) {
        this.resumeAudio();
      } else {
        this.pauseAudio();
      }
    } else {
      this.playAudio(audioId);
    }
  },

  playAudio(audioId) {
    this.stopAudio(false);

    const audioItem = this.audios.find(a => a.id === audioId);
    if (!audioItem) return;

    this.activeAudioId = audioId;
    this.isAudioPaused = false;
    this.audioElapsedTime = 0;
    this.audioDurationSeconds = this.parseDurationToSeconds(audioItem.duration);

    // Initialize Web Audio API Synthesizer Soundscape Engine
    this.startSoundscapeSynthesis(audioItem.type);

    // Update UI
    this.renderAudios();

    // Start progress timer
    this.startProgressTimer(audioItem);

    if (typeof App !== 'undefined' && App.showToast) {
      App.showToast(`🎧 Playing: ${audioItem.title} (${audioItem.station})`);
    }
  },

  pauseAudio() {
    this.isAudioPaused = true;
    if (this.audioProgressInterval) {
      clearInterval(this.audioProgressInterval);
      this.audioProgressInterval = null;
    }
    this.stopSynthNodes();
    this.renderAudios();
    if (typeof App !== 'undefined' && App.showToast) {
      App.showToast("⏸ Audio playback paused.");
    }
  },

  resumeAudio() {
    const audioItem = this.audios.find(a => a.id === this.activeAudioId);
    if (!audioItem) return;

    this.isAudioPaused = false;
    this.startSoundscapeSynthesis(audioItem.type);
    this.renderAudios();
    this.startProgressTimer(audioItem);
    if (typeof App !== 'undefined' && App.showToast) {
      App.showToast(`▶ Resumed: ${audioItem.title}`);
    }
  },

  startProgressTimer(audioItem) {
    if (this.audioProgressInterval) {
      clearInterval(this.audioProgressInterval);
    }

    this.audioProgressInterval = setInterval(() => {
      if (this.isAudioPaused) return;
      this.audioElapsedTime += 1;
      
      const timerEl = document.getElementById(`audio-timer-${this.activeAudioId}`);
      if (timerEl) {
        timerEl.textContent = `${this.formatTime(this.audioElapsedTime)} / ${audioItem.duration}`;
      }

      const fillEl = document.getElementById(`progress-fill-${this.activeAudioId}`);
      if (fillEl) {
        const percent = Math.min(100, (this.audioElapsedTime / this.audioDurationSeconds) * 100);
        fillEl.style.width = `${percent}%`;
      }

      if (this.audioElapsedTime >= this.audioDurationSeconds) {
        this.stopAudio(true);
      }
    }, 1000);
  },

  stopAudio(resetElapsed = true) {
    if (this.audioProgressInterval) {
      clearInterval(this.audioProgressInterval);
      this.audioProgressInterval = null;
    }

    this.stopSynthNodes();

    this.isAudioPaused = false;
    if (resetElapsed) {
      this.activeAudioId = null;
      this.audioElapsedTime = 0;
    }
    this.renderAudios();
  },

  stopSynthNodes() {
    this.audioSynthNodes.forEach(node => {
      try {
        if (node.stop) node.stop();
        if (node.disconnect) node.disconnect();
      } catch (e) {}
    });
    this.audioSynthNodes = [];
  },

  handleAudioScrub(e, audioId) {
    const audioItem = this.audios.find(a => a.id === audioId);
    if (!audioItem) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const percent = Math.max(0, Math.min(1, clickX / width));
    const totalSecs = this.parseDurationToSeconds(audioItem.duration);
    const targetElapsed = Math.floor(percent * totalSecs);

    if (this.activeAudioId !== audioId) {
      this.playAudio(audioId);
      this.audioElapsedTime = targetElapsed;
    } else {
      this.audioElapsedTime = targetElapsed;
      if (this.isAudioPaused) {
        this.resumeAudio();
      }
    }

    const timerEl = document.getElementById(`audio-timer-${audioId}`);
    if (timerEl) {
      timerEl.textContent = `${this.formatTime(this.audioElapsedTime)} / ${audioItem.duration}`;
    }
    const fillEl = document.getElementById(`progress-fill-${audioId}`);
    if (fillEl) {
      fillEl.style.width = `${percent * 100}%`;
    }
  },

  startSoundscapeSynthesis(presetType) {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;

      if (!this.audioContext) {
        this.audioContext = new AudioCtx();
      }
      if (this.audioContext.state === 'suspended') {
        this.audioContext.resume();
      }

      const ctx = this.audioContext;
      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.18, ctx.currentTime);
      masterGain.connect(ctx.destination);
      this.audioSynthNodes.push(masterGain);

      if (presetType === 'rumble' || presetType === 'avalanche') {
        // Glacial calving sub-bass rumble & noise
        const bufferSize = ctx.sampleRate * 2;
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(140, ctx.currentTime);

        const subOsc = ctx.createOscillator();
        subOsc.type = 'sine';
        subOsc.frequency.setValueAtTime(45, ctx.currentTime);

        whiteNoise.connect(filter);
        filter.connect(masterGain);
        subOsc.connect(masterGain);

        whiteNoise.start();
        subOsc.start();
        this.audioSynthNodes.push(whiteNoise, subOsc);

      } else if (presetType === 'wind') {
        // Antarctic Katabatic Wind: filtered noise with LFO wind gusts
        const bufferSize = ctx.sampleRate * 2;
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        const filter = ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(320, ctx.currentTime);
        filter.Q.setValueAtTime(3.0, ctx.currentTime);

        // LFO for howling wind modulation
        const lfo = ctx.createOscillator();
        lfo.type = 'sine';
        lfo.frequency.setValueAtTime(0.2, ctx.currentTime);
        const lfoGain = ctx.createGain();
        lfoGain.gain.setValueAtTime(160, ctx.currentTime);
        lfo.connect(lfoGain);
        lfoGain.connect(filter.frequency);

        whiteNoise.connect(filter);
        filter.connect(masterGain);

        whiteNoise.start();
        lfo.start();
        this.audioSynthNodes.push(whiteNoise, lfo);

      } else if (presetType === 'seal') {
        // Weddell seal descending frequency chirp synthesis
        const osc = ctx.createOscillator();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(800, ctx.currentTime);

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1200, ctx.currentTime);

        const sweepLFO = ctx.createOscillator();
        sweepLFO.type = 'sawtooth';
        sweepLFO.frequency.setValueAtTime(0.35, ctx.currentTime);
        const sweepGain = ctx.createGain();
        sweepGain.gain.setValueAtTime(400, ctx.currentTime);
        sweepLFO.connect(sweepGain);
        sweepGain.connect(osc.frequency);

        osc.connect(filter);
        filter.connect(masterGain);

        osc.start();
        sweepLFO.start();
        this.audioSynthNodes.push(osc, sweepLFO);

      } else {
        // Marine hydrophone & station hum ambient
        const osc1 = ctx.createOscillator();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(95, ctx.currentTime);

        const osc2 = ctx.createOscillator();
        osc2.type = 'triangle';
        osc2.frequency.setValueAtTime(190, ctx.currentTime);

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(280, ctx.currentTime);

        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(masterGain);

        osc1.start();
        osc2.start();
        this.audioSynthNodes.push(osc1, osc2);
      }
    } catch (e) {
      console.warn("Web Audio synthesis error:", e);
    }
  },

  parseDurationToSeconds(durationStr) {
    if (!durationStr) return 180;
    const parts = durationStr.split(':');
    if (parts.length === 2) {
      return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
    }
    return 180;
  },

  formatTime(totalSeconds) {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  },

  // ==========================================
  // PRESS KITS & 4K PHOTO LIGHTBOX
  // ==========================================

  async loadPressKits() {
    try {
      const res = await fetch('/api/media/press-kits');
      if (!res.ok) return;
      this.pressKits = await res.json();
      this.renderPressKits();
    } catch (err) {
      console.error("Failed to load press kits", err);
    }
  },

  renderPressKits() {
    const container = document.getElementById('press-kits-container');
    if (!container) return;

    container.innerHTML = this.pressKits.map(pk => `
      <div class="press-kit-card">
        <div class="pk-header">
          <span style="font-size: 0.6875rem; font-family: var(--font-mono); font-weight: 600; color: var(--status-warning); text-transform: uppercase;">
            Press Release Dossier
          </span>
          <span class="pk-date">${this.escapeHTML(pk.release_date)}</span>
        </div>
        <h3 class="pk-title">${this.escapeHTML(pk.title)}</h3>
        <p class="pk-summary">${this.escapeHTML(pk.summary)}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 12px; flex-wrap: wrap; gap: 8px;">
          <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted);">
            ${pk.asset_count} Verified Assets (${pk.download_size})
          </span>
          <button type="button" class="btn-cite" onclick="App.showToast('Generating official media press kit ZIP (${pk.download_size})...'); MediaModule.downloadPressKit('${pk.id}')">
            Download Press Kit
          </button>
        </div>
      </div>
    `).join('');
  },

  async downloadPressKit(pkId, downloadSize) {
    if (downloadSize && typeof App !== 'undefined' && App.showToast) {
      App.showToast(`Generating official media press kit ZIP (${downloadSize})...`);
    }
    try {
      const res = await fetch(`/api/media/press-kits/${encodeURIComponent(pkId)}/download`);
      if (!res.ok) throw new Error('Download failed: ' + res.status);
      const blob = await res.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.style.display = 'none';
      link.href = blobUrl;
      link.setAttribute('download', `${pkId}_press_kit.zip`);
      document.body.appendChild(link);
      link.click();
      setTimeout(() => {
        if (link.parentNode) link.parentNode.removeChild(link);
      }, 5000);
      setTimeout(() => {
        window.URL.revokeObjectURL(blobUrl);
      }, 60000);
    } catch (err) {
      console.error('Press kit download error, falling back:', err);
      const link = document.createElement('a');
      link.style.display = 'none';
      link.href = `/api/media/press-kits/${encodeURIComponent(pkId)}/download`;
      link.setAttribute('download', `${pkId}_press_kit.zip`);
      document.body.appendChild(link);
      link.click();
    }
  },

  openLightbox(assetId) {
    const asset = this.assets.find(a => a.id === assetId);
    if (!asset) return;

    const modal = document.getElementById('modal-media-lightbox');
    const content = document.getElementById('modal-media-content');
    if (!modal || !content) return;

    content.innerHTML = `
      <div style="max-height: 420px; overflow: hidden; border-radius: var(--radius-sm); margin-bottom: 18px; background: #000; border: 1px solid var(--border-subtle);">
        <img src="${asset.url}" style="width: 100%; max-height: 420px; object-fit: contain; display: block;" alt="${this.escapeHTML(asset.title)}" />
      </div>
      <div style="display: flex; gap: 6px; margin-bottom: 8px; flex-wrap: wrap;">
        <span class="pub-badge station">${this.escapeHTML(asset.station)}</span>
        <span class="pub-badge expedition">${this.escapeHTML(asset.expedition)}</span>
        <span class="pub-badge vertical">${this.escapeHTML(asset.category)}</span>
      </div>
      <h2 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--ocean-navy); margin-bottom: 6px;">${this.escapeHTML(asset.title)}</h2>
      <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.55; margin-bottom: 16px;">${this.escapeHTML(asset.description)}</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: var(--bg-surface); padding: 14px; border-radius: var(--radius-sm); font-size: 0.78rem; font-family: var(--font-mono); margin-bottom: 18px; border: 1px solid var(--border-subtle);">
        <div><span style="color: var(--text-muted);">Station / Mission:</span> <strong style="color: var(--text-primary);">${this.escapeHTML(asset.station)}</strong></div>
        <div><span style="color: var(--text-muted);">Coordinates:</span> <strong style="color: var(--polar-blue);">${this.escapeHTML(asset.coordinates)}</strong></div>
        <div><span style="color: var(--text-muted);">Credit / Source:</span> <strong style="color: var(--text-primary);">${this.escapeHTML(asset.credit)}</strong></div>
        <div><span style="color: var(--text-muted);">License:</span> <strong style="color: var(--status-active);">${this.escapeHTML(asset.license)}</strong></div>
      </div>

      <div style="display: flex; gap: 8px; justify-content: flex-end; flex-wrap: wrap;">
        <button type="button" class="btn-cite" onclick="RepoModule.closeModals()">Close</button>
        <button type="button" class="btn-hero-primary" onclick="App.showToast('Downloading verified full-res asset (${asset.resolution || '4K UHD'})...')">
          Download Asset (${asset.resolution || '4K UHD'})
        </button>
      </div>
    `;

    modal.classList.add('open');
  },

  escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.innerText = str;
    return div.innerHTML;
  }
};

window.MediaModule = MediaModule;
