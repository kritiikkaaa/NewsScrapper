const root = document.documentElement;
const toggle = document.querySelector('.theme-toggle');
const savedTheme = localStorage.getItem('briefly-theme');
if (savedTheme === 'light') root.classList.add('light');
toggle?.addEventListener('click', () => {
  root.classList.toggle('light');
  localStorage.setItem('briefly-theme', root.classList.contains('light') ? 'light' : 'dark');
});

document.querySelector('.url-form')?.addEventListener('submit', () => document.querySelector('.loader')?.classList.add('show'));

if (window.entityChart && document.getElementById('entityChart')) {
  const colors = ['#a78bfa', '#22d3ee', '#fbbf24', '#fb7185', '#34d399', '#818cf8'];
  new Chart(document.getElementById('entityChart'), {
    type: 'doughnut', data: { labels: window.entityChart.labels, datasets: [{ data: window.entityChart.values, backgroundColor: colors, borderWidth: 0 }] },
    options: { cutout: '68%', plugins: { legend: { position: 'bottom', labels: { color: getComputedStyle(document.body).color, padding: 14, usePointStyle: true } } }, responsive: true, maintainAspectRatio: false }
  });
}
