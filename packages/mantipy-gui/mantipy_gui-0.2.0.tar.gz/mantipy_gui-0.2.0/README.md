# mantipy-gui

Modern GUI framework for Python that bridges the gap between web technologies and native applications.

## 🧠 Why mantipy-gui?

mantipy-gui solves the real pain points in Python GUI development:

### 🔥 1. Modern UI Without JS Framework Hell
- Use any HTML/JS frontend: React, Svelte, HTMX, or plain HTML
- Embed it into a native Python window, without Electron bloat
- Full JavaScript, CSS, video, canvas support — because it's Chromium

### 🧩 2. Native App Logic in Python
- Button clicks, IPC, data processing — all in Python
- Your whole backend and frontend in one language

### 🌐 3. Pluggable DNS Resolution
- Support .evr, .dao, .ipfs, .lnbtc, or your custom protocol
- A single function hook makes your browser/app future-ready

### 🛠️ 4. Customizable UI Layout
- Native widgets (sidebars, tabs, console) can live beside the browser
- Build apps, not just websites

### 🧪 5. Perfect for Local-first, Decentralized, and dApp UIs
- Build powerful offline tools with web interfaces
- Native .evr access with no DNS hacks
- Self-contained IPFS-UI frontends

## Installation

```bash
pip install mantipy-gui
```

## Quick Start

```python
from mantipy_gui import Window, BrowserView

app = Window(title="My Mantipy App")
browser = BrowserView()
app.add_view(browser)

# Load from URL
browser.load("https://example.com")

# Load local HTML
browser.load_html("<h1>Hello from Mantipy!</h1>")

# Custom domain resolution
@browser.resolver(".evr")
def resolve_evr(domain):
    # Your custom resolver for .evr domains
    return f"https://ipfs.io/ipfs/your-hash"

app.run()
```

## Examples

Check out the [examples](./examples) directory for more use cases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 