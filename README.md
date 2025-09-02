# LoL Skin Chroma Browser

A Python GUI tool for browsing **darkseal-org/lol-skins chromas**. This application allows you to preview skins, view images directly from README files, and quickly open the corresponding skin files in File Explorer.
## Download
[https://github.com/martreedev/LOL-Skin-Chroma-Browser/releases/tag/release](https://github.com/martreedev/LOL-Skin-Chroma-Browser/releases/tag/release)

## Overview

The LoL Skin Chroma Browser provides a simple drag-and-drop interface to explore all your custom champion skins. You can:

- Browse champions and their skin chromas.
- Preview skin images directly from README.md files.
- Quickly open skin files in File Explorer.
- Search champions using partial or full names.

---

## Folder Structure

The tool expects a **Super Folder** containing all champion folders. Each champion folder contains a `chromas` folder, and each chroma folder contains the README and skin files.  

```text
skins/
├─ ChampionName1/
│  ├─ chromas/
│  │  ├─ SkinName1/
│  │  │  ├─ README.md
│  │  │  └─ chroma1.zip
│  │  ├─ SkinName2/
│  │  │  ├─ README.md
│  │  │  └─ chroma2.zip
├─ ChampionName2/
│  ├─ chromas/
│  │  └─ ...
├─ ChampionName3/
│  └─ ...
```
* Super Folder: The main folder you drag into the application, contains all champion skins.

* Main Folder (ChampionName): Each champion has its own folder.

* Chromas Folder: Contains all skins for a champion.

* Skin Folder: Each skin folder contains a README.md and corresponding zip files.

## Features
* Drag & Drop: Drag the super folder into the main window to populate all champions.
* Champion View: Click a champion to open a scrollable list of its skins.
* Skin Preview: Displays the first image from each skin README for quick preview.
* Full Skin Viewer: Click a skin to open all images from its README in a new scrollable window.
* Open Skin Files: Click an image or file name to open File Explorer highlighting the corresponding skin file.
* Partial Search: Search champions by typing part of their name; scrolls to the first match.

## Installation

1. Install required Python packages:
```text
pip install tkinterdnd2 pillow requests
```


2. Run the application:
```text
python main.py
```
## Usage
1. Launch the application.
2. Drag your Super Folder (main skins folder) into the window.
3. Use the search bar at the bottom of the main window to quickly jump to a champion folder. Partial matches are supported.
<img width="309" height="408" alt="image1" src="https://github.com/user-attachments/assets/b7717dd7-4201-4275-afab-c6509239c8a3" />

4. Scroll through the champions and click a champion name to open their skins.
5. In the champion window, click a skin name.

<img width="269" height="323" alt="image2" src="https://github.com/user-attachments/assets/0117d021-6ca6-476f-9139-9720c892453f" />

6. Click the chroma you want.
<img width="269" height="323" alt="image1" src="https://github.com/user-attachments/assets/a8db8ffd-5ec6-4ba7-a516-bd29b1f69290" />

7. Click any image or file name to open File Explorer highlighting the corresponding file.

## Dependencies
* [Python 3.10+](https://www.python.org/)
* [Pillow](https://pillow.readthedocs.io/en/stable/) - for image handling
* [requests](https://pypi.org/project/requests/)  – to fetch images from URLs
* [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)
* [darkseal-org skins folder](https://github.com/darkseal-org/lol-skins/tree/main/skins) this is the Super Folder containing the champion skin folders

## License
```text
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
