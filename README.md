# AI Debater

An automated multi-agent debate framework that orchestrates multi-turn arguments, routes reasoning steps, and executes debate logic in an isolated sandbox environment.

---

## Features

- **Multi-Agent Debate Orchestration:** Manages back-and-forth arguments between opposing perspectives.
- **Dynamic Routing:** Directs model queries and decision paths based on conversation flow.
- **Isolated Execution:** Provides a sandbox environment to test and run model interactions safely.
- **Automated Pipelines:** Configured with GitHub Actions for automated testing and runs.

---

## Project Structure

```text
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
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Supaman1/Ai-debator.git](https://github.com/Supaman1/Ai-debator.git)
   cd Ai-debator
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the project root:

```env
API_KEY=your_api_key_here
```

---

## Usage

Run the main pipeline:

```bash
python main.py
```

---

## CI/CD Pipeline

Automated debate runs and environment checks are configured via GitHub Actions in `.github/workflows/run_pipeline.yml`.

---

## License

This project is licensed under the MIT License.
