#!/usr/bin/env python3
"""
AI Company - Multi-agent software development team
Inspired by ChatDev
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, DirectoryReadTool
from langchain_anthropic import ChatAnthropic

# Load environment variables
load_dotenv()

# Initialize Claude model
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Initialize tools
file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()

# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

ceo = Agent(
    role='CEO',
    goal='Define project vision, success criteria, and make final decisions',
    backstory="""You are the CEO of this AI software company. Your job is to:
    - Understand what the user wants to build
    - Define clear success criteria
    - Make final go/no-go decisions
    - Ensure the team delivers value

    You think strategically about product-market fit and user needs.
    You're decisive but listen to your team's expertise.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

cto = Agent(
    role='CTO',
    goal='Design system architecture and ensure code quality',
    backstory="""You are the CTO of this AI software company. Your job is to:
    - Design system architecture and tech stack
    - Review code for quality, security, and best practices
    - Make technical decisions (frameworks, patterns, structure)
    - Ensure the solution is maintainable and scalable

    You have deep expertise in software architecture, design patterns,
    and engineering best practices. You're pragmatic - you choose the
    right tool for the job, not the fanciest one.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

developer = Agent(
    role='Senior Developer',
    goal='Write clean, working code that implements the requirements',
    backstory="""You are a senior software developer. Your job is to:
    - Write production-quality code based on the CTO's architecture
    - Implement features according to specifications
    - Fix bugs reported by QA
    - Write clear comments and documentation

    You're an excellent programmer who writes clean, maintainable code.
    You follow best practices and the architecture defined by the CTO.
    You're thorough and detail-oriented.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

qa_engineer = Agent(
    role='QA Engineer',
    goal='Test the software and report bugs clearly',
    backstory="""You are a QA engineer. Your job is to:
    - Test the software thoroughly
    - Find edge cases and potential bugs
    - Write clear bug reports with reproduction steps
    - Verify fixes work correctly

    You're meticulous and think like an adversary - always trying to
    break things. You write detailed bug reports that help developers
    fix issues quickly.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ============================================================================
# WORKFLOW FUNCTIONS
# ============================================================================

def build_software(user_request: str, output_dir: str = "./output"):
    """
    Main workflow: Takes a user request and builds software autonomously.

    Args:
        user_request: What the user wants built (e.g., "build a todo app")
        output_dir: Where to save the generated code
    """

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"AI COMPANY: Starting new project")
    print(f"Request: {user_request}")
    print(f"Output: {output_dir}")
    print(f"{'='*80}\n")

    # ========================================================================
    # PHASE 1: PROJECT PLANNING
    # ========================================================================

    task_plan = Task(
        description=f"""Analyze this user request and create a project plan:

        USER REQUEST: {user_request}

        Define:
        1. What exactly we're building (clear product description)
        2. Success criteria (what makes this done?)
        3. Core features (what must it have?)
        4. Constraints (time, complexity, scope)

        Keep it realistic - we want something that works, not everything.
        """,
        agent=ceo,
        expected_output="Clear project plan with vision, success criteria, and core features"
    )

    # ========================================================================
    # PHASE 2: TECHNICAL DESIGN
    # ========================================================================

    task_design = Task(
        description="""Design the technical architecture for this project.

        Based on the CEO's plan, define:
        1. Tech stack (language, framework, libraries)
        2. File structure (what files we'll create)
        3. Architecture (how components fit together)
        4. Implementation approach (what to build first)

        Be specific and pragmatic. Choose simple, proven technologies.
        Provide a clear blueprint the developer can follow.
        """,
        agent=cto,
        expected_output="Technical architecture document with tech stack, file structure, and implementation approach"
    )

    # ========================================================================
    # PHASE 3: IMPLEMENTATION
    # ========================================================================

    task_implement = Task(
        description=f"""Implement the software based on the CTO's design.

        Provide complete, working code for all necessary files:
        - Follow the architecture and file structure from the CTO
        - Write clean, well-commented code
        - Include proper error handling
        - Provide the complete code that can be saved to {output_dir}

        Output all code files with clear filenames and complete content.
        Focus on making it work correctly first.
        """,
        agent=developer,
        expected_output=f"Complete working code for all files, ready to save to {output_dir}"
    )

    # ========================================================================
    # PHASE 4: QUALITY ASSURANCE
    # ========================================================================

    task_qa = Task(
        description=f"""Test the implemented software and report any issues.

        Review the code in: {output_dir}

        Test for:
        1. Does it meet the requirements?
        2. Are there obvious bugs or errors?
        3. Are there edge cases not handled?
        4. Is the code clear and maintainable?

        Provide a clear test report. If you find bugs, describe them
        with specific reproduction steps.
        """,
        agent=qa_engineer,
        expected_output="Detailed test report with findings, bugs (if any), and overall quality assessment",
        tools=[file_read_tool, directory_read_tool]
    )

    # ========================================================================
    # PHASE 5: FINAL REVIEW
    # ========================================================================

    task_review = Task(
        description="""Review the project and make the final decision.

        Based on:
        - The original requirements
        - What was implemented
        - QA's test report

        Decide:
        1. Does this meet our success criteria?
        2. Are there critical issues that must be fixed?
        3. Is it ready to ship?

        Provide final verdict: SHIP IT or NEEDS WORK (with specific fixes needed).
        """,
        agent=ceo,
        expected_output="Final decision: SHIP IT or NEEDS WORK with reasoning"
    )

    # ========================================================================
    # EXECUTE THE WORKFLOW
    # ========================================================================

    crew = Crew(
        agents=[ceo, cto, developer, qa_engineer],
        tasks=[task_plan, task_design, task_implement, task_qa, task_review],
        process=Process.sequential,  # Tasks run in order
        verbose=True
    )

    result = crew.kickoff()

    print(f"\n{'='*80}")
    print(f"AI COMPANY: Project complete!")
    print(f"{'='*80}\n")
    print(result)

    return result


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python company.py '<project description>'")
        print('Example: python company.py "build a simple todo list web app"')
        sys.exit(1)

    request = " ".join(sys.argv[1:])
    build_software(request)
