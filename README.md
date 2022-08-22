# SocialNetwork

## Social Network Application

### Installation
In terminal:

```git clone https://https://github.com/arttre/SocialNetwork.git -b main``` -- installing repository

```cd StarNaviProject``` -- moving to a _main directory_

### Run with Docker
Inside _main directory_:

```docker-compose build``` -- building docker images

```docker-compose up``` -- running our images

If any problems uccur, simply use ```Ctrl+C``` command and rerun ```docker-compose up``` command.

Here it is, now you can work with application, using ```http://127.0.0.1:8000/docs``` url.

### Run without Docker
Use a virual environment.

```pip install -r requirements.txt``` -- installing all requirements

*_pip_ must be installed.

Inside _main directory_:
```python3 -m uvicorn main:app```
to run our local server.

After that you can use ```http://127.0.0.1:8000/docs``` link to get API access.

*of course, _python3_ must be installed.

### Additional information

You can change MYSQL credentials in .env file.

Use ```http://127.0.0.1:8080/docs``` link to get database access throughout _phpmyadmin_.
