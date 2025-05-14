# Axalense

**Axalense** is a framework developed at Axamine ai for image analysis and various other Vision langauge task its  tool built with **Groq** technology. It enables developers to easily analyze and moderate images using intelligent visual recognition and natural language prompts.

> Ideal for content moderation, compliance, and automated visual understanding workflows.

---

## ✨ Features

- 🔍 **AI-Powered Moderation** using Groq
- ⚡ Fast and lightweight
- 🖼️ Simple image analysis with custom prompts
- 📦 Easy integration in Python apps and moderation pipelines

---

## 📦 Installation

```bash
pip install Axalense

from Axalense import axavision

if __name__ == "__main__":
    result = axavision.analyze_image("image-path", "Prompt", "YOUR_API_KEY")
    print(result)

