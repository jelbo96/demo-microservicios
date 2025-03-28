# Servicio-3

Solicitudes curl para probar:

````bash
curl --location 'http://localhost:8083/challenge/process' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ytzYuziC6RyIsvkIoXRmS9CXTv1OC0Yc' \
--data '{
           "version": 1,
           "timeSearch": "2d"
         }'
```bash

```bash
         curl --location 'http://localhost:8083/challenge/search' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ytzYuziC6RyIsvkIoXRmS9CXTv1OC0Yc' \
--data '{
           "version": 1,
           "type": "BAJA",
           "sended": false
         }'
````

```bash
         curl --location 'http://localhost:8083/challenge/send' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ytzYuziC6RyIsvkIoXRmS9CXTv1OC0Yc' \
--data '{
           "version": 1,
           "type": "BAJA"
         }'
```
