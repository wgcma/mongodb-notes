
This runs a MongoDB container and connects to it using `mongosh`.

```
docker run -d --name mongo-practice -p 27017:27017 mongo:latest

docker exec -it mongo-practice mongosh
```
