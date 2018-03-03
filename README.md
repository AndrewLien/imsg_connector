# iMessage Python Wrapper Proof Of Concept
A proof of concept conceptualizing the usage of AppleScript to send imessage information, and using sqlite3 to read chat database. The integration between the two can serve as a python alternative to sending and receiving data through iMessages. 

## Getting Started
Nothing much. It's just a library with limited functions ready to import. 


### How To Use

Import the library
```
from imessage_connector import iMessageConnector
```

Initialize the connector
```
imc = iMessageConnector()
```

Send a new message
```
imc.imessage_send('phone_number','Message here')
```

Get array list of users in your iMessage history.
```
imc.get_imsg_recipients()
```

Get array of messages from a particular phone number (Requires the + before each number, each element in above is considered a key)
```
imc.get_messages_for_recipient('+15551237777')
```


