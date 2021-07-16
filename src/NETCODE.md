# Below is the documentation for netcodes when communicating with the server

> All communications are in json

```json
{
    "action": "verify|verify_response|game",
    "payload": {
        // the actual payload here
    }
}
```
action name      |client                 |server
-                |-                      |-
verify           | sends token           |
verify_response  |                       | response to `verify`
game (symmetric) | send game data        | send game data
## Verification

```json
{
    "action": "verify",
    "payload": {
        "TOKEN": "YOUR TOKEN HERE"
    }
}
```

when verification is success, the server returns

```json
{
    "action": "verify_response",
    "payload": {
        "status": "OK",
        "error": ""
    }
}
```
when the verification fails, the server returns

```json
{
    "action": "verify_response",
    "payload": {
        "status": "ERROR",
        "error": "Invalid Token"
    }
}
```

## Game data

Throughout the game play lifecycle, these are constantly sent

```json
{
    "action": "game",
    "payload": {
        "events":[
            {
                "name": "EVENT ID HERE",
                "value": {} // value or object. Different for every event
            }
        ]
    }
}
```

> Even if the two actions both send exactly the same structure, they send different events

example server payload

```json
{
    "action": "game",
    "payload": {
        "events":[
            {
                "name": "ENTITIES_UPDATE",
                "value": [
                    {
                        "uuid": "THE UUID",
                        // A bunch of other data
                    }
                ]
            },
            {
                "name": "SOUND",
                "value": "SOUND_ID HERE"
            }
        ]
    }
}
```

example client payload

```json
{
    "action": "game",
    "payload": {
        "events":[
            {
                "name": "MOVE_PLAYER",
                "value": {
                    "UP": false,
                    "DOWN": false,
                    // ...
                }
            },
            {
                "name": "MOVE_BAR",
                "value": {
                    "UP": false,
                    "DOWN": false,
                    // ...
                }
            }
        ]
    }
}
```
