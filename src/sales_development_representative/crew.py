from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

@CrewBase
class SalesDevelopmentRepresentative:
    """SalesDevelopmentRepresentative crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sales_development_representative(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_development_representative"],
            verbose=True
        )

    @agent
    def cold_email_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["cold_email_creator"],
            verbose=True
        )

    @agent
    def web_scraper(self) -> Agent:
        # Create the scraping tool
        scraping_tool = ScrapeWebsiteTool()
        
        # Get the base configuration
        config = self.agents_config["web_scraper"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            tools=[scraping_tool],
            verbose=True
        )

    @task
    def web_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config["web_scraping_task"]
        )

    @task
    def lead_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["lead_research_task"]
        )

    @task
    def email_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["email_creation_task"],
            output_file="report.md"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )