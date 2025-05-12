# freeai-utils

A lightweight collection of Python utility functions that can be installed directly using `pip` — no external `.exe` downloads or complicated setups required. This library trades some accuracy for ease of implementation. It's designed for developers who prefer quick functionality over manual setup. Just call the functions — they’ll handle the rest.

## Features

* **Audio recording**: Save recordings as `.wav` or `.mp3`
* **Speech-to-text**: Convert audio to text using Whisper
* **Text-to-speech**: Convert text into spoken audio
* **Image captioning**: Generate descriptions for images
* **OCR (Optical Character Recognition)**: Extract text from images using EasyOCR
* **Gemini API**: Interact with Google Cloud Gemini models via your API key

  * *Note: This works best with Google accounts that have no billing method added yet (completely free to use with limits).*

## Installation

```bash
pip install freeai-utils
```

> No need to install extra executables or clone large repositories — everything works out of the box with `pip`.

---

## 📖 Full API Reference

For a detailed list of all classes and methods, see [API.md](./API.md).

## Acknowledgements & References

See [THIRD_PARTY.md](./THIRD_PARTY.md) for a full list of third-party libraries and their licenses.

## Inspiration

This project was inspired by the GitHub repository:
[awesome-python](https://github.com/vinta/awesome-python)
