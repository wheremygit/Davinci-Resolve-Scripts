#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

try:
    resolve
except NameError:
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")

IGNORE_EXTENSIONS = {'.txt', '.md', '.exe', '.py', '.sh', '.json', '.xml', '.ini', '.db', '.log'}

def get_folder_path_via_linux_gui():
    if subprocess.run(["which", "zenity"], stdout=subprocess.DEVNULL).returncode == 0:
        cmd = ["zenity", "--file-selection", "--directory", "--title=Select Source Folder to Import Asset Bin"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    elif subprocess.run(["which", "kdialog"], stdout=subprocess.DEVNULL).returncode == 0:
        cmd = ["kdialog", "--getexistingdirectory", os.path.expanduser("~"), "--title", "Select Source Folder to Import Asset Bin"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    print("Error: Neither 'zenity' nor 'kdialog' found.")
    return None

def get_audio_codec(file_path):
    """Uses ffprobe to find the audio codec name cleanly."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return result.stdout.strip().lower()
    except Exception:
        return ""

def smart_bin_import():
    project_manager = resolve.GetProjectManager()
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        print("Error: Please open a project before running the script.")
        return

    media_pool = current_project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    target_dir_str = get_folder_path_via_linux_gui()
    if not target_dir_str:
        return

    source_dir = Path(target_dir_str)

    try:
        all_files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() not in IGNORE_EXTENSIONS and not f.name.startswith('.') and "_fixed" not in f.stem]
    except Exception as e:
        print(f"Error reading folder: {e}")
        return

    if not all_files:
        return

    bin_name = source_dir.name
    target_bin = None
    subfolders = root_folder.GetSubFolderList()
    if subfolders:
        for folder in subfolders:
            if folder.GetName() == bin_name:
                target_bin = folder
                break

    if not target_bin:
        target_bin = media_pool.AddSubFolder(root_folder, bin_name)
    if not target_bin:
        return

    media_pool.SetCurrentFolder(target_bin)

    for input_file in all_files:
        output_file = source_dir / f"{input_file.stem}_fixed{input_file.suffix}"

        if output_file.exists():
            media_pool.ImportMedia([str(output_file)])
            continue

        if input_file.suffix.lower() in {'.mp4', '.mkv', '.mov', '.avi', '.m4a'}:
            codec = get_audio_codec(input_file)

            if "flac" in codec or "pcm" in codec:
                print(f"Skipping transcode ({codec}). Importing directly: {input_file.name}")
                media_pool.ImportMedia([str(input_file)])
                continue

            print(f"Optimizing audio stream ({codec} -> flac): {input_file.name}")
            cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(input_file), "-c:v", "copy", "-c:a", "flac", str(output_file)]
            try:
                subprocess.run(cmd, check=True)
                media_pool.ImportMedia([str(output_file)])
                continue
            except subprocess.CalledProcessError:
                pass

        print(f"Directly importing asset: {input_file.name}")
        media_pool.ImportMedia([str(input_file)])

if __name__ == "__main__":
    smart_bin_import()
