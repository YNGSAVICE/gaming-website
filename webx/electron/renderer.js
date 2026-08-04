const address = document.getElementById('address');
const go = document.getElementById('go');
const tabsEl = document.getElementById('tabs');
const newTabBtn = document.getElementById('newtab');
const bookmarkBtn = document.getElementById('bookmark');
const showBookmarksBtn = document.getElementById('showBookmarks');

let tabs = [];
let current = null;

function createTab(url = 'https://www.bing.com') {
  const id = 'tab-' + Date.now();
  const tabBtn = document.createElement('button');
  tabBtn.textContent = 'New';
  tabBtn.dataset.id = id;
  tabBtn.addEventListener('click', () => switchTab(id));
  tabsEl.appendChild(tabBtn);

  const iframe = document.createElement('iframe');
  iframe.className = 'webview';
  iframe.src = url;
  iframe.style.display = 'none';
  document.body.appendChild(iframe);

  tabs.push({ id, btn: tabBtn, iframe });
  switchTab(id);
}

function switchTab(id) {
  tabs.forEach(t => {
    if (t.id === id) { t.iframe.style.display = 'block'; t.btn.classList.add('active'); current = t; address.value = t.iframe.src; }
    else { t.iframe.style.display = 'none'; t.btn.classList.remove('active'); }
  });
}

go.addEventListener('click', () => {
  if (!current) return;
  let url = address.value.trim();
  if (!url) return;
  if (!url.startsWith('http')) url = 'https://' + url;
  current.iframe.src = url;
});

newTabBtn.addEventListener('click', () => createTab());

bookmarkBtn.addEventListener('click', () => {
  if (!current) return;
  const bookmarks = JSON.parse(localStorage.getItem('webx.bookmarks') || '[]');
  bookmarks.push({ title: current.iframe.contentDocument?.title || current.iframe.src, url: current.iframe.src, addedAt: new Date().toISOString() });
  localStorage.setItem('webx.bookmarks', JSON.stringify(bookmarks));
  alert('Bookmarked ' + current.iframe.src);
});

showBookmarksBtn.addEventListener('click', () => {
  const bookmarks = JSON.parse(localStorage.getItem('webx.bookmarks') || '[]');
  const list = bookmarks.map(b => b.title + '\n' + b.url).join('\n\n');
  alert(list || 'No bookmarks');
});

// init
createTab();
