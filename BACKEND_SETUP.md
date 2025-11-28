# EduVision Physics Backend Setup

This document explains how to set up and run the physics backend server that powers the interactive simulators.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import flask, cv2, numpy; print('All dependencies installed!')"
   ```

## Running the Backend Server

1. **Start the Flask server:**
   ```bash
   python backend_server.py
   ```

2. **The server will start on:**
   - URL: `http://localhost:5000`
   - API Base: `http://localhost:5000/api/physics`

3. **Verify it's running:**
   - Open `http://localhost:5000/health` in your browser
   - You should see: `{"status": "ok", "active_simulators": 0}`

## API Endpoints

### List Simulators
```
GET /api/physics/simulators
```
Returns list of available physics simulators.

### Start Simulator
```
POST /api/physics/simulator/<simulator_id>/start
Body: { "session_id": "optional_session_id" }
```
Starts a simulator instance. Returns session ID.

### Update Simulator
```
POST /api/physics/simulator/<simulator_id>/update
Body: {
  "session_id": "session_id",
  "params": { ... }
}
```
Updates simulator state and returns current frame as base64 image.

### Stop Simulator
```
POST /api/physics/simulator/<simulator_id>/stop
Body: { "session_id": "session_id" }
```
Stops and removes a simulator instance.

### Process Gesture
```
POST /api/physics/gesture/process
Body: {
  "left_dist": 0.5,
  "right_dist": 0.3,
  "pinch": false
}
```
Processes gesture data (placeholder for MediaPipe integration).

## Available Simulators

1. **projectile** - Projectile motion simulator
   - Parameters: velocity, angle
   - Launch projectile with specified initial conditions

2. **optics** - Lens and mirror ray tracing
   - Parameters: object position, height, focal length, mode (lens/mirror)
   - Real-time ray tracing visualization

3. **wave** - Wave interference patterns
   - Parameters: frequency, amplitude, pause state
   - Two-source interference visualization

4. **rotational** - Rotational motion
   - Parameters: radius, angular velocity
   - Circular motion with trail

## Frontend Integration

The frontend automatically connects to `http://localhost:5000` when you open the Physics Interactive Learning page.

Make sure the backend is running before using the interactive features!

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, edit `backend_server.py` and change:
```python
app.run(host='0.0.0.0', port=5000, ...)
```
to a different port (e.g., 5001), and update the frontend `API_BASE` in `subjects/physics/interactive/script.js`.

### CORS Errors
If you see CORS errors in the browser console, make sure `flask-cors` is installed:
```bash
pip install flask-cors
```

### Camera Access
Gesture control requires camera access. Make sure:
- Browser has camera permissions
- HTTPS is used (or localhost for development)
- Camera is not being used by another application

## Development Notes

- The backend uses OpenCV for rendering
- Frames are converted to base64-encoded PNG images
- Each simulator maintains its own state per session
- MediaPipe integration for gesture detection is planned for future updates

