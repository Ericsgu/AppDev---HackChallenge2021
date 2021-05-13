# AppDev---HackChallenge2021
## API Specification
### Base Endpoint: letsdoit2021.herokuapp.com

### 1) Register


<code>POST</code> /api/register/

Request
```
{
  "name": <USER INPUT>,
  "password": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": {
    "session_token": <SESSION TOKEN>,
    "session_expiration": <SESSION EXPIRATION>,
    "update_token": <UPDATE TOKEN>
  }
}
```

### 2) Login

<code>POST</code> /api/login/

Request
```
{
  "name": <USER INPUT>,
  "password": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": {
    "session_token": <SESSION TOKEN>,
    "session_expiration": <SESSION EXPIRATION>,
    "update_token": <UPDATE TOKEN>
  }
}
```

### 3) Get all lists

<code>GET</code> /api/lists/

Response
```
{
  "success": true,
  "data": {
    "lists": [<SERIALIZED LIST>, ...]
  }
}
```

### 4) Get list by List ID

<code>GET</code> /api/lists/{list_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "list_name": <USER INPUT>, 
    "events": [<SERIALIZED EVENT>, ...]    
  }
}
```

### 5) Create a list

<code>POST</code> /api/lists/

Request
```
{
  "list_name": <USER INPUT>,
  "is_public": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": {
   "id": <ID>,
   "list_name": <USER INPUT>, 
   "events": []
  }
}
```

### 7) Edit list by List ID
<code> POST </code> /api/lists/{list_id}/

Request
```
{
  "list_name": <USER INPUT>
  "is_public": <USER INPUT>
 }
```
Response
```
{
  "success": true,
  "data": {
   "id": <ID>,
   "list_name": <LIST NAME>, 
   "events": [<SERIALIZED EVENT>, ...]
  }
}
```

### 8) Delete list by List ID
<code> DELETE </code> /api/lists/{list_id}/delete/

Response
```
{
  "success": true,
  "data": {
   "id": <ID>,
   "list_name": <LIST NAME>, 
   "events": [<SERIALIZED EVENT>, ...]
  }
}
```

### 9) Get all events from a specific list
<code> GET </code> /api/lists/{list_id}/events/

Response
```
{
  "success": true,
  "data": {
   "events": [<SERIALIZED EVENT>, ...]
  }
}
```

### 10) Get specific event from specific list

<code>GET</code> /api/lists/{list_id}/events/{event_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "main_title": <MAIN TITLE>,
    "sub_title": <SUB TITLE>,
    "in_progress": <IN PROGRESS>    
  }
}
```

### 11) Create event

<code>POST</code> /api/lists/{list_id}/events/

Request
```
{
  "main_title": <USER INPUT>,
  "sub_title": <USER INPUT>,
  "in_progress": <USER INPUT>
 }
 ```
 
Response
```
{
  "success": true,
  "data": {
   "id": <ID>,
    "main_title": <MAIN TITLE>,
    "sub_title": <SUB TITLE>,
    "in_progress": <IN PROGRESS>    
  }
}
```

### 12) Edit event's details

<code>POST</code> /api/lists/{list_id}/events/{event_id}/

Request
```
{
  "main_title": <USER INPUT>,
  "sub_title": <USER INPUT>,
  "in_progress": <USER INPUT>    
}
```
Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "main_title": <MAIN TITLE>,
    "sub_title": <SUB TITLE>,
    "in_progress": <IN PROGRESS>    
  }
}
```

### 13) Delete event
<code> DELETE </code> /api/lists/{list_id}/events/{event_id}/delete/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "main_title": <MAIN TITLE>,
    "sub_title": <SUB TITLE>,
    "in_progress": <IN PROGRESS>    
  }
}
```

### 14) Send a friend request

<code>POST</code> /api/friends/add/

Request
```
{
  "id": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "name": <NAME>,
    "friends": [<SERIALIZED FRIEND>, ...],
    "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
  }
}
```

### 15) Accept friend request

<code>POST</code> /api/friends/accept/{friend_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "name": <NAME>,
    "friends": [<SERIALIZED FRIEND>, ...],
    "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
  }
}
```

### 16) Reject friend request

<code>POST</code> /api/friends/reject/{friend_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "name": <NAME>,
    "friends": [<SERIALIZED FRIEND>, ...],
    "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
  }
 }
```

### 17) Get pending requests

<code>GET</code> /api/friends/requests/

Response
```
{
  "success": true,
  "data": {
    "requests": [<SERIALIZED FRIEND>, ...]
  }
}
```

### 18) Get friends list

<code>GET</code> /api/friends_lists/

Response
```
{
  "success": true,
  "data": {
    "friends": [<SERIALIZED FRIEND>, ...]
  }
}
```

### 19) Get all items
<code>GET</code> /api/lists/{list_id}/events/{event_id}/items/

Response
```
{
  "success": true,
  "data": {
   "items": [<SERIALIZED ITEM>, ...]
  }
}
```

### 20) Get item by ID
<code>GET</code> /api/lists/{list_id}/events/{event_id}/items/{item_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "event_id": <EVENT ID>,
    "completed": <COMPLETED>,
    "date": <DATE>,
    "title": <TITLE>, 
    "event": {
      "id": <EVENT ID>,
      "main_title": <MAIN TITLE>,
      "sub_title": <SUB TITLE>,
      "in_progress": <IN PROGRESS>
  }
}
```

### 21) Create item

<code>POST</code> /api/lists/{list_id}/events/{event_id}/items/

Request
```
{
  "completed": <USER INPUT>,
  "date": <USER INPUT>,
  "title": <USER INPUT>,
}
```
Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "event_id": <EVENT ID>,
    "completed": <COMPLETED>,
    "date": <DATE>,
    "title": <TITLE>,
  }
}
```

### 22) Edit item

<code>POST</code> /api/lists/{list_id}/events/{event_id}/items/{item_id}/

Request
```
{
  "completed": <USER INPUT>, 
  "date": <USER INPUT>, 
  "title": <USER INPUT>
```
Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "event_id": <EVENT ID>,
    "completed": <COMPLETED>,
    "date": <DATE>,
    "title": <TITLE>
  }
}
```

### 23) Delete item
<code>DELETE</code> /api/lists/{list_id}/events/{event_id}/items/{item_id}/

Response
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "event_id": <EVENT ID>,
    "completed": <COMPLETED>,
    "date": <DATE>,
    "title": <TITLE>
  }
}
```
