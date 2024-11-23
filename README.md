# fashion_brand_chatbot

## How to Run the Application with Docker Compose

To set up and run the application using Docker Compose, follow these steps:

### Prerequisites
1. Ensure you have Docker installed on your system. You can download it from the [official Docker website](https://www.docker.com/).
2. Install Docker Compose. If you have Docker Desktop installed, Docker Compose is already included. Check your installation by running:
   ```
   docker-compose --version
   ```

### Steps to Run
1. open the docker desktop 
2. Start the services defined in the `docker-compose.yml` file by running:
   ```
   docker compose -f "docker-compose.yml" up -d --build
   ```


### Stopping the Services
run:
```
docker compose -f "docker-compose.yml" down 
```


### Note
the pgadmin is to view the database, run on [localhost 5050](http://localhost:5050/)
the app is the api, run on [localhost 8080](http://localhost:8000/)

