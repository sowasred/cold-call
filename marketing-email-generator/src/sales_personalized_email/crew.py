from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel
from typing import List
import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


class PersonalizedEmail(BaseModel):
    to: str
    subject_line: str
    email_body: str

class EmailOutput(BaseModel):
    emails: List[PersonalizedEmail]

@CrewBase
class SalesPersonalizedEmailCrew:
    """SalesPersonalizedEmail crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    output_file = os.path.join("output", "personalized_email.json")

    @agent
    def prospect_researcher(self) -> Agent:
        scrape_tool = ScrapeWebsiteTool()
        serper_tool = SerperDevTool()
        
        return Agent(
            config=self.agents_config["prospect_researcher"],
            tools=[scrape_tool, serper_tool],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def content_personalizer(self) -> Agent:
        return Agent(
            config=self.agents_config["content_personalizer"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def email_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["email_copywriter"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_prospect_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_prospect_task"],
            agent=self.prospect_researcher(),
        )

    @task
    def personalize_content_task(self) -> Task:
        return Task(
            config=self.tasks_config["personalize_content_task"],
            agent=self.content_personalizer(),
        )

    @task
    def write_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_email_task"],
            agent=self.email_copywriter(),
            output_json=EmailOutput,
            output_file=self.output_file,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SalesPersonalizedEmail crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
