"""
Models for the Swarms API client.

This module contains Pydantic models that mirror the API's data structures.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentSpec(BaseModel):
    """Configuration for a single agent."""

    agent_name: Optional[str] = Field(
        None,
        description="The unique name assigned to the agent, which identifies its role and functionality within the swarm.",
    )
    description: Optional[str] = Field(
        None,
        description="A detailed explanation of the agent's purpose, capabilities, and any specific tasks it is designed to perform.",
    )
    system_prompt: Optional[str] = Field(
        None,
        description="The initial instruction or context provided to the agent, guiding its behavior and responses during execution.",
    )
    model_name: Optional[str] = Field(
        default="gpt-4o-mini",
        description="The name of the AI model that the agent will utilize for processing tasks and generating outputs.",
    )
    auto_generate_prompt: Optional[bool] = Field(
        default=False,
        description="A flag indicating whether the agent should automatically create prompts based on the task requirements.",
    )
    max_tokens: Optional[int] = Field(
        default=8192,
        description="The maximum number of tokens that the agent is allowed to generate in its responses.",
    )
    temperature: Optional[float] = Field(
        default=0.5,
        description="A parameter that controls the randomness of the agent's output.",
    )
    role: Optional[str] = Field(
        default="worker",
        description="The designated role of the agent within the swarm.",
    )
    max_loops: Optional[int] = Field(
        default=1,
        description="The maximum number of times the agent is allowed to repeat its task.",
    )
    tools_dictionary: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="A dictionary of tools that the agent can use to complete its task.",
    )

    class Config:
        arbitrary_types_allowed = True


class AgentCompletion(BaseModel):
    """Request model for agent completion."""

    agent_config: AgentSpec = Field(
        ..., description="The configuration of the agent to be completed."
    )
    task: str = Field(..., description="The task to be completed by the agent.")

    class Config:
        arbitrary_types_allowed = True


class ScheduleSpec(BaseModel):
    """Configuration for scheduled execution."""

    scheduled_time: datetime = Field(
        ...,
        description="The exact date and time (in UTC) when the swarm is scheduled to execute its tasks.",
    )
    timezone: Optional[str] = Field(
        "UTC", description="The timezone in which the scheduled time is defined."
    )


class SwarmSpec(BaseModel):
    """Configuration for a swarm of agents."""

    name: Optional[str] = Field(
        None, description="The name of the swarm.", max_length=100
    )
    description: Optional[str] = Field(
        None, description="A comprehensive description of the swarm's objectives."
    )
    agents: Optional[List[AgentSpec]] = Field(
        None, description="A list of agents participating in the swarm."
    )
    max_loops: Optional[int] = Field(
        default=1,
        description="The maximum number of execution loops allowed for the swarm.",
    )
    swarm_type: Optional[str] = Field(
        None, description="The classification of the swarm."
    )
    rearrange_flow: Optional[str] = Field(
        None,
        description="Instructions on how to rearrange the flow of tasks among agents.",
    )
    task: Optional[str] = Field(
        None,
        description="The specific task or objective that the swarm is designed to accomplish.",
    )
    img: Optional[str] = Field(
        None, description="An optional image URL associated with the swarm's task."
    )
    return_history: Optional[bool] = Field(
        True, description="Whether to return the swarm's execution history."
    )
    rules: Optional[str] = Field(
        None, description="Guidelines or constraints for the agents within the swarm."
    )
    schedule: Optional[ScheduleSpec] = Field(
        None, description="Details regarding the scheduling of the swarm's execution."
    )
    tasks: Optional[List[str]] = Field(
        None, description="A list of tasks that the swarm should complete."
    )
    messages: Optional[List[Dict[str, Any]]] = Field(
        None, description="A list of messages that the swarm should complete."
    )
    stream: Optional[bool] = Field(
        False, description="Whether the swarm should stream its output."
    )
    service_tier: Optional[str] = Field(
        "standard", description="The service tier to use for processing."
    )

    class Config:
        arbitrary_types_allowed = True
