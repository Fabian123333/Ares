---
title: FastAPI v0.1.0
language_tabs:
  - bash: Bash
  - python: Python
language_clients:
  - bash: ""
  - python: ""
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="fastapi">FastAPI v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

<h1 id="fastapi-api">api</h1>

## get_root__get

<a id="opIdget_root__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/', headers = headers)

print(r.json())

```

`GET /`

*Get Root*

> Example responses

> 200 Response

```json
null
```

<h3 id="get_root__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_root__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-secret">secret</h1>

## create_secret__post

<a id="opIdcreate_secret__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/secret/', headers = headers)

print(r.json())

```

`POST /secret/`

*Create*

> Body parameter

```json
{
  "name": "string",
  "description": "string",
  "secret": "string"
}
```

<h3 id="create_secret__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[modules__secret__StructNew](#schemamodules__secret__structnew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_secret__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_secret__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-host">host</h1>

## getAll_host__get

<a id="opIdgetAll_host__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/host/', headers = headers)

print(r.json())

```

`GET /host/`

*Getall*

> Example responses

> 200 Response

```json
null
```

<h3 id="getall_host__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="getall_host__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_host__post

<a id="opIdcreate_host__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/host/', headers = headers)

print(r.json())

```

`POST /host/`

*Create*

> Body parameter

```json
{
  "hostname": "string",
  "description": "string",
  "ip_address": "string",
  "type": "linux",
  "credential_id": "string"
}
```

<h3 id="create_host__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[StructHostNew](#schemastructhostnew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_host__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_host__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_host__id__get

<a id="opIdget_host__id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/host/{id}', headers = headers)

print(r.json())

```

`GET /host/{id}`

*Get*

<h3 id="get_host__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_host__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_host__id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-credential">credential</h1>

## getCredentials_credential__get

<a id="opIdgetCredentials_credential__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/credential/', headers = headers)

print(r.json())

```

`GET /credential/`

*Getcredentials*

> Example responses

> 200 Response

```json
null
```

<h3 id="getcredentials_credential__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="getcredentials_credential__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_credential__post

<a id="opIdcreate_credential__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/credential/', headers = headers)

print(r.json())

```

`POST /credential/`

*Create*

> Body parameter

```json
{
  "name": "string",
  "type": "password",
  "username": "root",
  "description": "string",
  "secret_id": "string"
}
```

<h3 id="create_credential__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[modules__credential__StructNew](#schemamodules__credential__structnew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_credential__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_credential__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_credential__id__get

<a id="opIdget_credential__id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/credential/{id}', headers = headers)

print(r.json())

```

`GET /credential/{id}`

*Get*

<h3 id="get_credential__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_credential__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_credential__id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-target">target</h1>

## getAll_target__get

<a id="opIdgetAll_target__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/target/', headers = headers)

print(r.json())

```

`GET /target/`

*Getall*

> Example responses

> 200 Response

```json
null
```

<h3 id="getall_target__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="getall_target__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_target__post

<a id="opIdcreate_target__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/target/', headers = headers)

print(r.json())

```

`POST /target/`

*Create*

> Body parameter

```json
{
  "name": "string",
  "fqdn": "string",
  "description": "string",
  "ip_address": "string",
  "location": "",
  "path": "/ares",
  "type": "string",
  "credential_id": "string"
}
```

<h3 id="create_target__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[modules__target__StructNew](#schemamodules__target__structnew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_target__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_target__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_target__id__get

<a id="opIdget_target__id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/target/{id}', headers = headers)

print(r.json())

```

`GET /target/{id}`

*Get*

<h3 id="get_target__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_target__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_target__id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-job">job</h1>

## getAll_job__get

<a id="opIdgetAll_job__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/job/', headers = headers)

print(r.json())

```

`GET /job/`

*Getall*

> Example responses

> 200 Response

```json
null
```

<h3 id="getall_job__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="getall_job__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_job__post

<a id="opIdcreate_job__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/job/', headers = headers)

print(r.json())

```

`POST /job/`

*Create*

> Body parameter

```json
{
  "name": "string",
  "description": "string",
  "type": "backup",
  "snapshots": 14,
  "interval": 720,
  "target_id": "string",
  "host_ids": [
    null
  ],
  "task_ids": [
    null
  ]
}
```

<h3 id="create_job__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[StructJobNew](#schemastructjobnew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_job__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_job__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## apply_job__job_id__get

<a id="opIdapply_job__job_id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/job/{job_id}', headers = headers)

print(r.json())

```

`GET /job/{job_id}`

*Apply*

<h3 id="apply_job__job_id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|job_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="apply_job__job_id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="apply_job__job_id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## delete_job__job_id__delete

<a id="opIddelete_job__job_id__delete"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/job/{job_id}', headers = headers)

print(r.json())

```

`DELETE /job/{job_id}`

*Delete*

<h3 id="delete_job__job_id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|job_id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete_job__job_id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete_job__job_id__delete-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## request_job_request__get

<a id="opIdrequest_job_request__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/job/request/', headers = headers)

print(r.json())

```

`GET /job/request/`

*Request*

> Example responses

> 200 Response

```json
null
```

<h3 id="request_job_request__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="request_job_request__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-task">task</h1>

## getAll_task__get

<a id="opIdgetAll_task__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/task/', headers = headers)

print(r.json())

```

`GET /task/`

*Getall*

> Example responses

> 200 Response

```json
null
```

<h3 id="getall_task__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="getall_task__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_task__post

<a id="opIdcreate_task__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/task/', headers = headers)

print(r.json())

```

`POST /task/`

*Create*

> Body parameter

```json
{
  "name": "string",
  "type": "file",
  "description": "string",
  "data": [
    null
  ]
}
```

<h3 id="create_task__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[StructTaskNew](#schemastructtasknew)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_task__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_task__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_task__id__get

<a id="opIdget_task__id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/task/{id}', headers = headers)

print(r.json())

```

`GET /task/{id}`

*Get*

<h3 id="get_task__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_task__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_task__id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_StructHostNew">StructHostNew</h2>
<!-- backwards compatibility -->
<a id="schemastructhostnew"></a>
<a id="schema_StructHostNew"></a>
<a id="tocSstructhostnew"></a>
<a id="tocsstructhostnew"></a>

```json
{
  "hostname": "string",
  "description": "string",
  "ip_address": "string",
  "type": "linux",
  "credential_id": "string"
}

```

StructHostNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|hostname|string|true|none|none|
|description|string|false|none|none|
|ip_address|string|false|none|none|
|type|string|false|none|none|
|credential_id|string|true|none|none|

<h2 id="tocS_StructJobNew">StructJobNew</h2>
<!-- backwards compatibility -->
<a id="schemastructjobnew"></a>
<a id="schema_StructJobNew"></a>
<a id="tocSstructjobnew"></a>
<a id="tocsstructjobnew"></a>

```json
{
  "name": "string",
  "description": "string",
  "type": "backup",
  "snapshots": 14,
  "interval": 720,
  "target_id": "string",
  "host_ids": [
    null
  ],
  "task_ids": [
    null
  ]
}

```

StructJobNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|description|string|false|none|none|
|type|string|false|none|none|
|snapshots|integer|false|none|none|
|interval|integer|false|none|none|
|target_id|string|true|none|none|
|host_ids|[any]|true|none|none|
|task_ids|[any]|true|none|none|

<h2 id="tocS_StructTaskNew">StructTaskNew</h2>
<!-- backwards compatibility -->
<a id="schemastructtasknew"></a>
<a id="schema_StructTaskNew"></a>
<a id="tocSstructtasknew"></a>
<a id="tocsstructtasknew"></a>

```json
{
  "name": "string",
  "type": "file",
  "description": "string",
  "data": [
    null
  ]
}

```

StructTaskNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|type|string|false|none|none|
|description|string|false|none|none|
|data|[any]|true|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[string]|true|none|none|
|msg|string|true|none|none|
|type|string|true|none|none|

<h2 id="tocS_modules__credential__StructNew">modules__credential__StructNew</h2>
<!-- backwards compatibility -->
<a id="schemamodules__credential__structnew"></a>
<a id="schema_modules__credential__StructNew"></a>
<a id="tocSmodules__credential__structnew"></a>
<a id="tocsmodules__credential__structnew"></a>

```json
{
  "name": "string",
  "type": "password",
  "username": "root",
  "description": "string",
  "secret_id": "string"
}

```

StructNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|type|string|false|none|none|
|username|string|false|none|none|
|description|string|false|none|none|
|secret_id|string|true|none|none|

<h2 id="tocS_modules__secret__StructNew">modules__secret__StructNew</h2>
<!-- backwards compatibility -->
<a id="schemamodules__secret__structnew"></a>
<a id="schema_modules__secret__StructNew"></a>
<a id="tocSmodules__secret__structnew"></a>
<a id="tocsmodules__secret__structnew"></a>

```json
{
  "name": "string",
  "description": "string",
  "secret": "string"
}

```

StructNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|description|string|false|none|none|
|secret|string|true|none|none|

<h2 id="tocS_modules__target__StructNew">modules__target__StructNew</h2>
<!-- backwards compatibility -->
<a id="schemamodules__target__structnew"></a>
<a id="schema_modules__target__StructNew"></a>
<a id="tocSmodules__target__structnew"></a>
<a id="tocsmodules__target__structnew"></a>

```json
{
  "name": "string",
  "fqdn": "string",
  "description": "string",
  "ip_address": "string",
  "location": "",
  "path": "/ares",
  "type": "string",
  "credential_id": "string"
}

```

StructNew

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|fqdn|string|false|none|none|
|description|string|false|none|none|
|ip_address|string|false|none|none|
|location|string|false|none|none|
|path|string|false|none|none|
|type|string|true|none|none|
|credential_id|string|true|none|none|

