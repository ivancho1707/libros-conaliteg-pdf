# Script de descarga para libros CONALITEG

1. Acerca del proyecto
    1. Motivación
    1. ¿Qué es un PDF indexado?
    1. ¿Cómo funciona este proyecto?
1. Uso del script
    1. Preparación del ambiente de ejecución
        1. Docker (recomendado)
        1. Manual
1. Licencias
    1. Este proyecto
    1. Libros de texto CONALITEG
        1. Renuncia legal



## Acerca del proyecto

Esta es una utilidad de línea de comando escrita en Python para 
descargar en formato PDF indexado los libros de texto gratuitos 
que la CONALITEG liberó en línea para el uso personal de los 
ciudadanos.

### Motivación

El [material liberado por la CONALITEG](https://www.gob.mx/conaliteg/articulos/conoce-el-catalogo-historico-de-los-libros-de-texto-gratuitos) 
es un esfuerzo valiosísimo en
términos educativos ya que documenta la evolución de la educación
pública en México y junto con la evolución de la ideosincracia y 
nececidades de sociedad méxicana.

No obstante, esta información está limitada ya que consiste de 
imágenes de cada una de las páginas de los libros de texto, con 
las que el lector no puede interactuar como lo haría con cualquier
otro material digital y tampoco tiene esa comodidad e intimidad que
ofrece un sostener en su manos un libro tradicional.

Estas obras entonces, no pueden ser consumidas por los usuarios de 
internet como lo acostumbran, aprovechando las herramientas a su
alcance que les permiten interactuar de manera más eficiente con la
información, desperdiciándose así la gran oportunidad de incorporar
a sus hábitos de aprendizaje éstos materiales de gran calidad.

### ¿Qué es un PDF indexado?

Un PDF indexado es un término coloquial en el internet que se le da
a un documento que a pesar de no estar originalmente compuesto de
texto, como en este caso scans de un libro, contiene la información
adjunta de los textos en lás imágenes permitiendo así al usuario
búscar, citar e interactuar con ellos.

Otra ventaja es que este formato permite la integración con varias
funciones de sistemas operativos como la búsqueda de definiciones de
palabras, y de accesibilidad para las personas con algún grado de 
debilidad visual, como indicar al ordenador leer el texto en voz alta.

### ¿Cómo funciona este proyecto?

Para lograr su cometido, este trabajo utiliza del una técnica llamada
Reconocimiento Óptico de Carácteres (OCR) para obtener texto contenido
en una imagen de manera precisa, descartando cualquier ambiguedad.

Ésto se logra por medio de varios procedimientos intermedios como 
el procesamiento dígital de imágenes, para limpiar la imágen; 
la inteligencia artificial, para detectar la presencia de patrones
que puedan ser interpretados como caracteres; algoritmos estadísticos 
y bases de datos de idiomas, para identificar con exactitud palabras
y secuencias de éstas que formen enunciadops coherentes.

Las tecnologías necesarias para este fin son proveídas en su mayoría
por bibliotecas de software libre.

## Uso del script

Este script ha sido desarrollado en Python, sin embargo se apoya en
dependencias otras que no son bibliotecas de python como es Tesseract
y su extensión de lenguaje español, los cuales necesitan ser
instalados por sus métodos correspondientes. 

### Preparación del ambiente de ejecución

Para ejecutar el script, se necesita la instalación de todas sus 
dependencias. A continuación se detallan 2 posibilidades

#### Docker (recomendado)

**Nota:** Se requiere de una instalación de Docker en su equipo 
para proceder.

Con el uso de una imagen de Docker que contiene las dependencias
necesarias instaladas se puede ejecutar el script de forma 
sencilla sin tener que instalar nada en el sistema operativo 
anfitrión.

Para descargar esta imagen, ejecute la siguiente instrucción en 
su línea de comandos:

```
docker pull ivancho1707/libros-conaliteg-pdf
```

Debido a las nuevas políticas de Docker Hub, la imagen pudiera
no estar disponible si no es usada en 90 días. Si este es el caso,
usted mismo puede construirla clonando este repositorio, o bien
descargando el archivo `Dockerfile` en el directorio principal de
este repositorio y ejecutando la siguiente instrucción desde el
directorio que contiene el archivo:

```
docker build -t ivancho1707/libros-conaliteg-pdf:1.0 -f Dockerfile . 
```

Una vez obtenida la imagen, ejecute la siguiente línea para correr
el script:

```
docker run -it --rm -v ${PWD}:/conaliteg/ ivancho1707/libros-conaliteg-pdf:1.0
```

Tome en cuenta que desde la ubicación en la que se ejecute este 
comando, se creará un directorio llamado `output` con la su nuevo
PDF indexado de terminar éxitosamente con la ejecución del
programa.

#### Manual

Clone este repositorio con git e instale en su sistema las 
siguientes aplicaciones:

* Python 3.6 o superior
* Ghostscript 9.15 o superior
* qpdf 8.1.0 o superior
* Tesseract 4.0.0-beta o superior
* Extensión del lenguaje Español de Tesseract

Posteriormente instale las dependencias de Python desde el 
directorio raíz del proyecto con el siguiente comando desde
su terminal:

```
pip3 install -r requirements.txt
```

finalmente ejecute el escript desde el mismo directorio con:

```
python3 main.py
```

## Licencias
### Este proyecto

Este proyecto tiene siguiente licencia:

```
Licensed under Creative Commons Attribution-ShareAlike 4.0.
```

### Libros de texto CONALITEG

Los derechos de los libros de texto son propiedad exclusiva de
la Comisión Nacional de Libros de Texto Gratuitos (CONALITEG) y
las entidades o personas a las que dicho organismo endose los
correspondientes derechos.

Para consultar la información especifica de cada libro refiérase 
a su respectiva portada.

#### Renuncia legal

El autor de esta herramienta no está afiliado con la CONALITEG 
o ninguna otra entidad involucrada en la elaboración de estos 
materiales educativos, ni posee los derechos sobre la obra, 
tampoco almacena, replica o distribuye ninguno de sus materiales
fuera de lo especifcado como uso justo (Fair Use)

Está estrictamente prohibida la venta, distribución o reproducción
impresa o digital, total o parcial de cualquiera de los materiales
de la CONALITEG. 

El lucrar con libros de texto gratuitos es un delito federal 
que se paga con incluso con cárcel. CUIDADO: Si usted paga por una
copia digital, está participado en un delito.
