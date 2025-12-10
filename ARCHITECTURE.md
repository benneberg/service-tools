# DISE Partner Portal - Refactored Architecture

## 📁 Project Structure

```
service-tools/
├── index.html              # Legacy monolithic version (backup)
├── index-new.html          # New modular version
├── shared/                 # Shared resources
│   ├── styles.css         # Global styles and animations
│   ├── utils.js           # Shared utility functions (toast, copy, download, tabs)
│   └── router.js          # Page routing and navigation
└── tools/                 # Individual tool modules
    ├── home/
    │   ├── index.html     # Home page HTML fragment
    │   ├── script.js      # Home page specific JavaScript
    │   └── README.md      # Home page documentation
    ├── signageos-chromeos/
    │   ├── index.html     # ChromeOS provisioning page HTML
    │   ├── script.js      # Script generation and interactions
    │   └── README.md      # Tool documentation
    └── signageos-unlock/
        ├── index.html     # Unlock device page HTML
        ├── script.js      # API interactions and form handling
        └── README.md      # Tool documentation
```

## 🎯 Architecture Benefits

### Modularity
- Each tool is self-contained in its own directory
- Easy to add, remove, or modify individual tools
- Clear separation of concerns

### Maintainability
- Shared utilities prevent code duplication
- Individual tool scripts are isolated
- Documentation lives with the code

### Scalability
- Add new tools by creating a new directory in `tools/`
- Follow the template structure for consistency
- No need to modify core files for new tools

## 🚀 Adding a New Tool

1. **Create Directory**
   ```
   tools/my-new-tool/
   ```

2. **Create Files**
   - `index.html` - Page structure
   - `script.js` - Tool-specific JavaScript
   - `README.md` - Documentation

3. **Update Router**
   Add to `shared/router.js`:
   ```javascript
   const PAGES = {
       ...
       'my-new-tool': 'My New Tool Title'
   };
   ```

4. **Update Menu**
   Add to `index-new.html` sidebar:
   ```html
   <a href="#my-new-tool" id="menu-my-new-tool" class="menu-item...">
       My New Tool
   </a>
   ```

5. **Load Fragment**
   Add to `index-new.html` loadPageFragments:
   ```javascript
   { id: 'my-new-tool', url: 'tools/my-new-tool/index.html' }
   ```

## 📝 Template Structure

### index.html Template
```html
<div class="page hidden" id="page-TOOL-ID">
  <h2 class="text-3xl font-bold text-white mb-6 border-b border-gray-700 pb-2">
    Tool Title
  </h2>
  
  <!-- Tool content here -->
</div>
```

### script.js Template
```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Tool-specific initialization
  const myButton = document.getElementById('myButton');
  
  if (myButton) {
    myButton.addEventListener('click', () => {
      // Use shared utilities
      showToast('success', 'Action completed');
    });
  }
});
```

### README.md Template
```markdown
# Tool Name

## Description
Brief description of what the tool does

## Features
- Feature 1
- Feature 2

## Usage
Step-by-step usage instructions

## Files
- `index.html` - Page structure
- `script.js` - Interaction logic
- `README.md` - This documentation
```

## 🔧 Shared Utilities

### Available in `shared/utils.js`

- **`showToast(type, text, opts)`** - Display toast notifications
  - Types: 'info', 'success', 'error'
  - Options: { loader: bool, persistent: bool, duration: ms }

- **`copyText(text)`** - Copy text to clipboard with toast feedback

- **`downloadScript(content, filename)`** - Download text as file

- **`switchTab(tabId, clickedButton)`** - Handle tab switching within tools

- **`toggleMenu(force)`** - Toggle sidebar menu

## 🎨 Styling

All shared styles are in `shared/styles.css`:
- Base styles and fonts
- Animations (slide-in, slide-out, spin)
- Sidebar and overlay transitions
- Tab styles and states
- Custom loaders

Tool-specific styles can be added inline or in separate CSS files.

## 🔄 Migration Path

1. **Phase 1** ✅ - Refactor structure (COMPLETE)
   - Create modular directory structure
   - Extract shared utilities
   - Create individual tool modules

2. **Phase 2** - Test and validate
   - Test `index-new.html` thoroughly
   - Verify all tools function correctly
   - Check mobile responsiveness

3. **Phase 3** - Switch to new version
   - Rename `index.html` to `index-old.html` (backup)
   - Rename `index-new.html` to `index.html`
   - Update any external links

## 📋 Current Tools

1. **Home** - Welcome page with partner notes
2. **SignageOS ChromeOS** - Provisioning script generator
3. **SignageOS Unlock** - Standalone device unlock tool

## 🐛 Troubleshooting

### Pages not loading
- Check browser console for fetch errors
- Verify file paths in `loadPageFragments()`
- Ensure all HTML fragments are valid

### Scripts not working
- Check that shared utilities load before tool scripts
- Verify element IDs match between HTML and JavaScript
- Check browser console for errors

### Styles not applying
- Ensure `shared/styles.css` is loaded
- Check for CSS conflicts with Tailwind
- Verify class names are correct

## 📚 Documentation

Each tool has its own README with:
- Description and purpose
- Feature list
- Usage instructions
- API documentation (if applicable)
- Last updated date

## 🔐 Security Notes

- All API calls use proper error handling
- User inputs are validated before processing
- Sensitive operations require confirmation
- Audit trail support where applicable

## 📞 Support

For issues or questions:
- Email: support@dise.com
- Check individual tool READMEs for specific guidance
