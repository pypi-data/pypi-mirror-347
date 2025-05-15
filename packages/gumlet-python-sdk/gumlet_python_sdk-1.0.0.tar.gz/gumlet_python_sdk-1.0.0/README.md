
# Getting Started with gumlet-rest-apis

## Install the Package

The package is compatible with Python versions `3.7+`.
Install the package from PyPi using the following pip command:

```bash
pip install gumlet-python-sdk==1.0.0
```

You can also view the package at:
https://pypi.python.org/pypi/gumlet-python-sdk/1.0.0

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| http_client_instance | `HttpClient` | The Http Client passed from the sdk user for making requests |
| override_http_client_configuration | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| http_call_back | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| timeout | `float` | The value to use for connection timeout. <br> **Default: 60** |
| max_retries | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| backoff_factor | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| retry_statuses | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| retry_methods | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| custom_header_authentication_credentials | [`CustomHeaderAuthenticationCredentials`](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/auth/custom-header-signature.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

```python
client = GumletrestapisClient(
    custom_header_authentication_credentials=CustomHeaderAuthenticationCredentials(
        authorization='Authorization'
    ),
    environment=Environment.PRODUCTION
)
```

## Authorization

This API uses the following authentication schemes.

* [`sec0 (Custom Header Signature)`](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/auth/custom-header-signature.md)

## List of APIs

* [API Endpoints](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/controllers/api-endpoints.md)

## SDK Infrastructure

### HTTP

* [HttpResponse](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/http-response.md)
* [HttpRequest](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/http-request.md)

### Utilities

* [ApiHelper](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/api-helper.md)
* [HttpDateTime](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/http-date-time.md)
* [RFC3339DateTime](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/rfc3339-date-time.md)
* [UnixDateTime](https://www.github.com/akbansa/gumlet-python-sdk/tree/1.0.0/doc/unix-date-time.md)

