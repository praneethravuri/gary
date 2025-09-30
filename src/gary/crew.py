import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from gary.models import JobAnalysis, ResumeContent, ResumeValidationReport
from gary.tools import ResumeWordDocGeneratorTool


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")



def llm_config(model: str, temperature: float) -> LLM:
    """
    Create LLM configuration with error handling.

    Args:
        model: The model name to use
        temperature: The temperature setting for the model

    Returns:
        Configured LLM instance

    Raises:
        LLMConfigurationError: If LLM configuration fails
    """
    try:

        llm = LLM(
            model=model,
            temperature=temperature,
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )
        return llm

    except Exception as e:
        raise Exception(f"Failed to configure LLM: {e}")


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
            llm=llm_config(
                "openrouter/deepseek/deepseek-chat-v3-0324", 0.1
            ),
            max_iter=3,
            allow_delegation=False,
        )

    @agent
    def resume_tailor(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_tailor"],
            verbose=True,
            llm=llm_config(
                "openrouter/deepseek/deepseek-chat-v3-0324", 0.4
            ),
            max_iter=5,
            allow_delegation=False,
        )

    @agent
    def resume_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_validator"],
            verbose=True,
            llm=llm_config(
                "openrouter/deepseek/deepseek-chat-v3-0324", 0.2
            ),
            max_iter=3,
            allow_delegation=False,
            tools=[ResumeWordDocGeneratorTool()],
        )


    @task
    def job_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_analysis_task"],
            agent=self.job_analyst(),
            output_pydantic=JobAnalysis,
        )

    @task
    def resume_tailoring_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_tailoring_task"],
            agent=self.resume_tailor(),
            context=[
                self.job_analysis_task()
            ],  # Use output from job analysis as context
            output_pydantic=ResumeContent,
        )

    @task
    def resume_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_validation_task"],
            agent=self.resume_validator(),
            context=[
                self.job_analysis_task(),
                self.resume_tailoring_task()
            ],  # Use outputs from job analysis and resume tailoring
            output_pydantic=ResumeValidationReport,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Gary crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file=True,
        )
