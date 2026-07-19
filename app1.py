import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, HTMLResponse
from rembg import remove, new_session
from PIL import Image

app = FastAPI(title="Background Remover")
session = new_session("birefnet-general")

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Background remover</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: sans-serif; max-width: 640px; margin: 60px auto; padding: 0 16px; text-align: center; background: #f8f9fa; }
    .card { background: #fff; border-radius: 12px; padding: 36px; box-shadow: 0 2px 12px rgba(0,0,0,.08); }
    h1 { margin: 0 0 6px; font-size: 24px; }
    p { color: #666; margin: 0 0 24px; }
    .drop { border: 2px dashed #cbd5e1; border-radius: 8px; padding: 32px; cursor: pointer;
            transition: border-color .2s; margin-bottom: 20px; }
    .drop:hover, .drop.over { border-color: #2563eb; background: #eff6ff; }
    .drop input { display: none; }
    .drop-label { color: #64748b; font-size: 14px; pointer-events: none; }
    .drop-label span { color: #2563eb; }
    button { width: 100%; padding: 12px; background: #2563eb; color: #fff; border: none;
             border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; }
    button:hover { background: #1d4ed8; }
    button:disabled { background: #93c5fd; cursor: not-allowed; }
    #status { margin-top: 14px; font-size: 14px; color: #64748b; min-height: 20px; }
    #result { margin-top: 24px; display: none; }
    #result img { max-width: 100%; border-radius: 8px; background: repeating-conic-gradient(#e2e8f0 0% 25%, #fff 0% 50%) 0 0 / 20px 20px; }
    #download { display: inline-block; margin-top: 12px; padding: 8px 20px; background: #f1f5f9;
                border-radius: 6px; color: #2563eb; text-decoration: none; font-size: 14px; }
    #download:hover { background: #e2e8f0; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Background remover</h1>
    <p>Upload a photo to get a transparent background PNG (BiRefNet)</p>

    <div class="drop" id="drop">
      <input type="file" id="file" accept="image/*">
      <div class="drop-label">Drag and drop your file or <span>browse for a photo</span></div>
    </div>

    <button id="btn" disabled>Remove background</button>
    <div id="status"></div>

    <div id="result">
      <img id="out">
      <br>
      <a id="download" download="nobg.png">Download PNG</a>
    </div>
  </div>

  <script>
    const drop = document.getElementById('drop');
    const fileInput = document.getElementById('file');
    const btn = document.getElementById('btn');
    const status = document.getElementById('status');
    let selectedFile = null;

    drop.onclick = () => fileInput.click();

    drop.ondragover = (e) => { e.preventDefault(); drop.classList.add('over'); };
    drop.ondragleave = () => drop.classList.remove('over');
    drop.ondrop = (e) => {
      e.preventDefault(); drop.classList.remove('over');
      const f = e.dataTransfer.files[0];
      if (f) setFile(f);
    };

    fileInput.onchange = () => { if (fileInput.files[0]) setFile(fileInput.files[0]); };

    function setFile(f) {
      selectedFile = f;
      drop.querySelector('.drop-label').textContent = f.name;
      btn.disabled = false;
    }

    btn.onclick = async () => {
      if (!selectedFile) return;
      btn.disabled = true;
      status.textContent = 'Processing...';
      document.getElementById('result').style.display = 'none';

      const fd = new FormData();
      fd.append('file', selectedFile);

      try {
        const res = await fetch('/remove-bg', { method: 'POST', body: fd });
        if (!res.ok) throw new Error(await res.text());
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const out = document.getElementById('out');
        const dl = document.getElementById('download');
        out.src = url;
        dl.href = url;
        document.getElementById('result').style.display = 'block';
        status.textContent = 'Ready!';
      } catch(e) {
        status.textContent = 'Error: ' + e.message;
      } finally {
        btn.disabled = false;
      }
    };
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    data = await file.read()
    img = Image.open(io.BytesIO(data)).convert("RGBA")

    result = remove(img, session=session)

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
