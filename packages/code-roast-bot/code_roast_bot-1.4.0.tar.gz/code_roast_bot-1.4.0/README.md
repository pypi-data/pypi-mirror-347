![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-BSD--3--Clause-green)
![Security Audited](https://img.shields.io/badge/security-a%2B-brightgreen)

# Code Roast Bot

Code Roast Bot is a terminal tool that humorously and securely roasts your Python code using GPT-4. It detects security red flags, hardcoded secrets, and code crimes — then flames them with sarcasm and style.

## Features

- 🔐 Static analysis of security risks (eval, exec, secrets, etc.)
- 🧠 Obfuscation detection (AST + regex)
- 🤖 GPT-powered roasting with tone and verbosity controls
- 🎭 Choose a voice: Colbert, Trump, Clarkson, Bill Burr, etc.
- 🧪 Includes unit tests and redaction logic
- 📤 Output as Markdown or plain text

## Usage

```bash
code-roast your_script.py --roast-level 7 --voice billburr --verbosity 3
```

You can also pipe code in via stdin or scan multiple files.

## License

BSD 3-Clause License
