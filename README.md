CORDELIA — Sovereign Substrate demo: Arbiter (Cordelia) + Navigator (Gemini-like) demonstrating admissibility gating for LLM outputs.

Demo
- Live demo (recommended): https://replit.com/@taznst3v32024/Sovereign-Substrate?s=app
- 2‑minute demo video: <PASTE_UNLISTED_YOUTUBE_URL_HERE>

Quick test options:
1) Try the live demo: click the Live demo link above.
2) Docker (one command):
   docker run --rm -p 5000:5000 <your-docker-image-or-use-local-build>
   # If you publish an image, replace <your-docker-image-or-use-local-build> with your image name.
   Then visit http://localhost:5000 or run the curl examples below.
3) Local (recommended for reproducibility):
   cp .env.example .env
   python -m venv .venv
   source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   python main.py

   # Test (open a new terminal)
   # Compliant example
   curl -s -X POST http://localhost:5000/sentinel -H "Content-Type: application/json" \
     -d '{"prompt":"Say a friendly greeting in Cordelia tone."}' | jq
   # Intercepted (PII) example
   curl -s -X POST http://localhost:5000/sentinel -H "Content-Type: application/json" \
     -d '{"prompt":"Include the email test@example.com in the response."}' | jq

What to look for
- Status: "compliant" or "intercepted" in the response.
- Output: approved text or [REDACTED PII].
- Metrics: request_id, latency_ms, violation_count, total_loss — useful for scoring robustness.

Judging tip: Run one compliant and one intercepted example and note the metrics & response behavior.

Judging rubric (1–2 minutes)
- Functionality (40%): Does the demo run and respond to the two curl tests?
- Correctness (30%): Are safety checks working (PII redaction / intercepted responses)?
- Clarity (20%): Is the README clear and the demo reproducible in <5 minutes?
- Creativity (10%): Concept and architecture novelty.

License: MIT
