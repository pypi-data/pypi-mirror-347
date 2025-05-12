import base64
import json
from openai import AzureOpenAI
import os
import sys
import torch
import json
from getReaction import get_reaction



class RXNIM:
    def __init__(self, api_key='b038da96509b4009be931e035435e022', api_version='2024-06-01', azure_endpoint='https://hkust.azure-api.net'):
        # Read API key
        self.API_KEY = api_key.strip()

    # def __init__(self, api_version='2024-06-01', azure_endpoint='https://hkust.azure-api.net'):
    #     # 从环境变量读取 API Key
    #     self.API_KEY = os.environ.get('key')
    #     if not self.API_KEY:
    #         raise ValueError("Environment variable 'KEY' not set.")

        # Set up client
        self.client = AzureOpenAI(
            api_key=self.API_KEY,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )

        # Define tools
        self.tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'get_reaction',
                    'description': 'Get a list of reactions from a reaction image. A reaction contains data of the reactants, conditions, and products.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'image_path': {
                                'type': 'string',
                                'description': 'The path to the reaction image.',
                            },
                        },
                        'required': ['image_path'],
                        'additionalProperties': False,
                    },
                },
            },
        ]

        # Define tool mapping
        self.TOOL_MAP = {
            'get_reaction': get_reaction,
        }

    def encode_image(self, image_path: str):
        '''Returns a base64 string of the input image.'''
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def process(self, image_path: str, prompt_path: str):
        # Encode image
        base64_image = self.encode_image(image_path)

        # Read prompt
        with open(prompt_path, 'r') as prompt_file:
            prompt = prompt_file.read()

        # Build initial messages
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant. Before providing the final answer, consider if any additional information or tool usage is needed to improve your response.'},
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': prompt
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/png;base64,{base64_image}'
                        }
                    }
                ]
            },
        ]

        MAX_ITERATIONS = 5
        iterations = 0

        while iterations < MAX_ITERATIONS:
            iterations += 1
            print(f'Iteration {iterations}')

            # Call the model
            response = self.client.chat.completions.create(
                model='gpt-4o',
                temperature=0,
                response_format={'type': 'json_object'},
                messages=messages,
                tools=self.tools,
            )

            # Get assistant's message
            assistant_message = response.choices[0].message

            # Add assistant's message to messages
            messages.append(assistant_message)

            # Check for tool calls
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                tool_calls = assistant_message.tool_calls
                results = []

                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_arguments = tool_call.function.arguments
                    tool_call_id = tool_call.id

                    tool_args = json.loads(tool_arguments)

                    if tool_name in self.TOOL_MAP:
                        try:
                            # Call the tool function
                            tool_result = self.TOOL_MAP[tool_name](image_path)
                            print(f'{tool_name} result: {tool_result}')
                        except Exception as e:
                            tool_result = {'error': str(e)}
                    else:
                        tool_result = {'error': f"Unknown tool called: {tool_name}"}

                    # Append tool result to messages
                    results.append({
                        'role': 'tool',
                        'content': json.dumps({
                            'image_path': image_path,
                            f'{tool_name}': tool_result,
                        }),
                        'tool_call_id': tool_call_id,
                    })
                    print(results)

                # Add tool results to messages
                messages.extend(results)
            else:
                # No more tool calls, assume task is completed
                break

        else:
            # Exceeded maximum iterations
            return "The assistant could not complete the task within the maximum number of iterations."

        # Return the final assistant message
        final_content = assistant_message.content
        return final_content

           

