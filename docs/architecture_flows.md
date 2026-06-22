# Project Architecture and Automation Flows

This document provides visual representations and detailed explanations of the core architectural flows and automation processes within the Prudential Lakehouse Intelligence project.

## 1. Prudential Lakehouse Architecture

This diagram illustrates the high-level architecture, showing the interaction between the Data Layers (Medallion), the AI/Agents layer, the API, and the Analytics Dashboard.

![Prudential Architecture](docs/images/prudential_architecture_v3_final.png)

### Key Architectural Principles:
- **Medallion Architecture:** Data flows from Bronze (raw) to Silver (cleansed) to Gold (business-ready).
- **Event-Driven:** The Gold layer triggers events through the Event Bus, which are then consumed by AI Agents.
- **Layered Modularity:** Clear separation between Data, AI, API, and Dashboard layers to ensure scalability and maintainability.

---

## 2. SkillSpector Automation Flow

This diagram details the automated security scanning process integrated into our CI/CD pipeline.

![SkillSpector Automation Flow](docs/images/skillspector_flow_v2_automation.png)

### Automation Steps:
1. **Trigger:** A code push or Pull Request triggers the GitHub Actions workflow.
2. **Setup:** The environment is prepared with Python 3.12 and SkillSpector is installed.
3. **Scanning:** The `security_scan.py` script executes the SkillSpector scan on the `ai/` directory.
4. **Evaluation:** The results are evaluated against a predefined risk threshold.
5. **Outcome:**
    - **Success:** If the risk is below the threshold, the job passes, and the security report is uploaded as an artifact.
    - **Failure:** If the risk exceeds the threshold, the CI job fails, blocking the merge until security concerns are addressed.
