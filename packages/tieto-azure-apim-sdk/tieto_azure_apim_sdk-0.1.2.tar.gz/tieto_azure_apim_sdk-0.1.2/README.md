# Tieto Azure APIM SDK

A Python SDK that allows you to query Azure OpenAI APIs securely through Azure API Management (APIM). This simplifies interaction with Azure OpenAI endpoints and abstracts the complexities of making authenticated HTTP requests.

---

## 📦 Installation

```bash
pip install tieto_azure_apim_sdk
```

Usage Example

```python 
from tieto_azure_apim_sdk import TietoAPIMClient
import os
from dotenv import load_dotenv

load_dotenv()

# Load configuration from environment variables
APIM_ENDPOINT = os.getenv("APIM_ENDPOINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")

# Initialize the client
client = TietoAPIMClient(APIM_ENDPOINT=APIM_ENDPOINT, SUBSCRIPTION_KEY=SUBSCRIPTION_KEY)

# Send a chat request
response = client.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How to build a website like Snapchat. give all the details in 200 words"}
    ],
    max_tokens=500,
    stream=False
)

print("Response:", response)

``` 

| Parameter          | Type   | Description                                                                                 |
| ------------------ | ------ | ------------------------------------------------------------------------------------------- |
| `APIM_ENDPOINT`    | `str`  | Your Azure API Management Gateway URL. Example: `https://my-apim.azure-api.net`             |
| `SUBSCRIPTION_KEY` | `str`  | The subscription key generated in Azure APIM for authenticating API requests.               |
| `messages`         | `list` | A list of chat messages following OpenAI's Chat Completion API format.                      |
| `max_tokens`       | `int`  | The maximum number of tokens to generate in the response.                                   |
| `stream`           | `bool` | If `True`, responses are streamed in chunks; if `False`, the complete response is returned. |

Example Scenarios

1. Basic Synchronous Request

```python
response = client.chat(
    messages=[{"role": "user", "content": "Tell me a joke."}],
    max_tokens=500,
    stream=False
)
``` 
2. Streaming Large Responses

```python
response = client.chat(
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms."}],
    max_tokens=1000,
    stream=True
)
```
 When using stream=True, make sure to handle the response appropriately in chunks.

📅 Versioning

This project uses Semantic Versioning.
Example:

MAJOR: Breaking API changes

MINOR: Backward-compatible new features

PATCH: Bug fixes


📄 License
This project is licensed under the MIT License.

Feel free to contribute or raise issues on GitHub. https://github.com/NaveenGandla/azure_apim_openai_sdk 
