import mimetypes
import os
from typing import List, Tuple, Dict, Any, Union
from pathlib import Path
import base64
from litellm import batch_completion, completion

class LLMInference:
    def __init__(self, model: str, api_key: str = None, tools: List[Dict] = None, **kwargs):
        self.model = model
        self.api_key = api_key
        self.tools = tools
        self.kwargs = kwargs

        if api_key == None:
            self.api_key = os.getenv('LITELLM_API_KEY')

    def _detect_type(self, item: Union[str, Path, dict]) -> Dict[str, Any]:
        """Detect and format different content types with error handling."""
        try:
            # Handle URLs
            if isinstance(item, str) and item.startswith(('http://', 'https://')):
                mime_type, _ = mimetypes.guess_type(item)
                if mime_type and mime_type.startswith('image'):
                    return {"type": "image_url", "image_url": {"url": item}}
                return {"type": "text", "text": item}

            # Handle files
            if isinstance(item, (Path, str)) and os.path.isfile(item):
                path = str(item)
                mime_type, _ = mimetypes.guess_type(path)
                if not mime_type:
                    return {"type": "text", "text": f"[File: {path}]"}

                if mime_type.startswith("image"):
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode('utf-8')
                    return {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{encoded}"}
                    }
                return {"type": "text", "text": f"[File: {path}]"}

            # Handle direct content dictionaries
            if isinstance(item, dict):
                return item

            # Default to text
            return {"type": "text", "text": str(item)}

        except Exception as e:
            return {"type": "text", "text": f"[Error processing item: {str(e)}]"}

    def _format_messages(self, conversation: List[Tuple[str, List[Any]]]) -> List[Dict[str, Any]]:
        """Validate and format conversation with strict type checking."""
        formatted = []
        for role, content_list in conversation:
            if role not in ["user", "assistant", "system", "tool"]:
                raise ValueError(f"Invalid role '{role}'. Must be one of: user, assistant, system, tool")
            
            if not isinstance(content_list, list):
                raise ValueError(f"Content for role '{role}' must be a list of content items")
            
            structured_content = [self._detect_type(c) for c in content_list]
            formatted.append({"role": role, "content": structured_content})
        return formatted

    def _format_batch(self, conversations: List[List[Tuple[str, List[Any]]]]) -> List[List[Dict[str, Any]]]:
        return [self._format_messages(conv) for conv in conversations]

    def _parse_output(self, response: dict) -> Dict[str, Any]:
        """Robust output parsing with error handling and multi-modal support."""
        result = {
            "response": response,
            "content": [],
            "text": "",
            "tool_calls": None,
            "error": None
        }

        # Handle API errors
        if "error" in response:
            result["error"] = response["error"]
            return result

        try:
            choice = response['choices'][0]['message']
            content = choice.get("content", "")

            # Parse multi-modal content
            if isinstance(content, list):
                result["content"] = content
            elif content:
                result["content"] = [{"type": "text", "text": content}]

            # Extract text content
            text_parts = [c["text"] for c in result["content"] if isinstance(c, dict) and c.get("type") == "text"]
            result["text"] = "\n".join(text_parts).strip()

            # Parse tool calls
            result["tool_calls"] = choice.get("tool_calls")
            if result["tool_calls"]:
                result["tool_calls"] = [{
                    "id": tc.get("id"),
                    "type": tc.get("type"),
                    "function": {
                        "name": tc["function"].get("name"),
                        "arguments": tc["function"].get("arguments")
                    }
                } for tc in result["tool_calls"]]

        except KeyError as e:
            result["error"] = f"Missing key in response: {str(e)}"
        except Exception as e:
            result["error"] = str(e)

        return result
    
    def __call__(self, conversation, batch=False, **kwargs):
        return self.run(conversation, batch, **kwargs)

    def run(self, 
            conversation: Union[List[Tuple[str, List[Any]]], List[List[Tuple[str, List[Any]]]]], 
            batch: bool = False, 
            ) -> Union[Dict, List[Dict]]:
        """
        Execute LLM inference with enhanced multi-modal support.
        
        Args:
            conversation: Single or batch of conversations (list of (role, content_list) tuples)
            batch: Set True if processing multiple conversations
            **kwargs: Additional LLM parameters (temperature, max_tokens, etc.)
            
        Returns:
            Dict or List[Dict] containing:
            - content: Structured multi-modal output
            - text: Concatenated text output
            - tool_calls: Formatted tool calls if any
            - error: Any processing errors
        """
        try:
            if batch or isinstance(conversation[0], list):
                conversations = conversation if isinstance(conversation[0], list) else [conversation]
                formatted_batch = self._format_batch(conversations)
                
                responses = batch_completion(
                    model=self.model,
                    messages=formatted_batch,
                    tools=self.tools,
                    api_key=self.api_key,
                    **self.kwargs
                )
                try: self.cost = response.usage.cost
                except: self.cost = 0
                return [self._parse_output(r) for r in responses]
            
            formatted = self._format_messages(conversation)
            response = completion(
                model=self.model,
                messages=formatted,
                tools=self.tools,
                api_key=self.api_key,
                **self.kwargs
            )
            try: self.cost = response.usage.cost
            except: self.cost = 0
            return self._parse_output(response)
        
        except Exception as e:
            error_msg = f"API call failed: {str(e)}"
            return {"error": error_msg}
