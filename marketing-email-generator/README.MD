# Marketing Email Generator Crew

This project uses multiple AI agents working together to research and analyze target companies and generate personalized, compelling email content, leveraging the powerful and flexible framework powered by [crewAI](https://crewai.com).

## Agent Architecture

### 1. Research Agent

- Analyzes company websites, social media, and public data
- Identifies key value propositions and pain points
- Extracts company culture and tone of voice
- Stores findings in a structured format for the content writer

### 2. Content Writer Agent

- Creates personalized email content based on research
- Adapts tone and style to match recipient company
- Incorporates proven cold email frameworks
- Ensures compelling subject lines and call-to-actions

### 3. Quality Control Agent

- Validates email content against best practices
- Checks for spam triggers and compliance
- Reviews personalization accuracy
- Suggests improvements for engagement

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system.
This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:

```bash
uv lock
```

```bash
uv sync
```

### Setup

1. Add your `OPENAI_API_KEY` into the `.env` file

2. Create a output directory in the root of the project

3. Optional Customization:
   - Modify `src/config/agents.yaml` to define your agents
   - Modify `src/config/tasks.yaml` to define your tasks
   - Modify `src/crew.py` to add your own logic, tools and specific args

## Running the Project

To generate personalized emails for your target companies:

```bash
uv run marketing-email-generator input/targets.csv input/sender.csv
```

This will:

1. Process each company in `targets.csv`
2. Use sender information from `sender.csv`
3. Generate personalized emails
4. Save results in `output/personalized_email.json`

### Output Structure

```json
{
  "emails": [
    {
      "to": "recipient@example.com",
      "subject_line": "Compelling subject line",
      "email_body": "Personalized email content..."
    }
  ]
}
```

## Documentation

- Visit [CrewAI documentation](https://docs.crewai.com)
- Reach out through [CrewAI GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with CrewAI docs](https://chatg.pt/DWjSBZn)
- [Check Available CrewAI Tools](https://github.com/crewAIInc/crewAI-tools)
