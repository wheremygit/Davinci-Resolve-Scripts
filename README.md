# DaVinci Resolve Smart Importer for Linux

> [!NOTE]
> These scripts were inspired by [Andrew Shark's Resolve Scripts](https://gitlab.com/AndrewShark/davinci-resolve-scripts).

> [!CAUTION]
> I don't know any code nor I am a dev thus these scripts were generated using an LLM. Use at your own risk.

A pair of automation scripts for **DaVinci Resolve Studio on Linux** that fixes the infamous "silent AAC audio" issue on import as well integrates with your DE's file picker offerring seemless media importing on the Linux Desktop until [Blackmagic Fixes it themseleves](https://forum.blackmagicdesign.com/viewtopic.php?f=33&t=149142).

Instead of dealing with separate tracks or fragile GUI automation, these scripts pre-process your media files instantly using FFmpeg. They clone the video stream exactly (zero quality loss, lightning-fast) and transcode the audio to lossless **FLAC**, then inject the unified clips directly into your open Resolve project.

https://github.com/user-attachments/assets/032bd35b-9f69-4b98-a275-6b8244826681

## Features

* **Smart Import:** Multi-select any combination of supported files (videos, audio, images). Videos are optimized on the fly; other assets are imported directly.
* **Smart Bin:** Select an entire directory. The script transcodes any video files inside it and automatically creates a matching, organized Bin (sub-folder) in your Media Pool.
* No separate audio tracks, no extra folders, and no temporary timelines.

---
## Script Dependencies

To run either the **Import Media** or **Import Bin** scripts, ensure the following core packages are installed on your system via your package manager (`pacman`, `apt`, `dnf`, etc.):

* **`python`** (Python 3.x is required to execute the automation scripts).
* **`ffmpeg`** (Required to handle the video stream copying and real-time transcoding of the audio stream into lossless FLAC).
* **`kdialog`** or **`zenity`** (Required for opening file/folder dialog windows cleanly).

> [!IMPORTANT]
> * **DaVinci Resolve Studio:** Blackmagic Design limits external Python scripting execution to the **Studio (paid)** version on Linux.

## Installation & Setup

### 1. Run the Installer

```bash
git clone https://github.com/wheremygit/DaVinci-Resolve-Smart-Importer.git
cd DaVinci-Resolve-Smart-Importer
chmod +x install.sh
./install.sh

```

The script will automatically verify your basic dependencies, build the necessary DaVinci Resolve directory paths, safely move the utilities into position, and apply standard execution permissions.

### 2. Run the Scripts in Resolve

1. Open DaVinci Resolve and open a project.
2. Navigate to the top menu: **Workspace > Scripts**.
3. Select your script to execute it.

> [!TIP]
> ### 3. (Optional) Assign Keyboard Shortcuts
> 
> 
> To speed up your workflow, you can map these scripts to keyboard shortcuts:
> 1. Go to **DaVinci Resolve > Keyboard Customization**.
> 2. Search for the name of your script (under the *Application > Workspace > Scripts* category).
> 3. Assign your preferred shortcut key bind.

---

> [!WARNING]
> ## Environment & Testing
>
> * **Tested OS:** Arch Linux (KDE Plasma)
> * **Tested Application:** DaVinci Resolve Studio 21
> * **Dependencies Checked:** FFmpeg, KDialog, Python 3.11+
