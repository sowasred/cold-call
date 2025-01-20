from enum import Enum
from crewai_tools import SeleniumScrapingTool, SerperDevTool
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

class LLMProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

class PersonalizedEmail(BaseModel):
    to: str
    subject_line: str
    email_body: str

class EmailOutput(BaseModel):
    emails: List[PersonalizedEmail]

@CrewBase
class MarketingEmailGeneratorCrew:
    """MarketingEmailGenerator crew"""

    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"
        self.output_file = os.path.join("output", "personalized_email.json")

        if os.getenv("USE_OLLAMA"):
            self.llm = LLM(
                model="ollama/llama3.2",
                base_url="http://localhost:11434"
            )
        else:
            self.llm = LLM(
                model="gpt-4o-mini",
                base_url="https://api.openai.com/v1"
            )

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingEmailGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager_agent=self.agents_config["manager"],
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[SeleniumScrapingTool(), SerperDevTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    @agent
    def content_personalizer(self) -> Agent:
        return Agent(
            config=self.agents_config["content_personalizer"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    @agent
    def email_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["email_copywriter"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    @task
    def research_prospect_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_prospect_task"],
            agent=self.researcher(),
            llm=self.llm,
        )

    @task
    def personalize_content_task(self) -> Task:
        return Task(
            config=self.tasks_config["personalize_content_task"],
            agent=self.content_personalizer(),
            llm=self.llm,
        )

    @task
    def write_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_email_task"],
            agent=self.email_copywriter(),
            output_json=EmailOutput,
            output_file=self.output_file,
            llm=self.llm,
        )
