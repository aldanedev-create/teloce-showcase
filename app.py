from pathlib import Path

from flask import Flask, render_template, send_from_directory

ROOT = Path(__file__).resolve().parent
PUBLIC_STATIC = ROOT / "public" / "static"

app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=None)


@app.get("/")
def home():
    return render_template("index.html", title="Teloce Motion Lab")


@app.get("/static/<path:asset>")
def static_asset(asset: str):
    return send_from_directory(PUBLIC_STATIC, asset)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "teloce-showcase"}


if __name__ == "__main__":
    print("Run `python build.py` before starting Flask.")
    app.run(host="127.0.0.1", port=5055, debug=True)

