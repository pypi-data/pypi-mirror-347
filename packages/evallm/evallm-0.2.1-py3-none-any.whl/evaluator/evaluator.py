from __future__ import annotations

from .connection.base import BaseConnection
from .connection.ollama import OllamaConnection
from .connection.openai import OpenAIConnection

from .tasks.base import BaseTask
from .tasks.summarization import Summarization
from .tasks.nli import NLI
from .tasks.pairwise import Pairwise
from .tasks.translation import Translation
from .tasks.generic import Generic

from .exceptions import BaseConnectionError, InvalidTaskError, ConnectionTypeError

from beartype.typing import Any

CONNECTION_MAP = {
    "ollama": OllamaConnection,
    "openai": OpenAIConnection,
}

TASK_MAP = {
    "summarization": Summarization,
    "nli": NLI,
    "pairwise": Pairwise,
    "translation": Translation,
    "generic": Generic,
}


class LLMEvaluator:
    """
    Main class for the LLM Evaluator.
    """

    def __init__(
        self,
        *,
        connection: str,
        task: str,
        repetition: int = 1,
        tireness: int = 3,
        **kwargs,
    ):
        if connection not in CONNECTION_MAP:
            raise ConnectionTypeError(f"Invalid connection type: {connection}.")
        if task not in TASK_MAP:
            raise InvalidTaskError(f"Invalid task type: {task}.")

        # Initialize the connection to the LLM
        # TODO : Add error handling for connection issues
        try:
            self.connection: BaseConnection = CONNECTION_MAP[connection](**kwargs)
        except BaseConnectionError as e:
            raise e

        # Initialize the evaluator for the specified task
        self.evaluator: BaseTask = TASK_MAP[task](
            connection=self.connection,
            repetition=repetition,
            timeout=tireness,
            **kwargs,
        )

    def evaluate(
        self,
        custom_prompt: str | None = None,
        *args,
        **kwargs,
    ) -> Any:
        """
        Evaluate the model with the given prompt.
        """
        # Evaluate the model with the given prompt
        # TODO : Add error handling for evaluation issues
        try:
            result = self.evaluator.perform(
                custom_prompt=custom_prompt, *args, **kwargs
            )
            return result

        except Exception as e:
            raise e
