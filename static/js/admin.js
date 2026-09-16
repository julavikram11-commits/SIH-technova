/**
 * admin.js - Unified Admin CMS & Governance Workflow Module (Integration Layer)
 * Implements the complete management dashboard:
 * 1. Portal Overview & KPIs
 * 2. Governance Moderation Queue (Approve & Publish Live)
 * 3. Manage Research Resources (View/Delete)
 * 4. Manage Media Assets (View/Delete/Add)
 * 5. Manage Outreach Announcements (View/Delete/Add)
 * 6. Researcher Ingestion Workbench (NLP Auto-Enrichment)
 */

const AdminModule = {
  queue: [],
  overview: {},
  resources: [],
  media: [],
  events: [],

  init() {
    this.bindAdminTabs();
    this.bindFormActions();
    this.loadOverview();
    this.loadQueue();
  },

  onActivate() {
    this.loadOverview();
    this.loadQueue();
  },

  bindAdminTabs() {
    const tabs = document.querySelectorAll('.admin-tab-btn');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.dataset.adminTab;

        // Hide all sub-panels
        document.querySelectorAll('.admin-sub-panel').forEach(panel => {
          panel.style.display = 'none';
        });

        // Show target sub-panel
        const targetPanel = document.getElementById(`admin-tab-${target}`);
        if (targetPanel) targetPanel.style.display = 'block';

        // Load data on tab activate
        if (target === 'overview') this.loadOverview();
        if (target === 'queue') this.loadQueue();
        if (target === 'resources') this.loadResources();
        if (target === 'media') this.loadMedia();
        if (target === 'outreach') this.loadOutreach();
      });
    });
  },

  // ================= 1. Overview & KPIs =================
  async loadOverview() {
    try {
      const res = await fetch('/api/admin/overview');
      if (!res.ok) return;
      this.overview = await res.json();
      this.renderOverview();
    } catch (err) {
      console.error("Failed to load overview KPIs", err);
    }
  },

  renderOverview() {
    const container = document.getElementById('admin-kpi-grid-container');
    if (!container) return;

    container.innerHTML = `
      <div class="admin-kpi-card">
        <div class="admin-kpi-val">${this.overview.total_publications || 0}</div>
        <div class="admin-kpi-label">Research Publications</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val">${this.overview.total_datasets || 0}</div>
        <div class="admin-kpi-label">Open Datasets (GODL)</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val">${this.overview.total_media_assets || 0}</div>
        <div class="admin-kpi-label">Verified Media Assets</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val">${this.overview.total_outreach_articles || 0}</div>
        <div class="admin-kpi-label">Outreach Briefings</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val" style="color: var(--status-active);">${this.overview.active_stations || 4}</div>
        <div class="admin-kpi-label">Active Polar Bases</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val" style="color: var(--status-warning);">${this.overview.pending_queue_count || 0}</div>
        <div class="admin-kpi-label">Pending Governance Queue</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val">${this.overview.total_downloads || '14,890'}</div>
        <div class="admin-kpi-label">Total Data Downloads</div>
      </div>
      <div class="admin-kpi-card">
        <div class="admin-kpi-val" style="color: var(--polar-cyan);">${this.overview.rag_queries_answered || '3,412'}</div>
        <div class="admin-kpi-label">RAG Grounded Inquiries</div>
      </div>
    `;
  },

  // ================= 2. Governance & Review Queue =================
  async loadQueue() {
    try {
      const res = await fetch('/api/admin/queue');
      if (!res.ok) return;
      this.queue = await res.json();
      this.renderQueue();
    } catch (err) {
      console.error("Failed to load admin queue", err);
    }
  },

  renderQueue() {
    const tbody = document.getElementById('admin-queue-tbody');
    if (!tbody) return;

    if (this.queue.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">Queue is currently clear.</td></tr>`;
      return;
    }

    tbody.innerHTML = this.queue.map(item => `
      <tr>
        <td>
          <strong style="color: var(--text-primary);">${item.title}</strong>
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">
            ID: ${item.id} • ${item.type} • Submitter: ${item.submitter}
          </div>
          <div style="font-size: 0.75rem; color: var(--polar-cyan); margin-top: 4px;">
            AI Plain Summary: "${item.plain_summary}"
          </div>
        </td>
        <td>
          <span class="pub-badge station">${item.station}</span>
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 2px;">${item.expedition}</div>
        </td>
        <td>
          <div style="display: flex; gap: 4px; flex-wrap: wrap;">
            ${item.ai_suggested_tags.map(t => `<span class="keyword-tag">#${t}</span>`).join('')}
          </div>
        </td>
        <td>
          <span class="status-badge ${item.status}">
            ${item.status === 'PUBLISHED' ? 'PUBLISHED' : item.status === 'APPROVED' ? 'APPROVED' : 'PENDING REVIEW'}
          </span>
          <div style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 2px;">${item.gigw_compliance}</div>
        </td>
        <td>
          ${item.status !== 'PUBLISHED' ? `
            <button type="button" class="btn-approve-publish" onclick="AdminModule.approveItem('${item.id}')">
              Approve & Publish
            </button>
          ` : `
            <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--status-active); font-weight: 600;">
              Active Live
            </span>
          `}
        </td>
      </tr>
    `).join('');
  },

  async approveItem(subId) {
    try {
      const res = await fetch(`/api/admin/approve/${subId}`, { method: 'POST' });
      if (!res.ok) return;
      const data = await res.json();
      App.showToast(`"${data.published_item.title}" approved and published across Knowledge Repository & Outreach.`);
      await this.loadQueue();
      await this.loadOverview();
      if (window.RepoModule) await RepoModule.loadPublications();
    } catch (err) {
      console.error("Approve failed", err);
      App.showToast("Failed to approve item.");
    }
  },

  // ================= 3. Manage Research Resources =================
  async loadResources() {
    try {
      const res = await fetch('/api/repository/publications');
      if (!res.ok) return;
      const data = await res.json();
      this.resources = data.publications;
      this.renderResources();
    } catch (err) {
      console.error("Failed to load resources", err);
    }
  },

  renderResources() {
    const tbody = document.getElementById('admin-resources-tbody');
    if (!tbody) return;

    tbody.innerHTML = this.resources.map(r => `
      <tr>
        <td>
          <strong style="color: var(--text-primary);">${r.title}</strong>
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">ID: ${r.id} • DOI: ${r.doi}</div>
        </td>
        <td><span class="pub-badge station">${r.station}</span></td>
        <td>${r.vertical}</td>
        <td style="font-family: var(--font-mono);">${r.year}</td>
        <td>
          <button type="button" class="btn-delete" onclick="AdminModule.deletePublication('${r.id}')">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  },

  async deletePublication(pubId) {
    if (!confirm(`Are you sure you want to remove publication ${pubId} from the repository?`)) return;
    try {
      const res = await fetch(`/api/repository/publications/${pubId}`, { method: 'DELETE' });
      if (!res.ok) return;
      App.showToast(`Publication ${pubId} removed.`);
      await this.loadResources();
      await this.loadOverview();
      if (window.RepoModule) {
        RepoModule.cachedPublications = [];
        await RepoModule.loadPublications();
      }
    } catch (err) {
      console.error("Delete failed", err);
    }
  },

  // ================= 4. Manage Media Assets =================
  async loadMedia() {
    try {
      const res = await fetch('/api/media/assets');
      if (!res.ok) return;
      const data = await res.json();
      this.media = data.assets;
      this.renderMediaTable();
    } catch (err) {
      console.error("Failed to load media", err);
    }
  },

  renderMediaTable() {
    const tbody = document.getElementById('admin-media-tbody');
    if (!tbody) return;

    tbody.innerHTML = this.media.map(m => `
      <tr>
        <td>
          <strong style="color: var(--text-primary);">${m.title}</strong>
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">ID: ${m.id} • ${m.category}</div>
        </td>
        <td><span class="pub-badge expedition">${m.type.toUpperCase()}</span></td>
        <td>${m.station}</td>
        <td><span style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--status-active);">${m.license}</span></td>
        <td>
          <button type="button" class="btn-delete" onclick="AdminModule.deleteMedia('${m.id}')">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  },

  async deleteMedia(assetId) {
    if (!confirm(`Remove media asset ${assetId}?`)) return;
    try {
      const res = await fetch(`/api/media/assets/${assetId}`, { method: 'DELETE' });
      if (!res.ok) return;
      App.showToast(`Media asset ${assetId} deleted.`);
      await this.loadMedia();
      await this.loadOverview();
      if (window.MediaModule) await MediaModule.loadAssets();
    } catch (err) {
      console.error("Delete failed", err);
    }
  },

  // ================= 5. Manage Outreach & Events =================
  async loadOutreach() {
    try {
      const res = await fetch('/api/outreach/events');
      if (!res.ok) return;
      this.events = await res.json();
      this.renderOutreachEvents();
    } catch (err) {
      console.error("Failed to load events", err);
    }
  },

  renderOutreachEvents() {
    const tbody = document.getElementById('admin-events-tbody');
    if (!tbody) return;

    tbody.innerHTML = this.events.map(e => `
      <tr>
        <td>
          <strong style="color: var(--text-primary);">${e.title}</strong>
          <div style="font-size: 0.72rem; color: var(--text-muted);">${e.summary}</div>
        </td>
        <td style="font-family: var(--font-mono); font-size: 0.75rem;">${e.date}</td>
        <td><span class="pub-badge vertical">${e.category}</span></td>
        <td><span style="color: var(--status-active); font-family: var(--font-mono); font-size: 0.75rem;">${e.status}</span></td>
        <td>
          <button type="button" class="btn-delete" onclick="AdminModule.deleteEvent('${e.id}')">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  },

  async deleteEvent(eventId) {
    if (!confirm(`Remove event ${eventId}?`)) return;
    try {
      const res = await fetch(`/api/outreach/events/${eventId}`, { method: 'DELETE' });
      if (!res.ok) return;
      App.showToast(`Event ${eventId} removed.`);
      await this.loadOutreach();
      await this.loadOverview();
      if (window.OutreachModule) await OutreachModule.loadEvents();
    } catch (err) {
      console.error("Delete failed", err);
    }
  },

  // ================= 6. Submission Form & AI Auto-Enrich =================
  bindFormActions() {
    const aiEnrichBtn = document.getElementById('btn-ai-auto-tag');
    const form = document.getElementById('new-submission-form');
    const newMediaForm = document.getElementById('new-media-form');
    const newEventForm = document.getElementById('new-event-form');

    if (aiEnrichBtn) {
      aiEnrichBtn.addEventListener('click', async () => {
        const title = document.getElementById('sub-title')?.value.trim();
        const content = document.getElementById('sub-abstract')?.value.trim();

        if (!title || !content) {
          App.showToast("Please provide Title and Abstract for NLP analysis.");
          return;
        }

        App.showToast("Extracting NLP Taxonomy & Plain-Language Summary...");
        try {
          const res = await fetch('/api/ai/suggest-tags', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
          });

          if (!res.ok) return;
          const data = await res.json();

          const tagsField = document.getElementById('sub-tags');
          const summaryField = document.getElementById('sub-summary');

          if (tagsField) tagsField.value = data.suggested_tags.join(', ');
          if (summaryField) summaryField.value = data.auto_summary;

          App.showToast("NLP Taxonomy extraction & summary populated.");
        } catch (err) {
          console.error("NLP Auto-tagging failed", err);
        }
      });
    }

    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('sub-title').value.trim();
        const submitter = document.getElementById('sub-author').value.trim();
        const expedition = document.getElementById('sub-expedition').value;
        const station = document.getElementById('sub-station').value;
        const type = document.getElementById('sub-type').value;
        const abstractContent = document.getElementById('sub-abstract').value.trim();
        const tagsRaw = document.getElementById('sub-tags').value.trim();
        const plainSummary = document.getElementById('sub-summary').value.trim();

        const tags = tagsRaw ? tagsRaw.split(',').map(t => t.trim()) : ["Polar Science"];

        try {
          const res = await fetch('/api/admin/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title,
              submitter,
              expedition,
              station,
              type,
              abstract_content: abstractContent,
              tags,
              plain_summary: plainSummary
            })
          });

          if (!res.ok) return;
          App.showToast(`Submitted "${title}" to Governance Moderation Queue.`);
          form.reset();

          document.querySelector('[data-admin-tab="queue"]').click();
          await this.loadQueue();
          await this.loadOverview();
        } catch (err) {
          console.error("Submission failed", err);
        }
      });
    }

    // New Media Asset Form
    if (newMediaForm) {
      newMediaForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('media-new-title').value.trim();
        const type = document.getElementById('media-new-type').value;
        const category = document.getElementById('media-new-category').value.trim();
        const station = document.getElementById('media-new-station').value;
        const expedition = document.getElementById('media-new-expedition').value.trim();
        const credit = document.getElementById('media-new-credit').value.trim();
        const desc = document.getElementById('media-new-desc').value.trim();

        try {
          const res = await fetch('/api/media/assets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title,
              type,
              category,
              station,
              expedition,
              location: "Expedition Location Recorded",
              coordinates: "Polar Coordinates",
              credit,
              description: desc,
              license: "Government Open Access / CC-BY 4.0"
            })
          });

          if (!res.ok) return;
          App.showToast(`Media asset "${title}" registered.`);
          newMediaForm.reset();
          await this.loadMedia();
          await this.loadOverview();
          if (window.MediaModule) await MediaModule.loadAssets();
        } catch (err) {
          console.error("Add media failed", err);
        }
      });
    }

    // New Event / Announcement Form
    if (newEventForm) {
      newEventForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('evt-new-title').value.trim();
        const date = document.getElementById('evt-new-date').value;
        const category = document.getElementById('evt-new-category').value;
        const summary = document.getElementById('evt-new-summary').value.trim();

        try {
          const res = await fetch('/api/outreach/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title,
              date,
              category,
              summary,
              status: "Active / Upcoming"
            })
          });

          if (!res.ok) return;
          App.showToast(`Announcement "${title}" published.`);
          newEventForm.reset();
          await this.loadOutreach();
          await this.loadOverview();
          if (window.OutreachModule) await OutreachModule.loadEvents();
        } catch (err) {
          console.error("Add event failed", err);
        }
      });
    }
  }
};

window.AdminModule = AdminModule;
