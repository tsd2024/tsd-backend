# tsd-backend

## Team Members

| Name              | University ID       |
|-------------------|---------------------|
| Julia Mularczyk     | 148062             |
| Miłosz Matuszewski        | 148185             |
| Jan Szczuka      | 148075             |
| Jakub Mrówczyński     | 148068             |

## Required tools
- docker
- docker-compose

## Starting the app
To start the app

```bash
cp template.env .env

docker-compose up --build
```

## Running tests
```bash
docker-compose up -d

docker-compose exec fastapi pytest
```

## Deployment
CI/CD pipeline is configured in a way to showcase what steps are needed to deploy this app to production

1. Build images and push to AWS ECR (Amazon Elastic Container Registry)

2. Copy files from `deployment` directory
3. Run `setup.sh` file that will install docker and docker-compose
4. Run `docker-compose -f docker-compose.prod.yml up`

## Development
If you want to use pycharm to run/debug
- add python interpreter in the settings based on the docker compose ( do it also if you want to have suggestions in pycharm)
- comment/delete entrypoint from docker-compose.yml
- run the app with start button in main.py
- if it doesn't work, changed the working directory to the root of the project in that case tpd-backend
- if container didn't build properly run docker-compose build in the terminal and then use pycharm
- you can update pycharm interpreter by clicking in the bottom right corner name of the interpreter twice
