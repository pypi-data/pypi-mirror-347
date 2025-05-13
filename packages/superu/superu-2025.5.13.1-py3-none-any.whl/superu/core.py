import requests
import json

server_url = 'https://voip-middlware.superu.ai'
# server_url = 'http://localhost:5000'

class CallWrapper:
    def __init__(self, api_key):
        self.api_key = api_key

        
    def create(self, from_, to_, first_message_url, assistant_id , max_duration_seconds = 120 , **kwargs):
        response = requests.post(
            f'{server_url}/pypi_support/call_create',
            json={
                'from_': from_,
                'to_': to_,
                'first_message_url': first_message_url,
                'assistant_id': assistant_id,
                'max_duration_seconds': max_duration_seconds,
                'api_key': self.api_key,
                **kwargs
            }
        )
        return response
        
    
    def analysis(self, call_uuid , custom_fields = None):
        if custom_fields is not None:
            required_keys = {"field", "definition", "outputs_options"}
            for i, field in enumerate(custom_fields):
                if not isinstance(field, dict):
                    raise ValueError(f"custom_fields[{i}] is not a dictionary")
                
                missing_keys = required_keys - field.keys()
                if missing_keys:
                    raise ValueError(f"custom_fields[{i}] is missing keys: {missing_keys}")

                if not isinstance(field["field"], str):
                    raise ValueError(f"custom_fields[{i}]['field'] must be a string")
                if not isinstance(field["definition"], str):
                    raise ValueError(f"custom_fields[{i}]['definition'] must be a string")
                if not isinstance(field["outputs_options"], list) or not all(isinstance(opt, str) for opt in field["outputs_options"]):
                    raise ValueError(f"custom_fields[{i}]['outputs_options'] must be a list of strings")

        response = requests.request(
            "POST",
            f'{server_url}/pypi_support/call_analysis',
            json={'api_key': self.api_key, "call_uuid": call_uuid, "custom_fields": custom_fields}
        )
        return response


    # def __getattr__(self, name):
    #     # Delegate all other methods/attributes
    #     return getattr(self._real, name)

class AssistantWrapper:
    def __init__(self, api_key):
        self.api_key = api_key

    def create(self, name, transcriber, model, voice , **kwargs):
        payload = {
            "name": name,
            "transcriber": transcriber,
            "model": model,
            "voice": voice,
            **kwargs
        }

        response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
        if response.status_code != 200:
            raise Exception(f"Failed to create assistant: {response.status_code}, {response.text}")
        return response.json()

    def list(self):
        response = requests.post(f'{server_url}/pypi_support/assistant_list', json={'api_key': self.api_key})
        if response.status_code != 200:
            raise Exception(f"Failed to list assistants: {response.status_code}, {response.text}")
        return response.json()
    
    def get(self, assistant_id):
        response = requests.get(f"{self.base_url}/{assistant_id}", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get assistant: {response.status_code}, {response.text}")
        return response.json()

class ToolWrapper:
    def __init__(self, vapi_private_key , vapi_public_key):
        self.base_url = "https://api.vapi.ai/tool"
        self.vapi_private_key = vapi_private_key
        self.vapi_public_key = vapi_public_key
        self.headers = {
            "Authorization": f"Bearer {self.vapi_private_key}",
            "Content-Type": "application/json"
        }

    def create(self, name, description, parameters, server_url,
               request_start=None, request_complete=None,
               request_failed=None, request_response_delayed=None,
               async_=False, timeout_seconds=10, secret=None, headers=None):
        """
        Create a 'function' type tool.

        Args:
            name (str): Function name.
            description (str): What the function does.
            parameters (dict): JSON schema for parameters.
            server_url (str): The endpoint that Vapi will call.
            request_start (str, optional): Message to say when starting.
            request_complete (str, optional): Message to say on success.
            request_failed (str, optional): Message to say on failure.
            request_response_delayed (str, optional): Message to say if slow.
            async_ (bool): Whether to call function async.
            timeout_seconds (int): Request timeout.
            secret (str, optional): Optional secret for auth.
            headers (dict, optional): Extra headers for the server call.

        Returns:
            dict: The created tool details.
        """
        messages = []
        if request_start:
            messages.append({"type": "request-start", "content": request_start})
        if request_complete:
            messages.append({"type": "request-complete", "content": request_complete})
        if request_failed:
            messages.append({"type": "request-failed", "content": request_failed})
        if request_response_delayed:
            messages.append({
                "type": "request-response-delayed",
                "content": request_response_delayed,
                "timingMilliseconds": 2000
            })

        payload = {
            "type": "function",
            "async": async_,
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            },
            "messages": messages,
            "server": {
                "url": server_url,
                "timeoutSeconds": timeout_seconds
            }
        }

        if secret:
            payload["server"]["secret"] = secret
        if headers:
            payload["server"]["headers"] = headers

        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to create tool: {response.status_code}, {response.text}")
        return response.json()
    
    def list(self):
        response = requests.get(f'{self.base_url}?limit=1000', headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to list tools: {response.status_code}, {response.text}")
        return response.json()
    
    def get(self, tool_id):
        response = requests.get(f'{self.base_url}/{tool_id}', headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get tool: {response.status_code}, {response.text}")
        return response.json()
            

class SuperU:
    def __init__(self, api_key):
        API_key_validation = self.validate_api_key(api_key)
        self.api_key = api_key
        self.user_id = API_key_validation['user_id']
        self.calls = CallWrapper(self.api_key)
        self.assistants = AssistantWrapper(self.api_key)

    def validate_api_key(self, api_key):
        response = requests.post(
            # 'https://shared-service.superu.ai/api_key_check',
            f'{server_url}/user/validate-api-key',
            headers={'Content-Type': 'application/json'},
            json={'api_key': api_key}
        )
        if response.status_code != 200:
            raise Exception(f"Invalid API key: {response.status_code}, {response.text}")
        return response.json()
    
    # def __getattr__(self, name):
    #     return getattr(self._client, name)
    

# check_api_key = SuperU('VGa2Gnaj2EA8JcQ25SZxI4ZeoM')

# check_api_key.calls.create(from_='918035737904', 
#                            to_='919327434748', 
#                            first_message_url='https://mirrar-medialibrary.s3.ap-south-1.amazonaws.com/londhe-jewellers/ElevenLabs_2025-04-29T07_41_22_Tarini+-+Expressive+%26+Cheerful+Hindi+Narrator_pvc_sp100_s90_sb90_se0_b_m2.mp3' ,
#                            assistant_id='83789bdd-ab1b-40f2-9a91-8457dbb8b7d8' , 
#                            max_duration_seconds=120)

# print(check_api_key.calls.analysis(call_uuid='59aa30b5-00f4-44fb-b238-84eabb629c14').text)




# assitant_list = check_api_key.assistants.list()
# print(assitant_list)
