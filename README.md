# Descripción
Encontrar cuántos números primos hay en los primeros k números usando un proceso paralelo con un número variable de trabajadores. La verificación se realiza en paquetes de 100 números. K tiene que ser leído como un argumento.

La salida debe ser:

· El número de primos (salida de root).

· El tiempo de ejecución en segundos (salida de root).

· El número de paquetes que verificó cada proceso (esta salida debe ser dada por cada proceso).

La implementación en paralelo debe seguir la siguiente lógica para n procesos:

1. Distribuir un paquete en cada proceso mediante mensajes (el root solo será administrador)

2. Cada proceso recibe el paquete, realiza la validación y envía el total de primos encontrados en el paquete al root.

3. Cuando el root recibe el resultado de un proceso debe enviarle inmediatamente otro paquete para procesar

Los pasos 2 y 3 se deben ejecutar mientras que el root tenga paquetes por validar.

# Instalación
Desplazate a la carpeta donde tienes almacenado el proyecto en la terminal, y luego ejecuta el siguiente comando dependiendo de tu plataforma

En windows
`docker run -d -it --name mpi -v ${pwd}/target:/app augustosalazar/un_mpi_image:v4`

En linux
`docker run -d -it --name mpi -v "$(pwd)"/target:/app augustosalazar/un_mpi_image:v4`

# Ejecución

`docker exec -it mpi mpiexec  --oversubscribe --allow-run-as-root -n <trabajdores> python /app/primerCheckerG7.py <k>`

**Debes reemplazar <trabajadores> con el número de trabajdores que deseas y <k> con el número hasta el cual deseas buscar primos**