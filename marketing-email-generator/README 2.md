# SalesPersonalizedEmail Crew

Welcome to the SalesPersonalizedEmail Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

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
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/sales_personalized_email/config/agents.yaml` to define 
your agents
- Modify `src/sales_personalized_email/config/tasks.yaml` to define 
your tasks
- Modify `src/sales_personalized_email/crew.py` to add your own 
logic, tools and specific args
- Modify `src/sales_personalized_email/main.py` to add custom inputs 
for your agents and tasks

2. Prepare your CSV files:

   a. Create a `sender.csv` file with your company information:
   ```csv
   Company Summary,Company Name,Company Website,Email,Full Name,Title,Phone
   "Your Company","https://company.com","hello@company.com","John Doe","Business Development","(123) 456-7890","Your company description..."
   ```

   b. Create a `targets.csv` file with target companies:
   ```csv
   Company Name,Industry,Category,Subcategory,Phone,Email,Facebook,Instagram,Twitter,LinkedIn,Address,Website,Rating
   "Target Inc","Industry","Category","Subcategory","https://target.com","555-1234","contact@target.com","","","",""
   ```

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
uv run sales_personalized_email targets.csv sender.csv
```

This will process each company in `targets.csv` using the sender information from `sender.csv` and generate personalized emails.

## Understanding Your Crew

The sales-personalized-email Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate to analyze target companies and generate personalized sales emails. The configuration files in the `config` directory define:

- `agents.yaml`: The capabilities and configurations of each agent
- `tasks.yaml`: The sequence of tasks performed for each target company

## Documentation

For support, questions, or feedback:
- Visit our [documentation](https://docs.crewai.com)
- Reach out through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)
- [Check Available CrewAI Tools](https://github.com/crewAIInc/crewAI-tools)
