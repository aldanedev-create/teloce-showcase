# Teloce Motion Lab

A small Flask showcase for Teloce-Py. It demonstrates `.vel` components, a generated client-side router, hash navigation, Three.js animation, scoped CSS, lifecycle cleanup, and a Vercel-compatible `public/` build.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate   # macOS/Linux
python -m pip install -r requirements.txt
python build.py
python app.py
```

Open <http://127.0.0.1:5055>. The HTML shell mounts the router:

```html
<div id="app"></div>
<script type="module">
  import router from "/static/js/router.js";
  router.mount(document.querySelector("#app"));
</script>
```

## How it works

`build.py` compiles every `.vel` file into `public/static/js`, then generates `public/static/js/router.js` with imports for the three page components. Flask renders `templates/index.html`; the browser loads the router, reads the hash, and mounts the active component into `#app`.

The Home page creates and disposes a Three.js scene in `.vel` lifecycle hooks. The Tutorial page is a copy-paste lesson. The Playground makes route state visible. `/legacy` demonstrates a redirect to `/tutorial`.

## Deploy to Vercel

Push this repository to GitHub and import it into Vercel. Vercel detects the top-level Flask `app` in `app.py`; the `tool.vercel.scripts.build` entry runs `python build.py`, and generated browser files are placed in `public/`.

```bash
npx vercel dev
npx vercel --prod
```

Three.js is pinned to `0.171.0` in the `.vel` source. For a fully self-contained production build, bundle Three.js instead of relying on the CDN.
