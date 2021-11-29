# swagger_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**invoke_invoke_post**](DefaultApi.md#invoke_invoke_post) | **POST** /invoke | Invoke

# **invoke_invoke_post**
> ResponseMessage invoke_invoke_post(body)

Invoke

### Example
```python
{
"messages": [
{
"pressure_head_1": 0,
"pressure_head_2": 0,
"pressure_head_3": 0,
"pressure_head_4": 0,
"vibration_head_1": 0,
"vibration_head_2": 0,
"vibration_head_3": 0,
"vibration_head_4": 0,    
"angle": 0,
"timestamp": "2019-08-24T14:15:22Z"
}
],
"servertime": "2019-08-24T14:15:22Z"
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FullMessage**](FullMessage.md)|  | 

### Return type

[**ResponseMessage**](ResponseMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

