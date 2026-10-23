// State Management
let currentTopic = 'technology';
let currentIsCategory = true;
let isJsonView = false;
let currentRawData = null;

// DOM Elements
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const categoryChips = document.getElementById('category-chips');
const newsGrid = document.getElementById('news-grid');
const jsonView = document.getElementById('json-view');
const jsonCode = document.getElementById('json-code');
const currentQueryTitle = document.getElementById('current-query-title');
const resultsCount = document.getElementById('results-count');
const errorBanner = document.getElementById('error-banner');
const errorTitle = document.getElementById('error-title');
const errorMessage = document.getElementById('error-message');
const errorRetryBtn = document.getElementById('error-retry-btn');
const refreshBtn = document.getElementById('refresh-btn');
const viewModeToggle = document.getElementById('view-mode-toggle');
const viewModeText = document.getElementById('view-mode-text');
const copyJsonBtn = document.getElementById('copy-json-btn');
const copyText = document.getElementById('copy-text');
const apiStatusBadge = document.getElementById('api-status-badge');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  fetchNews(currentTopic, currentIsCategory);
});

function setupEventListeners() {
  // Search Form Submit
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;

    // Remove active class from all chips
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));

    currentTopic = query;
    currentIsCategory = false;
    fetchNews(currentTopic, currentIsCategory);
  });

  // Category Chip Clicks
  categoryChips.addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;

    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');

    searchInput.value = '';
    currentTopic = chip.dataset.category;
    currentIsCategory = true;
    fetchNews(currentTopic, currentIsCategory);
  });

  // Refresh Button
  refreshBtn.addEventListener('click', () => {
    fetchNews(currentTopic, currentIsCategory);
  });

  // Error Retry
  errorRetryBtn.addEventListener('click', () => {
    fetchNews(currentTopic, currentIsCategory);
  });

  // View Mode Toggle (Cards vs Raw JSON)
  viewModeToggle.addEventListener('click', toggleViewMode);

  // Copy JSON
  copyJsonBtn.addEventListener('click', copyJsonToClipboard);
}

// Fetch News from Backend API
async function fetchNews(topic, isCategory) {
  renderSkeletons();
  hideError();

  const titlePrefix = isCategory ? 'Top Headlines:' : 'Search Results for:';
  currentQueryTitle.textContent = `${titlePrefix} "${topic.charAt(0).toUpperCase() + topic.slice(1)}"`;

  try {
    const url = `/api/news?topic=${encodeURIComponent(topic)}&is_category=${isCategory}`;
    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || `Server responded with status ${response.status}`);
    }

    currentRawData = data.raw || data;
    jsonCode.textContent = JSON.stringify(currentRawData, null, 2);

    const articles = data.articles || [];
    resultsCount.textContent = `${articles.length} Article${articles.length === 1 ? '' : 's'}`;

    if (articles.length === 0) {
      showError(
        'No Articles Found',
        `We couldn't find any recent headlines for "${topic}". Try another search term or topic!`
      );
      newsGrid.innerHTML = '';
      return;
    }

    renderArticles(articles);
    updateApiStatus(true);
  } catch (err) {
    console.error('Fetch error:', err);
    showError('Error Loading News', err.message || 'Unable to connect to the news server.');
    newsGrid.innerHTML = '';
    updateApiStatus(false);
  }
}

// Render Articles to Grid
function renderArticles(articles) {
  newsGrid.innerHTML = articles.map((article, index) => {
    const publishedDate = article.publishedAt 
      ? new Date(article.publishedAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
      : 'Recently';

    const imageHtml = article.urlToImage
      ? `<img src="${escapeHtml(article.urlToImage)}" alt="${escapeHtml(article.title)}" loading="lazy" onerror="this.onerror=null; this.parentElement.innerHTML = getPlaceholderHtml();">`
      : getPlaceholderHtml();

    return `
      <article class="article-card" id="article-${index + 1}">
        <div class="card-media">
          <span class="source-badge">${escapeHtml(article.source || 'News')}</span>
          ${imageHtml}
        </div>
        <div class="card-body">
          <div class="card-meta">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span>${publishedDate}</span>
          </div>
          <h3 class="article-title">${escapeHtml(article.title)}</h3>
          <p class="article-description">${escapeHtml(article.description || 'No description available for this headline.')}</p>
          <div class="card-footer">
            <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener noreferrer" class="read-btn" id="link-article-${index + 1}">
              <span>Read Full Story</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// Render Skeleton Loading States
function renderSkeletons() {
  newsGrid.innerHTML = Array(5).fill(0).map(() => `
    <div class="skeleton-card" aria-hidden="true">
      <div class="skeleton-img"></div>
      <div class="card-body">
        <div class="skeleton-text skeleton-title"></div>
        <div class="skeleton-text skeleton-desc-1"></div>
        <div class="skeleton-text skeleton-desc-2"></div>
      </div>
    </div>
  `).join('');
}

// Helper: Media Placeholder
function getPlaceholderHtml() {
  return `
    <div class="card-media-placeholder">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
        <circle cx="9" cy="9" r="2"/>
        <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
      </svg>
    </div>
  `;
}

// Toggle View Mode (News vs JSON)
function toggleViewMode() {
  isJsonView = !isJsonView;
  if (isJsonView) {
    newsGrid.classList.add('hidden');
    jsonView.classList.remove('hidden');
    viewModeText.textContent = 'View News Cards';
  } else {
    jsonView.classList.add('hidden');
    newsGrid.classList.remove('hidden');
    viewModeText.textContent = 'View Raw JSON';
  }
}

// Copy JSON
async function copyJsonToClipboard() {
  if (!currentRawData) return;
  try {
    await navigator.clipboard.writeText(JSON.stringify(currentRawData, null, 2));
    copyText.textContent = 'Copied!';
    setTimeout(() => {
      copyText.textContent = 'Copy JSON';
    }, 2000);
  } catch (err) {
    console.error('Clipboard copy failed:', err);
  }
}

// Status & Error Handlers
function showError(title, message) {
  errorTitle.textContent = title;
  errorMessage.textContent = message;
  errorBanner.classList.remove('hidden');
}

function hideError() {
  errorBanner.classList.add('hidden');
}

function updateApiStatus(isOnline) {
  if (isOnline) {
    apiStatusBadge.style.background = 'rgba(16, 185, 129, 0.12)';
    apiStatusBadge.style.color = '#10b981';
    apiStatusBadge.querySelector('.status-label').textContent = 'NewsAPI Live';
  } else {
    apiStatusBadge.style.background = 'rgba(244, 63, 94, 0.12)';
    apiStatusBadge.style.color = '#f43f5e';
    apiStatusBadge.querySelector('.status-label').textContent = 'API Error';
  }
}

// XSS Protection
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
