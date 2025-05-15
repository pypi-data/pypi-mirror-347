import shutil
import click
from pathlib import Path
from rich.console import Console

from sbkube.utils.file_loader import load_config_file

console = Console()

@click.command(name="build")
@click.option("--app-dir", default="config", help="앱 구성 디렉토리 (내부 config.yaml 파일 사용)")
@click.option("--base-dir", default=".", help="프로젝트 루트 디렉토리 (기본: 현재 경로)")
def cmd(app_dir, base_dir):
    """prepare 결과를 기반으로 Helm/Git 리소스를 전처리하고 build 디렉토리 생성"""
    BASE_DIR = Path(base_dir).resolve()
    CHARTS_DIR = BASE_DIR / "charts"
    REPOS_DIR = BASE_DIR / "repos"
    BUILD_DIR = BASE_DIR / "build"
    OVERRIDES_DIR = BASE_DIR / "overrides"
    VALUES_DIR = BASE_DIR / "values"

    console.print(f"[bold green]\U0001f3d7️ build 시작: {app_dir}[/bold green]")

    app_path = Path(app_dir)
    config_path = (BASE_DIR / app_path / "config").resolve()

    apps_config = load_config_file(str(config_path))

    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    success = 0

    for app in apps_config.get("apps", []):
        if app["type"] not in ("pull-helm", "pull-helm-oci", "pull-git", "copy-app"):
            continue

        total += 1
        app_type = app.get("type")
        app_name = app.get("name")
        specs = app.get("specs", {})

        try:
            if app_type in ("pull-helm", "pull-helm-oci"):
                repo = specs["repo"]
                chart = specs["chart"]
                dest = specs.get("dest", app_name)

                src_chart_path = CHARTS_DIR / repo / chart
                dst_path = BUILD_DIR / dest

                if not src_chart_path.exists():
                    console.print(f"[red]❌ Helm 차트 없음: {src_chart_path}[/red]")
                    continue

                shutil.copytree(src_chart_path, dst_path)
                console.print(f"[cyan]📁 Helm 차트 복사: {src_chart_path} → {dst_path}[/cyan]")

                for override in specs.get("overrides", []):
                    override_src = OVERRIDES_DIR / dest / override
                    override_dst = dst_path / override
                    if override_src.exists():
                        override_dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(override_src, override_dst)
                        console.print(f"[yellow]🔁 override: {override_src} → {override_dst}[/yellow]")

                for remove in specs.get("removes", []):
                    target = dst_path / remove
                    if target.exists() and target.is_file():
                        target.unlink()
                        console.print(f"[red]🗑️ remove: {target}[/red]")

            elif app_type == "pull-git":
                repo = specs["repo"]
                paths = specs.get("paths", [])
                dst_path = BUILD_DIR / app_name
                dst_path.mkdir(parents=True, exist_ok=True)

                for c in paths:
                    src = REPOS_DIR / repo / c["src"]
                    dst = dst_path / c["dest"]
                    shutil.copytree(src, dst)
                    console.print(f"[magenta]📂 Git 복사: {src} → {dst}[/magenta]")

            elif app_type == "copy-app":
                paths = specs.get("paths", [])
                dst_path = BUILD_DIR / app_name
                dst_path.mkdir(parents=True, exist_ok=True)

                for c in paths:
                    src = Path(c["src"]).resolve()
                    dst = dst_path / c["dest"]
                    shutil.copytree(src, dst)
                    console.print(f"[blue]📂 copy-app: {src} → {dst}[/blue]")

            success += 1

        except Exception as e:
            console.print(f"[red]❌ {app_type} 실패: {app_name} → {e}[/red]")

    console.print(f"[bold green]✅ build 완료: {BUILD_DIR} ({success}/{total} 개 완료)[/bold green]")