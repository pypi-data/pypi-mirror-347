"""Agent module."""

import os
from typing import Any, Union
import logfire
from huggingface_hub.errors import LocalEntryNotFoundError
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool
from pydantic_ai.agent import ModelSettings
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.messages import ModelMessage, RetryPromptPart, ToolCallPart
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from smolagents import load_tool
from aic_core.agent.agent_hub import AgentHub
from aic_core.agent.result_types import ComponentRegistry


if os.environ.get("LOGFIRE_TOKEN", None):  # pragma: no cover
    logfire.configure()
    logfire.instrument_pydantic_ai()


class AgentConfig(BaseModel):
    """Configuration class for Agent initialization."""

    model: str
    """Model name. Must be a valid pydantic_ai.models.KnownModelName."""
    result_type: list[str] = ["str"]
    """Result type. Can be name of Python primitives or a list of HF Hub file names."""
    system_prompt: str = "You are a helpful assistant."
    """System prompt for the agent."""
    # deps_type: type[AgentDepsT] = (NoneType,)
    name: str = "Agent"
    """Name of the agent."""
    model_settings: dict | None = None
    """Model settings for the agent."""
    retries: int = 1
    """Number of retries for the agent."""
    result_tool_name: str = "final_result"
    """Name of the result tool."""
    result_tool_description: str | None = None
    """Description of the result tool."""
    result_retries: int | None = None
    """Number of retries for the result tool."""
    known_tools: list[str] = []
    """List of known tools for the agent."""
    hf_tools: list[str] = []
    """List of Hugging Face tools for the agent."""
    mcp_servers: list[str] = []
    """List of MCP servers commands for the agent."""
    defer_model_check: bool = False
    """Whether to defer model check for the agent."""
    end_strategy: str = "early"
    """End strategy for the agent."""
    instrument: bool = False
    """Whether to instrument the agent."""
    config_version: str = "0.0.1"
    """Version of the agent config."""
    repo_id: str = Field()
    """Hugging Face repo ID."""

    @classmethod
    def from_hub(cls, repo_id: str, agent_name: str) -> "AgentConfig":
        """Load an agent config from Hugging Face Hub."""
        repo = AgentHub(repo_id)
        config_obj = repo.load_config(agent_name)
        return cls(**config_obj)

    def push_to_hub(self) -> None:
        """Upload a JSON file to Hugging Face Hub."""
        repo = AgentHub(self.repo_id)

        # Verify before uploading
        agent_factory = AgentFactory(self)
        agent_factory.create_agent(api_key="key")

        # Upload the file
        repo.upload_content(
            filename=self.name,
            content=self.model_dump_json(indent=2),
            subdir=AgentHub.agents_dir,
        )


class AgentFactory:
    """Factory class to create an agent from a config."""

    def __init__(self, config: AgentConfig):
        """Initialise the agent factory."""
        self.config = config

    @classmethod
    def hf_to_pai_tools(cls, tool_name: str) -> Tool:
        """Convert a Hugging Face tool to a Pydantic AI tool."""
        try:
            tool = load_tool(tool_name, trust_remote_code=True, local_files_only=True)
        except LocalEntryNotFoundError:
            tool = load_tool(tool_name, trust_remote_code=True)
        return Tool(
            tool.forward,
            name=tool.name,
            # Do nothing if the tool function already has a docstring
            description=tool.description if not tool.forward.__doc__ else None,
        )

    def get_result_type(self) -> Any:
        """Creates a Union type from a list of types."""
        if not self.config.result_type:
            return str

        type_classes: list[Any] = []
        known_types = ComponentRegistry.get_registered_components()
        for type_str in self.config.result_type:
            # Handle built-in types and local class types
            try:
                if type_str in known_types:
                    type_classes.append(ComponentRegistry.get_component_class(type_str))
                else:
                    type_classes.append(eval(type_str))
            except NameError:  # Structured output
                hf_repo = AgentHub(self.config.repo_id)
                type_classes.append(hf_repo.load_result_type(type_str))

        if len(type_classes) == 1:
            return type_classes[0]
        # Create a new type using Union
        return Union.__getitem__(tuple(type_classes))

    def get_tools(self) -> list[Tool]:
        """Get the tools from known tools and hf tools."""
        tools = []
        hf_repo = AgentHub(self.config.repo_id)
        for tool_name in self.config.known_tools:
            tool = hf_repo.load_tool(tool_name)
            tools.append(Tool(tool))  # type: ignore[arg-type]
        for tool_name in self.config.hf_tools:
            tools.append(self.hf_to_pai_tools(tool_name))
        return tools

    def get_mcp_servers(self) -> list[MCPServerStdio]:
        """Get the MCP servers from the config."""
        servers = []
        for server in self.config.mcp_servers:
            if not server.strip():  # pragma: no cover
                continue
            command, *args = server.split()
            servers.append(MCPServerStdio(command, args))
        return servers

    def create_agent(self, api_key: str | None = None) -> Agent:
        """Create an agent from a config."""
        result_type = self.get_result_type()
        model_name = self.config.model.split(":")[1]
        model = OpenAIModel(model_name, provider=OpenAIProvider(api_key=api_key))
        return Agent(
            model=model,
            output_type=result_type,
            system_prompt=self.config.system_prompt,
            name=self.config.name,
            model_settings=ModelSettings(**self.config.model_settings)
            if self.config.model_settings
            else None,
            retries=self.config.retries,
            # result_tool_name=self.config.result_tool_name,
            # result_tool_description=self.config.result_tool_description,
            output_retries=self.config.result_retries,
            tools=self.get_tools(),
            mcp_servers=self.get_mcp_servers(),  # type: ignore[arg-type]
            defer_model_check=self.config.defer_model_check,
            end_strategy=self.config.end_strategy,  # type: ignore
            instrument=self.config.instrument,
        )


class AICAgent:
    """A wrapper around the pydantic_ai.Agent class."""

    def __init__(self, repo_id: str, agent_name: str) -> None:
        """Initialize the agent."""
        self.repo_id = repo_id
        self.agent = self._get_agent(agent_name)

    def _get_agent(self, agent_name: str) -> Agent:
        """Get the agent given the agent name."""
        agent_config = AgentConfig.from_hub(self.repo_id, agent_name)
        agent_factory = AgentFactory(agent_config)
        agent = agent_factory.create_agent()

        return agent

    async def get_response(
        self,
        user_prompt: str,
        history: list[ModelMessage],
        skip_retry_msgs: bool = True,
    ) -> list[ModelMessage]:
        """Get the response from the agent."""
        if self.agent._mcp_servers:
            async with self.agent.run_mcp_servers():  # pragma: no cover
                result = await self.agent.run(user_prompt, message_history=history)
        else:
            result = await self.agent.run(user_prompt, message_history=history)

        new_messages = result.new_messages()
        if skip_retry_msgs:
            # Skip retry messages and failed tool calls
            new_messages = [
                msg
                for i, msg in enumerate(new_messages)
                if not (
                    isinstance(msg.parts[0], RetryPromptPart)
                    or (
                        i > 0
                        and i < len(new_messages) - 1
                        and isinstance(msg.parts[0], ToolCallPart)
                        and isinstance(new_messages[i + 1].parts[0], RetryPromptPart)
                    )
                )
            ]
        return new_messages
