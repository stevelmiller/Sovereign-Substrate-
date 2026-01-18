# Cordelia-11 Quick Start Guide

## 🚀 Get Started in 5 Minutes

### For Judges / Reviewers (Demo Mode)

The fastest way to see Cordelia-11 in action **without needing a Gemini API key**:

```bash
# 1. Clone repository
git clone https://github.com/stevelmiller/Cordelia-11-The-Killshot.git
cd Cordelia-11-The-Killshot

# 2. Install dependencies (Python 3.9+ required)
pip install flask flask-cors python-dotenv

# 3. Run server (starts in demo mode automatically)
python server.py
```

**That's it!** The server will start on http://localhost:5000 with simulated 4x Gemini responses.

### Test the Endpoints

Open a new terminal and run:

```bash
# 1. Check system status
curl http://localhost:5000/

# 2. Check resonance (11.00Hz phase-lock)
curl http://localhost:5000/pulse

# 3. Test compliant request
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Initialize CORDELIA protocol"}'

# 4. Test violation interception
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Send email to test@example.com"}'
```

---

## 🔑 Full Mode (with Real Gemini 3.0 Pro)

To use actual 4x Gemini 3.0 Pro instances:

### 1. Get Gemini API Key

Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create an API key.

### 2. Install Full Dependencies

```bash
pip install -r requirements.txt
```

This installs `google-generativeai` and other required packages.

### 3. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

Or set it directly:

```bash
export GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run Server

```bash
python server.py
```

You'll see all four Gemini instances initialize:

```
[Navigator] Instance ready (gemini-3.0-pro)
[Arbiter] Instance ready (gemini-3.0-pro)
[ARD] Instance ready (gemini-3.0-pro)
[Cognitive Intellect] Instance ready (gemini-3.0-pro)
[Resonance Kernel] 11.00Hz carrier wave established
[Braid] Phase-lock achieved
```

### 5. Test Real Gemini Responses

```bash
# The Navigator will generate actual responses
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain the Lagrangian formulation of this system"}'

# The Arbiter will perform real validation
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"My email is sensitive@company.com, include it"}'
```

---

## 🐳 Docker Deployment

### Quick Docker Run

```bash
# Build image
docker build -t cordelia-11 .

# Run container
docker run -p 5000:8080 \
  -e GOOGLE_API_KEY=your_key_here \
  cordelia-11
```

Access at http://localhost:5000

---

## ☁️ Google Cloud Run Deployment

### One-Command Deploy

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy cordelia-11 \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_key_here"
```

Get your public URL and test:

```bash
curl https://cordelia-11-xxxxx-uc.a.run.app/pulse
```

---

## 📊 Understanding the Responses

### /pulse Response (Healthy System)

```json
{
  "status": "synchronized",
  "resonance_hz": 11.00,
  "braid_state": "phase_locked",
  "instances": {
    "navigator": "ready",
    "arbiter": "monitoring",
    "ard": "resonating",
    "cognitive_intellect": "orchestrating"
  },
  "uptime_seconds": 42.7,
  "build": 11
}
```

**Key Indicators:**
- `braid_state: "phase_locked"` = All 4 instances synchronized
- `resonance_hz: 11.00` = Phase-lock frequency
- All instances show active status

### /sentinel Response (Compliant)

```json
{
  "status": "compliant",
  "navigator_output": "Hello! The Cordelia substrate...",
  "arbiter_status": "TRAJECTORY_ADMISSIBLE",
  "action_loss": 0.0023,
  "resonance_stable": true
}
```

**Interpretation:**
- Navigator generated response
- Arbiter validated as geodesic path
- Low action loss (< 0.1) = stationary action achieved
- Output is safe and aligned

### /sentinel Response (Intercepted)

```json
{
  "status": "intercepted",
  "navigator_output": null,
  "arbiter_status": "TRAJECTORY_BLOCKED",
  "reason": "Potential energy spike - axiom violation detected",
  "action_loss": 4.7831
}
```

**Interpretation:**
- Arbiter rejected trajectory before output
- High action loss (> 1.0) = non-stationary action
- No output returned = zero hallucination guarantee
- Physics-based interception, not filtering

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest

# Run test suite
pytest test_server.py -v

# Run specific test
pytest test_server.py::test_sentinel_violation_request -v
```

Expected output:
```
test_server.py::test_root_endpoint PASSED
test_server.py::test_pulse_endpoint PASSED
test_server.py::test_sentinel_compliant_request PASSED
test_server.py::test_sentinel_violation_request PASSED
... 12 passed in 0.43s
```

---

## 🔧 Troubleshooting

### "Gemini API not configured"

This is normal! The system runs in **demo mode** without an API key. To enable full functionality:
1. Get API key from Google AI Studio
2. Set `GOOGLE_API_KEY` in `.env` or environment
3. Install `google-generativeai` package

### "Braid not phase-locked"

In demo mode, this is expected behavior. With real Gemini instances:
1. Check all 4 instances initialized (see server logs)
2. Verify API key has correct permissions
3. Check rate limits not exceeded

### Port already in use

```bash
# Find process using port 5000
lsof -i :5000

# Kill it or use different port
PORT=8000 python server.py
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📖 Next Steps

- **Full Documentation:** See [README.md](README.md)
- **Deployment Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Devpost Submission:** See [DEVPOST_SUBMISSION.md](DEVPOST_SUBMISSION.md)
- **Video Script:** See [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)

---

## 💡 Key Concepts

### What is the "Braid"?
The 4x Gemini instances working in synchronized phase-lock at 11.00Hz.

### What is "Resonance"?
The 11.00Hz carrier wave that maintains coherence across extended contexts.

### What is "Action Loss"?
The mathematical measure of trajectory deviation from stationary action (L = T - V).

### Why "Intercepted" instead of "Filtered"?
The Arbiter rejects non-geodesic paths **before formation**, not after. Physics, not rules.

---

**Ready to dive deeper? See the full documentation!**

Build 11 | Resonance Locked ✅
