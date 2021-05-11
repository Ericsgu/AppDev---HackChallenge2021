# AppDev---HackChallenge2021
## API Specification
### Base Endpoint: letsdoit21.herokuapp.com

### 1) Register User


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
  "data": [
    {
      "session_token": <SESSION TOKEN>,
      "session_expiration": <SESSION EXPIRATION>,
      "update_token": <UPDATE TOKEN>
    }
  ]
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
  "data": [
    {
      "session_token": <SESSION TOKEN>,
      "session_expiration": <SESSION EXPIRATION>,
      "update_token": <UPDATE TOKEN>
    }
  ]
}
```

### 3) Get Friends List

<code>GET</code> /api/friends_lists/

Response
```
{
  "success": true,
  "data": [
    {
      "friends": [<SERIALIZED FRIEND>, ...]
    }
  ]
}
```

### 4) Get User's Lists

<code>GET</code> /api/lists/

Response
```
{
  "success": true,
  "data": [
    {
      "lists": [<SERIALIZED LIST>, ...]
    }
  ]
}
```

### 5) Get Specific List by List ID

<code>GET</code> /api/lists/{list_id}/

Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "events": [<SERIALIZED EVENT>, ...]    
     }
  ]
}
```

### 6) Create a List

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
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "events": []
    }
  ]
}
```

### 7) Delete List by List ID
<code> DELETE </code> /api/lists/{list_id}/delete/

Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "events": [<SERIALIZED EVENT>, ...]
    }
  ]
}
```

### 8) Edit List by List ID
<code> POST </code> /api/lists/{list_id}/

Request
```
{
  "list_name": <USER INPUT>
  "is_public": <USER INPUT>
```
Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "events": [<SERIALIZED EVENT>, ...]
    }
  ]
}
```

### 9) Get Event from Specific List by ID

<code>GET</code> /api/lists/{list_id}/events/{event_id}/

Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
      "main_title": <MAIN TITLE>,
      "sub_title": <SUB TITLE>,
      "in_progress": <IN PROGRESS>    
    }
  ]
}
```

### 10) Edit Specific Event's Details

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
  "data": [
    {
      "id": <ID>,
      "main_title": <MAIN TITLE>,
      "sub_title": <SUB TITLE>,
      "in_progress": <IN PROGRESS>    
    }
  ]
}
```

### 11) Send a Friend Request

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
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIEND>, ...],
      "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
    }
  ]
}
```

### 12) Accept Friend Request from Friend ID

<code>POST</code> /api/friends/accept/{friend_id}/

Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIEND>, ...],
      "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
    }
  ]
}
```

### 13) Reject Friend Request from Friend ID

<code>POST</code> /api/friends/reject/{friend_id}/

Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIEND>, ...],
      "public_lists": [<SERIALIZED PUBLIC LIST>, ...]
    }
  ]
}
```

### 14) Get Pending Requests

<code>GET</code> /api/friends/requests/

Response
```
{
  "success": true,
  "data": [
    {
      "requests": [<SERIALIZED FRIEND>, ...]
    }
  ]
}
```

### 15) Create an Item

<code>POST</code> /api/<int:id>/lists/<int:list_id>/events/<int:event_id>/item/

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
  "data": [
    {
     
      "id": <ID>,
      "completed": <COMPLETED>,
      "date": <DATE>,
      "title": <TITLE>,
      "event_id": <EVENT_ID>        
    }
  ]
}
```

### 16) Get Item from Specific List and Spefic Event by ID

<code>GET</code> /api/<int:id>/lists/<int:list_id>/events/<int:event_id>/items/<int:item_id>

Response
```
{
  "success": true,
  "data": [
    {
     
      "id": <ID>,
      "completed": <COMPLETED>,
      "date": <DATE>,
      "title": <TITLE>,
      "event_id": <EVENT_ID>        
    }
  ]
}
```

### 17) Edit Specific Item's Details

<code>POST</code> /api/<int:id>/lists/<int:list_id>/events/<int:event_id>/items/<int:item_id>

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
  "data": [
    {
     
      "id": <ID>,
      "completed": <COMPLETED>,
      "date": <DATE>,
      "title": <TITLE>,
      "event_id": <EVENT_ID>        
    }
  ]
}
```
