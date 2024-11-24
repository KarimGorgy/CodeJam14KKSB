from google.cloud import dialogflow

credentials_path = "C:/Users/karim/Downloads/newagent-hhex-bd7a13d11e64.json"
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

project_id = "newagent-hhex"
session_id = "test-session"
text = "Hello!"
language_code = "en"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(project_id, session_id)

text_input = dialogflow.TextInput(text=text, language_code=language_code)
query_input = dialogflow.QueryInput(text=text_input)

response = session_client.detect_intent(request={"session": session, "query_input": query_input})
print(f"Detected intent: {response.query_result.intent.display_name}")
print(f"Fulfillment text: {response.query_result.fulfillment_text}")
