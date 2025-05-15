<p align="center">
  <img src="https://simi.anbuinfosec.live/bot-logo.png" width="200" alt="pysimsimi logo">
</p>

<h1 align="center">pysimsimi</h1>
<p align="center">
  Python wrapper for simi.anbuinfosec.live chat and teach APIs.
</p>

<p align="center">
  <a href="https://github.com/anbuinfosec/pysimsimi/issues">Report Issue</a> •
  <a href="https://github.com/anbuinfosec/pysimsimi">Source Code</a> •
  <a href="mailto:anbuinfosec@gmail.com">Contact Developer</a>
</p>

---

## 📦 Installation

```bash
pip install pysimsimi
````

Or install directly from source:

```bash
git clone https://github.com/anbuinfosec/pysimsimi
cd pysimsimi
pip install .
```

---

## 🚀 Features

* Simple interface to talk with the Simi bot
* Teach Simi new responses via API
* Easy integration in chatbots and personal projects
* Lightweight and dependency-free (only `requests`)

---

## 🧪 Example Usage

```python
from pysimsimi import talk, teach

# 🗣️ Talk with Simi
response = talk("Hi", "en")
print("Simi says:", response)

# 📚 Teach Simi
teach_response = teach("Hi", "Hello there!", "en")
print("Teaching result:", teach_response)
```

---

## 🐛 Issues

Have a bug or feature request? [Open an issue](https://github.com/anbuinfosec/pysimsimi/issues) on GitHub.
We appreciate contributions and feedback to improve `pysimsimi`.

---

## 👨‍💻 Developer

**Mohammad Alamin**

📧 [Email](mailto:anbuinfosec@gmail.com)

🌐 [Developer](https://facebook.com/anbuinfosec)

🌐 [Facebook Page](facebook.com/anbuinfosec.official)

🔒 Security & Developer Community: `anbuinfosec`

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://facebook.com/anbuinfosec">anbuinfosec</a>
</p>