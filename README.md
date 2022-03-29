# Python-Docker-Compose
Totally same like docker-compose but in this I wrote queries for creating, inserting of data.
see the file curd.py of this project and see curd.py of docker-compose project.

I guess this is useful when you want to define properties of column like PRIMARY KEY , NOTNULL. 
or when you want to create some custom table.

I also did that that's why Iam sharing. 


## How to Run ? 
Go to project's folder and then just run.

```bash
docker-compose up
```
## Copy generate files in your local directory
###Example

```bash
sudo docker cp <container-id-of-c_app>:/python-docker-compose/output/ /home/vishal/information/test/test2/
```