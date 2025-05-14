"""Agent config page."""

from typing import get_args
import streamlit as st
from code_editor import code_editor
from pydantic_ai.models import KnownModelName
from aic_core.agent.agent import AgentConfig
from aic_core.agent.agent_hub import AgentHub
from aic_core.agent.result_types import ComponentRegistry
from aic_core.streamlit.mixins import AgentSelectorMixin, ToolSelectorMixin
from aic_core.streamlit.page import AICPage


class AgentConfigPage(AICPage, AgentSelectorMixin, ToolSelectorMixin):
    """Agent config page."""

    def __init__(self, repo_id: str) -> None:
        """Initialize the page."""
        super().__init__()
        self.repo_id = repo_id

    def list_result_type_options(self) -> dict[str, str]:
        """List all result types."""
        python_types = {type: f"{type} (P)" for type in ["str", "int", "float", "bool"]}
        internal_types = {
            type: f"{type} (I)"
            for type in ComponentRegistry.get_registered_components()
        }
        external_types = {
            type: f"{type} (E)" for type in self.list_result_type_names(self.repo_id)
        }
        return {**python_types, **internal_types, **external_types}

    def configure(self, config: AgentConfig) -> AgentConfig:
        """Widgets to configure the agent."""
        model_options = [
            model
            for model in get_args(KnownModelName.__value__)
            if model.startswith("openai")
        ]
        model = st.selectbox(
            "Select a model",
            model_options,
            index=model_options.index(config.model),
        )

        result_type_options = self.list_result_type_options()
        result_type = st.multiselect(
            "Result type (**P**: Python, **I**: Internal, **E**: External)",
            options=result_type_options,
            format_func=lambda x: result_type_options[x],
            default=config.result_type,
        )
        st.write("**System prompt**")
        system_prompt = code_editor(
            config.system_prompt,
            lang="markdown",
            response_mode="debounce",
            options={"wrap": True},
        )["text"]
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=config.model_settings.get("temperature", 1.0)
            if config.model_settings
            else 1.0,
        )
        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=config.model_settings.get("top_p", 1.0)
            if config.model_settings
            else 1.0,
        )
        model_settings = {
            "temperature": temperature,
            "top_p": top_p,
        }
        retries = st.number_input(
            "Retries", min_value=0, max_value=100, value=config.retries
        )
        result_tool_name = st.text_input(
            "Result tool name", value=config.result_tool_name
        )
        result_tool_description = st.text_input(
            "Result tool description", value=config.result_tool_description
        )
        result_retries = st.number_input(
            "Result retries", min_value=0, max_value=100, value=config.retries
        )
        list_known_tools = self.list_function_names(self.repo_id)
        default_known_tools = [
            tool for tool in config.known_tools if tool in list_known_tools
        ]
        known_tools = st.multiselect(
            "Known tools", options=list_known_tools, default=default_known_tools
        )
        hf_tools = st.text_area("HF tools", value="\n".join(config.hf_tools))
        mcp_servers = st.text_area("MCP servers", value="\n".join(config.mcp_servers))
        defer_model_check = st.toggle(
            "Defer model check", value=config.defer_model_check
        )
        end_strategy = st.selectbox("End strategy", ["early", "exhaustive"])
        instrument = st.toggle("Instrument", value=config.instrument)
        name = st.text_input("Name", value=config.name)
        name = name.replace(" ", "_")

        return AgentConfig(
            model=model,
            result_type=result_type,
            system_prompt=system_prompt or config.system_prompt,
            model_settings=model_settings,
            retries=retries,
            result_tool_name=result_tool_name,
            result_tool_description=result_tool_description,
            result_retries=result_retries,
            known_tools=known_tools,
            hf_tools=[x for x in hf_tools.split("\n") if x],
            mcp_servers=[x for x in mcp_servers.split("\n") if x],
            defer_model_check=defer_model_check,
            end_strategy=end_strategy,
            name=name,
            instrument=instrument,
            repo_id=self.repo_id,
        )

    def save_config(self, config: AgentConfig) -> None:
        """Save the config and trigger a re-download of the files."""
        config.push_to_hub()
        hf_repo = AgentHub(self.repo_id)
        hf_repo.download_files()

    def run(self) -> None:
        """Main function."""
        st.title("Custom Agent")
        agent_name = self.agent_selector(self.repo_id)
        if agent_name:
            config = AgentConfig.from_hub(self.repo_id, agent_name)
        else:  # Initialize a new agent
            config = AgentConfig(model="openai:gpt-4o", repo_id=self.repo_id)
        new_config = self.configure(config)
        if st.button(
            "Save", on_click=self.save_config, args=(new_config,)
        ):  # pragma: no cover
            st.success("Agent pushed to the hub.")
