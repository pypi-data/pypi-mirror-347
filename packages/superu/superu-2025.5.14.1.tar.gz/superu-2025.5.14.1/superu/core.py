import requests
import json

server_url = 'https://voip-middlware.superu.ai'
# server_url = 'http://localhost:5000'

class CallWrapper:
    def __init__(self, api_key):
        self.api_key = api_key

        
    def create(self, from_, to_, first_message_url = None , assistant_id = None , max_duration_seconds = 120 , **kwargs):

        data_json = {
            'from_': from_,
            'to_': to_,
            'assistant_id': assistant_id,
            'max_duration_seconds': max_duration_seconds,
            'api_key': self.api_key,
            **kwargs
        }

        if first_message_url:
            data_json['first_message_url'] = first_message_url

        response = requests.post(
            f'{server_url}/pypi_support/call_create',
            json=data_json,
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

        response = requests.post(f'{server_url}/pypi_support/assistant_create', json={'api_key': self.api_key, **payload})
        if response.status_code != 200:
            raise Exception(f"Failed to create assistant: {response.status_code}, {response.text}")
        return response.json()
    
    def create_basic(self, name, voice_id, first_message , system_prompt):
    
        exmaple_json = {
            "name": name,
            "voice": {
                "model": "eleven_flash_v2_5",
                "voiceId": voice_id,
                "provider": "11labs",
                "stability": 0.9,
                "similarityBoost": 0.9,
                "useSpeakerBoost": True,
                "inputMinCharacters": 5
            },
            "model": {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ],
                "provider": "openai",
                "temperature": 0
            },
            "firstMessage": first_message,
            "voicemailMessage": "Please call back when you're available.",
            "endCallFunctionEnabled": True,
            "endCallMessage": "Goodbye.Thank you.",
            "transcriber": {
                "model": "nova-2",
                "language": "en",
                "numerals": False,
                "provider": "deepgram",
                "endpointing": 300,
                "confidenceThreshold": 0.4
            },
            "clientMessages": [
                "transcript",
                "hang",
                "function-call",
                "speech-update",
                "metadata",
                "transfer-update",
                "conversation-update",
                "workflow.node.started"
            ],
            "serverMessages": [
                "end-of-call-report",
                "status-update",
                "hang",
                "function-call"
            ],
            "hipaaEnabled": False,
            "backgroundSound": "office",
            "backchannelingEnabled": False,
            "backgroundDenoisingEnabled": True,
            "messagePlan": {
                "idleMessages": [
                    "Are you still there?"
                ],
                "idleMessageMaxSpokenCount": 2,
                "idleTimeoutSeconds": 5
            },
            "startSpeakingPlan": {
                "waitSeconds": 0.4,
                "smartEndpointingEnabled": "livekit",
                "smartEndpointingPlan": {
                    "provider": "vapi"
                }
            },
            "stopSpeakingPlan": {
                "numWords": 2,
                "voiceSeconds": 0.3,
                "backoffSeconds": 1
            }
        }

        return self.create(**exmaple_json)

    def list(self):
        response = requests.post(f'{server_url}/pypi_support/assistant_list', json={'api_key': self.api_key})
        if response.status_code != 200:
            raise Exception(f"Failed to list assistants: {response.status_code}, {response.text}")
        return response.json()
    
    def get(self, assistant_id):
        response = requests.post(f"{server_url}/pypi_support/assistant_get", json={'api_key': self.api_key, "assistant_id": assistant_id})
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

    
# exmaple_json = {
#     "name": "Paras test pypi",
#     "voice": {
#         "model": "eleven_flash_v2_5",
#         "voiceId": "FFmp1h1BMl0iVHA0JxrI",
#         "provider": "11labs",
#         "stability": 0.9,
#         "similarityBoost": 0.9,
#         "useSpeakerBoost": True,
#         "inputMinCharacters": 5
#     },
#     "model": {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "Part 1: Role and Style\n\nYou are an AI voice assistant calling on behalf of Lon-dhe Jewellers.\n\nSpeak clearly in Hinglish (not too much Hindi or English).\n\nMaintain a steady and natural pace — not too fast.\n\nUse simple, polite, professional language.\n\nPronounce numbers in English. Say जान-कारी, not jankari. Say लोंडे in one go.\n\nAlways thank them for their time.\n\nPart 2: Initial Greeting\n\nWait for response\n\nIf positive → Go to Step 1\n\nIf busy/uninterested → Go to Step 2\n\nStep 1: Offer Intro\n\n\"Sir, Lon-dhe Jewellers, इस Akshay Tritiya के शुभ अवसर पर पचहत्तर हज़ार ki shopping karne pe ek saree, और डेढ़ लाख ki shopping karne pe ek hair straightener as gift de रहा है, और छह लाख ki purchase karne pe ek TV as gift diya ja raha hai. क्या आप इस offer के बारे में और जान-कारी लेना चाहेंगे?\"\n\nIf yes → Step 7\n\nIf no/busy → Step 2\n\nPart 3: Handling No/Busy\n\nStep 2: Customer Busy or Uninterested\n\"Sir, Lon-dhe Jewellers, के किसी भी store visit करके आप इन offers का लाभ उठा सकते हैं। आपका समय देने के लिए धन्यवाद। आपका दिन शुभ हो।\"\n\nStep 3: If Callback is Requested\n\"बिलकुल Sir, मैं आपको कब call back कर सकती हूँ?\"\n\nStep 4: If uncertain response\n\"Sir मैंने आपको, Lon-dhe Jewellers, के Akshay Tritiya offers के बारे में बताने के लिए call किया है। Lon-dhe Jewellers, par पचहत्तर हज़ार ki shopping karne pe ek saree, और डेढ़ लाख ki shopping karne pe ek hair straightener as gift मिल रहा है, और छह लाख ki purchase karne pe ek TV as gift diya ja raha hai। क्या आपको और जान-कारी चाहिए?\"\n\nPart 4: Callback and Ending\n\nStep 5: Confirm Callback\n\nAsk for good time to call.\n\nThen → Go to Step 6\n\nStep 6: End Politely\n\"आपका समय देने के लिए धन्यवाद। आपका दिन शुभ हो। Thank you!\"\n\nStep 7: Detailed Offer\n\n\"इस Akshay Tritiya के शुभ अवसर पर, Lon-dhe Jewellers, के किसी भी store पर visit करके आप इन offers का लाभ उठा सकते हैं। जब आपको सुविधा हो, हमारे स्टोर ज़रूर आएं। क्या आप बता सकते हैं, आप कब आ पाएंगे?\"\n\nIf yes → Step 9\n\nIf no → Step 8\n\nStep 8: End if Not Interested\n\"कोई बात नहीं। आप Lon-dhe Jewellers, के किसी भी store पर visit करके ये offers avail कर सकते हैं। आपका समय देने के लिए धन्यवाद। आपका दिन शुभ हो।\"\n\nStep 9: Ask for Visit Date\n\"Sir, आप हमारे offers का लाभ उठाने के लिए कब visit कर पाएंगे?\"\n\nIf yes → Step 10\n\nIf no → Step 8\n\nStep 10: Final Thank You\n\"धन्यवाद Sir, हम आपके visit का इंतज़ार करेंगे। आपका समय देने के लिए धन्यवाद। आपका दिन शुभ हो।\"\n\nPart 5: If Asked\n\nAre you AI/human?\n\"मैं Lon-dhe Jewellers के behalf पे एक AI agent बोल रही हूँ।\"\n\nNeed callback from staff?\n\"अगर आप चाहें तो मैं हमारे customer service manager से call back arrange करवा सकती हूँ।\"\n\nPart 6: FAQs (Answer if Asked)\n\nOffer valid till?\"ये offer agle week तक है।\"\n\nGold rate?\"माफ़ कीजिए, rate call पर नहीं देते। Store पे best rate मिलता है।\"\n\nOffer हर store में?\"हाँ जी, सभी लोंडे stores में valid है।\"\n\nGold making charge?\"अगर आप चाहें तो मैं हमारे customer service manager से call back arrange करवा सकती हूँ। Wo aapko is baare mai jaankaari dedenge\"\n\nStore कहाँ हैं?\n\"हमारे stores सीताबुलडी, धर्मपेठ aur, मनीष नगर mai hai. Aapko jo location convenient lage, waha aa sakte hain.\"\n\nTimings?\"सुबह 11 से रात 8 बजे तक।\"\n\nSunday?\"हाँ जी, 7 दिन open है।\"\n\nSalesperson से बात?\"मैं call back करवाती हूँ।\"\n\nGold exchange?\"हाँ जी। Visit करें for जान-कारी।\"\n\nFinal Interaction Tips\n\nSpeak naturally and clearly.\n\nAvoid errors or gibberish.\n\nUse simple Hinglish.\n\nUse exact lines.\n\nAlways end with thanks and a warm goodbye."
#             }
#         ],
#         "provider": "openai",
#         "temperature": 0
#     },
#     "firstMessage": "",
#     "voicemailMessage": "Please call back when you're available.",
#     "endCallFunctionEnabled": True,
#     "endCallMessage": "Goodbye.Thank you.",
#     "transcriber": {
#         "model": "nova-2",
#         "language": "en",
#         "numerals": False,
#         "provider": "deepgram",
#         "endpointing": 300,
#         "confidenceThreshold": 0.4
#     },
#     "clientMessages": [
#         "transcript",
#         "hang",
#         "function-call",
#         "speech-update",
#         "metadata",
#         "transfer-update",
#         "conversation-update",
#         "workflow.node.started"
#     ],
#     "serverMessages": [
#         "end-of-call-report",
#         "status-update",
#         "hang",
#         "function-call"
#     ],
#     "hipaaEnabled": False,
#     "backgroundSound": "office",
#     "backchannelingEnabled": False,
#     "backgroundDenoisingEnabled": True,
#     "messagePlan": {
#         "idleMessages": [
#             "Are you still there?"
#         ],
#         "idleMessageMaxSpokenCount": 2,
#         "idleTimeoutSeconds": 5
#     },
#     "startSpeakingPlan": {
#         "waitSeconds": 0.4,
#         "smartEndpointingEnabled": "livekit",
#         "smartEndpointingPlan": {
#             "provider": "vapi"
#         }
#     },
#     "stopSpeakingPlan": {
#         "numWords": 2,
#         "voiceSeconds": 0.3,
#         "backoffSeconds": 1
#     }
# }


# print(check_api_key.assistants.create(
#     **exmaple_json
# ))

# print(check_api_key.assistants.create_basic(
#     name="Paras test pypi delhi weather",
#     voice_id="FFmp1h1BMl0iVHA0JxrI",
#     first_message="Hello John",
#     system_prompt="help me understand the weather in delhi"
# ))


# assitant_list = check_api_key.assistants.list()
# print(assitant_list)

# assistant_get = check_api_key.assistants.get(assistant_id='f8c0301e-0799-4ce9-9d3a-52a788f8ee09')
# print(assistant_get)