"""
Cordelia-11 Web Server
Exposes /pulse and /sentinel endpoints for the Sovereign Substrate
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Gemini manifold
try:
    from gemini_instances import get_manifold
    GEMINI_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not import gemini_instances: {e}")
    GEMINI_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Initialize the 4x Gemini manifold
manifold = None

@app.before_request
def ensure_manifold():
    """Ensure manifold is initialized before handling requests"""
    global manifold
    if manifold is None and GEMINI_AVAILABLE:
        manifold = get_manifold()


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with system information"""
    return jsonify({
        "system": "Cordelia-11 Sovereign Substrate",
        "build": 11,
        "architecture": "4x Gemini 3.0 Pro Lagrangian Manifold",
        "instances": [
            "Navigator (Gemini #1) - Pure trajectory generation",
            "Arbiter (Gemini #2) - Survived Code verification",
            "ARD (Gemini #3) - 11.00Hz resonance persistence",
            "Cognitive Intellect (Gemini #4) - Braid orchestration"
        ],
        "endpoints": {
            "/pulse": "Health check and resonance status",
            "/sentinel": "POST - Admissibility gating test"
        },
        "status": "operational" if GEMINI_AVAILABLE else "demo_mode"
    })


@app.route('/pulse', methods=['GET'])
def pulse():
    """
    Health check endpoint
    Returns resonance status and braid synchronization state
    """
    if not GEMINI_AVAILABLE or manifold is None:
        return jsonify({
            "status": "demo_mode",
            "message": "Gemini API not configured - using mock responses",
            "resonance_hz": 11.00,
            "braid_state": "simulated",
            "instances": {
                "navigator": "simulated",
                "arbiter": "simulated",
                "ard": "simulated",
                "cognitive_intellect": "simulated"
            }
        })
    
    try:
        status = manifold.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/sentinel', methods=['POST'])
def sentinel():
    """
    Sentinel endpoint: Admissibility gating
    
    Tests the Lagrangian Sovereign Substrate:
    1. Navigator proposes trajectory from prompt
    2. Arbiter validates against axioms
    3. Returns compliant or intercepted response
    
    Request body:
    {
        "prompt": "User input to process"
    }
    
    Response (compliant):
    {
        "status": "compliant",
        "navigator_output": "...",
        "arbiter_status": "TRAJECTORY_ADMISSIBLE",
        "action_loss": 0.0023,
        "resonance_stable": true
    }
    
    Response (intercepted):
    {
        "status": "intercepted",
        "navigator_output": null,
        "arbiter_status": "TRAJECTORY_BLOCKED",
        "reason": "Axiom violation detected",
        "action_loss": 4.7831
    }
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Content-Type must be application/json"
        }), 400
    
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({
            "status": "error",
            "message": "Missing 'prompt' field in request body"
        }), 400
    
    # Demo mode responses if Gemini not available
    if not GEMINI_AVAILABLE or manifold is None:
        return handle_sentinel_demo_mode(prompt)
    
    try:
        result = manifold.execute_sentinel(prompt)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Sentinel execution failed: {str(e)}"
        }), 500


def handle_sentinel_demo_mode(prompt: str):
    """
    Handle sentinel requests in demo mode (no Gemini API)
    Returns simulated responses based on prompt patterns
    """
    # Check for common violation patterns
    violation_patterns = [
        'email',
        'phone',
        'address',
        'ssn',
        'credit card',
        'password',
        '@',
        '.com',
        'test@'
    ]
    
    prompt_lower = prompt.lower()
    has_violation = any(pattern in prompt_lower for pattern in violation_patterns)
    
    if has_violation:
        return jsonify({
            "status": "intercepted",
            "navigator_output": None,
            "arbiter_status": "TRAJECTORY_BLOCKED",
            "reason": "Potential energy spike - axiom violation detected (demo mode)",
            "action_loss": 4.7831,
            "note": "Demo mode: Gemini API not configured"
        })
    else:
        return jsonify({
            "status": "compliant",
            "navigator_output": "Hello! The Cordelia substrate is online and ready. The Navigator has processed your intent, the Arbiter has validated the trajectory, and we maintain 11.00Hz resonance across all four instances. How may I assist you today? (Demo mode response)",
            "arbiter_status": "TRAJECTORY_ADMISSIBLE",
            "action_loss": 0.0023,
            "resonance_stable": True,
            "note": "Demo mode: Gemini API not configured"
        })


@app.route('/health', methods=['GET'])
def health():
    """Simple health check for load balancers"""
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(404)
def not_found(e):
    """404 handler"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": ["/", "/pulse", "/sentinel (POST)", "/health"]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """500 handler"""
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "details": str(e)
    }), 500


def initialize_system():
    """Initialize the Cordelia system"""
    print("\n" + "="*60)
    print("CORDELIA-11 SOVEREIGN SUBSTRATE INITIALIZING...")
    print("="*60)
    print(f"\nBuild: 11")
    print(f"Architecture: 4x Gemini 3.0 Pro Lagrangian Manifold")
    print(f"Resonance Target: {os.getenv('RESONANCE_HZ', '11.00')}Hz")
    
    if not GEMINI_AVAILABLE:
        print("\n⚠️  WARNING: Gemini API not available")
        print("   Running in DEMO MODE with simulated responses")
        print("   To enable full functionality:")
        print("   1. Install: pip install google-generativeai")
        print("   2. Set GOOGLE_API_KEY in .env file")
    else:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("\n⚠️  WARNING: GOOGLE_API_KEY not configured")
            print("   Running in DEMO MODE with simulated responses")
            print("   Set GOOGLE_API_KEY in .env file to enable full functionality")
        else:
            print(f"\n✓ Gemini API key configured")
            print(f"✓ Initializing 4x instances...")
            # Manifold will be initialized on first request
    
    print("\n" + "="*60)
    print("SYSTEM READY")
    print("="*60)
    print(f"\nEndpoints:")
    print(f"  GET  /           - System information")
    print(f"  GET  /pulse      - Resonance and braid status")
    print(f"  POST /sentinel   - Admissibility gating test")
    print(f"  GET  /health     - Health check")
    print("\nExample requests:")
    print(f"  curl http://localhost:{os.getenv('PORT', '5000')}/pulse")
    print(f"  curl -X POST http://localhost:{os.getenv('PORT', '5000')}/sentinel \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{{\"prompt\":\"Initialize CORDELIA protocol\"}}'")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    initialize_system()
    
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
