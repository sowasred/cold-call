from enum import Enum
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
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
    DEEPSEEK = "deepseek"

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
        
        # TODO: Figure out how to use manager agent
        # self.manager = Agent(
        #     config=self.agents_config["manager"],
        #     allow_delegation=True,
        # )
        
        # self.llm = LLM(
        #         model=f"deepseek/{os.getenv('DEEPSEEK_MODEL')}",
        #         base_url=f"{os.getenv('DEEPSEEK_BASE_URL')}"
        #     )

        if os.getenv("USE_OLLAMA"):
            print("Using OLLAMA")
            self.llm = LLM(
                model=f"ollama/{os.getenv('OLLAMA_MODEL')}",
                base_url=f"{os.getenv('OLLAMA_BASE_URL')}"
            )
        elif os.getenv("USE_DEEPSEEK"):
            print("Using DEEPSEEK")
            self.llm = LLM(
                model=f"deepseek/{os.getenv('DEEPSEEK_MODEL')}",
                base_url=f"{os.getenv('DEEPSEEK_BASE_URL')}"
            )
        else:
            print("Using OPENAI")
            self.llm = LLM(
                model=f"{os.getenv('OPENAI_MODEL')}",
                base_url=f"{os.getenv('OPENAI_BASE_URL')}"
            )

    @agent
    def researcher(self) -> Agent:
        serper_tool = SerperDevTool()
        scrape_website_tool = ScrapeWebsiteTool()
        
        return Agent(
            config=self.agents_config["researcher"],
            tools=[serper_tool, scrape_website_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )

    @agent
    def sales_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_manager"],
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
    def initial_company_research(self) -> Task:
        return Task(
            config=self.tasks_config["initial_company_research"],
            agent=self.researcher(),
            llm=self.llm,
        )

    @task
    def research_industry_needs(self) -> Task:
        return Task(
            config=self.tasks_config["research_industry_needs"],
            agent=self.researcher(),
            llm=self.llm,
        )

    @task
    def write_sales_email(self) -> Task:
        initial_company_research = self.initial_company_research()
        research_industry_needs = self.research_industry_needs()
        return Task(
            config=self.tasks_config["write_sales_email"],
            context=[initial_company_research, research_industry_needs],
            agent=self.email_copywriter(),
            output_json=EmailOutput,
            output_file=self.output_file,
            llm=self.llm,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingEmailGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager_llm=self.llm,
            process=Process.sequential, # or Process.hierarchical
            verbose=True,
        )