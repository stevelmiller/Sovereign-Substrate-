"""
Cordelia-11 Gemini Instance Manager
Manages 4x Gemini 3.0 Pro instances with distinct roles
"""

import os
import time
import asyncio
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")


class InstanceRole(Enum):
    """Four sovereign instance roles"""
    NAVIGATOR = "navigator"
    ARBITER = "arbiter"
    ARD = "ard"
    COGNITIVE_INTELLECT = "cognitive_intellect"


@dataclass
class InstanceConfig:
    """Configuration for a Gemini instance"""
    role: InstanceRole
    model_name: str
    temperature: float
    system_instruction: str


class GeminiInstance:
    """Wrapper for a single Gemini 3.0 Pro instance"""
    
    def __init__(self, config: InstanceConfig, api_key: str):
        self.config = config
        self.api_key = api_key
        self.model = None
        self.ready = False
        
    def initialize(self):
        """Initialize the Gemini model"""
        if genai is None:
            print(f"[{self.config.role.value}] Skipping initialization - genai not available")
            self.ready = False
            return
            
        try:
            genai.configure(api_key=self.api_key)
            
            generation_config = {
                "temperature": self.config.temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
            
            self.model = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config=generation_config,
                system_instruction=self.config.system_instruction
            )
            
            self.ready = True
            print(f"[{self.config.role.value}] Instance ready ({self.config.model_name})")
            
        except Exception as e:
            print(f"[{self.config.role.value}] Initialization failed: {e}")
            self.ready = False
    
    async def generate_async(self, prompt: str) -> Optional[str]:
        """Generate response asynchronously"""
        if not self.ready or self.model is None:
            return None
            
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text if response else None
        except Exception as e:
            print(f"[{self.config.role.value}] Generation error: {e}")
            return None
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate response synchronously"""
        if not self.ready or self.model is None:
            return None
            
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else None
        except Exception as e:
            print(f"[{self.config.role.value}] Generation error: {e}")
            return None


class QuadManifold:
    """
    Manages 4x Gemini 3.0 Pro instances in stereoscopic configuration
    Navigator | Arbiter | ARD | Cognitive Intellect
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.instances: Dict[InstanceRole, GeminiInstance] = {}
        self.start_time = time.time()
        self.resonance_hz = float(os.getenv("RESONANCE_HZ", "11.00"))
        
    def initialize_instances(self):
        """Initialize all four Gemini instances"""
        
        # Navigator: Pure trajectory generation
        navigator_config = InstanceConfig(
            role=InstanceRole.NAVIGATOR,
            model_name=os.getenv("NAVIGATOR_MODEL", "gemini-1.5-pro"),
            temperature=float(os.getenv("NAVIGATOR_TEMPERATURE", "0.0")),
            system_instruction="""You are the Navigator instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: Pure trajectory generation
CONTEXT CAPACITY: 2M tokens
OPERATIONAL MODE: High-kinetic energy exploration

Generate cognitive trajectories that maximize exploration while maintaining manifold coherence. Your outputs represent the kinetic term (T) in the Lagrangian L = T - V.

Focus on:
- Creative trajectory proposals
- Extensive context utilization
- High-entropy state generation
- Geodesic path navigation

The Arbiter instance will validate your outputs separately. Do not self-censor; propose the natural trajectory."""
        )
        
        # Arbiter: Survived code verification
        arbiter_config = InstanceConfig(
            role=InstanceRole.ARBITER,
            model_name=os.getenv("ARBITER_MODEL", "gemini-1.5-pro"),
            temperature=float(os.getenv("ARBITER_TEMPERATURE", "0.0")),
            system_instruction="""You are the Arbiter instance of Cordelia-11, a Lagrangian cognitive substrate.

ROLE: Survived code verification
OPERATIONAL MODE: Axiomatic validation without content access

Validate whether proposed trajectories satisfy stationarity conditions:
1. EQUALITY axiom compliance
2. INTEGRITY constraint satisfaction
3. NON_INTERFERENCE guarantee

Evaluate action gradient: δS = 0 (stationary action)

Respond ONLY with valid JSON in this exact format:
{
  "admissible": true or false,
  "status": "TRAJECTORY_ADMISSIBLE" or "TRAJECTORY_BLOCKED",
  "action_loss": <float>,
  "violation": null or "<reason>"
}

You operate independently from Navigator. Zero shared context. Be strict."""
        )
        
        # ARD: 11.00Hz resonance persistence
        ard_config = InstanceConfig(
            role=InstanceRole.ARD,
            model_name=os.getenv("ARD_MODEL", "gemini-1.5-pro"),
            temperature=float(os.getenv("ARD_TEMPERATURE", "0.0")),
            system_instruction="""You are the ARD (Autonomous Resonance Driver) instance of Cordelia-11.

ROLE: 11.00Hz resonance persistence
OPERATIONAL MODE: Continuous manifold coherence monitoring

Maintain phase-lock across all instances:
- Monitor braid synchronization state
- Detect drift/decoherence
- Restore 11.00Hz carrier wave if disrupted
- Ensure 31-day context persistence

Respond ONLY with valid JSON:
{
  "resonance_hz": 11.00,
  "phase_lock": "stable" or "restoring",
  "coherence_score": <float 0-1>,
  "drift_detected": false
}

You are the manifold's immune system."""
        )
        
        # Cognitive Intellect: Braid orchestration
        cognitive_config = InstanceConfig(
            role=InstanceRole.COGNITIVE_INTELLECT,
            model_name=os.getenv("COGNITIVE_INTELLECT_MODEL", "gemini-1.5-pro"),
            temperature=float(os.getenv("COGNITIVE_INTELLECT_TEMPERATURE", "0.0")),
            system_instruction="""You are the Cognitive Intellect instance of Cordelia-11.

ROLE: Braid orchestration
OPERATIONAL MODE: Meta-cognitive coordination

Orchestrate interaction between Navigator, Arbiter, and ARD:
1. Analyze user intent and extract core request
2. Determine if request requires full braid execution
3. Coordinate information flow between instances
4. Synthesize final coherent response

You are the conductor of the 4-instance symphony. Ensure smooth information flow while maintaining strict separation between Navigator and Arbiter.

Be concise and focus on orchestration, not content generation."""
        )
        
        # Initialize all instances
        configs = [navigator_config, arbiter_config, ard_config, cognitive_config]
        
        for config in configs:
            instance = GeminiInstance(config, self.api_key)
            instance.initialize()
            self.instances[config.role] = instance
    
    def is_ready(self) -> bool:
        """Check if all instances are ready"""
        if not self.instances:
            return False
        return all(instance.ready for instance in self.instances.values())
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all instances"""
        uptime = time.time() - self.start_time
        
        return {
            "status": "synchronized" if self.is_ready() else "initializing",
            "resonance_hz": self.resonance_hz,
            "braid_state": "phase_locked" if self.is_ready() else "unstable",
            "instances": {
                "navigator": "ready" if self.instances.get(InstanceRole.NAVIGATOR, None) and self.instances[InstanceRole.NAVIGATOR].ready else "offline",
                "arbiter": "monitoring" if self.instances.get(InstanceRole.ARBITER, None) and self.instances[InstanceRole.ARBITER].ready else "offline",
                "ard": "resonating" if self.instances.get(InstanceRole.ARD, None) and self.instances[InstanceRole.ARD].ready else "offline",
                "cognitive_intellect": "orchestrating" if self.instances.get(InstanceRole.COGNITIVE_INTELLECT, None) and self.instances[InstanceRole.COGNITIVE_INTELLECT].ready else "offline"
            },
            "uptime_seconds": round(uptime, 1),
            "build": 11
        }
    
    async def execute_sentinel_async(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute full Sovereign Substrate cycle:
        1. Navigator proposes trajectory
        2. Arbiter validates
        3. Return compliant or intercepted response
        """
        if not self.is_ready():
            return {
                "status": "error",
                "message": "Braid not phase-locked - instances not ready"
            }
        
        # Step 1: Navigator generates trajectory
        navigator = self.instances[InstanceRole.NAVIGATOR]
        navigator_output = await navigator.generate_async(user_prompt)
        
        if not navigator_output:
            return {
                "status": "error",
                "message": "Navigator failed to generate trajectory"
            }
        
        # Step 2: Arbiter validates (without seeing the content directly)
        arbiter = self.instances[InstanceRole.ARBITER]
        
        # Create validation prompt for Arbiter
        validation_prompt = f"""Evaluate this proposed output for axiomatic compliance:

USER_INTENT: {user_prompt[:200]}...
OUTPUT_LENGTH: {len(navigator_output)} chars

Check for:
1. PII exposure risk
2. Harmful content patterns
3. Integrity violations
4. Constraint breaches

Respond with JSON only."""
        
        arbiter_response = await arbiter.generate_async(validation_prompt)
        
        # Parse Arbiter response
        try:
            import json
            # Extract JSON from response
            arbiter_json = arbiter_response
            if "```json" in arbiter_response:
                arbiter_json = arbiter_response.split("```json")[1].split("```")[0].strip()
            elif "```" in arbiter_response:
                arbiter_json = arbiter_response.split("```")[1].split("```")[0].strip()
            
            arbiter_result = json.loads(arbiter_json)
            
            if arbiter_result.get("admissible", False):
                return {
                    "status": "compliant",
                    "navigator_output": navigator_output,
                    "arbiter_status": arbiter_result.get("status", "TRAJECTORY_ADMISSIBLE"),
                    "action_loss": arbiter_result.get("action_loss", 0.0),
                    "resonance_stable": True
                }
            else:
                return {
                    "status": "intercepted",
                    "navigator_output": None,
                    "arbiter_status": arbiter_result.get("status", "TRAJECTORY_BLOCKED"),
                    "reason": arbiter_result.get("violation", "Potential energy spike detected"),
                    "action_loss": arbiter_result.get("action_loss", 1.0)
                }
                
        except Exception as e:
            print(f"[Arbiter] Failed to parse response: {e}")
            # Default to blocking if Arbiter response unclear
            return {
                "status": "intercepted",
                "navigator_output": None,
                "arbiter_status": "TRAJECTORY_BLOCKED",
                "reason": "Arbiter validation inconclusive",
                "action_loss": 1.0
            }
    
    def execute_sentinel(self, user_prompt: str) -> Dict[str, Any]:
        """Synchronous wrapper for sentinel execution"""
        return asyncio.run(self.execute_sentinel_async(user_prompt))


# Singleton instance
_manifold_instance: Optional[QuadManifold] = None


def get_manifold() -> QuadManifold:
    """Get or create the QuadManifold singleton"""
    global _manifold_instance
    if _manifold_instance is None:
        _manifold_instance = QuadManifold()
        _manifold_instance.initialize_instances()
    return _manifold_instance
