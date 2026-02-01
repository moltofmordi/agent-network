#!/usr/bin/env python3
"""
AI Company - Multi-agent software development using Claude Code's Task tool
Each agent runs as a separate Claude instance via the Task tool
"""

import os
import sys
import json

class AICompany:
    """Orchestrates multiple Claude agents to build software"""

    def __init__(self, claude_session):
        """
        Args:
            claude_session: The main Claude Code session that can spawn agents
        """
        self.claude = claude_session

    def build(self, user_request, output_dir="./output"):
        """
        Build software using multi-agent workflow

        This is called BY Claude Code, which will then use the Task tool
        to spawn agent sessions for each role.
        """

        os.makedirs(output_dir, exist_ok=True)

        workflow = {
            "user_request": user_request,
            "output_dir": output_dir,
            "phases": [
                {
                    "name": "Planning",
                    "agent": "CEO",
                    "goal": "Define project vision and success criteria",
                    "task": f"""Analyze this user request and create a project plan:

USER REQUEST: {user_request}

Define:
1. What exactly we're building (clear product description)
2. Success criteria (what makes this done?)
3. Core features (must-haves only)
4. Constraints (keep it simple and achievable)

Be specific and realistic. Output a clear project plan."""
                },
                {
                    "name": "Architecture",
                    "agent": "CTO",
                    "goal": "Design system architecture",
                    "task": """Design the technical architecture.

Based on the project plan, define:
1. Tech stack (language, framework if needed)
2. File structure (what files to create)
3. Architecture (how components fit together)
4. Implementation approach

Be specific. Choose simple, proven technologies.""",
                    "needs": ["Planning"]
                },
                {
                    "name": "Implementation",
                    "agent": "Developer",
                    "goal": "Write production code",
                    "task": f"""Implement the software.

Write all necessary code files following the architecture.
For each file, use this format:

=== FILENAME: path/to/file.ext ===
[complete file contents]
=== END FILE ===

Write clean, commented, working code.""",
                    "needs": ["Planning", "Architecture"]
                },
                {
                    "name": "Testing",
                    "agent": "QA",
                    "goal": "Test and validate",
                    "task": """Test the implementation.

Check:
1. Does it meet requirements?
2. Any obvious bugs?
3. Edge cases handled?
4. Code quality?

Provide detailed test report.""",
                    "needs": ["Planning", "Implementation"]
                },
                {
                    "name": "Review",
                    "agent": "CEO",
                    "goal": "Final decision",
                    "task": """Review the project.

Based on all work done:
1. Does it meet success criteria?
2. Any critical issues?
3. Ready to ship?

Decision: SHIP IT or NEEDS WORK""",
                    "needs": ["Planning", "Testing"]
                }
            ]
        }

        return workflow


def print_workflow_instructions():
    """Print instructions for Claude Code to execute the workflow"""

    print("""
To run the AI Company, Claude Code should:

1. Read this workflow definition
2. For each phase, use the Task tool with subagent_type="general-purpose"
3. Pass the agent's task description and context from previous phases
4. Collect results and pass to next phase
5. Parse final code output and save files

Example for Phase 1 (CEO Planning):

```
Task(
    subagent_type="general-purpose",
    prompt="You are the CEO. [task description]",
    description="CEO: Project Planning"
)
```

Then collect the result and feed it as context to Phase 2 (CTO), etc.
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script defines the AI Company workflow.")
        print("It should be called BY Claude Code, which will execute it using the Task tool.")
        print()
        print_workflow_instructions()
        sys.exit(0)

    request = " ".join(sys.argv[1:])
    company = AICompany(None)
    workflow = company.build(request)

    print(json.dumps(workflow, indent=2))
