# Here is a documentation on how the game engine works

The game engine is a simple wrapper for pymunk

The server side is rendered using pygame for debugging purposes

Events have a property called `sender_rank`

And if this value is lower than self, the event will be rejected (this is how our code will deal with client server disagreements)

The event emitter class will be handled/serialized/deserialized in a different folder for future upgrades like binary websockets
