import os
import logging
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from src.gary.models import JobAnalysis, Resume

# Configure logging
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")


class LLMConfigurationError(Exception):
    """Exception raised when LLM configuration fails."""

    pass


class CrewInitializationError(Exception):
    """Exception raised when crew initialization fails."""

    pass


def validate_environment() -> None:
    """Validate required environment variables."""
    if not OPENROUTER_API_KEY:
        raise LLMConfigurationError(
            "OPENROUTER_API_KEY environment variable is not set"
        )

    if not OPENROUTER_BASE_URL:
        raise LLMConfigurationError(
            "OPENROUTER_BASE_URL environment variable is not set"
        )

    logger.info("Environment variables validated successfully")


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
        validate_environment()

        llm = LLM(
            model=model,
            temperature=temperature,
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

        logger.info(f"LLM configured successfully with model: {model}")
        return llm

    except Exception as e:
        logger.error(f"Failed to configure LLM: {e}")
        raise LLMConfigurationError(f"Failed to configure LLM: {e}")


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
                "openrouter/x-ai/grok-4-fast:free", 0.1
            ),
            max_iter=3,
            allow_delegation=False,
        )

    @agent
    def resume_tailorer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_tailorer"],
            verbose=True,
            llm=llm_config(
                "openrouter/anthropic/claude-sonnet-4", 0.4
            ),
            max_iter=5,
            allow_delegation=False,
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
            agent=self.resume_tailorer(),
            context=[
                self.job_analysis_task()
            ],  # Use output from job analysis as context
            output_pydantic=Resume,
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
