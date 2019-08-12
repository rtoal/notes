window.addEventListener('load', event => {
  setTimeout(() => {
    fetch('/most-recent-note').then(r => r.text()).then(most_recent => {
      let displayed = document.querySelector('article');
      displayed = displayed ? displayed.textContent.trim() : '';
      if (!displayed.startsWith(most_recent)) {
          window.location.reload();
      }
    });
  }, 1500);
});

document.querySelectorAll('article div').forEach(div => {
  if (div.textContent && div.textContent.trim().startsWith('/gif ')) {
    const q = encodeURIComponent(div.textContent.slice(5));
    const baseUrl = 'https://api.giphy.com/v1/gifs/search';
    const url = `${baseUrl}?api_key=dc6zaTOxFJmzC&limit=1&rating=g&q=${q}`;
    fetch(url).then(r => r.json()).then(result => {
      const imageUrl = result.data[0].images.original.url;
      div.innerHTML = `<img src=${imageUrl}>`;
    });
  }
});
