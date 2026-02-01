#!/usr/bin/env python3
"""
AI Company - Multi-agent software development team
Built from scratch with Anthropic SDK
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment
load_dotenv()

#===============================================================================
# AGENT CLASS
#===============================================================================

class Agent:
    """A single AI agent with a specific role"""

    def __init__(self, role, goal, backstory, model="claude-sonnet-4-20250514"):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []

    def think(self, task_description, context=None):
        """Execute a task and return the result"""

        system_prompt = f"""You are the {self.role} of an AI software company.

GOAL: {self.goal}

BACKSTORY: {self.backstory}

Your job is to complete the task assigned to you professionally and thoroughly.
Focus on delivering clear, actionable output that the next person in the workflow can use."""

        user_message = f"""TASK:
{task_description}"""

        if context:
            user_message += f"\n\nCONTEXT FROM PREVIOUS AGENTS:\n{context}"

        print(f"\n{'='*80}")
        print(f"[{self.role.upper()}] - Working on task...")
        print(f"{'='*80}\n")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        result = response.content[0].text

        print(f"\n{self.role} OUTPUT:\n")
        print(result)
        print(f"\n{'='*80}\n")

        return result


#===============================================================================
# COMPANY CLASS
#===============================================================================

class Company:
    """The AI company that coordinates agents"""

    def __init__(self):
        # Define all agents
        self.ceo = Agent(
            role="CEO",
            goal="Define project vision, success criteria, and make final decisions",
            backstory="""You understand what users want to build and define clear success criteria.
You think strategically about product-market fit. You're decisive but listen to your team."""
        )

        self.cto = Agent(
            role="CTO",
            goal="Design system architecture and ensure code quality",
            backstory="""You design system architecture, choose tech stacks, and review code quality.
You have deep expertise in software architecture and best practices.
You're pragmatic - you choose the right tool for the job."""
        )

        self.developer = Agent(
            role="Senior Developer",
            goal="Write clean, working code",
            backstory="""You write production-quality code based on architecture specs.
You're an excellent programmer who writes clean, maintainable code with good comments."""
        )

        self.qa = Agent(
            role="QA Engineer",
            goal="Test software and report bugs",
            backstory="""You test software thoroughly, find edge cases, and write clear bug reports.
You're meticulous and think like an adversary - always trying to break things."""
        )

    def build(self, user_request, output_dir="./output"):
        """Main workflow: build software from user request"""

        os.makedirs(output_dir, exist_ok=True)

        print(f"\n{'#'*80}")
        print(f"# AI COMPANY - NEW PROJECT")
        print(f"# Request: {user_request}")
        print(f"# Output: {output_dir}")
        print(f"{'#'*80}\n")

        # Phase 1: Planning
        plan = self.ceo.think(f"""Analyze this user request and create a project plan:

USER REQUEST: {user_request}

Define:
1. What exactly we're building (clear product description)
2. Success criteria (what makes this done?)
3. Core features (must-haves only)
4. Constraints (keep it simple and achievable)

Be specific and realistic.""")

        # Phase 2: Architecture
        architecture = self.cto.think("""Design the technical architecture.

Define:
1. Tech stack (language, framework if needed)
2. File structure (what files to create with brief descriptions)
3. Architecture (how components fit together)
4. Implementation approach (what to build first)

Be specific. Choose simple, proven technologies. Give a clear blueprint.""",
            context=plan)

        # Phase 3: Implementation
        code = self.developer.think(f"""Implement the software based on the design.

Write all necessary code files:
- Follow the CTO's architecture exactly
- Write clean, well-commented code
- Include proper error handling
- Output COMPLETE, RUNNABLE code for each file

For each file, use this format:
=== FILENAME: path/to/file.ext ===
[complete file contents here]
=== END FILE ===

Make it work correctly. Be thorough.""",
            context=f"PROJECT PLAN:\n{plan}\n\nARCHITECTURE:\n{architecture}")

        # Save the code files
        self._save_code_files(code, output_dir)

        # Phase 4: Testing
        qa_report = self.qa.think(f"""Review and test the implemented software.

Test for:
1. Does it meet the requirements?
2. Are there obvious bugs or errors?
3. Are edge cases handled?
4. Is the code clear and maintainable?

Provide a detailed test report. If you find bugs, list them with reproduction steps.""",
            context=f"REQUIREMENTS:\n{plan}\n\nCODE:\n{code}")

        # Phase 5: Final Review
        decision = self.ceo.think("""Review the project and make final decision.

Based on all the work done, decide:
1. Does this meet our success criteria?
2. Are there critical issues?
3. Is it ready to ship?

Final verdict: SHIP IT or NEEDS WORK (with specific fixes).""",
            context=f"PLAN:\n{plan}\n\nQA REPORT:\n{qa_report}")

        print(f"\n{'#'*80}")
        print(f"# PROJECT COMPLETE")
        print(f"# Status: {decision}")
        print(f"# Files saved to: {output_dir}")
        print(f"{'#'*80}\n")

        return {
            "plan": plan,
            "architecture": architecture,
            "code": code,
            "qa_report": qa_report,
            "decision": decision,
            "output_dir": output_dir
        }

    def _save_code_files(self, code_output, output_dir):
        """Parse and save code files from developer output"""

        lines = code_output.split('\n')
        current_file = None
        current_content = []

        for line in lines:
            if line.startswith('=== FILENAME:'):
                # Save previous file if exists
                if current_file:
                    filepath = os.path.join(output_dir, current_file)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'w') as f:
                        f.write('\n'.join(current_content))
                    print(f"✅ Saved: {filepath}")
                    current_content = []

                # Start new file
                current_file = line.split('FILENAME:')[1].strip().split('===')[0].strip()

            elif line.startswith('=== END FILE ==='):
                # Save current file
                if current_file:
                    filepath = os.path.join(output_dir, current_file)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'w') as f:
                        f.write('\n'.join(current_content))
                    print(f"✅ Saved: {filepath}")
                current_file = None
                current_content = []

            elif current_file:
                current_content.append(line)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python company_v2.py '<project description>' [api_key]")
        print('Example: python company_v2.py "build a todo list app"')
        print('   or:   python company_v2.py "build a todo list app" sk-ant-...')
        sys.exit(1)

    # Check if API key provided as last argument
    if len(sys.argv) >= 3 and sys.argv[-1].startswith('sk-ant-'):
        api_key = sys.argv[-1]
        request = " ".join(sys.argv[1:-1])
        os.environ['ANTHROPIC_API_KEY'] = api_key
    else:
        request = " ".join(sys.argv[1:])
        # Check if API key is in environment
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("ERROR: ANTHROPIC_API_KEY not set!")
            print("Either set it as environment variable or pass it as last argument:")
            print('  python company_v2.py "build a todo list app" sk-ant-your-key-here')
            sys.exit(1)

    company = Company()
    result = company.build(request)
