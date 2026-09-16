/**
 * ai-chat.js - Floating Conversational Polar Science AI Assistant Module
 * Features:
 *  - Floating interactive chatbot with launcher button and responsive modal
 *  - Multi-turn conversation memory with context and pronoun resolution
 *  - Dynamic natural science answering across all polar domains
 *  - Grounded RAG citations and verifiable NCPOR publication references
 *  - Animated typing indicator with pulsating live state
 *  - Robust error handling with retry capability
 *  - Enter key to submit, session reset / clear chat
 *  - Clickable sample prompt chips and progressive follow-up questions
 */

const AIChatModule = {
  isWaiting: false,
  chatHistory: [], // [{ role: 'user', content: '...' }, { role: 'assistant', content: '...' }]
  aiProvider: 'NCPOR Polar Science AI',

  async init() {
    this.bindChatInputs();
    this.bindSampleChips();
    this.bindResetButton();
    await this.checkAIStatus();
  },

  /**
   * Toggle the floating chat widget open/closed
   */
  toggleChat() {
    const widget = document.getElementById('floating-chat-widget');
    if (!widget) return;
    if (widget.classList.contains('active')) {
      this.closeChat();
    } else {
      this.openChat();
    }
  },

  /**
   * Open the floating chat widget and focus input
   */
  openChat() {
    const widget = document.getElementById('floating-chat-widget');
    const btn = document.getElementById('floating-chat-btn');
    if (widget) {
      widget.classList.add('active');
      widget.setAttribute('aria-hidden', 'false');
    }
    if (btn) {
      btn.classList.add('active');
    }
    setTimeout(() => {
      const input = document.getElementById('chat-user-input');
      if (input) input.focus();
    }, 150);
  },

  /**
   * Close / minimize the floating chat widget
   */
  closeChat() {
    const widget = document.getElementById('floating-chat-widget');
    const btn = document.getElementById('floating-chat-btn');
    if (widget) {
      widget.classList.remove('active');
      widget.setAttribute('aria-hidden', 'true');
    }
    if (btn) {
      btn.classList.remove('active');
    }
  },

  /**
   * Check backend AI status and provider name
   */
  async checkAIStatus() {
    try {
      const res = await fetch('/api/ai/status');
      if (res.ok) {
        const data = await res.json();
        this.aiProvider = data.provider || 'NCPOR Polar Science AI';
        const statusEl = document.getElementById('chat-provider-badge');
        if (statusEl) {
          statusEl.textContent = `● ${this.aiProvider}`;
        }
      }
    } catch (err) {
      console.warn("AI status check skipped", err);
    }
  },

  bindChatInputs() {
    const sendBtn = document.getElementById('chat-send-btn');
    const input = document.getElementById('chat-user-input');

    if (sendBtn) {
      sendBtn.addEventListener('click', () => this.handleSendMessage());
    }

    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.handleSendMessage();
        }
      });
    }
  },

  bindSampleChips() {
    document.querySelectorAll('.sample-query-chip, .fchat-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const queryText = chip.dataset.query || chip.textContent.trim();
        if (!queryText) return;
        this.handleChipClick(queryText);
      });
    });
  },

  handleChipClick(promptText) {
    this.openChat();
    const input = document.getElementById('chat-user-input');
    if (input) {
      input.value = promptText;
      this.handleSendMessage();
    }
  },

  bindResetButton() {
    const resetBtn = document.getElementById('btn-reset-chat');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.clearChat());
    }
  },

  clearChat() {
    this.chatHistory = [];
    const container = document.getElementById('chat-messages-container');
    if (container) {
      container.innerHTML = `
        <div class="chat-msg ai">
          <div class="ai-msg-header">
            <span class="ai-tag">NCPOR POLAR AI</span>
            <span class="ai-status">● Session Reset</span>
          </div>
          <div class="ai-response-body">
            <p>
              Chat session cleared! You can ask any question about India's polar research, Antarctic stations, Arctic expeditions, Southern Ocean, glaciology, or polar wildlife.
            </p>
          </div>
        </div>
      `;
      if (typeof App !== 'undefined' && App.showToast) {
        App.showToast("Chat session and conversation memory cleared.");
      }
    }
  },

  askFollowUp(questionText) {
    this.openChat();
    const input = document.getElementById('chat-user-input');
    if (input) {
      input.value = questionText;
      this.handleSendMessage();
    }
  },

  openWithPrompt(promptText) {
    this.openChat();
    const input = document.getElementById('chat-user-input');
    if (input) {
      input.value = promptText || '';
      input.focus();
    }
  },

  async handleSendMessage(retryQuery = null) {
    if (this.isWaiting) return;
    
    // Automatically make sure the chat drawer is visible/open so the user can see the response
    this.openChat();

    const input = document.getElementById('chat-user-input');
    const query = retryQuery || (input ? input.value.trim() : '');
    
    // Prevent sending empty queries
    if (!query) {
      if (typeof App !== 'undefined' && App.showToast) {
        App.showToast("Please type a question to ask Polar AI.");
      }
      if (input) input.focus();
      return;
    }

    if (!retryQuery && input) {
      input.value = '';
    }

    this.appendUserMessage(query);
    const loadingId = this.appendLoadingIndicator();
    this.isWaiting = true;

    try {
      const res = await fetch('/api/ai/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          history: this.chatHistory,
          audience: 'general'
        })
      });

      const loadingElem = document.getElementById(loadingId);
      if (loadingElem) loadingElem.remove();

      if (!res.ok) {
        if (res.status === 404) {
          throw new Error("AI endpoint not found (HTTP 404). Please ensure the backend router is active at /api/ai/ask.");
        } else if (res.status === 500) {
          throw new Error("Internal AI service error (HTTP 500). Please try again or rephrase your inquiry.");
        } else {
          throw new Error(`Server returned HTTP ${res.status}`);
        }
      }

      const data = await res.json();
      if (!data || typeof data.answer !== 'string') {
        throw new Error("Received invalid or empty response from Polar AI backend.");
      }

      // Append to multi-turn conversation memory
      this.chatHistory.push({ role: 'user', content: query });
      this.chatHistory.push({ role: 'assistant', content: data.answer || '' });

      // Keep maximum 16 turns in client memory to keep payloads efficient
      if (this.chatHistory.length > 16) {
        this.chatHistory = this.chatHistory.slice(-16);
      }

      this.renderAIResponse(data);
    } catch (err) {
      console.error("AI Chat failed:", err);
      const loadingElem = document.getElementById(loadingId);
      if (loadingElem) loadingElem.remove();

      this.renderErrorResponse(query, err.message || "Network communication issue with AI backend");
    } finally {
      this.isWaiting = false;
      const inputEl = document.getElementById('chat-user-input');
      if (inputEl) inputEl.focus();
    }
  },

  appendUserMessage(text) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msg = document.createElement('div');
    msg.className = 'chat-msg user';
    msg.innerHTML = `<div>${this.escapeHTML(text)}</div>`;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
  },

  appendLoadingIndicator() {
    const container = document.getElementById('chat-messages-container');
    if (!container) return null;

    const id = `loading-${Date.now()}`;
    const skeleton = document.createElement('div');
    skeleton.id = id;
    skeleton.className = 'chat-msg ai loading';
    skeleton.innerHTML = `
      <div class="ai-typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-text">Polar AI is thinking and synthesizing response...</span>
      </div>
    `;
    container.appendChild(skeleton);
    container.scrollTop = container.scrollHeight;
    return id;
  },

  renderAIResponse(data) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msg = document.createElement('div');
    msg.className = 'chat-msg ai';

    const formattedAnswer = this.formatMarkdown(data.answer || '');

    let citationsHTML = '';
    if (data.citations && data.citations.length > 0) {
      citationsHTML = `
        <div class="ai-citations-box">
          <span class="citations-title">Verified NCPOR Grounding Sources:</span>
          <div class="citations-list">
            ${data.citations.map(c => `
              <span class="citation-chip" title="View in research repository" onclick="App.switchTab('repository'); AIChatModule.closeChat();">
                📄 ${this.escapeHTML(c)}
              </span>
            `).join('')}
          </div>
        </div>
      `;
    }

    let outOfScopeNotice = '';
    if (data.in_scope === false) {
      outOfScopeNotice = `
        <div class="ai-domain-notice">
          <strong>Scientific Domain Scope:</strong> To preserve institutional accuracy, questions unrelated to polar science, oceanography, or cryospheric research are declined.
        </div>
      `;
    }

    let followUpsHTML = '';
    if (data.suggested_questions && data.suggested_questions.length > 0) {
      followUpsHTML = `
        <div class="ai-followups-box">
          <span class="followups-title">Suggested Follow-up Inquiries:</span>
          <div class="followups-list">
            ${data.suggested_questions.map(q => `
              <button type="button" class="follow-up-chip" onclick="AIChatModule.askFollowUp('${this.escapeHTML(q).replace(/'/g, "\\'")}')">
                ${this.escapeHTML(q)}
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }

    const providerLabel = data.provider || this.aiProvider;

    msg.innerHTML = `
      <div class="ai-msg-header">
        <div style="display: flex; align-items: center; gap: 6px;">
          <span class="ai-tag">NCPOR POLAR AI</span>
          <span class="ai-status">${data.in_scope !== false ? '● Grounded' : '▲ Domain Scope'}</span>
        </div>
        <span class="ai-provider">${this.escapeHTML(providerLabel)}</span>
      </div>
      <div class="ai-response-body">
        ${formattedAnswer}
      </div>
      ${outOfScopeNotice}
      ${citationsHTML}
      ${followUpsHTML}
    `;

    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
  },

  renderErrorResponse(failedQuery, errorMsg) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msg = document.createElement('div');
    msg.className = 'chat-msg ai error';
    msg.innerHTML = `
      <div class="ai-msg-header">
        <span class="ai-tag error">AI SERVICE NOTICE</span>
      </div>
      <div class="ai-error-body">
        Unable to complete AI response (${this.escapeHTML(errorMsg)}). Please verify backend connectivity.
      </div>
      <button type="button" class="btn-chat-retry" onclick="AIChatModule.handleSendMessage('${this.escapeHTML(failedQuery).replace(/'/g, "\\'")}')">
        ↻ Retry Question
      </button>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
  },

  formatMarkdown(text) {
    if (!text) return '';
    
    let html = this.escapeHTML(text);

    // Markdown tables parsing
    const tableRegex = /((?:\|[^\n]+\|\r?\n?)+)/g;
    html = html.replace(tableRegex, (tableMatch) => {
      const rows = tableMatch.trim().split(/\r?\n/).filter(r => r.includes('|'));
      if (rows.length < 2) return tableMatch;
      
      let tableHtml = '<div class="ai-table-wrapper"><table class="ai-table">';
      let isHeader = true;

      for (let i = 0; i < rows.length; i++) {
        const row = rows[i].trim();
        if (/^\|[\s\-:|]+\|$/.test(row)) {
          isHeader = false;
          continue;
        }
        const cells = row.split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        if (cells.length === 0) continue;

        if (isHeader) {
          tableHtml += '<thead><tr>' + cells.map(c => `<th>${c}</th>`).join('') + '</tr></thead><tbody>';
          isHeader = false;
        } else {
          tableHtml += '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
        }
      }
      tableHtml += '</tbody></table></div>';
      return tableHtml;
    });

    // Headings: ### H3, ## H2, # H1
    html = html.replace(/^###\s+(.*)$/gm, '<h4 class="ai-heading-3">$1</h4>');
    html = html.replace(/^##\s+(.*)$/gm, '<h3 class="ai-heading-2">$1</h3>');

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic: *text*
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Code: `code`
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Bullet points
    html = html.replace(/^[•\-\*]\s+(.*)$/gm, '<li>$1</li>');

    // Numbered lists
    html = html.replace(/^(\d+)\.\s+(.*)$/gm, '<li>$2</li>');

    // Wrap consecutive list items in <ul>
    html = html.replace(/(<li>.*?<\/li>(\s*<li>.*?<\/li>)*)/g, '<ul class="ai-list">$1</ul>');

    // Paragraphs / linebreaks
    html = html.replace(/\n\n+/g, '</p><p>');
    html = html.replace(/\n/g, '<br/>');

    // Clean up paragraph wrappers around div tables/headings
    html = html.replace(/<p>\s*<\/p>/g, '');
    html = html.replace(/<p>(<div class="ai-table-wrapper">[\s\S]*?<\/div>)<\/p>/g, '$1');
    html = html.replace(/<p>(<h[2-4][^>]*>[\s\S]*?<\/h[2-4]>)<\/p>/g, '$1');

    return `<p>${html}</p>`;
  },

  escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.innerText = str;
    return div.innerHTML;
  }
};

window.AIChatModule = AIChatModule;
