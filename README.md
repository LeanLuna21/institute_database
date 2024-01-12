Aplicacion BBDD alumnos

Bienvenido!
Esta es una app de escritorio pensada para manejar la base de datos de un instituto en el que una vez trabaje. La idea es poder llevar a cabo el proceso de pagos de los alumnos. Mediante la app, se puede ver que alumnos forman parte de la institucion, a que curso pertence cada uno, los precios y horarios de dichos cursos, los meses que el alumno adeuda en caso que asi sea, y los datos mas relevantes de los alumnos.
El administrador/a podra Buscar, Actualizar, Agregar, y Borrar registros y a su vez, registrar los pagos de los alumnos en la BBDD, e imprimir el comprobante de pago.


El primer paso para poder ejecutar la app, deberás descomprimir el archivo a un directorio con el nombre de tu preferencia.

En segundo lugar, y antes de ejecutar la app, será necesario instalar una serie de paquetes que la app va a necesitar para correr, por ej: pandas, jinja2, pdfkit... Para ello, recomendamos crear un virtual environment, y ejecutar el comando  << pip install -r requirements.py >> en tu carpeta de proyecto.

Una vez hecho eso, debemos instalar "wkhtmltopdf", que es una libreria open source que permite transformar un documento html(en el que creamos la factura) en un archivo .pdf para su posterior impresion. Para ello, debemos seguir los pasos en el documento "pasos-para-invoice.txt"

Para poder montar la app a un archivo ejecutable .exe, seguir los pasos en el documento  "pasos-para-el-exe.txt"

Para poder ejecutar la app, lo primero que debemos hacer es entrar en la carpeta de 'resources' y cargar los archivos .csv del cual extraeremos a informacion.
Los archivos deben ser 4 y sus nombres y contenido debe ser el siguiente:

1. alumnos.csv -> Contiene informacion de los alumnos. Se necesitará:
    - legajo
    - apellido
    - nombre 
    - telefono
    - dni
    - curso (id)

2. cursos.csv -> Contiene informacion de los cursos. Se necesitará:
    - id (nro)
    - nombre
    - precio 
    - profesor (id)

3. profesores.csv -> Contiene informacion de los profesores. Se necesitará::
    - id (nro)
    - apellido
    - nombre
    - telefono
    - mail

4. pagos.csv -> Contiene informacion sobre los pagos realizados o no realizados de los alumnos. Se necesitara:
    - legajo
    - curso (id)
    - valor de fotocopias
    - una columna por cada mes del año (January to December)

Una vez cargados los .csv, ejecutar por consola, dentro de la carpeta correspondiete, el archivo db_test.py. (Esto hara que esos documentos .csv se carguen en la BBDD a usar.)

