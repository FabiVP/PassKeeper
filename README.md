# Proyecto de fin de curso PassKeeper
## Descripción
Desarrolla una herramienta para que los usuarios puedan almacenar y gestionar
sus contraseñas de forma segura. El proyecto debe implementar las
funcionalidades básicas de añadir, editar y eliminar contraseñas, asegurando la
protección de los datos con una base de datos SQLite y empleando
contenedores Docker para gestionar el entorno de desarrollo.
## Integrantes 
| Apellidos y nombres | Rol |
|---------------------|-----|
|Chavez Apaza, Marcos Alberto |    Programador    |
|Ñaupari Cmarena, Julio Armando |  Programador      |
|Villaverde Pacheco, Fabiola Karina  |    Programador    |

## Instrucciones
| 1. Clonar el repositorio |
| --------------------- |
| Para comenzar a trabajar con un repositorio remoto, debes clonarlo en tu máquina local. Usa el siguiente comando reemplazando '<URL_DEL_REPOSITORIO>' por la URL del repositorio remoto.|
|                                    |
|    git clone <URL_DEL_REPOSITORIO> |
|                   |
|Por ejemplo, si el repositorio se encuentra en GitHub, la URL podría ser similar a 'https://github.com/usuario/nombre_repositorio.git'. El comando completo sería:|
|                                               |
|    git clone https://github.com/usuario/nombre_repositorio.git   |
|                                    |
|2. Ver las ramas remotas disponibles|
|---------------------|-----|
|Después de clonar el repositorio, puedes listar todas las ramas remotas con el siguiente comando: |
|                      |
|    git branch -r     |
|                              |
|Esto mostrará algo como lo siguiente:   |
|                                  |
|    origin/HEAD -> origin/main    |
|   origin/develop   |
|    origin/main     |
|    origin/release/passkeeper2  |
|                |
|3. Crear ramas locales a partir de ramas remotas|
|---------------------|-----|
|Para trabajar con las ramas remotas, primero debes crear ramas locales que rastreen su correspondiente rama remota. Usa el comando 'git checkout --track' seguido del nombre de la rama| ||remota.                                  |
|                                                        |
|    git checkout --track origin/<nombre_de_la_rama>     |
|                                       |
|Ejemplo para la rama 'develop':        |
|                                       |
|   git checkout --track origin/develop |
|                            |
|Esto crea una nueva rama local llamada 'develop' que rastrea la rama remota 'origin/develop'.|
|4. Verificar las ramas locales disponibles|
|---------------------|-----|
|Para listar todas las ramas locales en tu repositorio, usa el siguiente comando:|
|     |
|   git branch      |
|                       |
|Esto mostrará una lista de ramas locales y marcará con un asterisco (*) la rama actualmente activa.  |
|5. Cambiar entre ramas locales      |
|---------------------|-----|
|Para cambiar a una rama específica, usa el siguiente comando:   |
|                                             |
|    git checkout <nombre_de_la_rama>        |
|              |
|Por ejemplo, para cambiar a la rama 'release/passkeeper2':   |
|                 |
|   git checkout release/passkeeper2        |
|                             |
|Esto cambiará el contenido de tu carpeta local para reflejar el estado de esa rama.|
|6. Manejo de errores comunes |
|---------------------|-----|
|Si cometes un error al escribir un comando, Git te proporcionará sugerencias para corregirlo. Por ejemplo, si escribes 'git brach' en lugar de 'git branch', verás un mensaje como este: |
|                                                 |
|    git: 'brach' is not a git command. See 'git --help'.   |
|                                    |
|    The most similar command is     |
|        branch                      |
|                                        |
|Corrige el comando y vuelve a ejecutarlo.|
|7. Para el funcionamiento de la app|
|---------------------|-----|
|Estando en la rama realease/passkeeper, la cual es la versión final.|
|                           |
|Nos dirigimos al terminal y instalamos :|
|Base de datos SQLalchemy:|
|    pip install sqlalchemy|
|Para las interfaces:|
|   pip install PyQt6|
|Y para el funcionamiento, osea para la vinculación de la app con la base de datos se necesita tener instalado la aplicación SQLite|
|                         |
|SQLiteDatabaseBrowserPortable.exe|
 
