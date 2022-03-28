# Build and run api
```bash
docker-compose up -d
docker exec -it dailymotion_api dailymotion/scripts/initdb.py
```

# Openapi docs
http://<your_ip_address>:8090/docs

# Mail server
http://<your_ip_address>:8025

# Remove app 
docker-compose down
docker volume rm dailymotion_pgdata