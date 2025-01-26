from enum import Enum
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, validator
from typing import List, Optional
import re
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.llm_providers import LLMProvider, initialize_llm

class PersonalizedEmail(BaseModel):
    company_email: str
    subject_line: str
    email_body: str
    company_name: str

    @validator('email_body')
    def clean_html(cls, v):
        # First convert the plain text/markdown to HTML structure
        paragraphs = v.split('\n')  # Changed from \n\n to \n to handle list items properly
        html_content = []
        
        in_list = False
        list_items = []
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
                
            # Convert markdown bold to HTML strong
            p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
            # Convert markdown links to HTML anchor tags
            p = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', p)
            
            # Handle bullet points
            if p.startswith('- '):
                if not in_list:
                    in_list = True
                    list_items = []  # Reset list items when starting new list
                # Remove the bullet point marker and add as separate list item
                item_content = p[2:].strip()
                list_items.append(f'<li>{item_content}</li>')
            else:
                if in_list:
                    # Close previous list
                    html_content.append(f'<ul style="margin: 10px 0; padding-left: 20px;">{" ".join(list_items)}</ul>')
                    list_items = []  # Clear list items after adding to content
                    in_list = False
                if p:  # Only add non-empty paragraphs
                    html_content.append(f'<p>{p}</p>')
        
        # Close any remaining list at the end of processing
        if in_list and list_items:  # Check both flags to ensure we have items to add
            html_content.append(f'<ul style="margin: 10px 0; padding-left: 20px;">{" ".join(list_items)}</ul>')
        
        # Join all content and wrap in table structure with styling
        v = '<tr><td>' + ''.join(html_content) + '</td></tr>'
        
        # Remove any unnecessary escaping
        v = v.replace('\\n', '').replace('\\/', '/').strip()
        #escape quotes
        v = v.replace('"', '\\"')
        
        return v

    class Config:
        json_encoders = {
            # Don't do any additional string processing
            str: lambda v: v
        }

class EmailOutput(BaseModel):
    emails: List[PersonalizedEmail]

@CrewBase
class MarketingEmailGeneratorCrew:
    """MarketingEmailGenerator crew"""

    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_file = os.path.join(output_dir, "personalized_email.json")
        
        # Add JSON encoding configuration
        self.json_config = {
            'ensure_ascii': False,
            'allow_nan': False,
            'indent': 2
        }

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
            output_file=self.output_file,
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
            format_kwargs={
                'ensure_ascii': False,
                'allow_nan': False,
                'indent': 2,
                'escape_forward_slashes': False,
                'separators': (',', ': '),
                'html_output': True,
            }
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