#!/usr/bin/env python3
"""
AI Company - Multi-agent software development team
Uses Claude Code's existing authentication via subprocess
"""

import os
import sys
import json
import subprocess
import tempfile

#===============================================================================
# AGENT EXECUTION VIA CLAUDE CODE
#===============================================================================

def run_agent(role, goal, backstory, task, context=None):
    """Execute an agent task using Claude Code's authentication"""

    system_prompt = f"""You are the {role} of an AI software company.

GOAL: {goal}

BACKSTORY: {backstory}

Your job is to complete the task assigned to you professionally and thoroughly.
Focus on delivering clear, actionable output that the next person in the workflow can use."""

    user_message = f"""TASK:
{task}"""

    if context:
        user_message += f"\n\nCONTEXT FROM PREVIOUS AGENTS:\n{context}"

    # Create a temporary file with the prompt
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(f"SYSTEM: {system_prompt}\n\n")
        f.write(f"USER: {user_message}")
        prompt_file = f.name

    print(f"\n{'='*80}")
    print(f"[{role.upper()}] - Working on task...")
    print(f"{'='*80}\n")

    try:
        # Use openclaw CLI to execute the prompt
        result = subprocess.run(
            ['openclaw', 'ask', '--file', prompt_file],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"Error running agent: {result.stderr}")
            return None

        output = result.stdout.strip()

        print(f"\n{role} OUTPUT:\n")
        print(output)
        print(f"\n{'='*80}\n")

        return output

    finally:
        # Clean up temp file
        try:
            os.unlink(prompt_file)
        except:
            pass


#===============================================================================
# COMPANY WORKFLOW
#===============================================================================

def build_software(user_request, output_dir="./output"):
    """Main workflow: build software from user request"""

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'#'*80}")
    print(f"# AI COMPANY - NEW PROJECT")
    print(f"# Request: {user_request}")
    print(f"# Output: {output_dir}")
    print(f"{'#'*80}\n")

    # Phase 1: Planning (CEO)
    plan = run_agent(
        role="CEO",
        goal="Define project vision, success criteria, and make final decisions",
        backstory="""You understand what users want to build and define clear success criteria.
You think strategically about product-market fit. You're decisive but listen to your team.""",
        task=f"""Analyze this user request and create a project plan:

USER REQUEST: {user_request}

Define:
1. What exactly we're building (clear product description)
2. Success criteria (what makes this done?)
3. Core features (must-haves only)
4. Constraints (keep it simple and achievable)

Be specific and realistic."""
    )

    if not plan:
        print("CEO planning failed!")
        return

    # Phase 2: Architecture (CTO)
    architecture = run_agent(
        role="CTO",
        goal="Design system architecture and ensure code quality",
        backstory="""You design system architecture, choose tech stacks, and review code quality.
You have deep expertise in software architecture and best practices.
You're pragmatic - you choose the right tool for the job.""",
        task="""Design the technical architecture.

Define:
1. Tech stack (language, framework if needed)
2. File structure (what files to create with brief descriptions)
3. Architecture (how components fit together)
4. Implementation approach (what to build first)

Be specific. Choose simple, proven technologies. Give a clear blueprint.""",
        context=plan
    )

    if not architecture:
        print("CTO design failed!")
        return

    # Phase 3: Implementation (Developer)
    code = run_agent(
        role="Senior Developer",
        goal="Write clean, working code",
        backstory="""You write production-quality code based on architecture specs.
You're an excellent programmer who writes clean, maintainable code with good comments.""",
        task=f"""Implement the software based on the design.

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
        context=f"PROJECT PLAN:\n{plan}\n\nARCHITECTURE:\n{architecture}"
    )

    if not code:
        print("Developer implementation failed!")
        return

    # Save code files
    save_code_files(code, output_dir)

    # Phase 4: Testing (QA)
    qa_report = run_agent(
        role="QA Engineer",
        goal="Test software and report bugs",
        backstory="""You test software thoroughly, find edge cases, and write clear bug reports.
You're meticulous and think like an adversary - always trying to break things.""",
        task=f"""Review and test the implemented software.

Test for:
1. Does it meet the requirements?
2. Are there obvious bugs or errors?
3. Are edge cases handled?
4. Is the code clear and maintainable?

Provide a detailed test report. If you find bugs, list them with reproduction steps.""",
        context=f"REQUIREMENTS:\n{plan}\n\nCODE:\n{code}"
    )

    if not qa_report:
        print("QA testing failed!")
        return

    # Phase 5: Final Review (CEO)
    decision = run_agent(
        role="CEO",
        goal="Define project vision, success criteria, and make final decisions",
        backstory="""You understand what users want to build and define clear success criteria.
You think strategically about product-market fit. You're decisive but listen to your team.""",
        task="""Review the project and make final decision.

Based on all the work done, decide:
1. Does this meet our success criteria?
2. Are there critical issues?
3. Is it ready to ship?

Final verdict: SHIP IT or NEEDS WORK (with specific fixes).""",
        context=f"PLAN:\n{plan}\n\nQA REPORT:\n{qa_report}"
    )

    print(f"\n{'#'*80}")
    print(f"# PROJECT COMPLETE")
    print(f"# Status: {decision}")
    print(f"# Files saved to: {output_dir}")
    print(f"{'#'*80}\n")


def save_code_files(code_output, output_dir):
    """Parse and save code files from developer output"""

    lines = code_output.split('\n')
    current_file = None
    current_content = []

    for line in lines:
        if line.startswith('=== FILENAME:'):
            # Save previous file if exists
            if current_file:
                filepath = os.path.join(output_dir, current_file)
                os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else output_dir, exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write('\n'.join(current_content))
                print(f"✓ Saved: {filepath}")
                current_content = []

            # Start new file
            current_file = line.split('FILENAME:')[1].strip().split('===')[0].strip()

        elif line.startswith('=== END FILE ==='):
            # Save current file
            if current_file:
                filepath = os.path.join(output_dir, current_file)
                os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else output_dir, exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write('\n'.join(current_content))
                print(f"✓ Saved: {filepath}")
            current_file = None
            current_content = []

        elif current_file:
            current_content.append(line)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python company_v3.py '<project description>'")
        print('Example: python company_v3.py "build a calculator"')
        sys.exit(1)

    request = " ".join(sys.argv[1:])
    build_software(request)
