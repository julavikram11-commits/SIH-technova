/**
 * repository.js - Structured Polar Knowledge Repository Module (Pillar 2)
 * Handles Faceted Search, Sorting, Academic Citation Records, Resource Registration, AI Summaries, and Datasets.
 */

const RepoModule = {
  publications: [],
  datasets: [],
  searchDebounceTimer: null,
  cachedPublications: [],

  async init() {
    this.bindSearchAndFilters();
    this.bindAddResourceForm();
    await this.loadPublications();
    await this.loadDatasets();
  },

  bindSearchAndFilters() {
    const searchInput = document.getElementById('repo-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(this.searchDebounceTimer);
        this.searchDebounceTimer = setTimeout(() => {
          this.loadPublications();
        }, 200);
      });
    }

    const stationFilter = document.getElementById('repo-filter-station');
    const verticalFilter = document.getElementById('repo-filter-vertical');
    const yearFilter = document.getElementById('repo-filter-year');
    const sortFilter = document.getElementById('repo-filter-sort');

    [stationFilter, verticalFilter, yearFilter, sortFilter].forEach(el => {
      if (el) el.addEventListener('change', () => this.loadPublications());
    });
  },

  filterByStation(stationName) {
    const filter = document.getElementById('repo-filter-station');
    if (filter) {
      filter.value = stationName;
      this.loadPublications();
    }
  },

  async loadPublications() {
    const query = document.getElementById('repo-search-input')?.value.trim() || '';
    const station = document.getElementById('repo-filter-station')?.value || '';
    const vertical = document.getElementById('repo-filter-vertical')?.value || '';
    const year = document.getElementById('repo-filter-year')?.value || '';
    const sortBy = document.getElementById('repo-filter-sort')?.value || 'newest';

    // Instant client-side filtering if cache exists
    if (this.cachedPublications.length > 0) {
      let filtered = [...this.cachedPublications];
      const q = query.toLowerCase();

      if (q) {
        filtered = filtered.filter(p => {
          const haystack = `${p.title} ${p.abstract} ${(p.keywords || []).join(' ')} ${p.authors} ${p.station} ${p.vertical} ${p.expedition}`.toLowerCase();
          return haystack.includes(q);
        });
      }

      if (station) {
        filtered = filtered.filter(p => (p.station || '').toLowerCase().includes(station.toLowerCase()));
      }

      if (vertical) {
        filtered = filtered.filter(p => (p.vertical || '').toLowerCase().includes(vertical.toLowerCase()));
      }

      if (year) {
        filtered = filtered.filter(p => String(p.year) === String(year));
      }

      // Sort
      if (sortBy === 'oldest') {
        filtered.sort((a, b) => a.year - b.year);
      } else if (sortBy === 'citations') {
        filtered.sort((a, b) => (b.citation_count || 0) - (a.citation_count || 0));
      } else if (sortBy === 'title') {
        filtered.sort((a, b) => a.title.localeCompare(b.title));
      } else {
        filtered.sort((a, b) => b.year - a.year);
      }

      this.publications = filtered;
      this.renderPublications(filtered.length);
      return;
    }

    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (station) params.append('station', station);
    if (vertical) params.append('vertical', vertical);
    if (year) params.append('year', year);
    if (sortBy) params.append('sort_by', sortBy);

    try {
      const res = await fetch(`/api/repository/publications?${params.toString()}`);
      if (!res.ok) return;
      const data = await res.json();
      this.publications = data.publications;
      if (!query && !station && !vertical && !year) {
        this.cachedPublications = [...data.publications];
      }
      this.renderPublications(data.count);
    } catch (err) {
      console.error("Failed to load publications", err);
    }
  },

  renderPublications(totalCount) {
    const container = document.getElementById('publications-list-container');
    const countBadge = document.getElementById('repo-results-count');
    if (countBadge) countBadge.textContent = `${totalCount} Peer-Reviewed Publications Indexed`;
    if (!container) return;

    if (this.publications.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 48px 20px; background: var(--bg-surface); border-radius: var(--radius-md); border: 1px dashed var(--border-medium);">
          <h4 style="font-size: 1rem; color: var(--text-primary); margin-bottom: 4px;">No matching research publications found</h4>
          <p style="font-size: 0.8125rem; color: var(--text-muted);">Refine your search keywords or reset discipline/station filters.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = this.publications.map(p => `
      <article class="pub-card" aria-label="${p.title}">
        <div class="pub-badges-row">
          <span class="pub-badge station">${p.station}</span>
          <span class="pub-badge expedition">${p.expedition}</span>
          <span class="pub-badge vertical">${p.vertical}</span>
          <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); margin-left: auto;">
            ${p.year} • ${p.citation_count || 0} Citations
          </span>
        </div>

        <h3 class="pub-title" style="cursor: pointer;" onclick="RepoModule.openDetailsModal('${p.id}')">
          ${p.title}
        </h3>
        <p class="pub-authors">${p.authors} <span style="color: var(--text-muted);">(${p.affiliation || 'NCPOR, Ministry of Earth Sciences'})</span></p>
        <p class="pub-abstract">${p.abstract}</p>

        <div class="pub-keywords">
          ${p.keywords.map(kw => `<span class="keyword-tag">#${kw}</span>`).join('')}
        </div>

        <div class="pub-actions">
          <button type="button" class="btn-explain-ai" onclick="RepoModule.openExplainModal('${p.id}')">
            Plain-Language AI Breakdown
          </button>
          <button type="button" class="btn-cite" onclick="RepoModule.openDetailsModal('${p.id}')">
            Full Metadata
          </button>
          <button type="button" class="btn-cite" onclick="RepoModule.openCitationModal('${p.id}')">
            BibTeX Citation
          </button>
          <span class="doi-link">DOI: ${p.doi}</span>
        </div>
      </article>
    `).join('');
  },

  openDetailsModal(pubId) {
    const pub = this.publications.find(p => p.id === pubId);
    if (!pub) return;

    const modal = document.getElementById('modal-explain-paper');
    const content = document.getElementById('modal-explain-content');
    if (!modal || !content) return;

    content.innerHTML = `
      <div style="display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap;">
        <span class="pub-badge station">${pub.station}</span>
        <span class="pub-badge expedition">${pub.expedition}</span>
        <span class="pub-badge vertical">${pub.vertical}</span>
      </div>

      <h2 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--text-primary); margin-bottom: 8px; line-height: 1.3;">
        ${pub.title}
      </h2>
      <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 2px;">
        <strong>Authors:</strong> ${pub.authors}
      </p>
      <p style="font-size: 0.8125rem; color: var(--text-muted); margin-bottom: 16px;">
        <strong>Affiliation:</strong> ${pub.affiliation || 'National Centre for Polar and Ocean Research, Goa'}
      </p>

      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 18px;">
        <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--polar-cyan); text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
          Technical Abstract
        </h4>
        <p style="font-size: 0.875rem; color: var(--text-primary); line-height: 1.6;">${pub.abstract}</p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; font-size: 0.78rem; font-family: var(--font-mono); background: var(--bg-surface); padding: 14px; border-radius: var(--radius-sm); margin-bottom: 18px; border: 1px solid var(--border-subtle);">
        <div><span style="color: var(--text-muted);">Publication ID:</span> <strong style="color: var(--text-primary);">${pub.id}</strong></div>
        <div><span style="color: var(--text-muted);">Year:</span> <strong style="color: var(--text-primary);">${pub.year}</strong></div>
        <div><span style="color: var(--text-muted);">DOI:</span> <strong style="color: var(--polar-cyan);">${pub.doi}</strong></div>
        <div><span style="color: var(--text-muted);">Dataset:</span> <strong style="color: var(--status-active);">${pub.dataset_attached || 'Annexed'}</strong></div>
      </div>

      <div style="display: flex; gap: 8px; justify-content: flex-end; flex-wrap: wrap;">
        <button type="button" class="btn-explain-ai" onclick="RepoModule.openExplainModal('${pub.id}')">
          Plain-Language AI Breakdown
        </button>
        <button type="button" class="btn-cite" onclick="RepoModule.openCitationModal('${pub.id}')">
          Export Citation (BibTeX)
        </button>
        <button type="button" class="btn-cite" onclick="RepoModule.downloadPublication('${pub.id}')">
          Download Publication
        </button>
      </div>
    `;

    modal.classList.add('open');
  },

  openAddResourceModal() {
    const modal = document.getElementById('modal-add-resource');
    if (modal) modal.classList.add('open');
  },

  bindAddResourceForm() {
    const form = document.getElementById('add-resource-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const title = document.getElementById('new-pub-title').value.trim();
      const authors = document.getElementById('new-pub-authors').value.trim();
      const station = document.getElementById('new-pub-station').value;
      const expedition = document.getElementById('new-pub-expedition').value;
      const vertical = document.getElementById('new-pub-vertical').value;
      const year = parseInt(document.getElementById('new-pub-year').value, 10) || 2024;
      const abstract = document.getElementById('new-pub-abstract').value.trim();
      const keywordsRaw = document.getElementById('new-pub-keywords').value.trim();

      const keywords = keywordsRaw ? keywordsRaw.split(',').map(k => k.trim()) : ["Polar Science", "NCPOR"];

      try {
        const res = await fetch('/api/repository/publications', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title,
            authors,
            station,
            expedition,
            vertical,
            year,
            abstract,
            keywords
          })
        });

        if (!res.ok) return;
        App.showToast(`"${title}" successfully cataloged in the Knowledge Repository.`);
        form.reset();
        this.closeModals();
        this.cachedPublications = [];
        await this.loadPublications();
      } catch (err) {
        console.error("Failed to add resource", err);
        App.showToast("Error adding research resource.");
      }
    });
  },

  async loadDatasets() {
    try {
      const res = await fetch('/api/repository/datasets');
      if (!res.ok) return;
      this.datasets = await res.json();
      this.renderDatasets();
    } catch (err) {
      console.error("Failed to load datasets", err);
    }
  },

  renderDatasets() {
    const tbody = document.getElementById('datasets-table-body');
    if (!tbody) return;

    tbody.innerHTML = this.datasets.map(d => `
      <tr>
        <td>
          <strong style="color: var(--text-primary);">${d.title}</strong>
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted);">ID: ${d.id} • ${d.published_date}</div>
          <div style="font-size: 0.72rem; color: var(--polar-cyan); margin-top: 2px;">
            Params: ${d.parameters.slice(0, 3).join(', ')}...
          </div>
        </td>
        <td><span class="pub-badge station">${d.station}</span></td>
        <td><span style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--polar-cyan);">${d.format}</span></td>
        <td style="font-family: var(--font-mono);">${d.records_count}</td>
        <td><span style="font-size: 0.75rem; color: var(--status-active); font-family: var(--font-mono);">${d.license}</span></td>
        <td>
          <button type="button" class="btn-cite" onclick="RepoModule.downloadDataset('${d.id}')">
            Download (${d.size})
          </button>
        </td>
      </tr>
    `).join('');
  },

  async openExplainModal(pubId) {
    const modal = document.getElementById('modal-explain-paper');
    const content = document.getElementById('modal-explain-content');
    if (!modal || !content) return;

    content.innerHTML = `
      <div style="text-align: center; padding: 36px 20px;">
        <p style="color: var(--polar-cyan); font-size: 0.9rem; font-family: var(--font-mono);">Synthesizing plain-language summary & climate significance...</p>
      </div>
    `;
    modal.classList.add('open');

    try {
      const res = await fetch(`/api/repository/explain/${pubId}`);
      if (!res.ok) return;
      const data = await res.json();

      content.innerHTML = `
        <div style="display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap;">
          <span class="pub-badge station">${data.station}</span>
          <span class="pub-badge expedition">${data.expedition}</span>
        </div>
        <h2 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--text-primary); margin-bottom: 14px; line-height: 1.3;">
          ${data.title}
        </h2>

        <div style="background: var(--bg-surface); border-left: 3px solid var(--polar-cyan); padding: 14px; border-radius: var(--radius-sm); margin-bottom: 16px;">
          <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--polar-cyan); text-transform: uppercase; margin-bottom: 4px;">
            Plain-Language Summary (Citizen & Outreach)
          </h4>
          <p style="font-size: 0.875rem; color: var(--text-primary); line-height: 1.6;">
            ${data.layman_summary}
          </p>
        </div>

        <div style="margin-bottom: 16px;">
          <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">
            Scientific Research Question
          </h4>
          <p style="font-size: 0.84375rem; color: var(--text-secondary); line-height: 1.5;">
            ${data.research_question}
          </p>
        </div>

        <div style="margin-bottom: 16px;">
          <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">
            Key Discoveries
          </h4>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px;">
            ${data.key_discoveries.map(kd => `
              <li style="display: flex; gap: 8px; font-size: 0.8125rem; color: var(--text-secondary);">
                <span style="color: var(--status-active); font-weight: 700;">✓</span> ${kd}
              </li>
            `).join('')}
          </ul>
        </div>

        <div style="background: var(--bg-surface); border-left: 3px solid var(--status-warning); padding: 12px; border-radius: var(--radius-sm);">
          <h4 style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--status-warning); text-transform: uppercase; margin-bottom: 4px;">
            Societal & National Relevance
          </h4>
          <p style="font-size: 0.8125rem; color: var(--text-secondary); line-height: 1.5;">
            ${data.why_it_matters_to_citizens}
          </p>
        </div>
      `;
    } catch (err) {
      content.innerHTML = `<p style="color: var(--status-alert);">Failed to generate AI breakdown.</p>`;
    }
  },

  async openCitationModal(pubId) {
    const modal = document.getElementById('modal-citation');
    const content = document.getElementById('modal-citation-content');
    if (!modal || !content) return;

    modal.classList.add('open');
    content.innerHTML = `<p style="color: var(--text-secondary); font-size: 0.85rem;">Generating citation records...</p>`;

    try {
      const res = await fetch(`/api/repository/citation/${pubId}`);
      if (!res.ok) return;
      const data = await res.json();

      content.innerHTML = `
        <h3 style="font-family: var(--font-heading); font-size: 1.25rem; margin-bottom: 14px; color: var(--text-primary);">Export Citation</h3>
        
        <div style="margin-bottom: 16px;">
          <label style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); font-weight: 600; text-transform: uppercase;">APA Format</label>
          <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 12px; border-radius: var(--radius-sm); font-size: 0.8125rem; color: var(--text-secondary); margin-top: 4px; line-height: 1.5;">
            ${data.apa}
          </div>
          <button type="button" class="btn-cite" style="margin-top: 6px; font-size: 0.75rem;" onclick="navigator.clipboard.writeText(\`${data.apa}\`); App.showToast('APA Citation copied to clipboard.');">Copy APA</button>
        </div>

        <div>
          <label style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); font-weight: 600; text-transform: uppercase;">BibTeX Format</label>
          <pre style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 12px; border-radius: var(--radius-sm); font-size: 0.75rem; font-family: var(--font-mono); color: var(--polar-cyan); margin-top: 4px; overflow-x: auto;">${data.bibtex}</pre>
          <button type="button" class="btn-cite" style="margin-top: 6px; font-size: 0.75rem;" onclick="navigator.clipboard.writeText(\`${data.bibtex}\`); App.showToast('BibTeX record copied to clipboard.');">Copy BibTeX</button>
        </div>
      `;
    } catch (err) {
      content.innerHTML = `<p style="color: var(--status-alert);">Error generating citation formats.</p>`;
    }
  },

  downloadDataset(datasetId) {
    if (!datasetId) return;
    window.location.href = `/api/repository/download/${encodeURIComponent(datasetId)}`;
  },

  downloadPublication(pubId) {
    if (!pubId) return;
    window.location.href = `/api/repository/publication/${encodeURIComponent(pubId)}/download`;
  },

  closeModals() {
    document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('open'));
  }
};

window.RepoModule = RepoModule;
