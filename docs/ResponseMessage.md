# ResponseMessage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataframeasjson** | **str** | dataframe with the kips | [optional] [default to '']
**success** | **bool** |  | [optional] [default to True]
**error** | **str** |  | [optional] [default to '']
**executiontime** | **float** |  | [optional] [default to 0]
**transerinputdata** | **bool** | trigger for upload kpi data und full cylcle data | [optional] [default to False]

## Example Message
```
{
"dataframeasjson": "["KPI1":123, "KPI2":124, (...) ]",
"success": true,
"error": "",
"executiontime": 0,
"transerinputdata": false
}
```


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

