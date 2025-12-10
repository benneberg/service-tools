/* -------------------------
  Shared Utilities & Core Functions
------------------------- */

// Toast system
const toastContainer = document.getElementById('toasts');
function showToast(type, text, opts = {}) {
  const el = document.createElement('div');
  const typeClasses = {
    info: 'bg-gray-700 text-white',
    success: 'bg-accent text-white',
    error: 'bg-red-600 text-white'
  };
  el.className = `toast shadow-lg rounded-md py-3 px-5 flex gap-3 items-center slide-in-bottom ${typeClasses[type] || typeClasses.info}`;
  
  if (opts.loader) {
    el.innerHTML = `<span class="btn-loader !border-t-white !border-r-transparent w-5 h-5"></span> <span>${text}</span>`;
  } else {
    el.textContent = text;
  }
  
  toastContainer.appendChild(el);
  if (!opts.persistent) {
    setTimeout(() => {
      el.classList.remove('slide-in-bottom');
      el.classList.add('slide-out-bottom');
      setTimeout(() => el.remove(), 300);
    }, opts.duration || 3000);
  }
  return el;
}

// Copy helper
function copyText(text) {
  try {
    const tempElement = document.createElement('textarea');
    tempElement.value = text;
    tempElement.setAttribute('readonly', '');
    tempElement.style.position = 'absolute';
    tempElement.style.left = '-9999px';
    document.body.appendChild(tempElement);
    
    tempElement.select();
    const success = document.execCommand('copy');
    
    document.body.removeChild(tempElement);

    if (success) {
        showToast('success', 'Copied to clipboard');
    } else {
        throw new Error('execCommand failed');
    }
    
  } catch (e) { 
      console.error("Copy failed via execCommand:", e);
      showToast('error', 'Copy failed. Try manually selecting the script text.');
  }
}

// Download helper
function downloadScript(scriptContent, filename) {
    const blob = new Blob([scriptContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    showToast('success', 'Script downloaded');
}

// Tab switching logic
function switchTab(tabId, clickedButton) {
    const parentPage = clickedButton.closest('.page');
    if (!parentPage) return;

    parentPage.querySelectorAll('.tab').forEach(btn => {
        btn.classList.remove('active');
    });
    parentPage.querySelectorAll('#tabContent > div').forEach(content => {
        content.classList.add('hidden');
    });

    clickedButton.classList.add('active');

    const contentToShow = parentPage.querySelector(`#tab-content-${tabId}`);
    if (contentToShow) {
        contentToShow.classList.remove('hidden');
    }
}

// Menu toggle
function toggleMenu(force) {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const isOpen = sidebar.classList.contains('open');
    
    const shouldOpen = force !== undefined ? force : !isOpen;

    if (shouldOpen) {
        sidebar.classList.add('open');
        overlay.classList.remove('pointer-events-none', 'opacity-0');
        overlay.classList.add('opacity-100');
    } else {
        sidebar.classList.remove('open');
        overlay.classList.remove('opacity-100');
        overlay.classList.add('pointer-events-none', 'opacity-0');
    }
}
