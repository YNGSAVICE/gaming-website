const address = document.getElementById('address');
const go = document.getElementById('go');
const webview = document.getElementById('webview');

go.addEventListener('click', () => {
  let url = address.value.trim();
  if (!url) return;
  if (!url.startsWith('http')) url = 'https://' + url;
  webview.src = url;
});
