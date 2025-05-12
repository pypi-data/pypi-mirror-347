import instructor
import anthropic
from anthropic.types import MessageParam # For prompt formatting
# Import specific errors if needed
from anthropic import APIError, RateLimitError

from karo.providers.base_provider import BaseProvider
from karo.schemas.base_schemas import BaseOutputSchema
from pydantic import BaseModel, Field, SecretStr, ValidationError
from typing import Any, Type, List, Dict, Optional, Union
import os
import logging
import json # For tool result content

logger = logging.getLogger(__name__)

from typing import Literal # Import Literal

class AnthropicProviderConfig(BaseModel):
    type: Literal["anthropic"] = Field("anthropic", description="Discriminator field for provider type.")
    api_key: Optional[SecretStr] = Field(None, description="Anthropic API key. Uses ANTHROPIC_API_KEY env var if None.")
    model: str = Field(..., description="Anthropic model name (e.g., 'claude-3-opus-20240229', 'claude-3-sonnet-20240229').")
    # Add other Anthropic client params like base_url, timeout if needed

class AnthropicProvider(BaseProvider):
    """
    Karo provider implementation for Anthropic Claude models.
    Uses the 'anthropic' library and 'instructor' for schema enforcement.
    """
    client: Any # Stores the instructor-patched client
    raw_client: anthropic.Anthropic # Store raw client for potential direct use
    model_name: str

    def __init__(self, config: AnthropicProviderConfig):
        """Initializes the Anthropic provider."""
        if not isinstance(config, AnthropicProviderConfig):
            raise TypeError("config must be an instance of AnthropicProviderConfig")

        self.config = config
        self.model_name = config.model
        # Anthropic client primarily uses env var ANTHROPIC_API_KEY or direct api_key param
        api_key_value = config.api_key.get_secret_value() if config.api_key else None # os.getenv("ANTHROPIC_API_KEY") is handled by client

        try:
            # Initialize the raw Anthropic client
            self.raw_client = anthropic.Anthropic(api_key=api_key_value)
            # Patch the client with instructor
            self.client = instructor.from_anthropic(self.raw_client)
            logger.info(f"AnthropicProvider initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}", exc_info=True)
            raise ConnectionError(f"Could not configure Anthropic client: {e}") from e

    def get_client(self) -> Any:
        """Returns the underlying, instructor-patched Anthropic client instance."""
        return self.client

    def get_model_name(self) -> str:
        """Returns the specific Anthropic model name being used."""
        return self.model_name

    def _format_prompt_for_anthropic(self, prompt: List[Dict[str, str]]) -> tuple[Optional[str], List[MessageParam]]:
        """
        Converts Karo's prompt format to Anthropic's format (system prompt + messages list).
        Handles role mapping and tool message formatting.
        """
        system_prompt_content: Optional[str] = None
        messages: List[MessageParam] = []

        # First, extract the system message if present
        for message in prompt:
            if message.get("role") == "system":
                system_prompt_content = message.get("content", "")
                break
        
        # Process all non-system messages
        for message in prompt:
            role = message.get("role")
            content = message.get("content", "")
            
            if role == "system":
                # Already handled above
                continue
            elif role == "user":
                messages.append({"role": "user", "content": content})
            elif role == "assistant":
                assistant_parts = []
                if content:
                    assistant_parts.append({"type": "text", "text": content})
                if assistant_parts:
                    messages.append({"role": "assistant", "content": assistant_parts})
            elif role == "tool":
                tool_call_id = message.get("tool_call_id")
                if tool_call_id and content:
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_call_id,
                                "content": content
                            }
                        ]
                    })
        
        # Ensure we have at least one message for Anthropic API
        if not messages:
            # Add a default user message if no messages were processed
            messages.append({"role": "user", "content": "Hello"})
            logger.warning("No valid messages found in prompt. Adding a default user message.")
        
        return system_prompt_content, messages

    def generate_response(
        self,
        prompt: List[Dict[str, str]],
        output_schema: Type[BaseOutputSchema],
        # Removed tools and tool_choice parameters
        **kwargs
    ) -> BaseOutputSchema: # Return type is now always the validated schema
        """Generates a response from the Anthropic LLM, enforcing the output schema."""
        try:
            system_prompt, messages = self._format_prompt_for_anthropic(prompt)
            # Removed call to _format_tools_for_anthropic

            # Prepare API call arguments
            api_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1024), # Anthropic requires max_tokens
                # Pass other standard Anthropic params from kwargs if present
                **{k: v for k, v in kwargs.items() if k in ["temperature", "top_p", "top_k"]}
            }
            if system_prompt:
                api_kwargs["system"] = system_prompt
            # Removed logic adding tools to api_kwargs

            # Use instructor-patched client
            # Instructor handles response_model validation
            response = self.client.messages.create(
                 response_model=output_schema, # Always enforce the output schema
                 **api_kwargs
            )

            # Instructor should return the validated schema instance
            return response

        except ValidationError as e:
             logger.error(f"Anthropic response validation error: {e}", exc_info=True)
             raise
        except (APIError, RateLimitError) as e:
            logger.error(f"Anthropic API Error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error during Anthropic API call: {e}", exc_info=True)
            raise