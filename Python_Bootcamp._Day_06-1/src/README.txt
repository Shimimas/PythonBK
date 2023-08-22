python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. recommendations.proto

sudo docker pull postgres
sudo docker run -p 0.0.0.0:5432:5432 -it --rm --name selectel-pgdocker -e POSTGRES_PASSWORD=selectel -e POSTGRES_USER=selectel -e POSTGRES_DB=selectel postgres
python3 create_tables.py