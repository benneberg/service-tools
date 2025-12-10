// Home page specific JavaScript
document.addEventListener('DOMContentLoaded', () => {
  /* Text Field Persistence (localStorage) */
  const partnerNote = document.getElementById('partnerNote');
  const savedNote = localStorage.getItem('partnerNote');
  if (partnerNote) {
      if (savedNote) {
          partnerNote.value = savedNote;
      }
      partnerNote.addEventListener('input', () => {
          localStorage.setItem('partnerNote', partnerNote.value);
      });
  }
});
