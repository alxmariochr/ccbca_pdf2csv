from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,  # ✅ Disable terminal emulation
    'packages': ['streamlit', 'pandas', 'numpy', 'pdfplumber', 're'],
    'plist': {
        'CFBundleName': 'BCA PDF to CSV',
        'CFBundleDisplayName': 'BCA PDF to CSV',
        'CFBundleIdentifier': 'com.alxmariochr.bca-pdf-converter',
        'CFBundleVersion': '1.0.0',
        'LSUIElement': True  # ✅ Prevent Dock icon and Terminal
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)