docker run -d --rm -p 5672:5672 --hostname my-rabbit --name some-rabbit rabbitmq:3-alpine

Notas:
la version alpine es más ligera en espacio
--rm para eliminar el contenedor
-p para conectar los puertos de mi máquina con los de docker
Importante el -d para que tengamos un daemon
le ponermos el nomber some-rabbit para hacer
docker logs --tail 100 some-rabbit

docker inspect some-rabbit para sacar la IP y ver los puertos expuestos
docker exec -it some-rabbit <orden> para entrar en un contenedor
