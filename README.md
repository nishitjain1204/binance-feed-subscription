# Real-Time Feed Subscription System with Django Channels and Docker

## Introduction
This project demonstrates a real-time feed subscription system using Django Channels for WebSocket support. Users can subscribe to channel groups to receive live feed updates from the Binance WebSocket API.

## Setup
To run this project, make sure you have Docker installed on your system.

1. Clone the repository:

```bash
   git clone https://github.com/yourusername/realtime-feed-subscription.git
   cd realtime-feed-subscription
```

2. Build and run the Docker image

```bash
docker compose up -d --build
```

## Endpoints

### Users

- `api/register/` - Registers the user and saves it in the system
```bash
curl --location 'http://127.0.0.1:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name" : "test4",
    "password" : "test3",
    "email" : "wdxwdwd@test5.com"

}'
```

- `api/login` - Logs in the user and generates JWT
```bash
curl --location 'http://127.0.0.1:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name" : "test4",
    "password" : "test3",
    "email" : "wdxwdwd@test5.com"

}'
```

- `api/subscribe/` - subscribes user to the channel
```bash
curl --location 'http://127.0.0.1:8000/api/subscribe/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNTA2NDA4LCJpYXQiOjE3MTI1MDI4MDgsImp0aSI6IjE5MjE3MWE5MmQyNTQ4ZmQ4ZmRmMTk3YmI3YjQwODc4IiwidXNlcl9pZCI6ImQzOThmODVlLTIzYWItNDczNC1hMzMwLWJlZDYyODlkYjQxZCJ9.5Db5k1kVgE9njlxFSZHbzvl3dahrJmDAvDG4VGHuibA' \
--header 'Content-Type: application/json' \
--data '{
"channel_group" : "newchannel"
}'
```

- `api/unsubscribe/` - unsubscribes user from the channel
```bash
curl --location 'http://127.0.0.1:8000/api/unsubscribe/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNTA2NDA4LCJpYXQiOjE3MTI1MDI4MDgsImp0aSI6IjE5MjE3MWE5MmQyNTQ4ZmQ4ZmRmMTk3YmI3YjQwODc4IiwidXNlcl9pZCI6ImQzOThmODVlLTIzYWItNDczNC1hMzMwLWJlZDYyODlkYjQxZCJ9.5Db5k1kVgE9njlxFSZHbzvl3dahrJmDAvDG4VGHuibA' \
--header 'Content-Type: application/json' \
--data '{
"channel_group" : "newchannel"
}'
```

- `ws://127.0.0.1:8000/ws/feed/?token=<token>`

  Websocket to access feed from the channel
  If user is subscribed to the channel using subscribe endpoint data stream is received otherwise it stays open

  



