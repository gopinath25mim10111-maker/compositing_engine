import cv2
import numpy as np
import os
from vfx_core import VFXProcessor

def nothing(x): pass

def load_background_files():
    folder = "backgrounds"
    if not os.path.exists(folder): os.makedirs(folder); return []
    # Now we look for VIDEO files too (.mp4)
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4'))]
    return [os.path.join(folder, f) for f in files]

def main():
    print("--- LiteVFX Cinema Engine ---")
    print("1. Hide -> Press 'r'")
    print("2. 'a'/'d' to switch (Supports Video & Images)")
    print("3. Press 'v' to Record")
    print("Press 'q' to Quit")
    
    cap = cv2.VideoCapture(0)
    # Try HD, but fall back safely if camera doesn't support it
    cap.set(3, 1280)
    cap.set(4, 720)
    
    ret, test_frame = cap.read()
    if not ret: return
    h, w = test_frame.shape[:2]
    print(f"Resolution: {w}x{h}")

    engine = VFXProcessor()
    
    # VIDEO RECORDER
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    is_recording = False

    # GALLERY SYSTEM (Now supports Video Playback)
    bg_files = load_background_files()
    bg_index = 0
    
    # This variable holds the 'Video Player' for the background
    bg_cap = None 
    current_static_bg = None # For images
    is_video_bg = False

    # Load first background
    if len(bg_files) > 0:
        path = bg_files[0]
        if path.endswith(".mp4"):
            bg_cap = cv2.VideoCapture(path)
            is_video_bg = True
            print(f"Loaded Video: {path}")
        else:
            img = cv2.imread(path)
            if img is not None:
                current_static_bg = cv2.resize(img, (w, h))
                is_video_bg = False
                print(f"Loaded Image: {path}")

    # Fallback Background
    default_bg = np.zeros((h, w, 3), dtype=np.uint8)
    default_bg[:] = (20, 0, 20)

    window_name = 'LiteVFX - Cinema'
    cv2.namedWindow(window_name)
    cv2.createTrackbar('Sensitivity', window_name, 15, 100, nothing)

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)

        # --- BACKGROUND LOGIC ---
        bg_frame_to_use = default_bg

        if is_video_bg and bg_cap is not None:
            # READ VIDEO FRAME
            v_ret, v_frame = bg_cap.read()
            if not v_ret:
                # Loop video: If it ends, go back to frame 0
                bg_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                v_ret, v_frame = bg_cap.read()
            
            if v_ret:
                bg_frame_to_use = v_frame
            else:
                bg_frame_to_use = default_bg
        elif not is_video_bg and current_static_bg is not None:
            # USE STATIC IMAGE
            bg_frame_to_use = current_static_bg

        # --- VFX LOGIC ---
        if engine.reference_bg is None:
            final_render = frame.copy()
            cv2.putText(final_render, "Hide & Press 'r'", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        else:
            val = cv2.getTrackbarPos('Sensitivity', window_name)
            # The engine will resize the video frame automatically inside
            composited = engine.apply_difference_key(frame, bg_frame_to_use, val)
            final_render = composited

        # --- RECORDING & UI ---
        if is_recording:
            if out is not None: out.write(final_render)
            cv2.circle(final_render, (30, 30), 10, (0, 0, 255), -1)
            cv2.putText(final_render, "REC", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow(window_name, final_render)

        # --- CONTROLS ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            engine.set_reference_background(frame)
        elif key == ord('v'):
            if is_recording:
                is_recording = False
                if out: out.release(); out = None
                print("Saved.")
            else:
                is_recording = True
                out = cv2.VideoWriter('vfx_output.mp4', fourcc, 20.0, (w, h))
                print("Recording...")
        
        # SWITCH BACKGROUNDS (Updated for Video)
        elif key == ord('d') or key == ord('a'):
            if len(bg_files) > 0:
                # Release old video if it was playing
                if bg_cap: bg_cap.release()
                
                # Math to cycle index
                if key == ord('d'): bg_index = (bg_index + 1) % len(bg_files)
                else: bg_index = (bg_index - 1) % len(bg_files)
                
                path = bg_files[bg_index]
                if path.endswith(".mp4"):
                    bg_cap = cv2.VideoCapture(path)
                    is_video_bg = True
                    print(f"Switched to Video: {path}")
                else:
                    img = cv2.imread(path)
                    if img is not None:
                        current_static_bg = cv2.resize(img, (w, h))
                        is_video_bg = False
                        print(f"Switched to Image: {path}")

    cap.release()
    if bg_cap: bg_cap.release()
    if out: out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()