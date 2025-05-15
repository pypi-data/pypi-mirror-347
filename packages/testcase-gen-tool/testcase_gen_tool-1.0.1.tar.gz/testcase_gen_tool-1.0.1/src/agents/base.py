import requests
import logging
from core.config import config

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self):
        self.api_url = config.get('model_base_url')
        self.api_key = config.get('api_token')
        
        if not all([self.api_url, self.api_key, config.get('model_name')]):
            raise ValueError("Missing required configuration: API_URL, API_KEY, or MODEL_NAME")
            
    def _chat_completion(self, prompt: str, model: str = None, temperature: float = 0.1) -> str:
        """
        Make API call to chat completion endpoint with error handling
        
        Args:
            prompt (str): The prompt to send to the model
            model (str): The model to use
            temperature (float): The temperature for generation
            
        Returns:
            str: The model's response
            
        Raises:
            ValueError: If prompt is empty
            requests.exceptions.RequestException: If API request fails
        """
        if model is None:
            model = config.get('model_name')
        
        if not prompt:
            raise ValueError("Prompt cannot be empty")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        # Calculate input token count
        input_tokens = sum(len(msg["content"].split()) for msg in payload["messages"])
        logger.debug(f"[Token Count] Input tokens: {input_tokens}")
        
        try:
            import time
            start_time = time.time()
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=(30, 240))
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(f" | Request duration: {duration:.2f}s")
            
            response.raise_for_status()
            result = response.json()
            
            # Get output token count
            output_tokens = len(result["choices"][0]["message"]["content"].split())
            logger.debug(f" | Output tokens: {output_tokens}")
            logger.debug(f" | Total tokens: {input_tokens + output_tokens}")
            
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f" | Request failed after {duration:.2f}s")
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise e
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            raise ValueError("Invalid API response format") 