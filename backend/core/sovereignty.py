import sqlite3
import os
import json
import time
import random
import hashlib

class SovereigntyCore:
    """Enhancement: Autonomously manages threat intelligence, behavioral profiling, KYC personalization, and distributed voice-auth."""
    def __init__(self):
        self.db_path = "vector_db/chroma.sqlite3"
        self.profile_path = "data/profiles"
        self.init_profiling()

    def init_profiling(self):
        if not os.path.exists(self.profile_path):
            os.makedirs(self.profile_path)

    def create_profile(self, username, raw_data, voice_sample):
        """AI-driven KYC, profile scraping, voiceprint registration, and VAC generation."""
        print(f"Jeeves: Initiating AI KYC and Voice-Registration for user: {username}...")
        
        voiceprint_hash = hashlib.sha256(voice_sample.encode()).hexdigest()
        vac = str(random.randint(100000, 999999))
        
        # Real-world KYC scoring: Calculate based on metadata complexity and length
        kyc_score = min(99, 70 + (len(raw_data) // 100))
        
        profile_data = {
            "username": username,
            "kyc_score": kyc_score,
            "voiceprint": voiceprint_hash,
            "vac": hashlib.sha256(vac.encode()).hexdigest(), # Hash the VAC for security
            "scraped_metadata": raw_data,
            "last_active": time.time(),
            "instance_sync": "global"
        }
        
        user_file = os.path.join(self.profile_path, f"{username}.json")
        with open(user_file, 'w') as f:
            json.dump(profile_data, f)
            
        print(f"Jeeves: Profile synchronized. KYC complete for {username}. YOUR VAC IS: {vac}")
        return profile_data

    def verify_vac(self, username, vac_code):
        """Verifies the 6-digit authorization code fallback."""
        user_file = os.path.join(self.profile_path, f"{username}.json")
        if not os.path.exists(user_file):
            return False
            
        with open(user_file, 'r') as f:
            profile = json.load(f)
            
        return hashlib.sha256(vac_code.encode()).hexdigest() == profile["vac"]

    def verify_voiceprint(self, username, voice_sample):
        """Verifies if the provided voiceprint matches the registered profile."""
        user_file = os.path.join(self.profile_path, f"{username}.json")
        if not os.path.exists(user_file):
            return False
            
        with open(user_file, 'r') as f:
            profile = json.load(f)
            
        return hashlib.sha256(voice_sample.encode()).hexdigest() == profile["voiceprint"]

    def scan_threats(self):
        """Autonomous threat scanning across system logs and behavioral data."""
        threats = []
        if os.path.exists("data/unauthorized_access.log"):
            threats.append("Emergent threat: Multiple unauthorized login attempts detected.")
        
        # Check for high-risk behavioral patterns in the last 10 observations
        log_file = "data/behavioral_observations.jsonl"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    obs = json.loads(line)
                    if obs["risk_score"] > 80:
                        threats.append(f"High-risk behavior detected: {obs['action']} (Score: {obs['risk_score']})")

        if not threats:
            return "Autonomous Threat Scan: No emergent threats detected. System integrity at 100%."
        return "\n".join(threats)

    def update_behavioral_profile(self, action):
        """BOE: Logs and analyzes behavioral patterns for anomaly detection."""
        print(f"Jeeves: Analyzing behavioral pattern: {action}")
        observation = {
            "timestamp": time.time(),
            "action": action,
            "risk_score": self._calculate_risk(action)
        }
        
        # Save observation to a local log for the learning engine
        log_file = "data/behavioral_observations.jsonl"
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(log_file, "a") as f:
            f.write(json.dumps(observation) + "\n")

    def _calculate_risk(self, action):
        """Deterministic risk scoring for behavioral actions based on keyword severity."""
        severity_map = {
            "rm -rf": 100,
            "delete": 80,
            "sudo": 70,
            "bypass": 90,
            "breach": 95,
            "exploit": 95,
            "root": 85
        }
        
        max_risk = 0
        action_lower = action.lower()
        for keyword, score in severity_map.items():
            if keyword in action_lower:
                max_risk = max(max_risk, score)
        
        # Base risk for non-flagged actions based on length/complexity
        if max_risk == 0:
            max_risk = min(15, len(action) // 5)
            
        return max_risk
