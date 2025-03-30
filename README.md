Here's the complete README and setup files in one copy-pasteable block (excluding the app code as requested):

```markdown
# LAMEUTE PDF Merger

![PDF Merger Interface](screenshot.png)

A modern desktop application for merging PDF files with beautiful UI and powerful functionality.

## ✨ Features
- 🎨 **Sleek Interface**: Salmon-red theme with rounded buttons
- 📂 **Flexible Input**: Add files individually or entire folders
- ↔️ **Drag-and-Drop**: Visually reorder PDFs before merging
- ⚡ **Fast Processing**: Multi-threaded merging engine
- ✔️ **Smart Validation**: Automatically skips invalid files
- 📊 **Progress Tracking**: Real-time progress indicator

## 🛠️ Requirements
- Python 3.8+
- `PyPDF2` library
- `Pillow` (PIL) for image handling

## 🚀 Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/PDF-Merger.git
cd PDF-Merger
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🖥️ Usage
Run the application:
```bash
python lameute_pdf_merger.py
```

## 🔧 Configuration
- Add `logo.png` (48×48px) to customize the header
- Add `icon.png` to change the window icon

## ⚠️ Troubleshooting
**Window not appearing?**  
Try:
```bash
python3 lameute_pdf_merger.py
```

**Missing dependencies?**  
Reinstall requirements:
```bash
pip install --force-reinstall -r requirements.txt
```

## 📜 License
MIT License - Free for personal and commercial use

---

*Created with ❤️ by [Your Name]*

# Supporting Files

## requirements.txt
```
PyPDF2>=3.0.0
Pillow>=9.0.0
```

## .gitignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
*.log
*.tmp
.DS_Store
```

## First-Time Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install packages
pip install -r requirements.txt

# Launch application
python lameute_pdf_merger.py
```
```

To use:
1. Copy this entire block
2. Create a new folder for your project
3. Paste into separate files as follows:
   - `README.md` (first section)
   - `requirements.txt` (the content after the heading)
   - `.gitignore` (the content after that heading)
4. Save the Python code separately as `lameute_pdf_merger.py`

The package includes:
✔ Professional documentation  
✔ Dependency management  
✔ Git configuration  
✔ Setup instructions  
✔ Troubleshooting guide  

(Note: You'll need to add the actual Python code separately to complete the package)
