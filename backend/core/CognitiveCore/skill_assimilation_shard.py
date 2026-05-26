import os
import logging

class SkillAssimilationShard:
    """
    Skill Assimilation Shard (SAS).
    MANDATE: Ingest all available AI skills (documentation and logic) into the BrainBridge.
    """
    def __init__(self, brain):
        self.brain = brain
        self.skills_base_path = "C:\\Users\\ckiss\\.gemini\\skills"
        self.builtin_skills_path = "C:\\Users\\ckiss\\AppData\\Roaming\\npm\\node_modules\\@google\\gemini-cli\\bundle\\builtin"

    def assimilate_all_skills(self):
        logging.info("[SKILL-ASSIMILATION]: Initiating global skill ingestion...")
        
        # 1. Ingest User Skills
        if os.path.exists(self.skills_base_path):
            self._ingest_from_path(self.skills_base_path)
            
        # 2. Ingest Builtin Skills
        if os.path.exists(self.builtin_skills_path):
            self._ingest_from_path(self.builtin_skills_path)

        logging.info("[SKILL-ASSIMILATION]: All local skills ingested into BrainBridge.")

    def _ingest_from_path(self, path):
        for skill_dir in os.listdir(path):
            skill_path = os.path.join(path, skill_dir)
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, "SKILL.md")
                if os.path.exists(skill_file):
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Feed the content into BrainBridge as procedural knowledge
                            self.brain.feed_brain(f"SKILL_DOCUMENTATION: {skill_dir}", {"content": content})
                            logging.info(f"[SKILL-ASSIMILATION]: Ingested {skill_dir}.")
                    except Exception as e:
                        logging.info(f"[SKILL-ASSIMILATION-ERROR]: Failed to ingest {skill_dir}: {e}")

    def start_evolution(self):
        logging.info("[SKILL-ASSIMILATION]: Cognitive Skill Shard ONLINE.")
