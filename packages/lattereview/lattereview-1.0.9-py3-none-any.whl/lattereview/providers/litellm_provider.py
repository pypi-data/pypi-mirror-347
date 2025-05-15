"""LiteLLM API provider implementation with comprehensive error handling and type safety."""

import base64
import inspect
from typing import Optional, List, Dict, Any, Union, Tuple, Type
import json
from pydantic import BaseModel, create_model
import litellm
from litellm import acompletion, completion_cost
from .base_provider import BaseProvider, ProviderError, ResponseError, InvalidResponseFormatError

litellm.drop_params = True  # Drop unsupported parameters from the API
litellm.enable_json_schema_validation = True  # Enable client-side JSON schema validation


class LiteLLMProvider(BaseProvider):
    provider: str = "LiteLLM"
    model: str = "gpt-4o-mini"
    custom_llm_provider: Optional[str] = None
    response_format_class: Optional[Any] = None

    def __init__(self, custom_llm_provider: Optional[str] = None, **data: Any) -> None:
        """Initialize the LiteLLM provider."""
        data_with_provider = {**data}
        if custom_llm_provider:
            data_with_provider["custom_llm_provider"] = custom_llm_provider

        super().__init__(**data_with_provider)

    def set_response_format(self, response_format: Dict[str, Any]) -> None:
        """Set the response format for JSON responses."""
        try:
            if not response_format:
                raise InvalidResponseFormatError("Response format cannot be empty")
            if isinstance(response_format, dict):
                self.response_format = response_format
                fields = {key: (value, ...) for key, value in response_format.items()}
                self.response_format_class = create_model("ResponseFormat", **fields)
            elif self._check_basemodel_class(response_format):
                self.response_format_class = response_format
        except Exception as e:
            raise ProviderError(f"Error setting response format: {str(e)}")

    async def get_response(
        self,
        input_prompt: str,
        image_path_list: List[str] = [],
        message_list: Optional[List[Dict[str, str]]] = None,
        **kwargs: Any,
    ) -> Tuple[Any, Dict[str, float]]:
        """Get a response from LiteLLM."""
        try:
            message_list = self._prepare_message_list(input_prompt, image_path_list, message_list)
            response = await self._fetch_response(message_list, kwargs)
            txt_response = self._extract_content(response)
            cost = completion_cost(completion_response=response)

            return txt_response, cost
        except Exception as e:
            raise ResponseError(f"Error getting response: {str(e)}")

    async def get_json_response(
        self,
        input_prompt: str,
        image_path_list: List[str] = [],
        message_list: Optional[List[Dict[str, str]]] = None,
        **kwargs: Any,
    ) -> Tuple[Any, Dict[str, float]]:
        """Get a JSON response from LiteLLM using the defined schema."""
        try:
            if not self.response_format_class:
                raise ValueError("Response format is not set")

            message_list = self._prepare_message_list(input_prompt, image_path_list, message_list)

            # Pass response format directly to acompletion
            kwargs["response_format"] = self.response_format_class

            response = await self._fetch_response(message_list, kwargs)
            txt_response = self._extract_content(response)

            # Parse the response as JSON if it's a string
            if isinstance(txt_response, str):
                txt_response = json.loads(txt_response)

            cost = completion_cost(completion_response=response)

            return txt_response, cost
        except Exception as e:
            raise ResponseError(f"Error getting JSON response: {str(e)}")

    def _prepare_message_list(
        self,
        input_prompt: str,
        image_path_list: List[str],
        message_list: Optional[List[Dict[str, str]]] = None,
        system_message: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Prepare the message list for the API call."""
        try:
            if message_list:
                if len(image_path_list) == 0:
                    message_list.append({"role": "user", "content": input_prompt})
                else:
                    content = [{"type": "text", "text": input_prompt}]
                    for image_input in image_path_list:
                        content.append({"type": "image_url", "image_url": {"url": self._encode_image(image_input)}})
                    message_list.append({"role": "user", "content": content})
            else:
                if len(image_path_list) == 0:
                    message_list = [
                        {"role": "system", "content": system_message or self.system_prompt},
                        {"role": "user", "content": input_prompt},
                    ]
                else:
                    content = [{"type": "text", "text": input_prompt}]
                    for image_input in image_path_list:
                        content.append({"type": "image_url", "image_url": {"url": self._encode_image(image_input)}})
                    message_list = [
                        {"role": "system", "content": system_message or self.system_prompt},
                        {"role": "user", "content": content},
                    ]
            return message_list
        except Exception as e:
            raise ProviderError(f"Error preparing message list: {str(e)}")

    async def _fetch_response(self, message_list: List[Dict[str, str]], kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """Fetch the raw response from LiteLLM."""
        try:
            response = await acompletion(
                model=self.model, messages=message_list, custom_llm_provider=self.custom_llm_provider, **(kwargs or {})
            )
            return response
        except Exception as e:
            raise ResponseError(f"Error fetching response: {str(e)}")

    def _extract_content(self, response: Any) -> str:
        """Extract content from the response, handling both direct content and tool calls."""
        try:
            if not response:
                raise ValueError("Empty response received")

            self.last_response = response
            response_message = response.choices[0].message

            # Check for direct content first
            if response_message.content is not None:
                return response_message.content

            # Check for tool calls if content is None
            if hasattr(response_message, "tool_calls") and response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    if tool_call.function.name == "json_tool_call":
                        return tool_call.function.arguments

            raise ValueError("No content or valid tool calls found in response")

        except Exception as e:
            raise ResponseError(f"Error extracting content: {str(e)}")

    # Function to encode the image
    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/{image_path.split('.')[-1]};base64,{base64_image}"

    def _check_basemodel_class(self, arg):
        """Check if the argument is a Pydantic BaseModel class."""
        return inspect.isclass(arg) and issubclass(arg, BaseModel)
