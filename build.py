from pathlib import Path
from shutil import copytree, rmtree
from tempfile import TemporaryDirectory

from teloce.build import build_project
from teloce.router import RouterCompiler, RouterGenerator

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"


def build_router() -> None:
    config = {
        "mode": "hash",
        "base": "/",
        "routes": [
            {"path": "/", "name": "home", "component": "HomePage"},
            {"path": "/tutorial", "name": "tutorial", "component": "TutorialPage"},
            {"path": "/playground", "name": "playground", "component": "PlaygroundPage"},
            {"path": "/legacy", "redirect": "/tutorial"},
        ],
    }
    compiler = RouterCompiler()
    router_config = compiler.compile(config)
    if router_config is None:
        raise RuntimeError("Router configuration failed: " + "; ".join(compiler.errors))
    router_file = PUBLIC / "static" / "js" / "router.js"
    router_file.parent.mkdir(parents=True, exist_ok=True)
    imports = (
        "import HomePage from './pages/HomePage.js';\n"
        "import TutorialPage from './pages/TutorialPage.js';\n"
        "import PlaygroundPage from './pages/PlaygroundPage.js';\n"
    )
    router_file.write_text(imports + RouterGenerator().generate(router_config) + "\nwindow.__teloceRouter = router;\n", encoding="utf-8")


def main() -> None:
    if PUBLIC.exists():
        rmtree(PUBLIC)
    with TemporaryDirectory(prefix="teloce-showcase-") as temporary:
        generated = Path(temporary) / "public"
        result = build_project(ROOT, generated, options={"dev": False, "source_maps": True, "clean": True})
        PUBLIC.mkdir(parents=True, exist_ok=True)
        copytree(generated / "static", PUBLIC / "static", dirs_exist_ok=True)
    build_router()
    print(f"Compiled {result['compiled']} components into {PUBLIC}")


if __name__ == "__main__":
    main()
