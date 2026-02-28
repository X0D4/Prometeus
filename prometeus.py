import asyncio
import re
import discord
from discord.ext import commands
import math
import random
import sqlite3

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect('operaciones.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS operaciones
             (nombre TEXT PRIMARY KEY, operacion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')


c.execute('''CREATE TABLE IF NOT EXISTS personajes
             (nombre TEXT PRIMARY KEY, raza TEXT, nombre_del_personaje TEXT, dificultad TEXT, vida INTEGER, energia INTEGER, poder_magico INTEGER, fuerza INTEGER, velocidad INTEGER, inteligencia INTEGER, alma INTEGER, cordura INTEGER, precision INTEGER, sigilo INTEGER, percepcion INTEGER, stamina INTEGER)''')


conn.commit()



parametros = {
    "humano": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (50, 100),
            "energia": 2,
            "poder_magico": (1, 8),
            "fuerza": (10, 35),
            "velocidad": 2,
            "inteligencia": (40, 70),
            "alma": (2),
            "cordura": 10,
            "precision": (0),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
            
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (90, 110),
            "energia": (2),
            "poder_magico": (1, 10),
            "fuerza": (20, 40),
            "velocidad": 2,
            "inteligencia": (60, 80),
            "alma": (2,3),
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (140, 160),
            "energia": 2,
            "poder_magico": (30, 40),
            "fuerza": (40, 60),
            "velocidad": (2, 4),
            "inteligencia": (70, 110),
            "alma": (3, 5),
            "cordura": 10,
            "precision": (0, 50),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (300, 1200),
            "energia": (12, 25),
            "poder_magico": (70, 1000),
            "fuerza": (130, 1000),
            "velocidad": (2, 20),
            "inteligencia": (90, 150),
            "alma": (5,15),
            "cordura": 10,
            "precision": (0, 300),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (500, 2000),
            "energia": (15, 50),
            "poder_magico": (350, 1500),
            "fuerza": (500, 1500),
            "velocidad": (2, 40),
            "inteligencia": (90, 150),
            "alma": (5,50),
            "cordura": 10,
            "precision": (0, 500),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
    },
    "driade": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (50, 100),
            "energia": 2,
            "poder_magico": (1, 8),
            "fuerza": (10, 35),
            "velocidad": 2,
            "inteligencia": (40, 70),
            "alma": 2,
            "cordura": 10,
            "precision": (0),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (90, 110),
            "energia": (2),
            "poder_magico": (1, 10),
            "fuerza": (20, 40),
            "velocidad": 2,
            "inteligencia": (60, 80),
            "alma": (2,3),
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (140, 160),
            "energia": 2,
            "poder_magico": (30, 40),
            "fuerza": (40, 60),
            "velocidad": (2, 4),
            "inteligencia": (70, 110),
            "alma": (3, 5),
            "cordura": 10,
            "precision": (0, 50),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (300, 1200),
            "energia": (12, 25),
            "poder_magico": (70, 1000),
            "fuerza": (130, 1000),
            "velocidad": (2, 20),
            "inteligencia": (90, 150),
            "alma": (5,15),
            "cordura": 10,
            "precision": (0, 300),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (500, 2000),
            "energia": (15, 50),
            "poder_magico": (350, 1500),
            "fuerza": (500, 1500),
            "velocidad": (2, 40),
            "inteligencia": (90, 150),
            "alma": (5,50),
            "cordura": 10,
            "precision": (0, 500),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
    },
    "aziward": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (50, 100),
            "energia": 2,
            "poder_magico": (1, 8),
            "fuerza": (10, 35),
            "velocidad": 2,
            "inteligencia": (40, 70),
            "alma": 2,
            "cordura": 10,
            "precision": (0),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (90, 110),
            "energia": (2),
            "poder_magico": (1, 10),
            "fuerza": (20, 40),
            "velocidad": 2,
            "inteligencia": (60, 80),
            "alma": (2,3),
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (140, 160),
            "energia": 2,
            "poder_magico": (30, 40),
            "fuerza": (40, 60),
            "velocidad": (2, 4),
            "inteligencia": (70, 110),
            "alma": (3, 5),
            "cordura": 10,
            "precision": (0, 50),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (300, 1200),
            "energia": (12, 25),
            "poder_magico": (70, 1000),
            "fuerza": (130, 1000),
            "velocidad": (2, 20),
            "inteligencia": (90, 150),
            "alma": (5,15),
            "cordura": 10,
            "precision": (0, 300),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (500, 2000),
            "energia": (15, 50),
            "poder_magico": (350, 1500),
            "fuerza": (500, 1500),
            "velocidad": (2, 40),
            "inteligencia": (90, 150),
            "alma": (5,50),
            "cordura": 10,
            "precision": (0, 500),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
    },
    "ascendido": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (20, 30),
            "energia": (2),
            "poder_magico": (20, 40),
            "fuerza": (5, 15),
            "velocidad": (2),
            "inteligencia": (60, 70),
            "alma": (3),
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (20, 40),
            "energia": 2,
            "poder_magico": (25, 60),
            "fuerza": (10, 25),
            "velocidad": 2,
            "inteligencia": (70, 80),
            "alma": 3,
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0),
            "percepcion": (0),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (50, 90),
            "energia": 2,
            "poder_magico": (40, 120),
            "fuerza": (25, 50),
            "velocidad": 2,
            "inteligencia": (70, 120),
            "alma": 3,
            "cordura": 10,
            "precision": (0, 250),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (275, 700),
            "energia": (15, 40),
            "poder_magico": (250, 1500),
            "fuerza": (120, 300),
            "velocidad": (2, 20),
            "inteligencia": (80, 160),
            "alma": (5,20),
            "cordura": 10,
            "precision": (250, 500),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (400, 1000),
            "energia": (35, 150),
            "poder_magico": (500, 2000),
            "fuerza": (150, 500),
            "velocidad": (2, 20),
            "inteligencia": (90, 170),
            "alma": (5,50),
            "cordura": 10,
            "precision": (1000, 4000),
            "sigilo": (0, 50),
            "percepcion": (0, 100),
            "stamina": (10),
        },
    },
    "condenado": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (100, 120),
            "energia": (0),
            "poder_magico": (0),
            "fuerza": (45, 60),
            "velocidad": (2),
            "inteligencia": (20, 70),
            "alma": (2),
            "cordura": 10,
            "precision": (0),
            "sigilo": (0, 20),
            "percepcion": (0),
            "stamina": (10),
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (120, 140),
            "energia": 0,
            "poder_magico": (0),
            "fuerza": (60, 80),
            "velocidad": 2,
            "inteligencia": (60, 80),
            "alma": 2,
            "cordura": 10,
            "precision": (0),
            "sigilo": (0, 20),
            "percepcion": (0),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (140, 200),
            "energia": 1,
            "poder_magico": (0, 20),
            "fuerza": (80, 150),
            "velocidad": 2,
            "inteligencia": (70, 80),
            "alma": 3,
            "cordura": 10,
            "precision": (0, 50),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (300, 1200),
            "energia": (2, 5),
            "poder_magico": (25, 100),
            "fuerza": (300, 900),
            "velocidad": (2, 20),
            "inteligencia": (80, 100),
            "alma": (5,20),
            "cordura": 10,
            "precision": (0, 200),
            "sigilo": (0, 80),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (1000, 4000),
            "energia": (10, 20),
            "poder_magico": (50, 200),
            "fuerza": (1200, 2400),
            "velocidad": (2, 20),
            "inteligencia": (90, 120),
            "alma": (5,30),
            "cordura": 10,
            "precision": (0, 300),
            "sigilo": (0, 100),
            "percepcion": (0, 20),
            "stamina": (10),
        },
    },
    "vampiro": {
        "muy_facil": {
            "nombre_del_personaje": "default",
            "vida": (20, 40),
            "energia": (2),
            "poder_magico": (15, 20),
            "fuerza": (25, 30),
            "velocidad": (2),
            "inteligencia": (80, 120),
            "alma": (2),
            "cordura": 10,
            "precision": (0, 20),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "facil": {
            "nombre_del_personaje": "default",
            "vida": (40, 80),
            "energia": (2),
            "poder_magico": (20, 35),
            "fuerza": (30, 50),
            "velocidad": (2),
            "inteligencia": (100, 140),
            "alma": (2),
            "cordura": 12,
            "precision": (0, 20),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "normal": {
            "nombre_del_personaje": "default",
            "vida": (100, 150),
            "energia": (2),
            "poder_magico": (40, 60),
            "fuerza": (40, 60),
            "velocidad": (2),
            "inteligencia": (120, 180),
            "alma": (3),
            "cordura": 14,
            "precision": (0, 20),
            "sigilo": (0, 20),
            "percepcion": (0, 20),
            "stamina": (10),
        },
        "dificil": {
            "nombre_del_personaje": "default",
            "vida": (300, 1000),
            "energia": (10, 30),
            "poder_magico": (100, 500),
            "fuerza": (100, 500),
            "velocidad": (2, 10),
            "inteligencia": (180, 250),
            "alma": (5,20),
            "cordura": 16,
            "precision": (0, 300),
            "sigilo": (0, 50),
            "percepcion": (0, 50),
            "stamina": (10),
        },
        "muy_dificil": {
            "nombre_del_personaje": "default",
            "vida": (500, 2000),
            "energia": (10, 20),
            "poder_magico": (50, 200),
            "fuerza": (1200, 2400),
            "velocidad": (2, 20),
            "inteligencia": (90, 120),
            "alma": (5,30),
            "cordura": 10,
            "precision": (0, 300),
            "sigilo": (0, 100),
            "percepcion": (0, 20),
            "stamina": (10),
        },
    },
}

def obtener_personaje(nombre):
    # Primero intentar buscar por el nombre del personaje
    personaje = c.execute("SELECT * FROM personajes WHERE nombre_del_personaje=?", (nombre,)).fetchone()
    # Si no se encontró ningún personaje, intentar buscar por la raza
    if not personaje:
        personaje = c.execute("SELECT * FROM personajes WHERE nombre=?", (nombre,)).fetchone()
    return personaje


@bot.event
async def on_ready():
    print(f'Estamos conectados como {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Ocurrió un error: {str(error)}')

@bot.command(aliases=['c'])
async def calcular(ctx, *args):
    try:
        operaciones = [c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (arg,)).fetchone()[0] if c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (arg,)).fetchone() else arg for arg in args]
        operacion = " ".join(operaciones)
        resultado = eval(operacion)
        await ctx.send(f"El resultado es: {resultado}")
    except Exception as e:
        await ctx.send(f"Error al calcular la operación.")


@bot.command(aliases=['g'])
async def guardar(ctx, nombre: str, *, operacion: str):
    try:
        if "dado" in operacion:
            c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (nombre, operacion))
            conn.commit()
            await ctx.send(f'Dado guardado bajo el nombre: {nombre}')
        else:
            c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (nombre, operacion))
            conn.commit()
            await ctx.send(f'Operación guardada bajo el nombre: {nombre}')
    except:
        await ctx.send(f'Error al guardar la operación.')

@bot.command(aliases=['v'])
async def ver(ctx, nombre: str):
    operacion = c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (nombre,)).fetchone()
    if operacion:
        await ctx.send(f'La operación guardada "{nombre}" es: {operacion[0]}')
    else:
        await ctx.send(f'No se encontró ninguna operación guardada con el nombre: {nombre}')

@bot.command(aliases=['s'])
async def sobreescribir(ctx, nombre: str):
    # Recuperar la operación guardada
    operacion_guardada = c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (nombre,)).fetchone()
    if operacion_guardada:
        # Solicitar al usuario que escriba el nuevo dado
        await ctx.send('Escribe el nuevo dado.')
        try:
            # Esperar a que el usuario escriba el nuevo dado
            msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
            # Extraer el nuevo nombre y la nueva operación del mensaje del usuario
            nuevo_nombre, nueva_operacion = msg.content.split(' ', 1)
            # Sobreescribir la operación guardada
            c.execute("UPDATE operaciones SET nombre=?, operacion=? WHERE nombre=?", (nuevo_nombre, nueva_operacion, nombre))
            conn.commit()
            await ctx.send(f'El dado "{nombre}" ha sido sobrescrito con éxito. Ahora se llama "{nuevo_nombre}" y su operación es "{nueva_operacion}".')
        except Exception as e:
            await ctx.send(f"Error al sobreescribir el dado: {e}")
    else:
        await ctx.send(f'Error: No se encontró ningún dado guardado con el nombre: {nombre}')



@bot.command(aliases=['d'])
async def dado(ctx, maximo: int, *args):
    numero = random.randint(1, maximo)
    if args:
        try:
            operaciones = [c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (arg,)).fetchone()[0] if c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (arg,)).fetchone() else arg for arg in args]
            operacion = " ".join(operaciones)
            operacion = operacion.replace("dado", str(numero))
            resultado = eval(str(numero) + operacion)
            await ctx.send(f'Has lanzado un {numero}!\n{numero} {operacion} = {resultado}')
        except Exception as e:
            await ctx.send(f"Error al calcular la operación.")
    else:
        await ctx.send(f'Has lanzado un {numero}!')

@bot.command(aliases=['u', "usar_dado"])
async def usar(ctx, nombre: str):
    # Recuperar la operación guardada
    operacion_guardada = c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (nombre,)).fetchone()
    if operacion_guardada:
        operacion = operacion_guardada[0]
        # Verificar si la operación incluye un lanzamiento de dado
        if "!d" in operacion:
            # Extraer el máximo del dado
            maximo = int(operacion.split("!d")[1].split()[0])
            # Generar un número aleatorio
            numero = random.randint(1, maximo)
            # Reemplazar el lanzamiento de dado en la operación por el número aleatorio
            operacion = operacion.replace("!d " + str(maximo), str(numero))
            # Verificar si la operación incluye otra operación guardada
            for match in re.findall(r'\b[A-Za-z_]+\b', operacion):
                # Recuperar la otra operación guardada
                otra_operacion_guardada = c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (match,)).fetchone()
                if otra_operacion_guardada:
                    # Reemplazar el nombre de la otra operación guardada en la operación por su valor
                    operacion = operacion.replace(match, otra_operacion_guardada[0])
            try:
                # Calcular el resultado de la operación
                resultado = eval(operacion)
                await ctx.send(f'Se han lanzado los dados {nombre}\n{numero} {operacion[len(str(numero)):]} = {resultado}')
            except Exception as e:
                await ctx.send(f"Error al calcular la operación.")
        else:
            await ctx.send(f'Error: La operación guardada "{nombre}" no incluye un lanzamiento de dado.')
    else:
        await ctx.send(f'Error: No se encontró ninguna operación guardada con el nombre: {nombre}')

@bot.command(aliases=['ue'])
async def usar_efecto(ctx, nombre: str):
    # Recuperar la operación guardada
    operacion_guardada = c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (nombre,)).fetchone()
    if operacion_guardada:
        operacion = operacion_guardada[0]
        # Verificar si la operación incluye una operación de combate
        if "!cc" in operacion:
            # Extraer los argumentos de la operación de combate
            args = operacion.split("!cc")[1].split()
            # Ejecutar el comando de combate con los argumentos extraídos
            await calcular_combate(ctx, *args)
        else:
            await ctx.send(f'Error: La operación guardada "{nombre}" no incluye una operación de combate o es un dado.')
    else:
        await ctx.send(f'Error: No se encontró ninguna operación guardada con el nombre: {nombre}')



@bot.command()
async def hola(ctx):
    await ctx.send(f'¡Hola {ctx.author.name}!')

@bot.command(aliases=['p'])
async def preguntar(ctx, *, pregunta: str):
    respuestas_basicas = {
        "¿Cómo estás?": "¡Estoy bien, gracias! ¿Y tú?",
        "¿Qué haces?": "Estoy aquí para ayudarte. ¿Cómo puedo asistirte hoy?",
    }
    respuesta = respuestas_basicas.get(pregunta, "Lo siento, no tengo una respuesta para esa pregunta.")
    await ctx.send(respuesta)


@bot.command(aliases=['l'])
async def lista(ctx):
    try:
        operaciones = c.execute("SELECT * FROM operaciones ORDER BY fecha").fetchall()
        for operacion in operaciones:
            nombre = operacion[0]
            operacion_texto = operacion[1]
            await ctx.send(f'Nombre: {nombre}, Operación: {operacion_texto}')
    except Exception as e:
        await ctx.send(f'Error al listar las operaciones: {str(e)}')


@bot.command()
async def crear(ctx, raza: str, dificultad: str):
    raza = raza.lower().strip()
    dificultad = dificultad.lower().strip()
    nombre_del_personaje = raza
    
   
    print(f"raza: {raza}, dificultad: {dificultad}")  # Verificación de los argumentos del comando
    print(parametros)  # Verificación de los parámetros
    print(f"raza en parametros: {raza in parametros}")  # Verificar si la raza está en los parámetros
    print(f"dificultad en parametros de raza: {dificultad in parametros[raza] if raza in parametros else 'raza no encontrada'}")  # Verificar si la dificultad está en los parámetros de la raza
    if raza in parametros and dificultad in parametros[raza]:
        nombre = nombre_del_personaje  # Cambio aquí
        # num_personajes

        num_personajes = c.execute("SELECT COUNT(*) FROM personajes WHERE nombre LIKE ?", (raza + '%',)).fetchone()[0]
        print(f"Num Personajes: {num_personajes}")  # Verificación de la base de datos

        num_personajes = c.execute("SELECT COUNT(*) FROM personajes WHERE nombre LIKE ?", (raza + '%',)).fetchone()[0]
        nombre = f"{raza}{num_personajes + 1}"
        
        vida = random.randint(*parametros[raza][dificultad]["vida"]) if isinstance(parametros[raza][dificultad]["vida"], tuple) else parametros[raza][dificultad]["vida"]
        energia = random.randint(*parametros[raza][dificultad]["energia"]) if isinstance(parametros[raza][dificultad]["energia"], tuple) else parametros[raza][dificultad]["energia"]
        poder_magico = random.randint(*parametros[raza][dificultad]["poder_magico"]) if isinstance(parametros[raza][dificultad]["poder_magico"], tuple) else parametros[raza][dificultad]["poder_magico"]
        fuerza = random.randint(*parametros[raza][dificultad]["fuerza"]) if isinstance(parametros[raza][dificultad]["fuerza"], tuple) else parametros[raza][dificultad]["fuerza"]
        velocidad = random.randint(*parametros[raza][dificultad]["velocidad"]) if isinstance(parametros[raza][dificultad]["velocidad"], tuple) else parametros[raza][dificultad]["velocidad"]
        inteligencia = random.randint(*parametros[raza][dificultad]["inteligencia"]) if isinstance(parametros[raza][dificultad]["inteligencia"], tuple) else parametros[raza][dificultad]["inteligencia"]
        alma = random.randint(*parametros[raza][dificultad]["alma"]) if isinstance(parametros[raza][dificultad]["alma"], tuple) else parametros[raza][dificultad]["alma"]
        cordura = parametros[raza][dificultad]["cordura"]
        precision = random.randint(*parametros[raza][dificultad]["precision"]) if isinstance(parametros[raza][dificultad]["precision"], tuple) else parametros[raza][dificultad]["precision"]
        sigilo = random.randint(*parametros[raza][dificultad]["sigilo"]) if isinstance(parametros[raza][dificultad]["sigilo"], tuple) else parametros[raza][dificultad]["sigilo"]
        percepcion = random.randint(*parametros[raza][dificultad]["percepcion"]) if isinstance(parametros[raza][dificultad]["percepcion"], tuple) else parametros[raza][dificultad]["percepcion"]
        stamina = random.randint(*parametros[raza][dificultad]["stamina"]) if isinstance(parametros[raza][dificultad]["stamina"], tuple) else parametros[raza][dificultad]["stamina"]

        # Guardar el personaje en la base de datos
        c.execute("INSERT INTO personajes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (nombre, raza, nombre_del_personaje, dificultad, vida, energia, poder_magico, fuerza, velocidad, inteligencia, alma, cordura, precision, sigilo, percepcion, stamina))

        # Guardar las estadísticas como operaciones
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_nombre_del_personaje", nombre_del_personaje))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_vida", vida))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_energia", energia))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_poder_magico", poder_magico))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_fuerza", fuerza))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_velocidad", velocidad))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_inteligencia", inteligencia))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_alma", alma))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_cordura", cordura))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_precision", precision))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_sigilo", sigilo))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_percepcion", percepcion))
        c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_stamina", stamina))

        conn.commit()

        await ctx.send(f"Personaje '{nombre}' creado con éxito!")
        await ficha(ctx, nombre)
    else:
        await ctx.send("Raza o dificultad inválida.")

@bot.command()
async def modificar(ctx, nombre: str):
    # Verificar si el personaje existe
    personaje = obtener_personaje(nombre)
    if personaje:
        # Preguntar qué característica se desea modificar
        await ctx.send('¿Qué característica deseas modificar? (nombre_del_personaje, vida, energia, poder_magico, fuerza, velocidad, inteligencia, alma, cordura, precision, sigilo, percepcion, stamina)')
        def check(m):
         return m.author == ctx.author and m.channel == ctx.channel and m.content in ['nombre_del_personaje', 'vida', 'energia', 'poder_magico', 'fuerza', 'velocidad', 'inteligencia', 'alma', 'cordura','precision', 'sigilo', 'percepcion', 'stamina' ]
        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send('Tiempo de espera agotado. Por favor, intenta de nuevo.')
        else:
            caracteristica = msg.content

            # Preguntar el nuevo valor para la característica
            await ctx.send('Añade el nuevo valor.')
            if caracteristica == "nombre_del_personaje":
                def check(m):  return m.author == ctx.author and m.channel == ctx.channel
            else:
                def check(m):  return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            try:
                msg = await bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('Tiempo de espera agotado. Por favor, intenta de nuevo.')
            else:
                valor = msg.content
                if caracteristica != "nombre_del_personaje":
                    valor = int(valor)

                # Actualizar la característica en la base de datos
                c.execute(f"UPDATE personajes SET {caracteristica}=? WHERE nombre=?", (valor, nombre))
                # Actualizar la operación correspondiente
                c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_{caracteristica}", valor))
                
                # Si se está cambiando el nombre del personaje, actualizar el nombre de todas las operaciones relacionadas
                if caracteristica == "nombre_del_personaje":
                    c.execute("UPDATE personajes SET nombre=? WHERE nombre=?", (valor, nombre))
                    operaciones = c.execute("SELECT nombre FROM operaciones WHERE nombre LIKE ?", (nombre + '%',)).fetchall()
                    for operacion in operaciones:
                        nueva_operacion = valor + operacion[0][len(nombre):]
                        c.execute("UPDATE operaciones SET nombre=? WHERE nombre=?", (nueva_operacion, operacion[0]))
                
                conn.commit()

                await ctx.send(f'{caracteristica.capitalize()} de {nombre} actualizada a {valor}.')
    else:
        await ctx.send(f'Error: El personaje "{nombre}" no existe.')

@bot.command()
async def ficha(ctx, nombre: str):
    # Verificar si el personaje existe
    personaje = obtener_personaje(nombre)
    if personaje:
        # Mostrar las características del personaje
        await ctx.send(f'Raza: {personaje[1]}\nNombre del Personaje: {personaje[2]}\nDificultad: {personaje[3]}\nVida: {personaje[4]}\nEnergía: {personaje[5]}\nPoder mágico: {personaje[6]}\nFuerza: {personaje[7]}\nVelocidad: {personaje[8]}\nInteligencia: {personaje[9]}\nAlma: {personaje[10]}\nCordura: {personaje[11]}\nPrecision: {personaje[12]}\nSigilo: {personaje[13]}\nPercepcion: {personaje[14]}\nStamina: {personaje[15]}')

    else:
        await ctx.send(f'Error: El personaje "{nombre}" no existe.')

@bot.command()
async def eliminar_ficha(ctx, nombre_del_personaje: str):
    # Verificar si el personaje existe
    personaje = c.execute("SELECT * FROM personajes WHERE nombre_del_personaje=?", (nombre_del_personaje,)).fetchone()
    if personaje:
        # Eliminar todas las operaciones asociadas al personaje
        c.execute("DELETE FROM operaciones WHERE nombre LIKE ?", (personaje[0] + '%',))
        # Eliminar el personaje
        c.execute("DELETE FROM personajes WHERE nombre_del_personaje=?", (nombre_del_personaje,))
        conn.commit()
        await ctx.send(f'Personaje "{nombre_del_personaje}" y todas sus operaciones han sido eliminadas.')
    else:
        await ctx.send(f'Error: El personaje "{nombre_del_personaje}" no existe.')
        

@bot.command(aliases=['eliminar'])
async def delete(ctx, nombre: str):
    # Verificar si el nombre corresponde a un personaje
    personaje = obtener_personaje(nombre)
    if personaje:
        # Eliminar el personaje de la base de datos
        c.execute("DELETE FROM personajes WHERE nombre=?", (nombre,))
        # Eliminar las operaciones asociadas al personaje
        c.execute("DELETE FROM operaciones WHERE nombre LIKE ?", (nombre + '%',))
        conn.commit()

        await ctx.send(f'Personaje "{nombre}" y todas sus operaciones asociadas han sido eliminados.')
    else:
        # Si no es un personaje, intentar eliminar como operación
        operacion = c.execute("SELECT * FROM operaciones WHERE nombre=?", (nombre,)).fetchone()
        if operacion:
            c.execute("DELETE FROM operaciones WHERE nombre=?", (nombre,))
            conn.commit()
            await ctx.send(f'Operación "{nombre}" ha sido borrada.')
        else:
            await ctx.send(f'Error: No se encontró ninguna operación o personaje con el nombre "{nombre}".')

# comando de combate

@bot.command(aliases=['cc'])
async def calcular_combate(ctx, *args):
    try:
        # Verificar si la operación involucra a una estadística de personaje
        if "_" in args[0]:
            nombre, caracteristica = args[0].split("_", 1)
            # Verificar si el nombre corresponde a un personaje
            personaje = obtener_personaje(nombre)
            if personaje:
                # Reemplazar los nombres de las estadísticas de personajes en la operación por sus valores
                operacion = " ".join([str(c.execute("SELECT operacion FROM operaciones WHERE nombre=?", (arg,)).fetchone()[0]) if c.execute("SELECT * FROM operaciones WHERE nombre=?", (arg,)).fetchone() else arg for arg in args])
                try:
                    resultado = eval(operacion)
                except Exception as e:
                    await ctx.send(f"Error al calcular la operación: {str(e)}. Asegúrate de que esté correctamente formateada.")
                else:
                    # Asegurarse de que el resultado no sea negativo
                    resultado = max(0, resultado)

                    # Actualizar la característica en la base de datos
                    c.execute(f"UPDATE personajes SET {caracteristica}=? WHERE nombre_del_personaje=?", (resultado, nombre))
                    # Actualizar la operación correspondiente
                    c.execute("INSERT OR REPLACE INTO operaciones VALUES (?,?,CURRENT_TIMESTAMP)", (f"{nombre}_{caracteristica}", resultado))
                    conn.commit()

                    await ctx.send(f'{nombre}_{caracteristica}: {operacion} = {resultado}\n\nFicha actualizada.')

                    # Mostrar la ficha del personaje
                    personaje = c.execute("SELECT * FROM personajes WHERE nombre_del_personaje=?", (nombre,)).fetchone()
                    await ctx.send(f'Raza: {personaje[1]}\nNombre del Personaje: {personaje[2]}\nDificultad: {personaje[3]}\nVida: {personaje[4]}\nEnergía: {personaje[5]}\nPoder mágico: {personaje[6]}\nFuerza: {personaje[7]}\nVelocidad: {personaje[8]}\nInteligencia: {personaje[9]}\nAlma: {personaje[10]}\nCordura: {personaje[11]}\nPrecision: {personaje[12]}\nSigilo: {personaje[13]}\nPercepcion: {personaje[14]}\nStamina: {personaje[15]}')
            else:
                await ctx.send(f'Error: El personaje "{nombre}" no existe.')
        else:
            await ctx.send(f'Error: Debes proporcionar una estadística de personaje para modificar.')
    except Exception as e:
        await ctx.send(f"Error al calcular la operación. Asegúrate de que esté correctamente formateada.")

@bot.command()
async def lista_fichas(ctx):
    
    # Recuperar todas las fichas de la base de datos
    c.execute("SELECT * FROM personajes")
    fichas = c.fetchall()

    # Crear un mensaje con todas las fichas
    mensaje = "Fichas:\n"
    for ficha in fichas:
        mensaje = f"Raza: {ficha[1]}\n"
        mensaje += f"Nombre del Personaje: {ficha[2]}\n"
        mensaje += f"Dificultad: {ficha[3]}\n"
        mensaje += f"Vida: {ficha[4]}\n"
        mensaje += f"Energía: {ficha[5]}\n"
        mensaje += f"Poder mágico: {ficha[6]}\n"
        mensaje += f"Fuerza: {ficha[7]}\n"
        mensaje += f"Velocidad: {ficha[8]}\n"
        mensaje += f"Inteligencia: {ficha[9]}\n"
        mensaje += f"Alma: {ficha[10]}\n"
        mensaje += f"Cordura: {ficha[11]}\n"
        mensaje += f"Precisión: {ficha[12]}\n"
        mensaje += f"Sigilo: {ficha[13]}\n"
        mensaje += f"Percepción: {ficha[14]}\n"
        mensaje += f"Stamina: {ficha[15]}\n"

        # Enviar el mensaje
        await ctx.send(mensaje)


try:
    bot.run('MTE1MjYwMzEzODM5NDY4OTUzNw.GQyg9F.6MSwDPToaYacH2DhmHlE8oZlp3-z6qrblfHI1I')
except Exception as e:
    print(f'El bot no se pudo iniciar: {str(e)}')
