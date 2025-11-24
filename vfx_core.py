import cv2
import numpy as np

class VFXProcessor:
    def __init__(self):
        self.reference_bg = None

    def set_reference_background(self, frame):
        self.reference_bg = cv2.GaussianBlur(frame, (15, 15), 0)
        print("Background captured!")

    def apply_difference_key(self, frame, background_img, threshold=20):
        if self.reference_bg is None:
            return frame

        # Safety Check: Ensure background exists
        if background_img is None:
            return frame

        # --- STEP 1: PREPARE INPUTS ---
        frame_height, frame_width = frame.shape[:2]
        try:
            bg_resized = cv2.resize(background_img, (frame_width, frame_height))
        except Exception:
            return frame # Return original if resize fails

        # --- STEP 2: SHAPE DETECTION ---
        blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        delta = cv2.absdiff(self.reference_bg, blurred_frame)
        gray_delta = cv2.cvtColor(delta, cv2.COLOR_BGR2GRAY)
        _, raw_mask = cv2.threshold(gray_delta, threshold, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(raw_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clean_mask = np.zeros_like(raw_mask)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                cv2.drawContours(clean_mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
        
        clean_mask = cv2.GaussianBlur(clean_mask, (5, 5), 0)
        
        # --- STEP 3: COLOR HARMONIZATION ---
        try:
            avg_color_row = np.average(bg_resized, axis=0)
            avg_color = np.average(avg_color_row, axis=0)
            tint_layer = np.zeros_like(frame, dtype=np.uint8)
            tint_layer[:] = avg_color
            user_tinted = cv2.addWeighted(frame, 0.85, tint_layer, 0.15, 0)
            user_final = cv2.convertScaleAbs(user_tinted, alpha=1.1, beta=10)
        except Exception:
            user_final = frame # Fallback if color math fails

        # --- STEP 4: COMPOSITING ---
        mask_inv = cv2.bitwise_not(clean_mask)
        mask_stack = np.dstack([clean_mask]*3) / 255.0
        mask_inv_stack = np.dstack([mask_inv]*3) / 255.0

        fg = user_final.astype(float) * mask_stack
        bg = bg_resized.astype(float) * mask_inv_stack
        
        final_comp = cv2.add(fg, bg)
        
        # CRITICAL RETURN STATEMENT
        return final_comp.astype(np.uint8)

    def apply_cinematic_grade(self, frame):
        return frame