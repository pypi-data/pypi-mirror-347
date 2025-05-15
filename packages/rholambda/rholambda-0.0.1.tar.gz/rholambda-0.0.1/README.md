# pyrholambda

Python client library for the Rholambda API

## Installation

```bash
pip install rholambda



from rholambda import Rholambda

# Set your API key
Rholambda.set_apk('your_api_key_here')

# Ask a question
response = Rholambda.ask('What is the meaning of life?')
print(response)