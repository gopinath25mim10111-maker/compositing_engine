# LiteVFX Engine: Real-Time Compositing Pipeline 🎬

> **A High-Performance Computer Vision VFX Engine optimized for low-spec hardware.**

LiteVFX is a Python-based real-time compositing tool designed to perform "Difference Keying" (Green-screen-style removal without a green screen) on integrated graphics systems (like Intel Celeron/UHD Graphics).

Unlike heavy AI models that lag on older laptops, LiteVFX uses **NumPy vectorization** and **Morphological Image Processing** to achieve high FPS compositing with features like video background playback and color harmonization.

## 🚀 Key Features

* **Difference Keying Algorithm:** Mathematically subtracts a static reference frame to isolate the subject.
* **Solid Body Detection:** Uses **Contour Finding** to fill the subject's body, solving the "transparent shirt" issue common in simple keyers.
* **Color Harmonization:** Automatically analyzes the background video's average color and tints the user to match the lighting (Light Wrapping).
* **Cinema-Grade Compositing:** Supports looping `.mp4` video backgrounds.
* **Integrated DVR:** Records HD (`.mp4`) output with a visual "REC" indicator.
* **Gallery System:** Hot-swappable backgrounds (Images & Video) using keyboard shortcuts.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Computer Vision:** OpenCV (`cv2`)
* **Math Engine:** NumPy
* **Hardware Target:** Optimized for Intel Celeron N4500 / 4GB RAM

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/LiteVFX_Engine.git](https://github.com/YOUR_USERNAME/LiteVFX_Engine.git)
    cd LiteVFX_Engine
    ```

2.  Install dependencies:
    ```bash
    pip install opencv-python numpy
    ```

3.  Download assets (Backgrounds):
    ```bash
    python setup_assets.py
    ```

## 🎮 How to Use

The Workflow:
Calibration: When the app starts, hide from the camera (duck down) so it sees only the wall.

Capture: Press r to memorize the empty room.

Action: Stand up. You will be composited into the scene.

Tuning: Use the Slider at the top.

Left (Lower): More solid body (Fixes holes).

Right (Higher): Cleaner background (Removes noise).

Directing:

d: Next Background (Video/Image).

a: Previous Background.

v: Start/Stop Recording.

q: Quit.

📂 Project Structure
main.py: The "Director." Handles camera input, user inputs, and video recording.

vfx_core.py: The "Math Engine." Contains the algorithms for Shape Detection, Keying, and Color Grading.

setup_assets.py: Automation script to download demo backgrounds from the web.

Built as a Portfolio Project for Computational Physics & Computer Vision.


#### 2. Create `.gitignore` (Crucial for Professionals)
This file tells GitHub: *"Do not upload my junk files."*
Create a file named `.gitignore` (yes, it starts with a dot) and paste this:

```text
# Ignore Python cache files
__pycache__/
*.py[cod]

# Ignore Video Outputs (Too big for GitHub)
*.avi
*.mp4

# Ignore the background images (Users should run the setup script)
backgrounds/

Run the main engine:
```bash
python main.py# compositing_engine
