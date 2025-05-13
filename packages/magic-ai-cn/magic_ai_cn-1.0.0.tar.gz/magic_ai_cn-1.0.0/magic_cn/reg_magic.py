#@title Registro y verificar
import requests
import re
import random
import string
import uuid
import time
import os
from bs4 import BeautifulSoup
import http.client
import json
import gzip
import io

def obtener_creditos(cookie_session):
    host = "magi.sand.ai"
    url_path = "/api/v1/credits/user"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "traceparent": "00-39ecb5673f1742f3a5bf91a754154fbc-ecc23c174747ffc4-01",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://magi.sand.ai/app/projects ",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": f"session={cookie_session}"
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", url_path, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        #print("Estado:", response.status)

        # Descomprimir si es necesario
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Parsear JSON
        try:
            json_response = json.loads(data)
            credit_amount = json_response.get("creditAmount")
            #print("Crédito disponible:", credit_amount)
            return credit_amount  # Devolvemos solo el crédito

        except json.JSONDecodeError:
            print(f"\r⚠ No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠ Error.", end='', flush=True)
        return None

    finally:
        conn.close()

def verificar_email(verification_code):
    host = "magi.sand.ai"
    url_path = "/api/v1/user/verify-email"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-df8be20e6f8d4cca83a696be4c30ef38-6fce088d024cdbe5-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/register/verify?verificationCode= {verification_code}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    body = {
        "verificationCode": verification_code
    }

    body_json = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", url_path, body=body_json, headers=headers)

        response = conn.getresponse()

        # Leer datos comprimidos o no comprimidos
        raw_data = response.read()

        # Verificar si está comprimido con gzip
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        #print("Estado:", response.status)

        # Extraer encabezados importantes
        set_cookie = None
        trace_id = None

        for header, value in response.getheaders():
            if header.lower() == "set-cookie":
                set_cookie = value
            if header.lower() == "traceid":
                trace_id = value

        print(f"\r⏳ Registro Automatizado.", end='', flush=True)

        # Parsear JSON si hay contenido
        if data.strip():
            try:
                json_response = json.loads(data)
                #print("Respuesta JSON:", json_response)
                return {
                    "cookie": set_cookie,
                    "trace_id": trace_id,
                    "user_data": json_response
                }
            except json.JSONDecodeError:
                #print("Respuesta no es JSON:", data)
                return {
                    "cookie": set_cookie,
                    "trace_id": trace_id,
                    "raw_response": data
                }
        else:
            #print("No hubo cuerpo en la respuesta.")
            print(f"\r⚠ No hubo cuerpo en la respuesta.", end='', flush=True)
            return {
                "cookie": set_cookie,
                "trace_id": trace_id
            }

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠ Error.", end='', flush=True)
        return None

    finally:
        conn.close()



def registrarse(mail, username, password):
    # Datos de conexión
    host = "magi.sand.ai"
    url_path = "/api/v1/user/signup"

    # Encabezados
    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-6c3e8dc9442c431badcf00e3de939090-5a444f8ff0b5c91c-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://magi.sand.ai/app/register ",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    # Cuerpo de la solicitud
    body = {
        "displayName": username,
        "email": mail,
        "password": password
    }

    # Convertir cuerpo a JSON
    body_json = json.dumps(body)

    try:
        # Establecer conexión HTTPS
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", url_path, body=body_json, headers=headers)

        # Obtener respuesta
        response = conn.getresponse()
        raw_data = response.read()  # Leer los datos sin decodificar todavía

        print(f"\r⏳ Registro Automatizado..", end='', flush=True)

        # Verificar si la respuesta está comprimida
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz_file:
                data = gz_file.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Mostrar respuesta procesada
        print(f"\r⏳ Registro Automatizado...", end='', flush=True)

        # Opcional: parsear como JSON
        try:
            json_response = json.loads(data)
            print(f"\r⏳ Registro Automatizado.", end='', flush=True)
            id_usuario = json_response.get("id")

            return id_usuario
        except json.JSONDecodeError:
            #print("La respuesta no es un JSON válido.")
            print(f"\r⚠ La respuesta no es un JSON válido.", end='', flush=True)
            return "Error"

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠ Error.", end='', flush=True)
        return "Error"

    finally:
        conn.close()


def extraer_valor_session(cookie: str) -> str | None:
    """
    Extrae el valor de la cookie 'session' de una cadena de cookies.

    Parámetros:
        cookie (str): Cadena que contiene la cookie.

    Retorna:
        str | None: Valor de la cookie 'session' si se encuentra, de lo contrario None.
    """
    match = re.search(r'session=([^;]+)', cookie)
    return match.group(1) if match else None


COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def extraer_codigo(html):
    soup = BeautifulSoup(html, "html.parser")

    # Buscar el código en un párrafo con estilo específico
    codigo_tag = soup.find("p", style="margin: 30px 0; font-size: 24px")
    if codigo_tag:
        return codigo_tag.text.strip()

    # Si el código no se encuentra en el estilo esperado, buscar con regex
    codigo_match = re.search(r"\b\d{6}\b", soup.get_text())
    if codigo_match:
        return codigo_match.group()

    return None  # Retorna None si no encuentra el código


def delete_temp_mail(username_email, dominios_dropdown, extracted_string):
    """Borra el correo temporal especificado."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/del_mail.php"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://email-fake.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'embx=%5B%22{username_email}%40{dominios_dropdown}%22%2C',
    }

    data = f'delll={extracted_string}'

    response = requests.post(url, headers=headers, data=data)

    if "Message deleted successfully" in response.text:
        #print("Temporary mail deleted...")
        print(f"\r⏳ Registro Automatizado..", end='', flush=True)
        return True
    else:
        #print("Error deleting temporary email...")
        print(f"\r⚠ Error deleting temporary email...", end='', flush=True)
        return False

def generar_contrasena():
    """Genera una contraseña aleatoria."""
    caracteres = string.ascii_letters + "0123456789" + "#$%&/()@_-*+[]"
    longitud = 10
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def enviar_formulario(url, datos):
    """Envía una solicitud POST a un formulario web."""
    response = requests.post(url, data=datos)
    return response

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio

def generar_nombre_completo():
    """Genera un nombre completo triplicando el nombre y apellido, junto con un número aleatorio de 3 dígitos."""
    nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
               "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
               "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
               "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa",
               # Nombres comunes de EE.UU.
               "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
               "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
               "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
               "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
               "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry",
               "Tyler", "Aaron", "Henry", "Douglas", "Jose", "Peter", "Adam", "Zachary", "Nathan", "Walter",
               "Kyle", "Harold", "Carl", "Arthur", "Gerald", "Roger", "Keith", "Jeremy", "Terry", "Lawrence",
               "Sean", "Christian", "Ethan", "Austin", "Joe", "Jordan", "Albert", "Jesse", "Willie", "Billy"]

    apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
                 "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
                 "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
                 "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez",
                 # Apellidos comunes de EE.UU.
                 "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                 "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                 "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                 "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                 "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood"]


    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    numero = random.randint(100, 999)

    nombre_completo = f"{nombre}_{apellido}_{numero}"
    return nombre_completo



def extract_verification_code(html_content):
    """
    Busca y devuelve el código de verificación UUID en una URL dentro del contenido HTML.

    :param html_content: str - Contenido HTML donde buscar el código.
    :return: str | None - El código UUID si se encuentra, sino None.
    """
    # Patrón para encontrar el UUID en la URL específica
    pattern = r'https://magi\.sand\.ai/app/register/verify\?verificationCode=([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})'

    match = re.search(pattern, html_content)

    if match:
        return match.group(1)  # Devuelve solo el UUID
    else:
        return None




def get_verification_code(username_email, dominios_dropdown):
    """Obtiene el código de verificación del correo y el identificador."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        **COMMON_HEADERS,
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Cookie': f'surl={dominios_dropdown}%2F{username_email}',
    }

    response = requests.get(url, headers=headers)

    #print(response.text)
    print(f"\r⏳ Registro Automatizado..", end='', flush=True)

    # Utiliza una expresión regular para encontrar el código de 6 dígito
    verification_code = extract_verification_code(response.text)
    #verification_code_match = re.search(r'<strong>(\d{6})</strong>', response.text)

    # Utiliza una expresión regular para encontrar el identificador largo
    identifier_match = re.search(r'delll:\s*"([a-zA-Z0-9]+)"', response.text)

    # Extrae y retorna los valores si fueron encontrados
    if verification_code and identifier_match:
        #verification_code = verification_code_match.group(1)
        identifier = identifier_match.group(1)
        return verification_code, identifier
    else:
        return None, None




def extract_code_from_text(body_text):
    # Buscar un patrón de 6 dígitos en el texto
    match = re.search(r'\b\d{6}\b', body_text)
    if match:
        return match.group(0)
    return None

def check_code_with_retries(username_email, dominios_dropdown, retries=6, delay=10):
    for attempt in range(retries):
        #print(f"Intento {attempt + 1} de {retries}...")
        print(f"\r⏳ Registro Automatizado Intento {attempt + 1} de {retries}", end='', flush=True)
        code, identifier = get_verification_code(username_email, dominios_dropdown)
        if code:
            #print(f"Código de verificación: {code}")
            delete_temp_mail(username_email, dominios_dropdown, identifier)
            return code
        #print("Código no encontrado. Esperando 10 segundos antes de reintentar...")
        time.sleep(delay)
    #print("Se alcanzó el máximo de intentos sin éxito.")
    print(f"\r❌ Se alcanzó el máximo de intentos sin éxito.", end='', flush=True)
    return None

def guardar_credenciales(username, password):
    """
    Guarda las credenciales en un archivo de texto sin sobrescribir las anteriores.
    """
    ruta_archivo = "/content/cuenta.txt"
    with open(ruta_archivo, "a") as archivo:
        archivo.write(f"{username}:{password}\n")
    print(f"📂 Credenciales guardadas en {ruta_archivo}")


# Ejemplo de uso
def register():
    """
    Función generadora que registra un usuario y envía actualizaciones en tiempo real.
    """
    password_segura = generar_contrasena()
    url = 'https://email-fake.com/'
    # Supongamos que el formulario en el sitio web tiene un campo llamado 'campo_correo'
    datos = {'campo_correo': 'ejemplo@dominio.com'}
    # Enviar la solicitud POST al formulario
    response = enviar_formulario(url, datos)
    # Obtener un sitio web aleatorio de los dominios extraídos
    sitio_domain = obtener_sitio_web_aleatorio(response.text)
    # Generar y mostrar un nombre completo
    nombre_completo = generar_nombre_completo()
    time.sleep(3)
    # Llamar a la función con valores personalizados
    correo = f'{nombre_completo}@{sitio_domain}'
    username = nombre_completo
    password = password_segura
    email = correo


    # Llamar a la función
    id_user = registrarse(correo, username, password)

    if id_user == "Error":
        #print("❌ El nombre de usuario ya está en uso. Generando uno nuevo...\n")
        print(f"\r❌ El nombre de usuario ya está en uso. Generando uno nuevo...", end='', flush=True)
        register()  # Llamada recursiva para generar un nuevo usuario
    else:
        #print("✅ Solicitud de verificación enviada.\n")
        print(f"\r⏳ Registro Automatizado.", end='', flush=True)

    # Esperar y obtener el código de verificación
    #print("⏳ Esperando el código de verificación...\n")
    print(f"\r⏳ Registro Automatizado..", end='', flush=True)
    verification_code = check_code_with_retries(nombre_completo, sitio_domain)


    if verification_code:
        #print(f"✅ Código de verificación recibido: ******\n")
        print(f"\r⏳ Registro Automatizado...", end='', flush=True)
    else:
        #print("❌ No se pudo obtener el código de verificación.\n")
        print(f"\r❌ No se pudo obtener el código de verificación..", end='', flush=True)
        return

    # Registrar el usuario
    #print("⏳ Registrando usuario...\n")
    print(f"\r⏳ Registro Automatizado.", end='', flush=True)
    # Ejemplo de uso
    resultado = verificar_email(verification_code)
    if resultado:
        session_value = extraer_valor_session(resultado["cookie"])
        os.environ["SESSION_VALL"] = session_value
        #print("Valor de session:", session_value)
        #print("Cookie de sesión:", resultado["cookie"])
        #print("Trace-ID:", resultado["trace_id"])
        #print("✅ Usuario registrado exitosamente.\n")
        print(f"\r⏳ Registro Automatizado..", end='', flush=True)
    else:
        #print("❌ No se pudo registrar el usuario.\n")
        print(f"\r❌ No se pudo registrar el usuario.", end='', flush=True)


#register()

def credited():

  session_value = os.environ.get("SESSION_VALL")
  creditos = obtener_creditos(session_value)

  if creditos == None:
    #print("❌ No se pudo obtener los créditos.\n")
    print(f"\r❌ No se pudo obtener los créditos.", end='', flush=True)
    register()
    time.sleep(1)
    credited()
  else:
    if int(creditos) >= 30:
      #print(creditos)
      print(f"\r✅ Creditos: {creditos}", end='', flush=True)
    else:
      #print("❌ No hay créditos disponibles.\n")
      print(f"\r❌ No hay créditos disponibles.", end='', flush=True)
      register()
      time.sleep(1)
      credited()