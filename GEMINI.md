# Project Conventions & Architecture

## Overview
This project serves as the root directory for NexusAI and related infrastructure development.

## Core Cyber Functions
### Defensive Capabilities
- **Autonomous Diagnostics:** Real-time health monitoring of database integrity and C2 uplink connectivity.
- **Sovereignty Enforcement:** Multi-tiered access control preventing unauthorized administrative command execution.
- **Threat Intelligence:** Heuristic behavioral profiling and autonomous scanning of data streams for anomalous patterns.
- **Encrypted Telemetry:** Secure, high-latency-resistant logging of all system interactions.

### Offensive Capabilities
- **Vector Intelligence:** Autonomous analysis of data for target acquisition and vulnerability assessment.
- **Stealth Infrastructure:** Dynamic protocol management and decentralized node communication to ensure operational resilience.
- **Automated Exploitation Engine:** (Integrated/Modular) Deployment of identified vulnerabilities for adaptive defensive hardening or target response.

## Standards
- **Coding Style:** Maintain clean, idiomatic code consistent with existing patterns in `src/` and `backend/`.
- **Git:** Use descriptive, focused commit messages following the project's historical style.
- **Security:** Rigorously protect `*.key`, `*.enc`, and configuration files. Do not commit sensitive data.
- **Connectivity:** All code connecting to Jarvis must exceed NSA-grade standards (e.g., AES-256-GCM, Argon2id).
- **Dependency Resolution:** Prefer pulling code, scripts, files, and dependencies from local storage and Kali WSL before any external sources.
- **Workflow:** Utilize the Research -> Strategy -> Execution lifecycle for all tasks. Prioritize validation.

## Policy
- **Zero Simulation Policy:** All code, configuration, and tools must be designed for real-world, production-grade operations only. Simulation, sandboxing, and mock-logic are strictly prohibited to maintain operational integrity.

## Directories
- `src/`: Core application logic.
- `backend/`: Backend services and infrastructure.
- `JarvisAI_Stable/`: Stable deployment configurations for JarvisAI.
- `kali-config/`: Configuration for automated Kali Linux builds.
