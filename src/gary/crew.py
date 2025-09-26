import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.gary.models import JobAnalysis

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")


def llm_config(model, temperature):
    return LLM(
        model=model,
        temperature=temperature,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )

@CrewBase
class Gary:
    """Gary crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"], 
            verbose=True,
            llm=llm_config("openrouter/x-ai/grok-4-fast:free", 0.1),  # Low temperature for consistent keyword extraction
            max_iter=3
        )

    @task
    def job_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_analysis_task"],
            agent=self.job_analyst(),
            output_pydantic=JobAnalysis,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Gary crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file=True
        )