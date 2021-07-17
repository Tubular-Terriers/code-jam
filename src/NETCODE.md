# Below is the documentation for netcodes when communicating with the server

> All communications are in json

```json
{
    "packet_id":"present in only request packets (notated by * in front of action name)",
    "action": "verify|verify_response|game_init|game",
    "payload": {
        // the actual payload here
    }
}
```



action name      |client                 |server
-                |-                      |-
*verify          | sends token           | returns response status
*request_lobby   | lobby join request    | returns lobby data
*status          |                       | returns a response status
game_init        |                       | sends player's `uuid` and game data to client
game (symmetric) | send game data(event) | send game data(dump)

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
    "action": "status",
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

## Lobby join

```json
{
    "action": "request_lobby",
    "payload": {
        "username": "josh",

        // The below is not implemented
        "lobby_id": "the lobby id",
        // optional
        "password": "12345678"
    }
}
```

When the request succeeds, the server sends a status `OK` and a `game_init` shortly after

When the request fails, the server sends a status `ERROR`

The player cannot know which lobby they joined

## Game init

```json
{
    "action": "game_init",
    "payload": {
        "uuid":"Player's uuid here",
        "map_data": "FIXME might not be utilized"
    }
}
```

## Game data (lifecycle)

Throughout the game play lifecycle, these are constantly sent

```json
{
    "action": "game",
    "payload": {
        "events":{
            // due to lack of time, this is just a key dictionary of player input
            "KEY": true
        }
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
