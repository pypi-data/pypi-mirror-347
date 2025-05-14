## Unofficial library collection for Y360 API

#### Installation

```bash
pip install y360-orglib

```
#### Import
```
import y360_orglib
```

### Available Modules:

- `serviceapp`: ServiceApps module for interacting with the Y360 Service Applications.
- `disk`: Disk Client module for interacting with the Y360 Disk REST API.
- `directory`: Directory API module for interacting with the Y360 Directory API.
- `audit`: Audit Log module for interacting with the Y360 Audit Log API.


### ServiceAppClient

Init client
```python
service_apps_client = ServiceAppClient(client_id, client_secret)
```

Get a service app token for for given User (subject_token).
- subject_token: User Id or Email<br/>
- subject_token_type: The type of the subject token.<br/>
    - If the subject_token is a User ID, the subject_token_type should be 'urn:yandex:params:oauth:token-type:uid'.
    - If the subject_token is an Email, the subject_token_type should be 'urn:yandex:params:oauth:token-type:email'.
    - Default value is 'urn:yandex:params:oauth:token-type:email'.
- Returns: ServiceAppTokenResponse - Response with service app token for provided User
        
```

service_apps_client.get_service_app_token(subject_token="user@email.com").access_token

or

service_apps_client.get_service_app_token(subject_token="12344556", subject_token_type = "urn:yandex:params:oauth:token-type:uid").access_token

```
