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
        application_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        agent_description: Optional[str] = None,
    ):
        """
        Initialize the CrewAI adapter.
        """
        self.trace = hivetrace
        self.application_id = application_id or "default_application"
        self.user_id = user_id or "default_user"
        self.session_id = session_id or "default_session"
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = agent_name or "Default Agent"
        self.agent_description = agent_description or "Default Agent Description"
        self.async_mode = self.trace.async_mode
        self.original_kickoff = None
        self.original_kickoff_async = None
        self.agents_info = {}

    def _get_agent_info(self, agent: Agent) -> Dict[str, Any]:
        """
        Gets agent information for additional_parameters.
        """
        info = {}
        if hasattr(agent, "role"):
            info["name"] = agent.role
        if hasattr(agent, "goal"):
            info["description"] = agent.goal
        return info

    async def input_async(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Asynchronously logs user input to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
                "agents": {
                    self.agent_id: {
                        "name": self.agent_name,
                        "description": self.agent_description,
                    }
                },
            }
        )

        try:
            await self.trace.input_async(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging input to Hivetrace: {e}")

    def input(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Synchronously logs user input to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        try:
            self.trace.input(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging input to Hivetrace: {e}")

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

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        if "agents" in params and params["agents"]:
            agent_uuid = next(iter(params["agents"]))
            agent_info = params["agents"][agent_uuid]
            if "name" in agent_info:
                params["agents"] = {
                    agent_uuid: {
                        "name": agent_info["name"],
                        "description": agent_info.get("description", ""),
                    }
                }

        try:
            await self.trace.output_async(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging output to Hivetrace: {e}")

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

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        if "agents" in params and params["agents"]:
            agent_uuid = next(iter(params["agents"]))
            agent_info = params["agents"][agent_uuid]
            if "name" in agent_info:
                params["agents"] = {
                    agent_uuid: {
                        "name": agent_info["name"],
                        "description": agent_info.get("description", ""),
                    }
                }

        try:
            self.trace.output(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging output to Hivetrace: {e}")

    def _monitor_function_call(self, func: Callable, func_name: str) -> Callable:
        """
        Wraps a tool function to monitor its calls.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            if args:
                args_str = ", ".join([str(arg) for arg in args]) + (
                    f", {args_str}" if args_str else ""
                )

            result = func(*args, **kwargs)

            if self.async_mode:
                import asyncio

                asyncio.create_task(
                    self.trace.function_call_async(
                        application_id=self.application_id,
                        tool_call_id=str(uuid.uuid4()),
                        func_name=func_name,
                        func_args=args_str,
                        func_result=str(result),
                        additional_parameters={
                            "session_id": self.session_id,
                            "user_id": self.user_id,
                            "agents": {
                                self.agent_id: {
                                    "name": func_name,
                                    "description": "Function call",
                                }
                            },
                        },
                    )
                )
            else:
                self.trace.function_call(
                    application_id=self.application_id,
                    tool_call_id=str(uuid.uuid4()),
                    func_name=func_name,
                    func_args=args_str,
                    func_result=str(result),
                    additional_parameters={
                        "session_id": self.session_id,
                        "user_id": self.user_id,
                        "agents": {
                            self.agent_id: {
                                "name": func_name,
                                "description": "Function call",
                            }
                        },
                    },
                )

            return result

        return wrapper

    def _wrap_tool(self, tool: Any) -> Any:
        """
        Wraps a tool function to monitor its calls.
        """
        if hasattr(tool, "_run"):
            tool._run = self._monitor_function_call(tool._run, tool.name)
        return tool

    def agent_callback(self, message: Any) -> None:
        """
        Handler for agent messages.
        Formats and logs agent messages to Hivetrace.
        """
        try:
            print(f"Agent callback received message: {message}")
            print(f"Message type: {type(message)}")
            print(f"Message dir: {dir(message)}")

            agent_name = None
            agent_info = {}

            if hasattr(message, "agent"):
                print(f"Message has agent: {message.agent}")
                print(f"Agent dir: {dir(message.agent)}")
                agent_name = message.agent.role

                if hasattr(message.agent, "_agent_id"):
                    print(f"Agent has _agent_id: {message.agent._agent_id}")
                    agent_info = {
                        self.agent_id: {
                            "name": message.agent.role,
                            "description": getattr(message.agent, "goal", ""),
                        }
                    }
                    print(f"Agent info: {agent_info}")
                else:
                    print("Agent does not have _agent_id")

            message_text = ""
            if hasattr(message, "__dict__"):
                message_type = message.__class__.__name__
                details = []
                for key, value in message.__dict__.items():
                    if key not in ["__dict__", "__weakref__"]:
                        details.append(f"{key}: {value}")
                message_text = f"[Agent {agent_name}] {' | '.join(details)}"
            else:
                message_text = f"[Agent {agent_name}] {str(message)}"

            print(f"Final message text: {message_text}")
            print(f"Final agent info: {agent_info}")

            if self.async_mode:
                import asyncio

                asyncio.create_task(
                    self.output_async(
                        message_text,
                        additional_params={
                            "session_id": self.session_id,
                            "user_id": self.user_id,
                            "agents": agent_info,
                        },
                    )
                )
            else:
                self.output(
                    message_text,
                    additional_params={
                        "session_id": self.session_id,
                        "user_id": self.user_id,
                        "agents": agent_info,
                    },
                )
        except Exception as e:
            print(f"Error in agent_callback: {str(e)}")
            error_text = f"[Agent] Error logging: {str(e)} | Object: {message}"
            if self.async_mode:
                import asyncio

                asyncio.create_task(self.output_async(error_text))
            else:
                self.output(error_text)

    def task_callback(self, message: Any) -> None:
        """
        Handler for task messages.
        Formats and logs task messages to Hivetrace.
        """
        try:
            message_text = ""
            task_info = {}
            agent_info = {}

            if hasattr(message, "__dict__"):
                details = []
                for key, value in message.__dict__.items():
                    if key not in ["__dict__", "__weakref__"]:
                        details.append(f"{key}: {value}")
                        if key == "description":
                            task_info["description"] = value
                        elif key == "name":
                            task_info["name"] = value
                        elif key == "agent":
                            print(f"Found agent in message: {value}")
                            if isinstance(value, str):
                                agent_info = {
                                    self.agent_id: {
                                        "name": value,
                                        "description": "Save the money",
                                    }
                                }
                            elif hasattr(value, "role"):
                                agent_info = {
                                    self.agent_id: {
                                        "name": value.role,
                                        "description": getattr(value, "goal", ""),
                                    }
                                }
                            print(f"Created agent_info: {agent_info}")
                message_text = f"[Task] {' | '.join(details)}"
            else:
                message_text = f"[Task] {str(message)}"

            print(f"Final agent_info: {agent_info}")

            if self.async_mode:
                import asyncio

                asyncio.create_task(
                    self.output_async(
                        message_text,
                        additional_params={
                            "task": task_info,
                            "agents": agent_info,
                            "session_id": self.session_id,
                            "user_id": self.user_id,
                        },
                    )
                )
            else:
                self.output(
                    message_text,
                    additional_params={
                        "task": task_info,
                        "agents": agent_info,
                        "session_id": self.session_id,
                        "user_id": self.user_id,
                    },
                )
        except Exception as e:
            print(f"Error in task_callback: {str(e)}")
            error_text = f"[Task] Error logging: {str(e)} | Object: {message}"
            if self.async_mode:
                import asyncio

                asyncio.create_task(self.output_async(error_text))
            else:
                self.output(error_text)

    def _wrap_agent(self, agent: Agent) -> Agent:
        """
        Adds monitoring to the agent.
        Wraps existing agent callbacks to add logging.
        """
        print(f"Wrapping agent: {agent.role}")

        agent_id = self.agent_id
        print(f"Using agent_id: {agent_id}")
        agent._agent_id = agent_id

        if hasattr(agent, "tools"):
            agent.tools = [self._wrap_tool(tool) for tool in agent.tools]

        class MonitoredAgent(Agent):
            model_config = {"extra": "allow"}

            def __init__(
                self, callback_func: Callable[[Any], None], agent_id: str, **kwargs
            ):
                super().__init__(**kwargs)
                self._callback = callback_func
                self._step_callback = callback_func
                self._agent_id = agent_id
                print(f"MonitoredAgent initialized with agent_id: {agent_id}")

        monitored_agent = MonitoredAgent(
            callback_func=self.agent_callback,
            agent_id=agent_id,
            role=agent.role,
            goal=agent.goal,
            backstory=agent.backstory,
            llm=agent.llm,
            tools=agent.tools,
            verbose=agent.verbose,
            allow_delegation=agent.allow_delegation,
        )

        print(f"Created monitored agent with id: {monitored_agent._agent_id}")
        for attr in dir(agent):
            if not attr.startswith("_"):
                try:
                    setattr(monitored_agent, attr, getattr(agent, attr))
                except (AttributeError, ValueError):
                    pass

        return monitored_agent

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

        class MonitoredCrew(Crew):
            model_config = {"extra": "allow"}

            def __init__(self, original_crew: Crew, adapter):
                super().__init__(
                    agents=original_crew.agents,
                    tasks=original_crew.tasks,
                    verbose=original_crew.verbose,
                )
                self._adapter = adapter
                self._original_kickoff = original_crew.kickoff
                self._original_kickoff_async = getattr(
                    original_crew, "kickoff_async", None
                )

            def kickoff(self, *args, **kwargs):
                result = self._original_kickoff(*args, **kwargs)

                if result:
                    final_message = f"[Final Result] {str(result)}"

                    agent_info = {}
                    if self.agents and len(self.agents) > 0:
                        agent = self.agents[0]
                        agent_info = {
                            self._adapter.agent_id: {
                                "name": self._adapter.agent_name,
                                "description": self._adapter.agent_description,
                            }
                        }

                    if self._adapter.async_mode:
                        import asyncio

                        asyncio.create_task(
                            self._adapter.output_async(
                                final_message,
                                additional_params={
                                    "session_id": self._adapter.session_id,
                                    "user_id": self._adapter.user_id,
                                    "agents": agent_info,
                                },
                            )
                        )
                    else:
                        self._adapter.output(
                            final_message,
                            additional_params={
                                "session_id": self._adapter.session_id,
                                "user_id": self._adapter.user_id,
                                "agents": agent_info,
                            },
                        )

                return result

            async def kickoff_async(self, *args, **kwargs):
                if not self._original_kickoff_async:
                    raise NotImplementedError(
                        "Async kickoff is not supported by the original crew"
                    )

                result = await self._original_kickoff_async(*args, **kwargs)

                if result:
                    final_message = f"[Final Result] {str(result)}"

                    agent_info = {}
                    if self.agents and len(self.agents) > 0:
                        agent = self.agents[0]
                        agent_info = {
                            self._adapter.agent_id: {
                                "name": self._adapter.agent_name,
                                "description": self._adapter.agent_description,
                            }
                        }

                    if self._adapter.async_mode:
                        await self._adapter.output_async(
                            final_message,
                            additional_params={
                                "session_id": self._adapter.session_id,
                                "user_id": self._adapter.user_id,
                                "agents": agent_info,
                            },
                        )
                    else:
                        self._adapter.output(
                            final_message,
                            additional_params={
                                "session_id": self._adapter.session_id,
                                "user_id": self._adapter.user_id,
                                "agents": agent_info,
                            },
                        )

                return result

        crew.agents = [self._wrap_agent(agent) for agent in crew.agents]
        crew.tasks = [self._wrap_task(task) for task in crew.tasks]

        monitored_crew = MonitoredCrew(crew, self)

        return monitored_crew

    def track_crew(self, crew_setup_func: Callable) -> Callable:
        """
        Decorator for tracking the crew.
        Wraps the crew setup function to add monitoring.
        """

        @functools.wraps(crew_setup_func)
        def wrapper(*args, **kwargs):
            crew = crew_setup_func(*args, **kwargs)
            return self.wrap_crew(crew)

        return wrapper


def track_crew(
    hivetrace,
    application_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    agent_description: Optional[str] = None,
):
    """
    Decorator for tracking the CrewAI crew.
    Creates an adapter and applies it to the crew setup function.
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
        agent_id=agent_id,
        agent_name=agent_name,
        agent_description=agent_description,
    )

    def decorator(crew_setup_func):
        return adapter.track_crew(crew_setup_func)

    return decorator
