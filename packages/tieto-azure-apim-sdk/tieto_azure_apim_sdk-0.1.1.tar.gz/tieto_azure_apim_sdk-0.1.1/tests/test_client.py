import unittest
from tieto_azure_apim_sdk import TietoAPIMClient
from unittest.mock import patch

class TestAzureAPIMOpenAIClient(unittest.TestCase):
    @patch("azure_apim_openai_sdk.client.requests.post")
    def test_query_openai(self, mock_post, AZURE_APIM_ENDPOINT, AZURE_APIM_SUBSCRIPTION_KEY):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"result": "success"}

        client = TietoAPIMClient(AZURE_APIM_ENDPOINT, AZURE_APIM_SUBSCRIPTION_KEY)
        response = client.query_openai(
            api_path="openai/deployments/gpt-35/chat/completions",
            payload={"messages": [{"role": "user", "content": "Hello!"}]}
        )

        self.assertEqual(response["result"], "success")
