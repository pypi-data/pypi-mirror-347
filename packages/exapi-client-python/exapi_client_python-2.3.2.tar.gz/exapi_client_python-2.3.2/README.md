# API Client for python

This is an auto-generated SDK for the API.

## Example Usage

```py
// DISCLAIMER: This is an auto-generated example and library.
// This lib has NOT been tested by our support team.
// Please use at your own risk, and make tests before using it.
//
// install using "pip install exapi_client_python"
import exapi_client_python
from exapi_client_python.api import default_api
from exapi_client_python.configuration import Configuration

# Configure API key authorization
configuration = Configuration(
    host = "https://api.exkoin.com",
    api_key = {'ApiKeyAuth': 'YOUR_API_KEY'},
    api_secret = {'ApiSecretAuth': 'YOUR_API_SECRET'}
)

# Create an instance of the API class
api_instance = default_api.DefaultApi(api_client_python.ApiClient(configuration))

try:
    # Get account balance
    api_response = api_instance.get_balance()
    print("Account balance: %s" % api_response)
except api_client_python.ApiException as e:
    print("Exception when calling DefaultApi->get_balance: %s\n" % e)
```