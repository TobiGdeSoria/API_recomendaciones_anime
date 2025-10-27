// --- LOGIN ---
const loginBtn = document.getElementById('loginBtn');
if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const userId = document.getElementById('userId').value;
    if (!userId) {
      document.getElementById('errorMsg').innerText = 'Introduce un ID válido.';
      return;
    }
    localStorage.setItem('userId', userId);
    window.location.href = '/dashboard';
  });
}

// --- DASHBOARD ---
const userName = document.getElementById('userName');
if (userName) {
  const userId = localStorage.getItem('userId');
  if (!userId) window.location.href = '/';
  userName.innerText = `Usuario ${userId}`;
}

// Buscar animes
const searchBtn = document.getElementById('searchBtn');
if (searchBtn) {
  searchBtn.addEventListener('click', async () => {
    const query = document.getElementById('animeSearch').value.toLowerCase();
    const response = await fetch('anime copy.csv');
    const text = await response.text();
    const lines = text.split('\n').slice(1);
    const results = lines.filter(l => l.toLowerCase().includes(query));
    const div = document.getElementById('results');
    div.innerHTML = '';
    results.slice(0, 10).forEach(line => {
      const cols = line.split(',');
      const id = cols[0];
      const name = cols[1];
      const card = document.createElement('div');
      card.innerHTML = `<b>${name}</b><br>${renderStars(id)}`;
      div.appendChild(card);
    });
  });
}

function renderStars(animeId) {
  let starsHTML = '';
  for (let i = 1; i <= 5; i++) {
    starsHTML += `<span class="star" data-anime="${animeId}" data-rating="${i}">★</span>`;
  }
  return starsHTML;
}

document.addEventListener('click', e => {
  if (e.target.classList.contains('star')) {
    const rating = e.target.dataset.rating;
    const animeId = e.target.dataset.anime;
    const stars = document.querySelectorAll(`[data-anime="${animeId}"]`);
    stars.forEach(s => s.classList.remove('selected'));
    for (let i = 0; i < rating; i++) stars[i].classList.add('selected');
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `anime_id=${animeId}&rating=${rating}`
    })
    .then(() => alert('Calificación guardada ✅'));
  }
});

// Ajustes
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
if (settingsBtn) settingsBtn.addEventListener('click', () => settingsModal.classList.remove('hidden'));
document.getElementById('btnCloseModal')?.addEventListener('click', () => settingsModal.classList.add('hidden'));
document.getElementById('btnLogout')?.addEventListener('click', () => {
  localStorage.removeItem('userId');
  window.location.href = '/';
});
