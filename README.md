# Background Removal Service (BiRefNet)

A lightweight web service for automatic background removal from portrait and product images using **BiRefNet (SOTA 2024)**.

The service provides a simple web interface and REST API for removing image backgrounds while preserving fine details such as hair, fur and transparent objects.

---

## Features

- One-click background removal
- Drag & drop image upload
- Transparent checkerboard preview
- PNG export with alpha channel
- FastAPI REST API
- ONNX Runtime inference
- Apple Silicon (CoreML) acceleration

---

## Tech Stack

- Python 3.10+
- FastAPI
- rembg
- BiRefNet
- Pillow
- ONNX Runtime

---

## Project Structure

```
background-removal-service/
├── app.py
├── requirements.txt
├── README.md
├── research.pdf
└── screenshots/
    ├── before.png
    └── after.png
```

---

## Installation

```bash
git clone https://github.com/<your-username>/background-removal-service.git

cd background-removal-service

python -m venv .venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run

**Note:** The model (~400 MB) will be downloaded once on the first launch.

```bash
python app.py
```

Open

```
http://localhost:8000
```

### Docker (optional)

```bash
docker build -t bg-removal .
docker run -p 8000:8000 bg-removal
```
---

## Requirements

- Python 3.10 or higher
- macOS / Linux / Windows
- Apple Silicon with CoreML Execution Provider
- NVIDIA GPU via `rembg[gpu]`

---

## Model Selection

BiRefNet was selected after comparing several state-of-the-art background removal models.

| Model | Edge Quality | Speed (Apple M1 Pro) | License |
|--------|--------------|----------------------|----------|
| **BiRefNet** | ★★★★★ | ~0.7 s | Apache 2.0 |
| RMBG-2.0 | ★★★★★ | no Apple Silicon support | Commercial |
| SAM 2 | ★★★★☆ | ~2–4 s | Apache 2.0 |
| MediaPipe Selfie | ★★★☆☆ | ~30 ms | Apache 2.0 |

A detailed comparison is available in **research.pdf**.

---

## Demo

### Original

![Original](examples/before.png)

### Result

![Result](examples/after.png)

---

## Future Production Improvements

- **Task queue**: for high-load scenarios, the inference can be offloaded to a background task queue (Celery + Redis / RabbitMQ) with async endpoint returning `task_id` and a separate status endpoint
- **Model serving**: the model can be served via TorchServe or Triton Inference Server for GPU batching and versioning
- **Caching**: repeated requests for the same image can be cached by content hash to avoid redundant inference
  

## License

MIT
