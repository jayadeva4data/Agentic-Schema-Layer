from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/health")\ndef health():\n    return {"status": "ok"}
