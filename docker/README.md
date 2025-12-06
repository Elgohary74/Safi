After changing any part of `docker-compose.yml` file, make sure to run those lines:

```bash
cd docker

# stop any running containers, if there is no running ones, an error will arise
sudo docker stop $(sudo docker ps -aq)

# remove containers from system, if there is no running containers, an error will arise
sudo docker rm $(sudo docker ps -aq)

# remove any downloaded images
sudo docker rmi $(sudo docker images -q)

# remove all volumes
sudo docker volume rm $(sudo docker volume ls -q)
 
sudo docker system prune --all

# After finishing
sudo docker compose up -d
```
