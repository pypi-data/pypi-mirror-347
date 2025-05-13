import base64
import json
from openai import AzureOpenAI
import os
import sys
import torch
import json
from RxnIM.reaction.getReaction import get_reaction



class RXNIM:
    def __init__(self, api_key='b038da96509b4009be931e035435e022', api_version='2024-06-01', azure_endpoint='https://hkust.azure-api.net'):
        self.API_KEY = api_key.strip()
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

    def process(self, image_path: str):
        # Encode image
        base64_image = self.encode_image(image_path)

        # Read prompt
        
        prompt = """ 
You are a helpful assistant in identifying chemistry data in an image. In this reaction image, there is a chemistry reaction diagram with one step or multiple step reactions. Your task is to review both the  reactions, and output an array of entries in a json format, which consists of the properly-substituted reactions and all items of the entry present in the table. Your output should be a list of reactions. Each reaction entry should contain its reactants (in SMILES format and with label when the label is provided such as "1a","2a","3b" ...,, or else use "label":"None"), its conditions (Note that molecular smiles or text can both appear in the conditions. First recheck the image carefully and correct the OCR errors and missings of the tool for the text content, and then identify the text or smiles condition role in"agent","solvent","yield","time(such as "1 h", "24 h")","temperature (Note "rt" is temperature too)",if there is no then use "None"), its products (in SMILES format and with label when the label is provided such as "1a","2a","3b" ..., or else use "label":"None"). Make sure that the SMILES strings are correctly formatted.
here is an example output:
{"reactions":[{"reaction_id":"1","reactants":[{"smiles":"Oc1ccc2cccc(C(O)c3ccccc3)c2c1","label":"1a"},{"smiles":"c1ccc2c(c1)[nH]c1ccccc12","label":"None"},...],"conditions":[{"role":"agent","smiles":"*c1cc2ccccc2c2c1OP(=O)(O)Oc1c(*)cc3ccccc3c1-2"}, {"role":"agent","text":"DCM"},{"role": "solvent","text": "toluene"},,...],"products":[{"smiles":"Oc1ccc2cccc([C@H](c3ccccc3)n3c4ccccc4c4ccccc43)c2c1","label":"None"}]}]}
"""
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
            #(f'Iteration {iterations}')

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
                            #print(f'{tool_name} result: {tool_result}')
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
                    #print(results)

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

           

