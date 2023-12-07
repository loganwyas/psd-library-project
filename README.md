# psd-library-project

## Application Overview

This application is a system that contains the catalogs of all libraries. It keeps track of the amount of books, movies, and other materials in these libraries. Users, after logging in, can checkout items in a library's catalog, along with returning those items, from the application. Librarians can additionally add, delete, or modify the items of their libraries. Any user can also change the information in their profile, such as profile picture, name, and password.

## Development Environment

To setup a development environment, you must first clone this repository. Once cloned, you will need to install all of the necessary packages. To get the client packages, go into the "client" folder and run `npm install`. To get the server packages, go into the "server" folder and run `pip install -r requirements.txt`

## Running the application

There are two ways in which the application can be run: command line and Docker. In both cases, the client will be at http://localhost:3001, and the server will be at http://localhost:5001.

### Command Line

We have created a single file that can be used to start the application. Run `bash run_dev_app.sh` in a Git Bash terminal in the root directory of the repository, and both the client and server will be running on their respective ports. If you want the client and server in separate terminal windows, open `run_dev_app.sh` and run each of the commands written in that file.

### Docker

We have Dockerfiles for the application, so it can be run using Docker. To do so, first make sure that Docker is installed and running on your machine. Then, run `docker compose build` to create an image of the application. Finally, run `docker compose up`, and the application should be up and running on their respective ports.
