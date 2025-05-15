<p align="center">
  <img align="center" width="300" src="https://github.com/user-attachments/assets/744026c6-7916-40ca-ad51-66bd9a53e4b0" />
</p>

<p align="center">

<a href="https://pypi.org/project/PyPasta/">
    <img src="https://img.shields.io/pypi/v/PyPasta?color=red&logo=pypi&logoColor=red">
  </a>

  <a href="https://t.me/Pycodz">
    <img src="https://img.shields.io/badge/Telegram-Channel-blue.svg?logo=telegram">
  </a>
  
  <a href="https://t.me/DevZ44d" target="_blank">
    <img alt="Telegram Owner" src="https://img.shields.io/badge/Telegram-Owner-red.svg?logo=telegram" />
  </a>
</p>



> [!IMPORTANT]
> `PyPasta` is a lightweight Python utility for interacting with the Pastebin API. It allows users to upload code snippets with metadata like title, syntax highlighting, and expiration time, as well as retrieve and display paste content via a simple interface.

### Installation and Development 🚀

- Via PyPi ⚡️
```shell
# via PyPi
pip install PyPasta -U
```

### 🚀 Quick Start .
```python
from PyPasta import Paste
object = Paste()
# Uploading Paste .

object.upload(
    api_dev_key= "",        # Your Pastebin Developer API key (default provided but recommended to use your own)
    syntax="" ,             # Syntax highlighting format (e.g., python, html, text)
    code="" ,               # The actual code snippet to upload
    expire_date="10M" ,     # Expiration time (10M, 1H, 1D, 1W, 2W, 1M, 6M, 1Y, or N for never)
    title="" ,              # Name/title of the paste
    private= 1              # Paste visibility (0=public, 1=unlisted, 2=private)
)

# Get Paste .

object.get("")              # ID Of Paste
```

### Features 📚

- ✅ Upload code snippets to Pastebin using their API

- 📝 Set paste title, syntax format, expiration date, and visibility

- 🔍 Retrieve existing pastes by ID

- 🌐 Fetch paste metadata (title, visibility) and raw code content

- 🎨 Clean and colored terminal output using colorama


### Notes ✍️

- Make sure to **[get your own API key](https://pastebin.com/doc_api)** from Pastebin.

- This tool is ideal for quick snippet sharing, backups, or automated code posting from scripts.

## 💬 Help & Support .
- Follow updates via the **[Telegram Channel](https://t.me/Pycodz)**.
- For general questions and help, join our **[Telegram chat](https://t.me/PyChTz)**.