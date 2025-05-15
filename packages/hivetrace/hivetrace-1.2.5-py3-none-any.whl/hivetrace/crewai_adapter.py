import functools
import uuid
from typing import Any, Callable, Dict, Optional

from crewai import Agent, Crew, Task


class CrewAIAdapter:
    """
    Integration adapter for monitoring CrewAI agents with Hivetrace.
    """

    def __init__(
        self,
        hivetrace,
        application_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        """
        Initialize the CrewAI adapter.

        Parameters:
        - hivetrace: The hivetrace instance for logging
        - application_id: ID of the application in Hivetrace
        - user_id: ID of the user in the conversation
        - session_id: ID of the session in the conversation
        - agent_id_mapping: Mapping from agent role names to their IDs
        """
        self.trace = hivetrace
        self.application_id = application_id
        self.user_id = user_id
        self.session_id = session_id
        self.agent_id_mapping = agent_id_mapping if agent_id_mapping is not None else {}
        self.async_mode = self.trace.async_mode
        self.agents_info = {}

    def _get_agent_mapping(self, role: str) -> Dict[str, str]:
        """
        Gets agent ID and description from the mapping.
        """
        if self.agent_id_mapping and role in self.agent_id_mapping:
            mapping_data = self.agent_id_mapping[role]
            if isinstance(mapping_data, dict):
                return {
                    "id": mapping_data.get("id", str(uuid.uuid4())),
                    "description": mapping_data.get("description", ""),
                }
            elif isinstance(mapping_data, str):
                return {"id": mapping_data, "description": ""}
        return {"id": str(uuid.uuid4()), "description": ""}

    def _prepare_and_log(
        self,
        log_method_name_stem: str,
        is_async: bool,
        message_content: Optional[str] = None,
        tool_call_details: Optional[Dict[str, Any]] = None,
        additional_params_from_caller: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Helper method to prepare parameters and log to Hivetrace.
        """
        final_additional_params = additional_params_from_caller or {}
        final_additional_params.setdefault("user_id", self.user_id)
        final_additional_params.setdefault("session_id", self.session_id)

        log_kwargs = {
            "application_id": self.application_id,
            "additional_parameters": final_additional_params,
        }

        if log_method_name_stem in ["input", "output"]:
            if message_content is None:
                print(f"Warning: message_content is None for {log_method_name_stem}")
                return
            log_kwargs["message"] = message_content
        elif log_method_name_stem == "function_call":
            if tool_call_details is None:
                print("Warning: tool_call_details is None for function_call")
                return
            log_kwargs.update(tool_call_details)
        else:
            print(f"Error: Unsupported log_method_name_stem: {log_method_name_stem}")
            return

        method_to_call_name = f"{log_method_name_stem}{'_async' if is_async else ''}"

        try:
            actual_log_method = getattr(self.trace, method_to_call_name)
            if is_async:
                import asyncio

                asyncio.create_task(actual_log_method(**log_kwargs))
            else:
                actual_log_method(**log_kwargs)
        except AttributeError:
            print(f"Error: Hivetrace object does not have method {method_to_call_name}")
        except Exception as e:
            print(f"Error logging {log_method_name_stem} to Hivetrace: {e}")

    async def input_async(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Asynchronously logs user input to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        self._prepare_and_log(
            "input",
            True,
            message_content=message,
            additional_params_from_caller=additional_params,
        )

    def input(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Synchronously logs user input to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        self._prepare_and_log(
            "input",
            False,
            message_content=message,
            additional_params_from_caller=additional_params,
        )

    async def output_async(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Asynchronously logs agent output to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        processed_params = additional_params or {}
        if "agents" in processed_params and processed_params["agents"]:
            agent_uuid = next(iter(processed_params["agents"]))
            agent_info_val = processed_params["agents"][agent_uuid]
            if isinstance(agent_info_val, dict) and "name" in agent_info_val:
                processed_params["agents"] = {
                    agent_uuid: {
                        "name": agent_info_val["name"],
                        "description": agent_info_val.get("description", ""),
                    }
                }

        self._prepare_and_log(
            "output",
            True,
            message_content=message,
            additional_params_from_caller=processed_params,
        )

    def output(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Synchronously logs agent output to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        processed_params = additional_params or {}
        if "agents" in processed_params and processed_params["agents"]:
            agent_uuid = next(iter(processed_params["agents"]))
            agent_info_val = processed_params["agents"][agent_uuid]
            if isinstance(agent_info_val, dict) and "name" in agent_info_val:
                processed_params["agents"] = {
                    agent_uuid: {
                        "name": agent_info_val["name"],
                        "description": agent_info_val.get("description", ""),
                    }
                }

        self._prepare_and_log(
            "output",
            False,
            message_content=message,
            additional_params_from_caller=processed_params,
        )

    def _monitor_function_call(
        self, func: Callable, func_name: str, agent_role: str
    ) -> Callable:
        """
        Wraps a tool function to monitor its calls, attributing to the specified agent_role.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_list_str = [str(arg) for arg in args]
            kwargs_list_str = [f"{k}={v}" for k, v in kwargs.items()]
            all_args_str = ", ".join(args_list_str + kwargs_list_str)

            result = func(*args, **kwargs)

            agent_mapping = self._get_agent_mapping(agent_role)
            mapped_agent_id = agent_mapping["id"]
            mapped_agent_description = agent_mapping["description"]

            tool_call_id = str(uuid.uuid4())

            tool_call_details = {
                "tool_call_id": tool_call_id,
                "func_name": func_name,
                "func_args": all_args_str,
                "func_result": str(result),
            }

            additional_params_for_log = {
                "agents": {
                    mapped_agent_id: {
                        "name": agent_role,
                        "description": mapped_agent_description,
                    }
                },
            }

            self._prepare_and_log(
                "function_call",
                self.async_mode,
                tool_call_details=tool_call_details,
                additional_params_from_caller=additional_params_for_log,
            )
            return result

        return wrapper

    def _wrap_tool(self, tool: Any, agent_role: str) -> Any:
        """
        Wraps a tool's _run method to monitor its calls, passing the agent_role.
        """
        if hasattr(tool, "_run") and callable(tool._run):
            tool._run = self._monitor_function_call(
                tool._run,
                tool.name if hasattr(tool, "name") else "unknown_tool",
                agent_role,
            )
        return tool

    def agent_callback(self, message: Any) -> None:
        """
        Callback for agent actions.
        """
        message_text: str
        additional_params_for_log: Dict[str, Any]

        if isinstance(message, dict) and message.get("type") == "agent_thought":
            agent_id_from_message = message.get("agent_id")
            role = message.get("role", "")

            agent_mapping = self._get_agent_mapping(role)
            final_agent_id = agent_id_from_message or agent_mapping.get("id")

            agent_info_details = {
                "name": message.get("agent_name", role),
                "description": agent_mapping.get(
                    "description", message.get("agent_description", "Agent thought")
                ),
            }
            message_text = f"Thought from agent {role}: {message['thought']}"
            additional_params_for_log = {"agents": {final_agent_id: agent_info_details}}
        else:
            message_text = str(message)
            additional_params_for_log = {"agents": self.agents_info}

        self._prepare_and_log(
            "input",
            self.async_mode,
            message_content=message_text,
            additional_params_from_caller=additional_params_for_log,
        )

    def task_callback(self, message: Any) -> None:
        """
        Handler for task messages.
        Formats and logs task messages to Hivetrace.
        """
        message_text = ""
        agent_info_for_log = {}

        if hasattr(message, "__dict__"):
            details = []
            for key, value in message.__dict__.items():
                if key not in [
                    "__dict__",
                    "__weakref__",
                    "callback",
                ]:
                    details.append(f"{key}: {value}")
                    if key == "agent":
                        current_agent_role = ""
                        if isinstance(value, str):
                            current_agent_role = value
                        elif hasattr(value, "role"):
                            current_agent_role = value.role

                        if current_agent_role:
                            agent_mapping = self._get_agent_mapping(current_agent_role)
                            mapped_id = agent_mapping["id"]
                            agent_info_for_log = {
                                mapped_id: {
                                    "name": current_agent_role,
                                    "description": agent_mapping["description"]
                                    or (
                                        getattr(value, "goal", "")
                                        if hasattr(value, "goal")
                                        else "Task agent"
                                    ),
                                }
                            }
            message_text = f"[Task] {' | '.join(details)}"
        else:
            message_text = f"[Task] {str(message)}"

        self._prepare_and_log(
            "output",
            self.async_mode,
            message_content=message_text,
            additional_params_from_caller={"agents": agent_info_for_log},
        )

    def _wrap_agent(self, agent: Agent) -> Agent:
        """
        Wraps an agent to monitor its actions.
        """
        agent_mapping = self._get_agent_mapping(agent.role)
        agent_id_for_monitored_agent = agent_mapping["id"]

        agent_props = agent.__dict__.copy()

        original_tools = getattr(agent, "tools", [])
        wrapped_tools = [self._wrap_tool(tool, agent.role) for tool in original_tools]
        agent_props["tools"] = wrapped_tools

        for key_to_remove in ["id", "agent_executor", "agent_ops_agent_id"]:
            if key_to_remove in agent_props:
                del agent_props[key_to_remove]

        monitored_agent = self.MonitoredAgent(
            adapter_instance=self,
            callback_func=self.agent_callback,
            agent_id=agent_id_for_monitored_agent,
            **agent_props,
        )

        return monitored_agent

    class MonitoredAgent(Agent):
        model_config = {"extra": "allow"}

        def __init__(
            self,
            adapter_instance: Any,
            callback_func: Callable[[Any], None],
            agent_id: str,
            **kwargs,
        ):
            if "id" in kwargs:
                del kwargs["id"]

            super().__init__(**kwargs)
            self._adapter_instance = adapter_instance
            self.callback_func = callback_func
            self.agent_id = agent_id
            self._last_thought = None

        def _execute_task(self, task: Task) -> str:
            """
            Override _execute_task to capture thoughts
            """
            result = super()._execute_task(task)

            if hasattr(self, "_last_thought") and self._last_thought:
                agent_role = self.role if hasattr(self, "role") else "UnknownRole"
                agent_goal = self.goal if hasattr(self, "goal") else "Agent thought"

                self.callback_func(
                    {
                        "type": "agent_thought",
                        "agent_id": self.agent_id,
                        "role": agent_role,
                        "thought": self._last_thought,
                        "agent_name": agent_role,
                        "agent_description": agent_goal,
                    }
                )
                self._last_thought = None
            return result

        def _think(self, thought: str) -> None:
            """
            Override _think to capture thoughts
            """
            self._last_thought = thought

            if hasattr(self, "callback_func"):
                agent_role = self.role if hasattr(self, "role") else "UnknownRole"
                agent_goal = self.goal if hasattr(self, "goal") else "Agent thought"

                self.callback_func(
                    {
                        "type": "agent_thought",
                        "agent_id": self.agent_id,
                        "role": agent_role,
                        "thought": thought,
                        "agent_name": agent_role,
                        "agent_description": agent_goal,
                    }
                )
            super()._think(thought)

    def _wrap_task(self, task: Task) -> Task:
        """
        Adds monitoring to the task.
        Wraps existing task callbacks to add logging.
        """
        original_callback = task.callback

        def combined_callback(message):
            self.task_callback(message)
            if original_callback:
                original_callback(message)

        task.callback = combined_callback
        return task

    def wrap_crew(self, crew: Crew) -> Crew:
        """
        Adds monitoring to the existing CrewAI crew.
        Wraps all agents and tasks in the crew, as well as the kickoff methods.
        """

        current_agents_info = {}
        for agent_instance in crew.agents:
            if hasattr(agent_instance, "role"):
                agent_mapping = self._get_agent_mapping(agent_instance.role)
                agent_id = agent_mapping["id"]
                description = agent_mapping["description"] or getattr(
                    agent_instance, "goal", ""
                )
                current_agents_info[agent_id] = {
                    "name": agent_instance.role,
                    "description": description,
                }
        self.agents_info = current_agents_info

        wrapped_agents = [self._wrap_agent(agent) for agent in crew.agents]
        wrapped_tasks = [self._wrap_task(task) for task in crew.tasks]

        monitored_crew_instance = self.MonitoredCrew(
            original_crew_agents=wrapped_agents,
            original_crew_tasks=wrapped_tasks,
            original_crew_verbose=crew.verbose,
            manager_llm=getattr(crew, "manager_llm", None),
            memory=getattr(crew, "memory", None),
            process=getattr(crew, "process", None),
            config=getattr(crew, "config", None),
            adapter=self,
        )
        return monitored_crew_instance

    class MonitoredCrew(Crew):
        model_config = {"extra": "allow"}

        def __init__(
            self,
            adapter,
            original_crew_agents,
            original_crew_tasks,
            original_crew_verbose,
            **kwargs,
        ):
            super().__init__(
                agents=original_crew_agents,
                tasks=original_crew_tasks,
                verbose=original_crew_verbose,
                **kwargs,
            )
            self._adapter = adapter

        def _log_kickoff_result(self, result: Any):
            if result:
                final_message = f"[Final Result] {str(result)}"
                agent_info_for_log = {}
                for agent in self.agents:
                    if hasattr(agent, "agent_id") and hasattr(agent, "role"):
                        agent_info_for_log[agent.agent_id] = {
                            "name": agent.role,
                            "description": getattr(agent, "goal", ""),
                        }

                additional_params = {
                    "agents": agent_info_for_log,
                }
                self._adapter._prepare_and_log(
                    "output",
                    self._adapter.async_mode,
                    message_content=final_message,
                    additional_params_from_caller=additional_params,
                )

        def kickoff(self, *args, **kwargs):
            result = super().kickoff(*args, **kwargs)
            self._log_kickoff_result(result)
            return result

        async def kickoff_async(self, *args, **kwargs):
            if not hasattr(super(), "kickoff_async"):
                raise NotImplementedError(
                    "Async kickoff is not supported by the underlying crew's superclass"
                )

            result = await super().kickoff_async(*args, **kwargs)
            self._log_kickoff_result(result)
            return result


def track_crew(
    hivetrace,
    application_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    agent_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
):
    """
    Decorator for tracking the CrewAI crew.
    Creates an adapter and applies it to the crew setup function.

    Parameters:
    - hivetrace: The hivetrace instance for logging
    - application_id: ID of the application in Hivetrace
    - user_id: ID of the user in Hivetrace
    - session_id: ID of the session in Hivetrace
    - agent_id_mapping: Mapping from agent role names to their metadata dict with 'id' and 'description'
                         e.g. {"Content Planner": {"id": "planner-123", "description": "Creates content plans"}}
    """
    if callable(hivetrace):
        raise ValueError(
            "track_crew requires at least the hivetrace parameter. "
            "Use @track_crew(hivetrace=your_hivetrace_instance)"
        )

    adapter = CrewAIAdapter(
        hivetrace=hivetrace,
        application_id=application_id,
        user_id=user_id,
        session_id=session_id,
        agent_id_mapping=agent_id_mapping if agent_id_mapping is not None else {},
    )

    def decorator(crew_setup_func):
        @functools.wraps(crew_setup_func)
        def wrapper(*args, **kwargs):
            crew = crew_setup_func(*args, **kwargs)
            return adapter.wrap_crew(crew)

        return wrapper

    return decorator
