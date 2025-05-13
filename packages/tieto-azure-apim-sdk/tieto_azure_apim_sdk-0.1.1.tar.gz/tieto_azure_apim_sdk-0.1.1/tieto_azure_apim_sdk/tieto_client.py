import requests


class TietoAPIMClient:
    def __init__(self, APIM_ENDPOINT, SUBSCRIPTION_KEY):
        self.endpoint = APIM_ENDPOINT
        self.subscription_key = SUBSCRIPTION_KEY
        if not self.endpoint or not self.subscription_key:
            raise ValueError("APIM_ENDPOINT or SUBSCRIPTION_KEY not set in environment variables.")
        self.headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Accept": "text/event-stream"
        }

    def chat(self, messages, max_tokens=500, stream=False):
        payload = {
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream
        }

        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload,
            stream=stream,
            verify=False
        )

        if response.status_code == 200:
            if stream:
                print("Streaming response:")
                for line in response.iter_lines():
                    if line:
                        print(line.decode("utf-8"))
            else:
                return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")