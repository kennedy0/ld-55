import datetime
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import field, dataclass
from pathlib import Path
from zipfile import ZipFile


@dataclass
class AppInfo:
    name: str
    icon_path: Path
    script_path: Path
    content_root: Path
    license: str = field(default=f"Copyright {datetime.datetime.now().year} Andrew Kennedy. All rights reserved.")


@dataclass
class BuildSettings:
    one_file: bool
    quiet: bool
    debug: bool
    output_folder: Path


def pbuild(app_info: AppInfo, build_settings: BuildSettings) -> int:
    """ Build the application. """
    # Paths
    # The build_path is the folder where the build is run. It gets cleaned up before and after every build.
    build_path = build_settings.output_folder / "build"
    pyinstaller_work_path = build_path / "work"
    pyinstaller_spec_path = build_path / "spec"

    # The dist_path is where the application is built to
    if build_settings.debug:
        dist_path = build_settings.output_folder / "debug"
    else:
        dist_path = build_settings.output_folder / "release"

    # Validation
    _validate_os()
    _validate_icon(app_info.icon_path)
    _validate_content(app_info.content_root)

    # Clean paths
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.rmtree(dist_path, ignore_errors=True)

    # Create paths
    build_settings.output_folder.mkdir(parents=True, exist_ok=True)
    build_path.mkdir(parents=True, exist_ok=True)

    # Write icon file
    icon_file = build_path / _get_icon_file_name()
    _write_icon_file(src=app_info.icon_path, dst=icon_file)

    # Write license file
    license_file = build_path / "LICENSE"
    with license_file.open('w') as fp:
        fp.write(AppInfo.license)

    # Zip content
    content_zip = build_path / "content"
    _zip_content(app_info.content_root, content_zip)

    # Create build command
    cmd = ["pyinstaller"]
    cmd += ["--specpath", pyinstaller_spec_path.as_posix()]
    cmd += ["--workpath", pyinstaller_work_path.as_posix()]
    cmd += ["--distpath", dist_path.as_posix()]
    cmd += ["--name", app_info.name]
    cmd += ["--icon", icon_file.as_posix()]
    cmd += ["--add-data", f"{license_file.as_posix()}{os.pathsep}."]
    cmd += ["--add-data", f"{content_zip.as_posix()}{os.pathsep}."]

    if build_settings.one_file:
        cmd += ["--onefile"]
    else:
        cmd += ["--onedir"]
        cmd += ["--contents-directory", "data"]

    if not build_settings.debug:
        cmd += ["--noconsole"]

    cmd += ["--collect-binaries", "sdl2dll"]
    cmd += ["--collect-data", "sdl2dll"]

    cmd += [app_info.script_path.as_posix()]

    # Build
    if build_settings.quiet:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    else:
        stdout = sys.stdout
        stderr = sys.stderr

    env = os.environ.copy()
    if build_settings.debug:
        env['PYTHONOPTIMIZE'] = "0"
    else:
        env['PYTHONOPTIMIZE'] = "2"

    proc = subprocess.Popen(cmd, env=env, stdout=stdout, stderr=stderr)
    proc.communicate()

    # Clean paths
    shutil.rmtree(build_path, ignore_errors=True)

    return proc.returncode


def _validate_os() -> None:
    """ Validate the operating system. """
    if platform.system() == "Windows":
        pass
    elif platform.system() == "Darwin":
        raise NotImplementedError("Building for MacOS is not implemented. pysdl2-dll is not working with PyInstaller.")
    elif platform.system() == "Linux":
        pass
    else:
        raise NotImplementedError(f"{platform.system()} is not a supported system")


def _validate_icon(icon_path: Path) -> None:
    """ Validate that the icon is in the correct format. """
    if not icon_path.suffix.lower() == ".png":
        raise RuntimeError(f"Icon '{icon_path.name}' must be a PNG file")


def _validate_content(content_path: Path) -> None:
    """ Validate that the content root exists. """
    if not content_path.is_dir():
        raise FileNotFoundError(content_path.as_posix())


def _get_icon_file_name() -> str:
    """ Get the platform-specific icon file path. """
    if platform.system() == "Windows":
        return "icon.ico"
    elif platform.system() == "Darwin":
        return "icon.icns"
    elif platform.system() == "Linux":
        return "icon.png"
    else:
        raise NotImplementedError(f"{platform.system()} is not a supported system")


def _write_icon_file(src: Path, dst: Path) -> None:
    """ Write the icon file to the build folder. """
    if platform.system() == "Windows":
        _write_icon_file_windows(src, dst)
    elif platform.system() == "Darwin":
        _write_icon_file_macos(src, dst)
    elif platform.system() == "Linux":
        _write_icon_file_linux(src, dst)
    else:
        raise NotImplementedError(f"{platform.system()} is not a supported system")


def _write_icon_file_windows(src: Path, dst: Path) -> None:
    """ Write the icon file for Windows. """
    from PIL import Image
    image = Image.open(src)
    image = image.resize((256, 256), resample=Image.Resampling.BILINEAR)
    image.save(dst)


def _write_icon_file_macos(src: Path, dst: Path) -> None:
    """ Write the icon file for macOS. """
    from PIL import Image
    image = Image.open(src)
    image.save(dst)


def _write_icon_file_linux(src: Path, dst: Path) -> None:
    """ Write the icon file for Linux. """
    shutil.copy(src, dst)


def _zip_content(src: Path, dst: Path) -> None:
    """ Zip the content root to a file. """
    files_to_zip = []
    for root, dirs, files in src.walk():
        for f in files:
            files_to_zip.append(root / f)

    with ZipFile(dst, 'w') as zf:
        for file in files_to_zip:
            zf.write(file, arcname=file.relative_to(src))
