# AI Debater
An automated multi-agent debate framework that orchestrates multi-turn arguments, routes reasoning steps, and executes debate logic in an isolated sandbox environment.
Features
 * Multi-Agent Debate Orchestration: Manages back-and-forth arguments between opposing perspectives.
 * Dynamic Routing: Directs model queries and decision paths based on conversation flow.
 * Isolated Execution: Provides a sandbox environment to test and run model interactions safely.
 * Automated Pipelines: Configured with GitHub Actions for automated testing and runs.
Project Structure
Ai-debator/
├── .github/
│   └── workflows/
│       └── run_pipeline.yml  # CI/CD automated workflow
├── config.py                 # Configuration and environment setup
├── debate.py                 # Core debate logic and turn management
├── main.py                   # Main entry point to initiate debates
├── router.py                 # Request routing and agent coordination
├── sandbox.py                # Safe execution sandbox for debate evaluation
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

(File structure verified against repository tree)
Installation
 * Clone the repository:
   git clone https://github.com/Supaman1/Ai-debator.git
cd Ai-debator

 * Set up a virtual environment (optional but recommended):
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

 * Install dependencies:
   pip install -r requirements.txt

   (Installs dependencies including requests and python-dotenv)
Configuration
Create a .env file in the project root to store your API credentials and environment settings:
# Add your environment variables or model API keys
API_KEY=your_api_key_here

Usage
Run the main entry script to initiate the debate flow:
python main.py

CI/CD Automation
This repository includes a predefined GitHub Actions workflow located at .github/workflows/run_pipeline.yml to automate pipeline runs and validation checks directly on GitHub.
License
This project is licensed under the MIT License.

