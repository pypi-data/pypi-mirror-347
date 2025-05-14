from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration

class ReplicateApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='replicate', integration=integration, **kwargs)
        self.base_url = "https://api.replicate.com/v1"

    def chat_deepseek_ai_deepseek_r1(self, input=None, stream=None) -> dict[str, Any]:
        """
        Generates predictions for AI-powered conversations and tasks using the DeepSeek AI model, enabling applications such as chatbot interactions and text completion, by sending HTTP POST requests to the specified endpoint.

        Args:
            input (object): input
            stream (boolean): stream
                Example:
                ```json
                {
                  "input": {
                    "prompt": "What is the speed of an unladen swallow?"
                  },
                  "stream": true
                }
                ```

        Returns:
            dict[str, Any]: OK / OK

        Tags:
            Chat, important
        """
        request_body = {
            'input': input,
            'stream': stream,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/deepseek-ai/deepseek-r1/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def chat_deepseek_ai_deepseek_r11(self, prediction_id) -> dict[str, Any]:
        """
        Retrieves the details of a specific prediction identified by {prediction_id}.

        Args:
            prediction_id (string): prediction_id

        Returns:
            dict[str, Any]: OK / OK / OK / OK / OK / OK / OK

        Tags:
            Images, important
        """
        if prediction_id is None:
            raise ValueError("Missing required parameter 'prediction_id'")
        url = f"{self.base_url}/v1/predictions/{prediction_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def meta_meta_llama31405b_instruct(self, input=None) -> dict[str, Any]:
        """
        Generates predictions using Meta's multilingual instruction-tuned Llama 3.1 405B model for dialogue and returns the result.

        Args:
            input (object): input
                Example:
                ```json
                {
                  "input": {
                    "frequency_penalty": 0.2,
                    "max_tokens": 512,
                    "min_tokens": 0,
                    "presence_penalty": 1.15,
                    "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
                    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "temperature": 0.6,
                    "top_p": 0.9
                  }
                }
                ```

        Returns:
            dict[str, Any]: OK

        Tags:
            Chat, important
        """
        request_body = {
            'input': input,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/meta/meta-llama-3.1-405b-instruct/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def meta_meta_llama370b_instruct(self, input=None) -> dict[str, Any]:
        """
        Submits a prediction request to the Meta Llama 3 70B Instruct model and returns the generated result.

        Args:
            input (object): input
                Example:
                ```json
                {
                  "input": {
                    "frequency_penalty": 0.2,
                    "max_tokens": 512,
                    "min_tokens": 0,
                    "presence_penalty": 1.15,
                    "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
                    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "temperature": 0.6,
                    "top_p": 0.9
                  }
                }
                ```

        Returns:
            dict[str, Any]: OK

        Tags:
            Chat
        """
        request_body = {
            'input': input,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/meta/meta-llama-3-70b-instruct/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def meta_meta_llama38b_instruct(self, input=None) -> dict[str, Any]:
        """
        Initiates a prediction using the Meta-Llama-3-8B-Instruct model and returns the generated text or code output.

        Args:
            input (object): input
                Example:
                ```json
                {
                  "input": {
                    "frequency_penalty": 0.2,
                    "max_tokens": 512,
                    "min_tokens": 0,
                    "presence_penalty": 1.15,
                    "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
                    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "temperature": 0.6,
                    "top_p": 0.9
                  }
                }
                ```

        Returns:
            dict[str, Any]: OK

        Tags:
            Chat
        """
        request_body = {
            'input': input,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/meta/meta-llama-3-8b-instruct/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def mistralai_mistral7b_v01(self, input=None) -> dict[str, Any]:
        """
        Generates predictions using the Mistral-7B model and returns the output.

        Args:
            input (object): input
                Example:
                ```json
                {
                  "input": {
                    "frequency_penalty": 0.2,
                    "max_tokens": 512,
                    "min_tokens": 0,
                    "presence_penalty": 1.15,
                    "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
                    "prompt_template": "{prompt}",
                    "temperature": 0.6,
                    "top_p": 0.9
                  }
                }
                ```

        Returns:
            dict[str, Any]: OK

        Tags:
            Chat
        """
        request_body = {
            'input': input,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/mistralai/mistral-7b-v0.1/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def black_forest_labs_flux_schnell(self, input=None) -> dict[str, Any]:
        """
        Generates high-quality images from text descriptions using a 12 billion parameter rectified flow transformer model.

        Args:
            input (object): input
                Example:
                ```json
                {
                  "input": {
                    "prompt": "black forest gateau cake spelling out the words \"FLUX SCHNELL\", tasty, food photography, dynamic shot"
                  }
                }
                ```

        Returns:
            dict[str, Any]: OK

        Tags:
            Images, important
        """
        request_body = {
            'input': input,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/models/black-forest-labs/flux-schnell/predictions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        return [
            self.chat_deepseek_ai_deepseek_r1,
            self.chat_deepseek_ai_deepseek_r11,
            self.meta_meta_llama31405b_instruct,
            self.meta_meta_llama370b_instruct,
            self.meta_meta_llama38b_instruct,
            self.mistralai_mistral7b_v01,
            self.black_forest_labs_flux_schnell
        ]
