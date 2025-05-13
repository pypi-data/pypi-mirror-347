"""AI provider implementations for TerminalAI.

This module contains provider classes for different AI services supported by TerminalAI.
It includes implementations for OpenRouter, Gemini, Mistral, and Ollama providers.

Note: System detection for command customization is handled in terminalai_cli.py's
get_system_context() function, which passes the detected OS information to these providers.
"""
import requests
from terminalai.config import load_config

class AIProvider:
    """Base class for all AI providers."""

    def query(self, prompt):
        """Query the AI provider with the given prompt.

        Args:
            prompt: The text prompt to send to the AI provider.

        Returns:
            The response from the AI provider.
        """
        raise NotImplementedError

    def generate_response(self, user_query, system_context, verbose=False):
        """Generate a response with the given query and system context.

        Args:
            user_query: The user's question or request
            system_context: The system context/instructions
            verbose: Whether to provide a more detailed response

        Returns:
            The formatted response from the AI
        """
        # Combine system context and user query
        full_prompt = f"{system_context}\n\n{user_query}"

        # If verbose is enabled, add instructions for a more detailed response
        if verbose:
            full_prompt += "\n\nPlease provide a detailed response with examples if applicable."

        # Get the response
        response = self.query(full_prompt)

        # Add AI marker prefix
        return f"[AI] {response}"

class OpenRouterProvider(AIProvider):
    """OpenRouter AI provider implementation."""

    def __init__(self, api_key):
        """Initialize the OpenRouter provider.

        Args:
            api_key: API key for OpenRouter service.
        """
        self.api_key = api_key

    def query(self, prompt):
        """Query OpenRouter API with the given prompt.

        Args:
            prompt: The text prompt to send to OpenRouter.

        Returns:
            The response text from OpenRouter.
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/coaxialdolor/terminalai"
        }

        # Check if the prompt includes a system prompt section
        if "\n\n" in prompt:
            system_prompt, user_prompt = prompt.split("\n\n", 1)
            data = {
                "model": "openai/gpt-3.5-turbo",  # Default model, can be modified
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
        else:
            # Just a user prompt without system instructions
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError, IndexError) as e:
            return f"[OpenRouter API error] {e}"

class GeminiProvider(AIProvider):
    """Google Gemini AI provider implementation."""

    def __init__(self, api_key):
        """Initialize the Gemini provider.

        Args:
            api_key: API key for Google Gemini service.
        """
        self.api_key = api_key

    def query(self, prompt):
        """Query Google Gemini API with the given prompt.

        Args:
            prompt: The text prompt to send to Gemini.

        Returns:
            The response text from Gemini.
        """
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json"
        }

        # Check if the prompt includes a system prompt section
        if "\n\n" in prompt:
            system_prompt, user_prompt = prompt.split("\n\n", 1)
            # Gemini doesn't natively support system prompts, so we'll format it
            formatted_prompt = (
                f"System instructions: {system_prompt}\n\nUser query: {user_prompt}"
            )
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": formatted_prompt}
                        ]
                    }
                ]
            }
        else:
            # Just a user prompt without system instructions
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (requests.RequestException, KeyError, IndexError) as e:
            return f"[Gemini API error] {e}"

class MistralProvider(AIProvider):
    """Mistral AI provider implementation."""

    def __init__(self, api_key):
        """Initialize the Mistral provider.

        Args:
            api_key: API key for Mistral service.
        """
        self.api_key = api_key

    def query(self, prompt):
        """Query Mistral API with the given prompt.

        Args:
            prompt: The text prompt to send to Mistral.

        Returns:
            The response text from Mistral.
        """
        # Real Mistral API call
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Check if the prompt includes a system prompt section
        if "\n\n" in prompt:
            system_prompt, user_prompt = prompt.split("\n\n", 1)
            data = {
                "model": "mistral-tiny",  # You can change to another model if needed
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
        else:
            # Just a user prompt without system instructions
            data = {
                "model": "mistral-tiny",  # You can change to another model if needed
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError, IndexError) as e:
            return f"[Mistral API error] {e}"

class OllamaProvider(AIProvider):
    """Ollama local model provider implementation."""

    def __init__(self, host, model="llama3"):
        """Initialize the Ollama provider.

        Args:
            host: The host URL for the Ollama server.
            model: The model name to use (defaults to llama3)
        """
        self.host = host
        self.model = model

    def query(self, prompt):
        """Query Ollama API with the given prompt.

        Args:
            prompt: The text prompt to send to Ollama.

        Returns:
            The response text from Ollama.
        """
        url = f"{self.host}/api/chat"
        headers = {
            "Content-Type": "application/json"
        }

        # Check if the prompt includes a system prompt section
        if "\n\n" in prompt:
            system_prompt, user_prompt = prompt.split("\n\n", 1)
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False
            }
        else:
            # Just a user prompt without system instructions
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }

        try:
            # Longer timeout for local models
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except (requests.RequestException, KeyError) as e:
            return f"[Ollama API error] {e}"

def get_provider(provider_name=None):
    """Get the provider instance for the specified name or the default one.

    Args:
        provider_name: Optional name of the provider to use. If None, use the default.

    Returns:
        An instance of the appropriate AI provider class, or None if unable to initialize.
    """
    config = load_config()

    # Use specified provider or default from config
    if not provider_name:
        provider_name = config.get("default_provider", "")

    if not provider_name:
        return None

    # Initialize the appropriate provider based on name
    if provider_name == "openrouter":
        api_key = config.get("providers", {}).get("openrouter", {}).get("api_key", "")
        if api_key:
            return OpenRouterProvider(api_key)
    elif provider_name == "gemini":
        api_key = config.get("providers", {}).get("gemini", {}).get("api_key", "")
        if api_key:
            return GeminiProvider(api_key)
    elif provider_name == "mistral":
        api_key = config.get("providers", {}).get("mistral", {}).get("api_key", "")
        if api_key:
            return MistralProvider(api_key)
    elif provider_name == "ollama":
        ollama_config = config.get("providers", {}).get("ollama", {})
        host = ollama_config.get("host", "http://localhost:11434")
        model = ollama_config.get("model", "llama3")
        return OllamaProvider(host, model)

    return None
