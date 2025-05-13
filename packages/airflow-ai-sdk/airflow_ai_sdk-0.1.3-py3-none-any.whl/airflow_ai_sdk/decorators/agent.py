"""
This module contains the decorators for the agent.
"""

from typing import TYPE_CHECKING, Any

from pydantic_ai.agent import Agent

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def agent(agent: Agent, **kwargs: dict[str, Any]) -> "TaskDecorator":
    """
    Decorator to make agent calls.
    """
    kwargs["agent"] = agent
    return task_decorator_factory(
        decorated_operator_class=AgentDecoratedOperator,
        **kwargs,
    )
