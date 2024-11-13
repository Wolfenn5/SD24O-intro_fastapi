from fastapi import FastAPI
from bd_biblioteca import libros, usuarios
from pydantic import BaseModel #BaseModel para tablas

# /docs para la interfaz de fast api -> 127.0.0.../docs
# Una operacion idempotente en si se cosidera un evento, por ejemplo un get siempre va a dar lo mismo
# en este caso el borrado igual va a devolver "Elemento borrado" siempre, solo la primera vez hara el borrado
# A excepcion del post si va a dar algo diferente cada vez que se ejecute, por eso es no idempotente

# El parametro de ruta es '/algo' -> http:/distribuidos.com/algo
# El parametro de cuerpo es como el que esta en    def insertar_libro(libro:LibroBase):
# El orden de los parametros SIEMPRE es primero el de ruta y luego el de cuerpo 


app = FastAPI()

#Metodo: GET
#URL; '/'
@app.get('/') # esta diagonal es el recurso (source)
def bienvenida():
    print("Atendiendo GET / ")
    respuesta = {"mensaje": "Bienvenido"}
    return respuesta

#Metodo Get
#URL '/libros'
#devuelva la lista de libros
@app.get('/libros')
def lista_libros():
    print("Atendiendo GET '/libros'")
    respuesta = libros
    return respuesta

#Metodo GET
#URL '/libros/{id}'
#devuelve un json
#parametro de ruta id
@app.get('/libros/{id}')
def informacion_libro(id:int):
    print("Atendiendo GET /libros/",id)
    if id >=0 and id <=len(libros)-1:
        respuesta = libros[id]
    else:
        respuesta = {
            "mensaje":"El libro no existe"
        }
    return respuesta


#Metodo DELETE
#URL '/libros/{id}'
#devuelve un mensaje
#parametro de ruta id
@app.delete('/libros/{id}')
def borra_libro(id:int):
    if id >=0 and id <=len(libros)-1:
        del libros[id] # del borra de una lista
    respuesta={
        "mensaje":"Elemento borrado"
    }
    return respuesta


#Metodo GET de lista usuarios
@app.get('/usuarios')
def lista_usuarios():
    print("Atendiendo GET '/usuarios'")
    respuesta = usuarios
    return respuesta


#Metodo GET de un solo usuario
@app.get('/usuarios/{id}')
def informacion_usuario(id:int):
    print("Atendiendo GET /usuarios/",id)
    if id >=0 and id <=len(usuarios)-1:
        respuesta = usuarios[id]
    else:
        respuesta = {
            "mensaje":"El usuario no existe"
        }
    return respuesta

#Metodo DELETE de un solo usuario {id}
@app.delete('/usuarios/{id}')
def borra_usuario(id:int):
    if id >=0 and id <=len(usuarios)-1:
        del usuarios[id] # del borra de una lista
    respuesta={
        "mensaje":"Usuario borrado"
    }
    return respuesta


# Mapear los recursos 

# Para mapear libros
# La llave (primary key) no se mapea
# con el =1 y =True indica que esos siempre van a estar por default
class LibroBase(BaseModel): # clase base que mapea 
    #id_libro#
    titulo:str
    unidades:int=1
    autor:str
    unidades_disponibles:bool=True


# Para mapear prestamos
class UsuarioBase(BaseModel):
    #id_usuario#
    nombre:str
    direccion:str

# Metodo Post para insertar un nuevo libro
# URL '/libros'
# Parametros de cuerpo (viajan en el cuerpo del mensaje http)
@app.post('/libros')
def insertar_libro(libro:LibroBase): # crea un libro de tipo LibroBase
    print("Insertando un nuevo libro")
    libro_nuevo = {} # diccionario para insertar libro nuevo
    # partes de las que consta el libro
    libro_nuevo['titulo'] = libro.titulo
    libro_nuevo['unidades'] = libro.unidades
    libro_nuevo['autor'] = libro.autor
    libro_nuevo['unidades_disponibles'] = libro.unidades_disponibles
    libro_nuevo['id'] = len(libros) # inventado para que la longitud sea el id
    libros.append(libro_nuevo) # append para insertar
    return libro_nuevo # aunque en varias ocasiones se recomienda que devuelva el id



# Metodo Post para insertar un usario nuevo
@app.post('/usuarios')
def insertar_usuario(usuario:UsuarioBase):
    print("Insertando un nuevo libro")
    usuario_nuevo = {} # diccionario para insertar libro nuevo
    # partes de las que consta el libro
    usuario_nuevo['nombre'] = usuario.nombre
    usuario_nuevo['direccion'] = usuario.direccion
    usuario_nuevo['id'] = len(usuarios) # inventado para que la longitud sea el id
    usuarios.append(usuario_nuevo) # append para insertar
    return usuario_nuevo # aunque en varias ocasiones se recomienda que devuelva el id



# Metodo PUT para actualizar
# URL 'libros/{id}'
@app.put('/libros/{id}')
def actualizar_disponibilidad_libro(id:int, libro:LibroBase): # primero se pone el parametro de ruta y despues el de cuerpo SIEMPRE el id y el objeto que contiene todo lo de libros
    # libros[id] en si es un libro de la BD
    # libro es la informacion nueva que manda el usuario
    libros[id].titulo = libro.titulo
    libros[id].autor = libro.autor
    libros[id].unidades = libro.unidades
    libros[id].unidades_disponibles = libro.unidades_disponibles
    respuesta = {
        "mensaje": "Se actualizo la disponibilidad" + id
    }
    return respuesta