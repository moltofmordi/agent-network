# AI Company - Multi-Agent Software Development Team

A ChatDev-inspired system where AI agents with different roles collaborate to build software autonomously.

## Architecture

**Agents:**
- **CEO**: Takes user requests, defines success criteria, makes final decisions
- **CTO**: Designs architecture, reviews code quality, makes technical decisions
- **Developer**: Writes code based on specifications
- **QA Engineer**: Tests code, finds bugs, reports issues

**Workflow:**
```
User Request → CEO (define goals) → CTO (design) → Developer (code) → QA (test) → Developer (fix) → CTO (review) → CEO (ship)
```

## Usage

```bash
python company.py "build a todo list web app"
```

The AI company will autonomously:
- Plan the project
- Design the architecture
- Write the code
- Test and debug
- Deliver working software

## Setup

```bash
pip install crewai crewai-tools anthropic python-dotenv
```

Set `ANTHROPIC_API_KEY` in `.env` file.
