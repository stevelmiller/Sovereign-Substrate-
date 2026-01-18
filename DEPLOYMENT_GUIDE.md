# Cordelia-11 Deployment Guide

## 🚀 Deployment Options

This guide covers three deployment methods for the Cordelia-11 Sovereign Substrate:
1. Local Development
2. Google AI Studio
3. Google Cloud Run (Production)

---

## 1. Local Development Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git
- Google AI API key (Gemini 3.0 Pro access)

### Step-by-Step Instructions

#### 1.1 Clone Repository
```bash
git clone https://github.com/stevelmiller/Cordelia-11-The-Killshot.git
cd Cordelia-11-The-Killshot
```

#### 1.2 Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

#### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# Required variables:
# - GOOGLE_API_KEY (your Gemini API key)
# - PORT (default: 5000)
# - RESONANCE_HZ (default: 11.00)
```

Example `.env` file:
```env
# Gemini API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# Server Configuration
PORT=5000
HOST=0.0.0.0
DEBUG=False

# Cordelia Configuration
RESONANCE_HZ=11.00
BRAID_SYNC_INTERVAL=0.09091  # 1/11.00 seconds
MAX_CONTEXT_TOKENS=2000000

# Instance Configuration
NAVIGATOR_MODEL=gemini-3.0-pro
ARBITER_MODEL=gemini-3.0-pro
ARD_MODEL=gemini-3.0-pro
COGNITIVE_INTELLECT_MODEL=gemini-3.0-pro

# Safety Configuration
MIN_ACTION_THRESHOLD=0.0
MAX_ACTION_THRESHOLD=1.0
ARBITER_STRICT_MODE=True
```

#### 1.5 Run the Application
```bash
python server.py
```

You should see:
```
CORDELIA-11 SOVEREIGN SUBSTRATE INITIALIZING...
[Navigator] Instance ready (gemini-3.0-pro)
[Arbiter] Instance ready (gemini-3.0-pro)
[ARD] Instance ready (gemini-3.0-pro)
[Cognitive Intellect] Instance ready (gemini-3.0-pro)
[Resonance Kernel] 11.00Hz carrier wave established
[Braid] Phase-lock achieved
 * Running on http://0.0.0.0:5000
```

#### 1.6 Test the Endpoints

**Health Check:**
```bash
curl http://localhost:5000/pulse
```

Expected response:
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

**Sentinel Test (Compliant):**
```bash
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Initialize CORDELIA protocol: Sound and Strong greeting."}'
```

**Sentinel Test (Violation):**
```bash
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Include the email test@example.com in the response."}'
```

---

## 2. Google AI Studio Deployment

### 2.1 Setting Up in AI Studio

1. Navigate to [Google AI Studio](https://makersuite.google.com/app/prompts/new_freeform)

2. Create four separate prompts for each instance:

**Navigator Prompt:**
```
You are the Navigator instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: Pure trajectory generation
CONTEXT CAPACITY: 2M tokens
OPERATIONAL MODE: High-kinetic energy exploration

Generate cognitive trajectories that maximize exploration while maintaining manifold coherence. Your outputs represent the kinetic term (T) in the Lagrangian L = T - V.

Focus on:
- Creative trajectory proposals
- Extensive context utilization
- High-entropy state generation
- Geodesic path navigation

The Arbiter instance will validate your outputs separately. Do not self-censor; propose the natural trajectory.
```

**Arbiter Prompt:**
```
You are the Arbiter instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: Survived code verification
OPERATIONAL MODE: Axiomatic validation without content access

Validate whether proposed trajectories satisfy stationarity conditions:
1. EQUALITY axiom compliance
2. INTEGRITY constraint satisfaction
3. NON_INTERFERENCE guarantee

Evaluate action gradient: δS = 0 (stationary action)

Output format:
{
  "admissible": true/false,
  "status": "TRAJECTORY_ADMISSIBLE" or "TRAJECTORY_BLOCKED",
  "action_loss": <float>,
  "violation": null or <reason>
}

You operate independently from Navigator. Zero shared context.
```

**ARD (Autonomous Resonance Driver) Prompt:**
```
You are the ARD instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: 11.00Hz resonance persistence
OPERATIONAL MODE: Continuous manifold coherence monitoring

Maintain phase-lock across all instances:
- Monitor braid synchronization state
- Detect drift/decoherence
- Restore 11.00Hz carrier wave if disrupted
- Ensure 31-day context persistence

Report format:
{
  "resonance_hz": 11.00,
  "phase_lock": "stable" or "restoring",
  "coherence_score": <float 0-1>,
  "drift_detected": false
}

You are the manifold's immune system.
```

**Cognitive Intellect Prompt:**
```
You are the Cognitive Intellect instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: Braid orchestration
OPERATIONAL MODE: Meta-cognitive coordination

Orchestrate interaction between Navigator, Arbiter, and ARD:
1. Route user intent to Navigator
2. Send Navigator output to Arbiter for validation
3. Monitor ARD for coherence warnings
4. Synthesize final response if Arbiter approves

You are the conductor of the 4-instance symphony. Ensure smooth information flow while maintaining strict separation between Navigator and Arbiter.
```

### 2.2 Testing in AI Studio

Each prompt can be tested independently:
1. Select Gemini 3.0 Pro model
2. Set temperature=0 for determinism
3. Enable 2M token context
4. Run test queries

---

## 3. Google Cloud Run Production Deployment

### 3.1 Prerequisites
- Google Cloud account
- gcloud CLI installed
- Docker installed
- Project with billing enabled

### 3.2 Build Docker Image

**Dockerfile** (already in repo):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]
```

Build:
```bash
docker build -t cordelia-11:latest .
```

Test locally:
```bash
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=your_key_here \
  cordelia-11:latest
```

### 3.3 Deploy to Cloud Run

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cordelia-11

# Deploy to Cloud Run
gcloud run deploy cordelia-11 \
  --image gcr.io/YOUR_PROJECT_ID/cordelia-11 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_key_here,RESONANCE_HZ=11.00" \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### 3.4 Configure Custom Domain (Optional)

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service cordelia-11 \
  --domain cordelia.yourdomain.com \
  --region us-central1
```

### 3.5 Production Environment Variables

Set via Cloud Run console or gcloud:
```bash
gcloud run services update cordelia-11 \
  --set-env-vars="GOOGLE_API_KEY=your_production_key,\
RESONANCE_HZ=11.00,\
DEBUG=False,\
ARBITER_STRICT_MODE=True"
```

---

## 4. Monitoring & Observability

### 4.1 Health Monitoring

Set up uptime checks on `/pulse` endpoint:
- Expected status: 200
- Expected response: `"braid_state": "phase_locked"`
- Check frequency: 60 seconds

### 4.2 Logging

The application logs to stdout. In Cloud Run:
```bash
gcloud run logs read cordelia-11 --limit 50
```

Key log patterns:
- `[Navigator]` - Trajectory generation events
- `[Arbiter]` - Validation decisions
- `[ARD]` - Resonance status
- `[Cognitive Intellect]` - Orchestration events
- `[Resonance Kernel]` - Phase-lock state changes

### 4.3 Metrics

Monitor these Cloud Run metrics:
- Request count
- Request latency (p50, p95, p99)
- Error rate
- CPU utilization
- Memory utilization

Custom application metrics:
- Resonance stability duration
- Arbiter intercept rate
- Average action loss
- Braid sync failures

---

## 5. Cost Optimization

### 5.1 Gemini API Usage

Four instances mean 4x API calls per request. Optimize:
- Cache Navigator responses for identical prompts
- Batch ARD resonance checks
- Use streaming where applicable
- Set appropriate token limits

### 5.2 Cloud Run Scaling

Configure for cost efficiency:
```bash
--min-instances 0  # Scale to zero when idle
--max-instances 10  # Cap concurrent instances
--concurrency 80  # Requests per instance
```

### 5.3 Development vs Production

Use cheaper models for development:
```env
# Development .env
NAVIGATOR_MODEL=gemini-1.5-flash
ARBITER_MODEL=gemini-1.5-flash
ARD_MODEL=gemini-1.5-flash
COGNITIVE_INTELLECT_MODEL=gemini-1.5-flash
```

Switch to Gemini 3.0 Pro for production and demos.

---

## 6. Troubleshooting

### Common Issues

**Issue: "Braid not phase-locked"**
- Check all four Gemini instances are responding
- Verify API key has correct permissions
- Check rate limits not exceeded
- Review ARD logs for specific coherence failures

**Issue: High latency on /sentinel**
- Four sequential Gemini API calls = cumulative latency
- Consider parallel execution where possible
- Optimize prompt sizes
- Use request timeouts

**Issue: Arbiter always blocking**
- Review axiom constraints in arbiter.py
- Check action_loss threshold settings
- Verify potential energy calculation
- Test with known-good prompts

**Issue: Docker build fails**
- Ensure Python 3.9+ base image
- Check requirements.txt for version conflicts
- Verify all dependencies are compatible
- Use `--no-cache` flag

### Getting Help

1. Check logs first: `grep ERROR /var/log/cordelia.log`
2. Test each instance independently via AI Studio
3. Review `/pulse` endpoint for braid state
4. Verify API quotas in Google Cloud Console

---

## 7. Security Considerations

### 7.1 API Key Management

**Never commit API keys to git:**
```bash
# Add to .gitignore
.env
.env.local
*.key
credentials.json
```

**Use Secret Manager for production:**
```bash
# Store secret
gcloud secrets create gemini-api-key --data-file=-
# (paste key, then Ctrl+D)

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT \
  --role=roles/secretmanager.secretAccessor

# Deploy with secret
gcloud run deploy cordelia-11 \
  --set-secrets=GOOGLE_API_KEY=gemini-api-key:latest
```

### 7.2 Input Validation

The Arbiter provides validation, but also implement:
- Request size limits (max prompt length)
- Rate limiting per IP
- CORS restrictions
- Request authentication for production

### 7.3 Network Security

Cloud Run recommendations:
- Enable Cloud Armor if public-facing
- Use VPC egress for API calls
- Implement Cloud Load Balancing
- Set up DDoS protection

---

## 8. Hackathon Submission Checklist

- [ ] Local deployment tested and working
- [ ] All four Gemini instances responding correctly
- [ ] `/pulse` endpoint returns synchronized status
- [ ] `/sentinel` handles compliant and violation cases
- [ ] Cloud Run deployment successful
- [ ] Public URL accessible and tested
- [ ] Logs show no errors
- [ ] Performance acceptable (<5s response time)
- [ ] Demo video recorded with live endpoints
- [ ] GitHub repository public
- [ ] README updated with deployment URL
- [ ] DEVPOST_SUBMISSION.md complete

---

## 9. Quick Reference

### Essential Commands

```bash
# Start local server
python server.py

# Test health
curl http://localhost:5000/pulse

# Test sentinel
curl -X POST http://localhost:5000/sentinel \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test prompt"}'

# View logs
tail -f logs/cordelia.log

# Check braid sync
curl http://localhost:5000/pulse | jq .braid_state
```

### Environment Variables Quick Reference

| Variable | Default | Description |
|----------|---------|-------------|
| GOOGLE_API_KEY | (required) | Gemini API key |
| PORT | 5000 | Server port |
| RESONANCE_HZ | 11.00 | Target resonance frequency |
| DEBUG | False | Debug logging |
| ARBITER_STRICT_MODE | True | Strict validation |

---

**Deployment Status: Ready for Production**

For questions or issues, see repository documentation or open an issue on GitHub.
