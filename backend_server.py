"""
EduVision Physics Backend Server
Flask server that exposes physics simulators as web APIs
"""

from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
import cv2
import numpy as np
import base64
import json
import time
import threading
import math
from io import BytesIO

# Import simulators (we'll adapt them for web use)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# We'll create web-friendly versions of the simulators
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Global state for active simulators
active_simulators = {}
simulator_lock = threading.Lock()

# ==================== Simulator Classes (Web-Adapted) ====================

class WebProjectileSimulator:
    """Web-friendly projectile motion simulator"""
    def __init__(self):
        self.width = 800
        self.height = 480
        # Ensure content fits within canvas bounds
        self.max_x = self.width - 20
        self.max_y = self.height - 20
        self.gravity = 9.81
        self.pixels_per_meter = 12.0
        self.origin_px = (60, self.height - 60)
        self.projectiles = []
        self.trajectory = []
        self.last_update = time.time()
        self.max_dt = 0.05
        self.x_meters_visible = 20.0
        self.y_meters_visible = 10.0
        
    def launch(self, velocity, angle_deg):
        import math
        angle_rad = math.radians(angle_deg)
        vx = float(velocity) * math.cos(angle_rad)
        vy = float(velocity) * math.sin(angle_rad)
        self.projectiles.append({
            'x': 0.0, 'y': 0.0, 'vx': vx, 'vy': vy, 't': time.time()
        })
        self.trajectory = []
        
    def update(self):
        now = time.time()
        dt = min(self.max_dt, now - self.last_update)
        self.last_update = now
        
        alive = []
        for p in self.projectiles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] -= self.gravity * dt
            self.trajectory.append((p['x'], p['y']))
            if p['y'] >= -5.0 and p['x'] < 2000.0:
                alive.append(p)
        self.projectiles = alive
        
        # Render canvas
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        canvas[:] = (10, 10, 30)
        
        # Draw grid
        for m in range(0, int(self.x_meters_visible)+1):
            x_px = int(self.origin_px[0] + m * self.pixels_per_meter)
            cv2.line(canvas, (x_px, 0), (x_px, self.height), (40, 40, 60), 1)
        for m in range(0, int(self.y_meters_visible)+1):
            y_px = int(self.origin_px[1] - m * self.pixels_per_meter)
            cv2.line(canvas, (0, y_px), (self.width, y_px), (40, 40, 60), 1)
            
        # Draw axes
        x_end = int(self.origin_px[0] + self.x_meters_visible * self.pixels_per_meter)
        cv2.line(canvas, (self.origin_px[0], self.origin_px[1]), 
                 (x_end, self.origin_px[1]), (200, 200, 200), 2)
        y_top = int(self.origin_px[1] - self.y_meters_visible * self.pixels_per_meter)
        cv2.line(canvas, (self.origin_px[0], self.origin_px[1]), 
                 (self.origin_px[0], y_top), (200, 200, 200), 2)
        
        # Draw trajectory with visible color (clamp to canvas bounds)
        if len(self.trajectory) >= 2:
            for i in range(1, len(self.trajectory)):
                x1 = int(self.origin_px[0] + self.trajectory[i-1][0] * self.pixels_per_meter)
                y1 = int(self.origin_px[1] - self.trajectory[i-1][1] * self.pixels_per_meter)
                x2 = int(self.origin_px[0] + self.trajectory[i][0] * self.pixels_per_meter)
                y2 = int(self.origin_px[1] - self.trajectory[i][1] * self.pixels_per_meter)
                # Clamp coordinates to canvas bounds
                x1 = max(0, min(self.width - 1, x1))
                y1 = max(0, min(self.height - 1, y1))
                x2 = max(0, min(self.width - 1, x2))
                y2 = max(0, min(self.height - 1, y2))
                # Use bright yellow/orange color for trajectory
                cv2.line(canvas, (x1, y1), (x2, y2), (0, 200, 255), 2)
        
        # Draw projectiles (clamp to canvas bounds)
        for p in self.projectiles:
            x_px = int(self.origin_px[0] + p['x'] * self.pixels_per_meter)
            y_px = int(self.origin_px[1] - p['y'] * self.pixels_per_meter)
            x_px = max(0, min(self.width - 1, x_px))
            y_px = max(0, min(self.height - 1, y_px))
            cv2.circle(canvas, (x_px, y_px), 6, (0, 180, 255), -1)
        
        # Origin marker
        cv2.circle(canvas, self.origin_px, 4, (220, 220, 220), -1)
        
        return canvas

class WebOpticsSimulator:
    """Web-friendly optics simulator"""
    def __init__(self):
        self.width = 800
        self.height = 480
        self.axis_y = self.height // 2
        self.lens_x = self.width * 3 // 5
        self.obj_x = self.width // 5
        self.obj_h = min(80, self.height // 6)  # Scale object height to fit
        self.focal = 120
        self.mode = 0  # 0 = lens, 1 = mirror
        self.show_rays = True
        
    def update(self):
        import math
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        canvas[:] = (12, 18, 28)
        
        # Optical axis
        cv2.line(canvas, (0, self.axis_y), (self.width, self.axis_y), (180, 180, 180), 1)
        
        # Scale lens/mirror to fit canvas
        lens_height = min(180, self.height // 3)
        
        # Draw lens or mirror (scaled to fit)
        if self.mode == 0:
            cv2.rectangle(canvas, (self.lens_x - 8, self.axis_y - lens_height), 
                         (self.lens_x + 8, self.axis_y + lens_height), (180, 220, 255), -1)
            cv2.rectangle(canvas, (self.lens_x - 8, self.axis_y - lens_height), 
                         (self.lens_x + 8, self.axis_y + lens_height), (90, 140, 180), 2)
        else:
            cv2.ellipse(canvas, (self.lens_x, self.axis_y), (lens_height, lens_height), 0, -90, 90, 
                       (180, 220, 255), 3)
        
        # Draw object
        obj_top = (self.obj_x, self.axis_y - self.obj_h)
        obj_bottom = (self.obj_x, self.axis_y)
        cv2.line(canvas, obj_bottom, obj_top, (255, 200, 80), 3)
        cv2.rectangle(canvas, (self.obj_x - 6, self.axis_y - self.obj_h - 12), 
                     (self.obj_x + 6, self.axis_y - self.obj_h), (255, 200, 80), -1)
        
        # Calculate image
        u = self.lens_x - self.obj_x
        if u == 0:
            u = 1e-6
        
        if self.mode == 0:
            eps = 1e-9
            denom = (1.0 / (self.focal + eps) - 1.0 / (u + eps))
            v = 1.0 / denom if abs(denom) > 1e-12 else float('inf')
        else:
            eps = 1e-9
            denom = (1.0 / (self.focal + eps) - 1.0 / (u + eps))
            v = 1.0 / denom if abs(denom) > 1e-12 else float('inf')
        
        if np.isfinite(v):
            image_x = int(self.lens_x + v)
            m = -v / u if abs(u) > 1e-9 else 0
            img_h = int(m * self.obj_h)
            img_top = (image_x, self.axis_y - img_h)
            img_bottom = (image_x, self.axis_y)
            color = (255, 230, 120) if v > 0 else (120, 235, 255)
            cv2.line(canvas, img_bottom, img_top, color, 2)
            cv2.rectangle(canvas, (image_x - 6, self.axis_y - img_h - 10), 
                         (image_x + 6, self.axis_y - img_h), color, -1)
        
        # Focal points
        fpx = int(self.lens_x + self.focal)
        fnx = int(self.lens_x - self.focal)
        cv2.circle(canvas, (fpx, self.axis_y), 4, (120, 255, 200), -1)
        cv2.circle(canvas, (fnx, self.axis_y), 4, (255, 120, 200), -1)
        
        # Draw principal rays if enabled
        if self.show_rays:
            y0 = self.axis_y - self.obj_h
            image_x = None
            img_h = 0
            
            if np.isfinite(v):
                image_x = int(self.lens_x + v)
                m = -v / u if abs(u) > 1e-9 else 0
                img_h = int(m * self.obj_h)
            
            # Ray 1: Parallel to axis from top of object -> through focal after lens
            p0 = (self.obj_x, int(y0))
            p1 = (self.lens_x, int(y0))
            cv2.line(canvas, p0, p1, (255, 255, 255), 1, cv2.LINE_AA)
            
            if self.mode == 0:  # Lens
                # Refracted: through focal point on other side
                if image_x is not None and np.isfinite(v):
                    p2 = (int(image_x), int(self.axis_y - img_h))
                    cv2.line(canvas, p1, p2, (255, 255, 255), 1, cv2.LINE_AA)
                else:
                    # Go toward focal point
                    p_f = (int(self.lens_x + self.focal), self.axis_y)
                    dx = 800
                    if self.focal != 0:
                        t = dx
                        p_far = (int(self.lens_x + t), int(y0 + (self.axis_y - p_f[1]) * (t / max(1, abs(self.focal)))))
                        cv2.line(canvas, p1, p_far, (255, 255, 255), 1, cv2.LINE_AA)
            else:  # Mirror
                # Reflect direction
                dx = -800 if self.focal > 0 else 800
                p_far = (int(self.lens_x + dx), int(y0))
                cv2.line(canvas, p1, p_far, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Ray 2: Through center of lens (undeviated)
            center = (self.lens_x, self.axis_y)
            if abs(self.lens_x - self.obj_x) > 1:
                p_end_x = center[0] + 300
                p_end_y = int(y0 + (center[1] - y0) * (300 / abs(self.lens_x - self.obj_x)))
                cv2.line(canvas, (self.obj_x, int(y0)), (p_end_x, p_end_y), (200, 200, 255), 1, cv2.LINE_AA)
            
            # Ray 3: Through focal point (object side) -> emerges parallel
            focal_obj_side = (self.lens_x - self.focal, self.axis_y)
            cv2.line(canvas, (self.obj_x, int(y0)), (int(focal_obj_side[0]), int(focal_obj_side[1])), (200, 255, 200), 1, cv2.LINE_AA)
            if self.mode == 0:  # Lens
                cv2.line(canvas, (int(focal_obj_side[0]), int(focal_obj_side[1])), (self.lens_x + 400, int(y0)), (200, 255, 200), 1, cv2.LINE_AA)
        
        return canvas

class WebWaveSimulator:
    """Web-friendly wave interference simulator"""
    def __init__(self):
        self.width = 780
        self.height = 480
        self.c = 1.0
        self.decay = 0.08
        self.sources = [
            {'pos': np.array([self.width*0.33, self.height*0.5]), 'amp': 0.9, 'freq': 1.2, 'phase': 0.0},
            {'pos': np.array([self.width*0.66, self.height*0.5]), 'amp': 0.9, 'freq': 1.2, 'phase': 0.0},
        ]
        self.two_source = True
        self.grid_x, self.grid_y = np.meshgrid(np.arange(self.width), np.arange(self.height))
        self.t = 0.0
        self.paused = False
        
    def update(self, dt=0.033):
        import math
        if not self.paused:
            self.t += dt
        
        field = np.zeros((self.height, self.width), dtype=np.float32)
        active = [self.sources[0]]
        if self.two_source:
            active.append(self.sources[1])
            
        for s in active:
            sx, sy = s['pos']
            rx = (self.grid_x - sx).astype(np.float32)
            ry = (self.grid_y - sy).astype(np.float32)
            r = np.hypot(rx, ry) + 1e-6
            omega = 2.0 * math.pi * float(s['freq'])
            arg = omega * (self.t - (r / self.c))
            att = 1.0 / (1.0 + r * self.decay)
            contrib = float(s['amp']) * att * np.sin(arg)
            field += contrib.astype(np.float32)
        
        # Render to color map
        vmax = max(0.5, np.max(np.abs(field)))
        img_norm = (field / vmax) * 127.0 + 128.0
        img_u8 = np.clip(img_norm, 0, 255).astype(np.uint8)
        canvas = cv2.applyColorMap(img_u8, cv2.COLORMAP_TURBO)
        
        # Draw sources
        cv2.circle(canvas, tuple(self.sources[0]['pos'].astype(int)), 8, (255, 255, 255), -1)
        if self.two_source:
            cv2.circle(canvas, tuple(self.sources[1]['pos'].astype(int)), 8, (255, 255, 255), -1)
        
        return canvas

class WebRotationalSimulator:
    """Web-friendly rotational motion simulator"""
    def __init__(self):
        self.width = 800
        self.height = 480
        self.center = (self.width // 2, self.height // 2)
        self.radius_m = 1.0
        self.pixels_per_meter = 80.0
        self.omega = 2.0
        self.theta = 0.0
        self.trail = []
        self.last_update = time.time()
        
    def update(self):
        import math
        now = time.time()
        dt = min(0.05, now - self.last_update)
        self.last_update = now
        
        self.theta += self.omega * dt
        x = self.radius_m * math.cos(self.theta)
        y = self.radius_m * math.sin(self.theta)
        self.trail.append((x, y))
        if len(self.trail) > 400:
            self.trail.pop(0)
        
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        canvas[:] = (20, 20, 20)
        
        r_px = int(round(self.radius_m * self.pixels_per_meter))
        cv2.circle(canvas, self.center, abs(r_px), (70, 70, 70), 2)
        cv2.line(canvas, (0, self.center[1]), (self.width, self.center[1]), (100, 100, 100), 1)
        cv2.line(canvas, (self.center[0], 0), (self.center[0], self.height), (100, 100, 100), 1)
        
        # Draw trail
        if len(self.trail) >= 2:
            pts = [(int(self.center[0] + xx * self.pixels_per_meter), 
                   int(self.center[1] - yy * self.pixels_per_meter)) 
                  for (xx, yy) in self.trail]
            for i in range(1, len(pts)):
                cv2.line(canvas, pts[i-1], pts[i], (200, 200, 200), 1)
        
        # Draw current position
        px = (int(self.center[0] + x * self.pixels_per_meter), 
              int(self.center[1] - y * self.pixels_per_meter))
        cv2.circle(canvas, px, 8, (0, 180, 255), -1)
        
        return canvas

class WebTrigSimulator:
    """Web-friendly trigonometric graph visualizer"""
    def __init__(self):
        self.width = 800
        self.height = 480
        self.func = 'sin'
        self.angle_deg = 30.0
        self.x_left = -360
        self.x_right = 360
        self.y_clip = 5.0
        self.show_grid = True
        
    def deg2rad(self, d):
        import math
        return d * math.pi / 180.0
    
    def compute_trig(self, fn, x_rad):
        import numpy as np
        if fn == "sin":
            y = np.sin(x_rad)
        elif fn == "cos":
            y = np.cos(x_rad)
        elif fn == "tan":
            y = np.tan(x_rad)
        elif fn == "csc":
            y = 1.0 / np.sin(x_rad)
        elif fn == "sec":
            y = 1.0 / np.cos(x_rad)
        elif fn == "cot":
            y = 1.0 / np.tan(x_rad)
        else:
            y = np.sin(x_rad)
        mask = np.isfinite(y) & (np.abs(y) < 1e6)
        return y, mask
    
    def update(self):
        import math
        import numpy as np
        
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        canvas[:] = (13, 13, 13)  # Dark background
        
        # Calculate graph area (with margins)
        margin = 60
        graph_x = margin
        graph_y = margin
        graph_w = self.width - 2 * margin
        graph_h = self.height - 2 * margin
        
        # Build x axis in degrees and radians
        x_degs = np.linspace(self.x_left, self.x_right, 2000)
        x_rads = np.array([self.deg2rad(d) for d in x_degs])
        
        # Compute y values
        y_vals, valid_mask = self.compute_trig(self.func, x_rads)
        
        # Find discontinuities
        diff = np.zeros_like(y_vals)
        diff[1:] = np.abs(np.diff(y_vals))
        big_jump = diff > (self.y_clip * 0.5)
        break_mask = (~valid_mask) | big_jump
        
        # Map degrees to pixel x coordinates
        def deg_to_x(deg):
            t = (deg - self.x_left) / (self.x_right - self.x_left) if (self.x_right - self.x_left) != 0 else 0
            return int(graph_x + t * graph_w)
        
        # Map y value to pixel y coordinates
        def y_to_pixel(y_val):
            t = (y_val + self.y_clip) / (2 * self.y_clip) if self.y_clip > 0 else 0.5
            t = max(0, min(1, t))
            return int(graph_y + (1 - t) * graph_h)
        
        # Draw grid if enabled
        if self.show_grid:
            # Horizontal grid lines (y values)
            for y_val in np.arange(-self.y_clip, self.y_clip + 0.5, 1.0):
                if abs(y_val) < 0.1:
                    continue  # Skip zero line (will draw axis)
                y_px = y_to_pixel(y_val)
                cv2.line(canvas, (graph_x, y_px), (graph_x + graph_w, y_px), (40, 40, 60), 1)
            
            # Vertical grid lines (x values)
            step = max(30, (self.x_right - self.x_left) // 20)
            for x_deg in range(int(self.x_left), int(self.x_right) + 1, step):
                x_px = deg_to_x(x_deg)
                cv2.line(canvas, (x_px, graph_y), (x_px, graph_y + graph_h), (40, 40, 60), 1)
        
        # Draw axes
        zero_y_px = y_to_pixel(0)
        cv2.line(canvas, (graph_x, zero_y_px), (graph_x + graph_w, zero_y_px), (200, 200, 200), 2)
        
        zero_x_deg = 0
        if self.x_left <= zero_x_deg <= self.x_right:
            zero_x_px = deg_to_x(zero_x_deg)
            cv2.line(canvas, (zero_x_px, graph_y), (zero_x_px, graph_y + graph_h), (200, 200, 200), 2)
        
        # Draw function curve (split at discontinuities)
        segments_x = []
        segments_y = []
        current_x = []
        current_y = []
        
        for xi, yi, br in zip(x_degs, y_vals, break_mask):
            if br:
                if current_x:
                    segments_x.append(np.array(current_x))
                    segments_y.append(np.array(current_y))
                    current_x = []
                    current_y = []
            else:
                if abs(yi) <= self.y_clip:  # Only draw if within clip range
                    current_x.append(xi)
                    current_y.append(yi)
        
        if current_x:
            segments_x.append(np.array(current_x))
            segments_y.append(np.array(current_y))
        
        # Draw each continuous segment
        color = (0, 140, 255)  # Math accent color (blue)
        for sx, sy in zip(segments_x, segments_y):
            if len(sx) < 2:
                continue
            points = []
            for x_deg, y_val in zip(sx, sy):
                x_px = deg_to_x(x_deg)
                y_px = y_to_pixel(y_val)
                points.append((x_px, y_px))
            
            # Draw as connected lines
            for i in range(1, len(points)):
                if 0 <= points[i-1][0] < self.width and 0 <= points[i-1][1] < self.height and \
                   0 <= points[i][0] < self.width and 0 <= points[i][1] < self.height:
                    cv2.line(canvas, points[i-1], points[i], color, 2)
        
        # Draw vertical marker at selected angle
        x_sel = float(self.angle_deg)
        if self.x_left <= x_sel <= self.x_right:
            x_sel_px = deg_to_x(x_sel)
            cv2.line(canvas, (x_sel_px, graph_y), (x_sel_px, graph_y + graph_h), (0, 255, 0), 1, cv2.LINE_AA)
            
            # Draw point marker
            y_sel, ok = self.compute_trig(self.func, np.array([self.deg2rad(x_sel)]))
            y_point = y_sel[0] if ok[0] and np.isfinite(y_sel[0]) and abs(y_sel[0]) <= self.y_clip else None
            
            if y_point is not None:
                y_sel_px = y_to_pixel(y_point)
                cv2.circle(canvas, (x_sel_px, y_sel_px), 6, (255, 0, 0), -1)
                
                # Label
                label = f"{y_point:.3f}"
                cv2.putText(canvas, label, (x_sel_px + 8, y_sel_px - 8), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw asymptotes for tan/cot/sec/csc
        if self.func in ("tan", "sec"):
            k_vals = np.arange(math.floor((self.x_left-90)/180)-1, math.ceil((self.x_right-90)/180)+1)
            for k in k_vals:
                xpos = 90 + 180*k
                if self.x_left - 1 <= xpos <= self.x_right + 1:
                    x_px = deg_to_x(xpos)
                    cv2.line(canvas, (x_px, graph_y), (x_px, graph_y + graph_h), (100, 100, 100), 1, cv2.LINE_AA)
        if self.func in ("cot", "csc"):
            k_vals = np.arange(math.floor(self.x_left/180)-1, math.ceil(self.x_right/180)+1)
            for k in k_vals:
                xpos = 180 * k
                if self.x_left - 1 <= xpos <= self.x_right + 1:
                    x_px = deg_to_x(xpos)
                    cv2.line(canvas, (x_px, graph_y), (x_px, graph_y + graph_h), (100, 100, 100), 1, cv2.LINE_AA)
        
        # Draw labels (properly spaced to avoid overlap)
        # Function name at top left
        cv2.putText(canvas, f"{self.func}(x)", (10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        # Angle info at top right (without degree symbol to avoid question marks)
        angle_text = f"Angle: {self.angle_deg:.1f} deg"
        (text_width, text_height), _ = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.putText(canvas, angle_text, (self.width - text_width - 15, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 1)
        # X range at bottom left (without degree symbols)
        x_range_text = f"X: [{self.x_left} to {self.x_right}] deg"
        cv2.putText(canvas, x_range_text, (10, self.height - 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        # Y range at bottom right
        y_range_text = f"Y: [-{self.y_clip:.1f} to {self.y_clip:.1f}]"
        (y_text_width, _), _ = cv2.getTextSize(y_range_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.putText(canvas, y_range_text, (self.width - y_text_width - 15, self.height - 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return canvas

# ==================== Helper Functions ====================

def image_to_base64(img):
    """Convert OpenCV image to base64 string"""
    _, buffer = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

# ---------------- Play audio helper ----------------
def play_audio_file(path):
    """Play an audio file non-blocking. Uses pygame if available, falls back to os.startfile (Windows)."""
    try:
        # Only run in main Werkzeug process to avoid double-play during reload
        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            return

        # Try pygame first (if available)
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()  # non-blocking
            print(f"▶️ Playing audio via pygame: {path}")
            return
        except Exception as e_pyg:
            print(f"⚠️ pygame play failed: {e_pyg}; trying os.startfile fallback")

        # Fallback for Windows (open with default app)
        if os.name == 'nt':
            try:
                os.startfile(path)
                print(f"▶️ Opened audio with os.startfile: {path}")
                return
            except Exception as e_os:
                print(f"❌ os.startfile fallback failed: {e_os}")

        print("⚠️ No available method to play audio on this platform.")
    except Exception as e:
        print(f"❌ Error in play_audio_file: {e}")

def play_most_recent_audio(temp_dir='temp_audio', specific_path=None):
    """If specific_path provided, play it; otherwise pick newest .mp3 in temp_dir. Runs in background thread."""
    try:
        if specific_path and os.path.exists(specific_path):
            path = specific_path
        else:
            if not os.path.exists(temp_dir):
                print("⚠️ temp_audio folder does not exist.")
                return
            mp3s = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith('.mp3')]
            if not mp3s:
                print("⚠️ No mp3 files found in temp_audio.")
                return
            path = max(mp3s, key=os.path.getmtime)
        # Spawn daemon thread so request handling isn't blocked
        t = threading.Thread(target=play_audio_file, args=(path,), daemon=True)
        t.start()
    except Exception as e:
        print(f"❌ Error in play_most_recent_audio: {e}")
# ---------------------------------------------------

# ==================== API Routes ====================

@app.route('/api/physics/simulators', methods=['GET'])
def list_simulators():
    """List available physics simulators"""
    return jsonify({
        'simulators': [
            {'id': 'projectile', 'name': 'Projectile Motion', 'description': 'Gesture-controlled projectile simulation'},
            {'id': 'optics', 'name': 'Optics Simulator', 'description': 'Lens and mirror ray tracing'},
            {'id': 'wave', 'name': 'Wave Interference', 'description': 'Wave interference patterns'},
            {'id': 'rotational', 'name': 'Rotational Motion', 'description': 'Circular motion visualization'}
        ]
    })

@app.route('/api/maths/simulators', methods=['GET'])
def list_maths_simulators():
    """List available mathematics simulators"""
    return jsonify({
        'simulators': [
            {'id': 'trig', 'name': 'Trigonometric Visualizer', 'description': 'Interactive trigonometric graph with angle marker'}
        ]
    })

@app.route('/api/physics/simulator/<simulator_id>/start', methods=['POST'])
def start_simulator(simulator_id):
    """Start a simulator instance"""
    session_id = request.json.get('session_id', f'session_{int(time.time())}')
    
    with simulator_lock:
        if simulator_id == 'projectile':
            active_simulators[session_id] = WebProjectileSimulator()
        elif simulator_id == 'optics':
            active_simulators[session_id] = WebOpticsSimulator()
        elif simulator_id == 'wave':
            active_simulators[session_id] = WebWaveSimulator()
        elif simulator_id == 'rotational':
            active_simulators[session_id] = WebRotationalSimulator()
        else:
            return jsonify({'error': 'Unknown simulator'}), 400
    
    return jsonify({'session_id': session_id, 'status': 'started'})

@app.route('/api/maths/simulator/<simulator_id>/start', methods=['POST'])
def start_maths_simulator(simulator_id):
    """Start a mathematics simulator instance"""
    session_id = request.json.get('session_id', f'session_{int(time.time())}')
    
    with simulator_lock:
        if simulator_id == 'trig':
            active_simulators[session_id] = WebTrigSimulator()
        else:
            return jsonify({'error': 'Unknown simulator'}), 400
    
    return jsonify({'session_id': session_id, 'status': 'started'})

@app.route('/api/physics/simulator/<simulator_id>/update', methods=['POST'])
def update_simulator(simulator_id):
    """Update simulator state and get frame"""
    session_id = request.json.get('session_id')
    params = request.json.get('params', {})
    
    if session_id not in active_simulators:
        return jsonify({'error': 'Simulator not found'}), 404
    
    sim = active_simulators[session_id]
    
    # Update parameters based on simulator type
    if simulator_id == 'projectile':
        if 'launch' in params:
            sim.launch(params['launch']['velocity'], params['launch']['angle'])
    elif simulator_id == 'optics':
        if 'obj_x' in params:
            sim.obj_x = params['obj_x']
        if 'obj_h' in params:
            sim.obj_h = params['obj_h']
        if 'lens_x' in params:
            sim.lens_x = params['lens_x']
        if 'focal' in params:
            sim.focal = params['focal']
        if 'mode' in params:
            sim.mode = params['mode']
        if 'show_rays' in params:
            sim.show_rays = params['show_rays']
    elif simulator_id == 'wave':
        if 'freq' in params:
            for s in sim.sources:
                s['freq'] = params['freq']
        if 'amp' in params:
            for s in sim.sources:
                s['amp'] = params['amp']
        if 'paused' in params:
            sim.paused = params['paused']
    elif simulator_id == 'rotational':
        if 'radius' in params:
            sim.radius_m = params['radius']
        if 'omega' in params:
            sim.omega = params['omega']
    
    # Get frame
    if simulator_id == 'wave':
        canvas = sim.update(dt=0.033)
    else:
        canvas = sim.update()
    
    img_base64 = image_to_base64(canvas)
    
    return jsonify({
        'frame': f'data:image/png;base64,{img_base64}',
        'timestamp': time.time()
    })

@app.route('/api/maths/simulator/<simulator_id>/update', methods=['POST'])
def update_maths_simulator(simulator_id):
    """Update mathematics simulator state and get frame"""
    session_id = request.json.get('session_id')
    params = request.json.get('params', {})
    
    if session_id not in active_simulators:
        return jsonify({'error': 'Simulator not found'}), 404
    
    sim = active_simulators[session_id]
    
    # Update parameters for trig simulator
    if simulator_id == 'trig':
        if 'func' in params:
            sim.func = params['func']
        if 'angle_deg' in params:
            sim.angle_deg = float(params['angle_deg'])
        if 'x_left' in params:
            sim.x_left = int(params['x_left'])
        if 'x_right' in params:
            sim.x_right = int(params['x_right'])
        if 'y_clip' in params:
            sim.y_clip = float(params['y_clip'])
        if 'show_grid' in params:
            sim.show_grid = bool(params['show_grid'])
    
    # Get frame
    canvas = sim.update()
    img_base64 = image_to_base64(canvas)
    
    return jsonify({
        'frame': f'data:image/png;base64,{img_base64}',
        'timestamp': time.time()
    })

@app.route('/api/physics/simulator/<simulator_id>/stop', methods=['POST'])
def stop_simulator(simulator_id):
    """Stop a simulator instance"""
    session_id = request.json.get('session_id')
    
    with simulator_lock:
        if session_id in active_simulators:
            del active_simulators[session_id]
            return jsonify({'status': 'stopped'})
        else:
            return jsonify({'error': 'Simulator not found'}), 404

@app.route('/api/maths/simulator/<simulator_id>/stop', methods=['POST'])
def stop_maths_simulator(simulator_id):
    """Stop a mathematics simulator instance"""
    session_id = request.json.get('session_id')
    
    with simulator_lock:
        if session_id in active_simulators:
            del active_simulators[session_id]
            return jsonify({'status': 'stopped'})
        else:
            return jsonify({'error': 'Simulator not found'}), 404

@app.route('/api/physics/gesture/process', methods=['POST'])
def process_gesture():
    """Process gesture data from frontend image with MediaPipe hand detection"""
    try:
        data = request.json
        image_base64 = data.get('image')
        
        if not image_base64:
            return jsonify({
                'left_dist': None,
                'right_dist': None,
                'pinch': False,
                'hands_detected': False,
                'annotated_frame': None
            })
        
        # Decode base64 image
        import base64
        image_data = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({
                'left_dist': None,
                'right_dist': None,
                'pinch': False,
                'hands_detected': False,
                'annotated_frame': None
            })
        
        # Convert BGR to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb.flags.writeable = False
        
        # Process with MediaPipe Hands
        try:
            import mediapipe as mp
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            
            # Initialize MediaPipe Hands if not already done
            if not hasattr(process_gesture, 'hands'):
                process_gesture.hands = mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=2,
                    min_detection_confidence=0.6,
                    min_tracking_confidence=0.6
                )
            
            results = process_gesture.hands.process(img_rgb)
            img_rgb.flags.writeable = True
            
            # Draw landmarks on the image
            annotated_img = img.copy()
            left_dist = None
            right_dist = None
            hands_detected = False
            
            if results.multi_hand_landmarks and results.multi_handedness:
                hands_detected = True
                img_h, img_w = annotated_img.shape[:2]
                
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Draw hand landmarks and connections
                    mp_drawing.draw_landmarks(
                        annotated_img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
                    
                    # Get hand label (Left or Right from camera perspective)
                    label = handedness.classification[0].label
                    
                    # Calculate normalized distance between thumb tip (4) and index tip (8)
                    lm = hand_landmarks.landmark
                    thumb_tip = lm[4]
                    index_tip = lm[8]
                    
                    # Calculate distance in normalized coordinates
                    dx = (index_tip.x - thumb_tip.x) * img_w
                    dy = (index_tip.y - thumb_tip.y) * img_h
                    dist_px = math.sqrt(dx*dx + dy*dy)
                    # Normalize by image diagonal
                    img_diag = math.sqrt(img_w*img_w + img_h*img_h)
                    normalized_dist = dist_px / img_diag if img_diag > 0 else 0
                    
                    # Draw line between thumb and index finger tips
                    x1, y1 = int(thumb_tip.x * img_w), int(thumb_tip.y * img_h)
                    x2, y2 = int(index_tip.x * img_w), int(index_tip.y * img_h)
                    cv2.line(annotated_img, (x1, y1), (x2, y2), (200, 200, 0), 2)
                    mid = ((x1+x2)//2, (y1+y2)//2)
                    cv2.circle(annotated_img, mid, 6, (255, 180, 0), -1)
                    
                    # Assign to left or right hand
                    # Note: MediaPipe's "Left" means left hand from user's perspective
                    if label == "Left":
                        left_dist = normalized_dist
                    else:
                        right_dist = normalized_dist
            
            # Pinch detection (right hand distance < threshold)
            pinch = False
            if right_dist is not None and right_dist < 0.15:
                pinch = True
            
            # Encode annotated frame to base64
            _, buffer = cv2.imencode('.jpg', annotated_img, [cv2.IMWRITE_JPEG_QUALITY, 85])
            annotated_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                'left_dist': left_dist,
                'right_dist': right_dist,
                'pinch': pinch,
                'hands_detected': hands_detected,
                'annotated_frame': f'data:image/jpeg;base64,{annotated_base64}'
            })
            
        except ImportError:
            # MediaPipe not available, return without landmarks
            return jsonify({
                'left_dist': None,
                'right_dist': None,
                'pinch': False,
                'hands_detected': False,
                'annotated_frame': None,
                'error': 'MediaPipe not available'
            })
            
    except Exception as e:
        print(f"Gesture processing error: {e}")
        return jsonify({
            'left_dist': None,
            'right_dist': None,
            'pinch': False,
            'hands_detected': False,
            'annotated_frame': None,
            'error': str(e)
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'active_simulators': len(active_simulators)})

# ==================== Text to Animation API (using tta.py) ====================

# Import tta.py functions (without modifying tta.py)
import sys
import os
import threading
import re
import base64
import subprocess

# Add gesture directory to path
gesture_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gesture')
if os.path.exists(gesture_dir):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import tta functions
TTA_AVAILABLE = False
summarize_topic = None
generate_questions = None
text_to_speech = None
generate_manim_code = None
render_video = None

try:
    # Try to import tta module
    import importlib.util
    # Get the correct path to tta.py
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    tta_path = os.path.join(backend_dir, 'gesture', 'tta.py')
    
    # Normalize the path
    tta_path = os.path.normpath(tta_path)
    
    print(f"🔍 Looking for tta.py at: {tta_path}")
    print(f"📁 Backend directory: {backend_dir}")
    
    if not os.path.exists(tta_path):
        # Try alternative path (if backend is in a subdirectory)
        alt_path = os.path.join(backend_dir, '..', 'gesture', 'tta.py')
        alt_path = os.path.normpath(os.path.abspath(alt_path))
        print(f"🔍 Trying alternative path: {alt_path}")
        if os.path.exists(alt_path):
            tta_path = alt_path
    
    if os.path.exists(tta_path):
        print(f"✅ Found tta.py at: {tta_path}")
        # Import tta.py directly as a module (it already has the correct fallback code)
        spec = importlib.util.spec_from_file_location("tta", tta_path)
        tta = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(tta)
            
            # Extract functions
            summarize_topic = tta.summarize_topic
            generate_questions = tta.generate_questions
            text_to_speech = tta.text_to_speech
            generate_manim_code = tta.generate_manim_code
            render_video = tta.render_video  # Also get render_video function
            TTA_AVAILABLE = True
            print("✅ TTA module loaded successfully")
            print(f"   - summarize_topic: {summarize_topic is not None}")
            print(f"   - generate_questions: {generate_questions is not None}")
            print(f"   - text_to_speech: {text_to_speech is not None}")
            print(f"   - generate_manim_code: {generate_manim_code is not None}")
            print(f"   - render_video: {render_video is not None}")
        except Exception as e:
            print(f"❌ Error loading TTA module: {e}")
            import traceback
            traceback.print_exc()
            TTA_AVAILABLE = False
    else:
        print(f"❌ tta.py not found at {tta_path}")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   Backend directory: {backend_dir}")
        TTA_AVAILABLE = False
except Exception as e:
    print(f"❌ Failed to load tta.py: {e}")
    import traceback
    traceback.print_exc()
    TTA_AVAILABLE = False

@app.route('/api/tta/summarize', methods=['POST'])
def tta_summarize():
    """Generate summary for a topic"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        subject = data.get('subject', 'general')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        summary = summarize_topic(topic)
        return jsonify({
            'summary': summary,
            'topic': topic,
            'subject': subject
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tta/generate-questions', methods=['POST'])
def tta_generate_questions():
    """Generate MCQ questions for a topic"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        questions = generate_questions(topic)
        return jsonify({
            'questions': questions,
            'topic': topic
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tta/generate-audio', methods=['POST'])
def tta_generate_audio():
    """Generate audio from text"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        text = data.get('text', '')
        topic = data.get('topic', 'topic')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Generate filename
        filename = re.sub(r'[^A-Za-z0-9_]', '_', topic) + ".mp3"
        filepath = os.path.join('temp_audio', filename)
        
        # Create temp_audio directory if it doesn't exist
        os.makedirs('temp_audio', exist_ok=True)
        
        # Generate speech
        text_to_speech(text, filepath)

        # Auto-play generated file (background) — no new files created
        try:
            play_most_recent_audio(specific_path=filepath)
        except Exception as e:
            print(f"⚠️ Auto-play failed to start: {e}")
        
        # Read and encode audio file
        with open(filepath, 'rb') as f:
            audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            'audio': f'data:audio/mpeg;base64,{audio_base64}',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tta/generate-manim', methods=['POST'])
def tta_generate_manim():
    """Generate Manim code for a topic"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        subject = data.get('subject', 'general')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        manim_code = generate_manim_code(topic)
        
        return jsonify({
            'manim_code': manim_code,
            'topic': topic,
            'subject': subject
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tta/render-video', methods=['POST'])
def tta_render_video():
    """Render Manim code to video"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        manim_code = data.get('manim_code', '')
        topic = data.get('topic', 'topic')
        
        if not manim_code:
            return jsonify({'error': 'Manim code is required'}), 400
        
        # Save Manim code to file
        filename = re.sub(r'[^A-Za-z0-9_]', '_', topic) + ".py"
        filepath = os.path.join('temp_manim', filename)
        os.makedirs('temp_manim', exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(manim_code)
        
        # Render video in background
        def render():
            import sys
            python_cmd = sys.executable
            # Get absolute paths
            base_dir = os.path.dirname(os.path.abspath(__file__))
            abs_filepath = os.path.abspath(filepath)
            filename_only = os.path.basename(filepath)
            filename_without_ext = os.path.splitext(filename_only)[0]
            
            # Manim outputs to media/videos/<filename_without_ext>/<quality>/<scene>.mp4
            # Use -pql for preview quality low (faster rendering)
            # Run from project root so media directory is created there
            cmd = f"{python_cmd} -m manim -pql {abs_filepath} AutoTeach"
            print(f"🎬 Starting video rendering...")
            print(f"📁 Working directory: {base_dir}")
            print(f"📄 Manim file: {abs_filepath}")
            print(f"📄 Filename (for output): {filename_without_ext}")
            print(f"🔧 Command: {cmd}")
            
            try:
                # Run Manim and capture output
                process = subprocess.Popen(
                    cmd, 
                    shell=True, 
                    cwd=base_dir, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for completion with timeout
                try:
                    stdout, stderr = process.communicate(timeout=600)
                    return_code = process.returncode
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    return_code = -1
                    print(f"❌ Video rendering timed out after 10 minutes")
                
                if return_code == 0:
                    print(f"✅ Video rendered successfully!")
                    if stdout:
                        output = stdout[-1000:] if len(stdout) > 1000 else stdout
                        print("Manim output:", output)
                    
                    # Check if video file exists
                    expected_paths = [
                        os.path.join(base_dir, 'media', 'videos', filename_without_ext, '480p15', 'AutoTeach.mp4'),
                        os.path.join(base_dir, 'media', 'videos', filename_without_ext, '720p30', 'AutoTeach.mp4'),
                    ]
                    found = False
                    for path in expected_paths:
                        if os.path.exists(path):
                            print(f"✅ Video file found at: {path}")
                            found = True
                            break
                    if not found:
                        print(f"⚠️ Video file not found in expected locations")
                        print(f"   Searched: {expected_paths}")
                else:
                    print(f"❌ Video rendering failed (return code: {return_code})")
                    if stderr:
                        error = stderr[-1000:] if len(stderr) > 1000 else stderr
                        print("Error output:", error)
                    if stdout:
                        output = stdout[-1000:] if len(stdout) > 1000 else stdout
                        print("Standard output:", output)
            except Exception as e:
                print(f"❌ Exception during video rendering: {e}")
                import traceback
                traceback.print_exc()
        
        render_thread = threading.Thread(target=render)
        render_thread.start()
        
        # Return immediately with status
        return jsonify({
            'status': 'rendering',
            'message': 'Video rendering started. This may take a few minutes.',
            'video_path': f'/api/tta/video/{re.sub(r"[^A-Za-z0-9_]", "_", topic)}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/temp_audio/<filename>', methods=['GET', 'OPTIONS'])
def tta_get_audio(filename):
    """Serve audio files from temp_audio folder"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(base_dir, 'temp_audio', filename)
        
        print(f"🔍 Serving audio file: {audio_path}")
        print(f"   File exists: {os.path.exists(audio_path)}")
        
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"✅ Audio file found: {audio_path} ({file_size} bytes)")
            response = send_file(audio_path, mimetype='audio/mpeg')
            # Add CORS headers
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response
        else:
            print(f"❌ Audio file not found: {audio_path}")
            error_response = jsonify({'error': 'Audio file not found'})
            error_response.headers.add('Access-Control-Allow-Origin', '*')
            error_response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
            return error_response, 404
    except Exception as e:
        print(f"❌ Error serving audio: {e}")
        import traceback
        traceback.print_exc()
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        error_response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return error_response, 500

@app.route('/api/tta/video/<topic>', methods=['GET', 'OPTIONS', 'HEAD'])
def tta_get_video(topic):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS, HEAD')
        response.headers.add('Access-Control-Allow-Headers', 'Range, Content-Type')
        return response
    """Serve rendered Manim video"""
    try:
        # Manim saves videos in media/videos/<filename_without_ext>/<quality>/AutoTeach.mp4
        # The filename is the topic name with special chars replaced
        safe_topic = re.sub(r'[^A-Za-z0-9_]', '_', topic)
        
        # Try different possible paths (Manim creates these directories)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Manim saves videos as: media/videos/<filename_without_ext>/<quality>/AutoTeach.mp4
        # The filename is the topic name with special chars replaced
        possible_paths = [
            # Standard Manim output locations
            os.path.join(base_dir, 'media', 'videos', safe_topic, '480p15', 'AutoTeach.mp4'),
            os.path.join(base_dir, 'media', 'videos', safe_topic, '720p30', 'AutoTeach.mp4'),
            os.path.join(base_dir, 'media', 'videos', safe_topic, '1080p60', 'AutoTeach.mp4'),
            # Alternative locations
            os.path.join(base_dir, 'temp_manim', 'media', 'videos', safe_topic, '480p15', 'AutoTeach.mp4'),
            # Direct temp_manim location
            os.path.join(base_dir, 'temp_manim', safe_topic + '.mp4'),
        ]
        
        print(f"🔍 Searching for video with topic: {topic} (safe: {safe_topic})")
        
        # Check all possible paths
        for path in possible_paths:
            if os.path.exists(path):
                file_size = os.path.getsize(path)
                print(f"✅ Found video at: {path} (size: {file_size} bytes)")
                response = send_file(path, mimetype='video/mp4')
                # Add CORS headers for web playback
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS, HEAD')
                response.headers.add('Access-Control-Allow-Headers', 'Range, Content-Type')
                response.headers.add('Accept-Ranges', 'bytes')
                response.headers.add('Content-Type', 'video/mp4')
                return response
        
        # If not found, list what directories exist
        media_dir = os.path.join(base_dir, 'media', 'videos')
        if os.path.exists(media_dir):
            print(f"📁 Media directory exists. Contents:")
            try:
                for item in os.listdir(media_dir):
                    item_path = os.path.join(media_dir, item)
                    if os.path.isdir(item_path):
                        print(f"  - {item}/")
                        # Check inside this directory
                        for quality in os.listdir(item_path):
                            quality_path = os.path.join(item_path, quality)
                            if os.path.isdir(quality_path):
                                print(f"    - {quality}/")
                                for file in os.listdir(quality_path):
                                    print(f"      - {file}")
            except Exception as e:
                print(f"Error listing directory: {e}")
        
        print(f"⚠️ Video not found. Searched paths:")
        for p in possible_paths:
            exists = "✅" if os.path.exists(p) else "❌"
            print(f"  {exists} {p}")
        
        return jsonify({'error': 'Video not found. Still rendering or rendering failed.'}), 404
    except Exception as e:
        print(f"❌ Error serving video: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/tta/process', methods=['POST'])
def tta_process():
    """Complete TTA workflow: summary, audio, manim code, questions"""
    if not TTA_AVAILABLE:
        return jsonify({'error': 'TTA module not available'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        subject = data.get('subject', 'general')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Step 1: Generate summary
        print(f"📝 Generating summary for topic: {topic}")
        summary = summarize_topic(topic)
        print(f"✅ Summary generated ({len(summary)} characters)")
        
        # Step 2: Generate audio (wait for it to complete)
        audio_filename = re.sub(r'[^A-Za-z0-9_]', '_', topic) + ".mp3"
        audio_filepath = os.path.join('temp_audio', audio_filename)
        os.makedirs('temp_audio', exist_ok=True)
        
        try:
            text_to_speech(summary, audio_filepath)
            print(f"✅ Audio generated: {audio_filepath}")
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            audio_filepath = None
        
        # Step 3: Generate Manim code (this can take time)
        print(f"🎬 Generating Manim code for topic: {topic}")
        manim_code = None
        try:
            manim_code = generate_manim_code(topic)
            if manim_code and len(manim_code) > 0:
                print(f"✅ Manim code generated successfully ({len(manim_code)} characters)")
                print(f"   First 100 chars: {manim_code[:100]}...")
            else:
                print(f"⚠️ Manim code generation returned empty result")
                manim_code = "# Error: Manim code generation returned empty result. Please try again."
        except Exception as e:
            print(f"❌ Error generating Manim code: {e}")
            import traceback
            traceback.print_exc()
            manim_code = f"# Error generating Manim code: {str(e)}\n# Please check the API connection and try again."
        
        # Step 3.5: START RENDERING VIDEO IMMEDIATELY (ONE GO - USING TTA.PY!)
        print(f"🔍 Checking if we should render video...")
        print(f"   manim_code exists: {manim_code is not None}")
        if manim_code:
            print(f"   manim_code length: {len(manim_code)}")
            print(f"   starts with '# Error': {manim_code.strip().startswith('# Error')}")
            print(f"   First 50 chars: {manim_code[:50]}")
        
        should_render = manim_code and len(manim_code) > 10 and not manim_code.strip().startswith('# Error')
        print(f"   Should render: {should_render}")
        
        if should_render:
            print(f"🎬🎬🎬 STARTING VIDEO RENDERING NOW - ONE GO!")
            safe_topic = re.sub(r'[^A-Za-z0-9_]', '_', topic)
            filename = safe_topic + ".py"
            filepath = os.path.join('temp_manim', filename)
            os.makedirs('temp_manim', exist_ok=True)
            
            # Save Manim code to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(manim_code)
            print(f"✅ Manim code saved to: {filepath}")
            
            # Start rendering in background thread IMMEDIATELY (using tta.py approach)
            def start_rendering():
                try:
                    import sys
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    abs_filepath = os.path.abspath(filepath)
                    python_cmd = sys.executable
                    filename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
                    cmd = f"{python_cmd} -m manim -pql {abs_filepath} AutoTeach"
                    
                    print(f"🎬🎬🎬 RENDERING VIDEO NOW!")
                    print(f"📁 Working directory: {base_dir}")
                    print(f"📄 File: {abs_filepath}")
                    print(f"📄 Output will be in: media/videos/{filename_without_ext}/480p15/AutoTeach.mp4")
                    print(f"🔧 Command: {cmd}")
                    
                    # Run Manim and wait for completion
                    result = subprocess.run(cmd, shell=True, cwd=base_dir, capture_output=True, text=True, timeout=600)
                    
                    if result.returncode == 0:
                        print(f"✅✅✅ VIDEO RENDERED SUCCESSFULLY!")
                        if result.stdout:
                            output = result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout
                            print("Manim output:", output)
                        
                        # Verify video file exists
                        expected_path = os.path.join(base_dir, 'media', 'videos', filename_without_ext, '480p15', 'AutoTeach.mp4')
                        if os.path.exists(expected_path):
                            file_size = os.path.getsize(expected_path)
                            print(f"✅✅✅ VIDEO FILE CONFIRMED: {expected_path} ({file_size} bytes)")
                        else:
                            print(f"⚠️ Video file not found at expected path: {expected_path}")
                    else:
                        print(f"❌ Video rendering failed (return code: {result.returncode})")
                        if result.stderr:
                            error = result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr
                            print("Error:", error)
                        if result.stdout:
                            output = result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout
                            print("Output:", output)
                except subprocess.TimeoutExpired:
                    print(f"❌ Video rendering timed out after 10 minutes")
                except Exception as e:
                    print(f"❌ Error in video rendering: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Start rendering thread IMMEDIATELY (non-daemon so it completes)
            render_thread = threading.Thread(target=start_rendering, daemon=False)
            render_thread.start()
            print(f"✅✅✅ VIDEO RENDERING THREAD STARTED - IT'S WORKING NOW!")
            print(f"   Thread ID: {render_thread.ident}")
            print(f"   Thread is alive: {render_thread.is_alive()}")
        
        # Step 4: Generate questions
        print(f"🧠 Generating questions for topic: {topic}")
        try:
            questions = generate_questions(topic)
            if questions and len(questions) > 0:
                print(f"✅ Questions generated successfully ({len(questions)} characters)")
            else:
                print(f"⚠️ Questions generation returned empty result")
                questions = "Error: Questions generation returned empty result."
        except Exception as e:
            print(f"❌ Error generating questions: {e}")
            import traceback
            traceback.print_exc()
            questions = f"Error generating questions: {str(e)}"
        
        # Read audio if it exists (wait a bit to ensure file is fully written)
        audio_data = None
        audio_base64 = None
        if audio_filepath:
            # Wait a moment for file to be fully written
            import time
            max_wait = 5  # 5 seconds max wait
            wait_count = 0
            while wait_count < max_wait and not os.path.exists(audio_filepath):
                time.sleep(0.5)
                wait_count += 0.5
                print(f"⏳ Waiting for audio file to be created... ({wait_count}s)")
            
            if os.path.exists(audio_filepath):
                try:
                    # Wait a bit more to ensure file is fully written
                    time.sleep(0.5)
                    
                    # Start playback of the most recent/generated audio (background thread)
                    try:
                        play_most_recent_audio(specific_path=audio_filepath)
                    except Exception as e:
                        print(f"⚠️ Auto-play failed to start: {e}")

                    with open(audio_filepath, 'rb') as f:
                        audio_data = f.read()
                        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    print(f"✅ Audio file read successfully ({len(audio_data)} bytes, base64: {len(audio_base64)} chars)")
                except Exception as e:
                    print(f"❌ Error reading audio file: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"⚠️ Audio file not found at: {audio_filepath} after waiting")
        
        # Video rendering will be triggered by frontend via /api/tta/render-video endpoint
        safe_topic = re.sub(r'[^A-Za-z0-9_]', '_', topic)
        video_path = f'/api/tta/video/{safe_topic}'
        
        # Prepare audio info for frontend
        audio_filename_out = None
        audio_url_out = None
        if audio_filepath and os.path.exists(audio_filepath):
            audio_filename_out = os.path.basename(audio_filepath)
            # Expose relative URL path for frontend to poll
            audio_url_out = f'/temp_audio/{audio_filename_out}'
            print(f"✅ Audio file info: filename={audio_filename_out}, url={audio_url_out}")
        
        response_data = {
            'summary': summary,
            'manim_code': manim_code,
            'questions': questions,
            'video_path': video_path,
            'topic': topic,
            'subject': subject,
            # Include audio info
            'audio_filename': audio_filename_out,
            'audio_url': audio_url_out,
            # Include base64 audio if available (for immediate use)
            'audio': f'data:audio/mpeg;base64,{audio_base64}' if audio_base64 else None
        }
        
        if audio_base64:
            print(f"✅ Audio added to response (base64 length: {len(audio_base64)})")
        else:
            print(f"⚠️ No audio in response")
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting EduVision Physics Backend Server...")
    print("API available at http://localhost:5000")

    # Use Waitress WSGI server on Windows to avoid werkzeug reloader/select issues.
    try:
        from waitress import serve
        # debug=False when running under waitress; threaded handling is internal to waitress
        serve(app, host='0.0.0.0', port=5000)
    except Exception as e:
        print("⚠️ Waitress not available or failed to start:", e)
        print("Falling back to Flask dev server (reloader disabled).")
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)

