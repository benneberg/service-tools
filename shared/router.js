// Router and page management
const PAGES = {
    'home': 'Home',
    'SignageOS-ChromeOS': 'SignageOS - ChromeOS Provisioning',
    'SignageOS-UnLockStandAloneDevice': 'SignageOS – Un Lock StandAloneDevice'
};

function router() {
    let hash = window.location.hash.substring(1) || 'home';
    const pageId = `page-${hash}`; 
    
    // 1. Handle Content Visibility
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));

    const activePage = document.getElementById(pageId);
    
    if (activePage) {
        activePage.classList.remove('hidden');
        document.getElementById('pageTitle').textContent = PAGES[hash] || 'Partner Portal';
        
        // 2. Handle Menu Active State
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('bg-gray-700', 'text-white');
            item.classList.add('text-gray-300', 'hover:bg-gray-700');
        });
        
        const activeMenuItem = document.getElementById(`menu-${hash}`);
        if (activeMenuItem) {
             activeMenuItem.classList.remove('text-gray-300', 'hover:bg-gray-700');
             activeMenuItem.classList.add('bg-gray-700', 'text-white');
        }
        
        // 3. Handle Tab State - Initialize default tab for pages with tabs
        if (hash === 'SignageOS-ChromeOS' || hash === 'SignageOS-UnLockStandAloneDevice') {
             const activePage = document.getElementById(`page-${hash}`);
             if (activePage) {
                 const defaultTabButton = activePage.querySelector('.tab[data-tab="script"]');
                 if (defaultTabButton) {
                     switchTab('script', defaultTabButton);
                 }
             }
        }

    } else {
        // If hash is invalid, default to home
        document.getElementById('page-home').classList.remove('hidden');
        document.getElementById('pageTitle').textContent = PAGES['home'];
        window.location.hash = 'home';
    }
    
    // Close menu after routing on mobile
    if (document.getElementById('sidebar').classList.contains('open')) {
      toggleMenu(false);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menuToggle');
  menuToggle.addEventListener('click', () => toggleMenu());
  
  // Sidebar links close menu
  document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', () => toggleMenu(false));
  });

  // Initialize router
  window.onhashchange = router;
  router();
});
