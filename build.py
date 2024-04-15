from pathlib import Path

from engine.builder import AppInfo
from engine.builder import BuildSettings
from engine.builder import pbuild


project_root = Path(__file__).parent
icon = project_root / "icon.png"
builds = project_root / "builds"


app_name = "HEXX-LD55"
script_file = project_root / "main.py"
content_root = project_root / "content"

debug_app_info = AppInfo(
    name=f"{app_name}-debug",
    icon_path=icon,
    script_path=script_file,
    content_root=content_root,
)

app_info = AppInfo(
    name=app_name,
    icon_path=icon,
    script_path=script_file,
    content_root=content_root,
)

debug_build_settings = BuildSettings(
    one_file=False,
    quiet=True,
    debug=True,
    output_folder=builds,
)

release_build_settings = BuildSettings(
    one_file=False,
    quiet=True,
    debug=False,
    output_folder=builds,
)

print(f"Building {debug_app_info.name}")
pbuild(debug_app_info, debug_build_settings)

print(f"Building {app_info.name}")
pbuild(app_info, release_build_settings)
