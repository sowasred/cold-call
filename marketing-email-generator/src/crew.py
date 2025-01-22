from enum import Enum
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.llm_providers import LLMProvider, initialize_llm

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

        active_llm = os.getenv("ACTIVE_LLM", "").upper()
        print(f"Active LLM: {active_llm}")
        try:
            provider = LLMProvider(active_llm)
        except ValueError:
            raise ValueError(
                f"Invalid LLM provider: {active_llm}. "
                f"Must be one of: {', '.join([p.value for p in LLMProvider])}"
            )
        
        self.llm = initialize_llm(provider)

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