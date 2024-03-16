# tsd-backend

To start the app

- copy template.env to .env
- copy template.docker-compose.yml to docker-compose.yml
- run `docker-compose up --build`

To add a new package
- add to requirements.in
- run ./compile-requirements.sh
- run `docker-compose up --build`

If you want to use pycharm to run/debug
- add python interpreter in the settings based on the docker compose ( do it also if you want to have suggestions in pycharm)
- comment/delete entrypoint from docker-compose.yml
- run the app with start button in main.py
- if it doesn't work, changed the working directory to the root of the project in that case tpd-backend
- if container didn't build properly run docker-compose build in the terminal and then use pycharm
- you can update pycharm interpreter by clicking in the bottom right corner name of the interpreter twice

To run tests
- TODO
