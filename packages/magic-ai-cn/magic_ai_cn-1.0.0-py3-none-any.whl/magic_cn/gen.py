#@title todo el proceso

import http.client
import json
import gzip
import io
import re
import time
import requests
import uuid
from reg_magic import *


def eliminar_proyecto(session_cookie, project_id):
    host = "magi.sand.ai"
    url_path = f"/api/v1/projects/{project_id}"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "traceparent": "00-41cb0850298b4045a2997e1ee3ddbbe9-05a09d0a52200b40-01",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&014a75e108f943ff8cf25b4dfc60ee30&uid_63h786x7tyczgquf',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://magi.sand.ai/app/projects ",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("DELETE", url_path, body=None, headers=headers)

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
            deleted_id = json_response.get("id")
            #print("ID del proyecto eliminado:", deleted_id)
            return deleted_id

        except json.JSONDecodeError:
            #print("⚠️ No se pudo parsear el JSON.")
            print(f"\r⚠️ No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("❌ Error al hacer la solicitud:", e)
        print(f"\r⚠️ Error al hacer la solicitud:", end='', flush=True)
        return None

    finally:
        conn.close()


def verificar_estado_y_descargar_video(session_cookie, generation_id, project_id, output_filename, contador_segundos):
    host = "magi.sand.ai"
    url_path = f"/api/v1/generations/{generation_id}?chunks=true"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "traceparent": "00-19050dc33fac4f65a359dbb2fc35ceeb-ccf57679ab531db5-01",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    while True:
        try:
            print(f"\r✅ Verificando estado de la generación...", end='', flush=True)
            conn = http.client.HTTPSConnection(host)
            conn.request("GET", url_path, headers=headers)

            response = conn.getresponse()
            raw_data = response.read()

            # Descomprimir si es necesario
            if response.getheader('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                    data = gz.read().decode('utf-8')
            else:
                data = raw_data.decode('utf-8')

            # Parsear JSON
            try:
                json_response = json.loads(data)
                #print(json_response)
                status = json_response.get("status")
                print(f"\r⏳ Estado actual: '{status}'", end='', flush=True)
                video_url = json_response.get("resultVideoURL")

                #print(f"Estado actual: {status}")

                if status == "Success" and video_url:
                    print(f"\r✅ Video generado y disponible..", end='', flush=True)
                    #print("Descargando video desde:", video_url)

                    # Descargar el video
                    respuesta = requests.get(video_url)
                    with open(output_filename, 'wb') as f:
                        f.write(respuesta.content)
                    print(f"\r✅ Video guardado como '{output_filename}'", end='', flush=True)

                    if output_filename:
                        # Datos de ejemplo
                        session_value = os.environ.get("SESSION_VALL")
                        project_id = os.environ.get("PROJECT_ID")

                        # Llamar a la función
                        proyecto_eliminado_id = eliminar_proyecto(session_value, project_id)

                        #if proyecto_eliminado_id:
                        #    print("\n✅ Proyecto eliminado con éxito:", proyecto_eliminado_id)
                        #else:
                        #    print("\n⚠️ No se pudo obtener confirmación del borrado.")

                    return video_url

                elif status in ["Failed", "Cancelled"]:
                    print(f"\r❌ La generación falló o fue cancelada.", end='', flush=True)
                    return None

                
            except json.JSONDecodeError:
                print(f"\r⚠️ Error al parsear JSON. Respuesta:", end='', flush=True)

        except Exception as e:
            #print("Error al conectar con el servidor:", e)
            print(f"\r⚠️ Error al conectar con el servidor:", end='', flush=True)

        finally:
            conn.close()

        # Esperar 10 segundos antes de volver a preguntar
        contador_segundos += 10
        minutos = contador_segundos // 60
        segundos = contador_segundos % 60
        print(f"\r⏱️ Processing: {status} Time elapsed: {minutos} minutes and {segundos} seconds", end='', flush=True)
        time.sleep(10)





def iniciar_generacion(text_prompt, session_cookie, project_id, asset_id, ai_model_id, calidad, enhanceprompt, aspect_ratio_id, duration):
    contador_segundos=0
    host = "magi.sand.ai"
    url_path = "/api/v1/generations"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-3e359e139f6e4df493a5d638e9404e1a-88808b0c9bc75fbd-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    # Cuerpo de la solicitud
    body = {
        "model": ai_model_id,
        "source": {
            "type": "image",
            "content": str(asset_id)  # ID de la imagen subida
        },
        "chunks": [
            {
                "duration": duration,
                "conditions": [
                    {
                        "type": "text",
                        "content": text_prompt
                    }
                ]
            }
        ],
        "aspectRatio": aspect_ratio_id,
        "extraArgs": {
            "enablePromptEnhancement": enhanceprompt,
            "tSchedulerFunc": "sd3",
            "tSchedulerArgs": "",
            "extraInferArgs": {
                "resolution": "720p",
                "enhancementType": "",
                "specialTokens": ["copyright"],
                "vaeModel": "2x",
                "nSampleSteps": calidad
            }
        }
    }

    body_json = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", url_path, body=body_json, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        #print("Estado:", response.status)

        # Descomprimir si es necesario
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Parsear JSON y extraer ID
        try:
            json_response = json.loads(data)
            generation_id = json_response.get("id")

            contador_segundos += 10
            minutos = contador_segundos // 60
            segundos = contador_segundos % 60
            print(f"\r⏱️ Processing... Time elapsed: {minutos} minutes and {segundos} seconds", end='', flush=True)

            return generation_id, contador_segundos
        except json.JSONDecodeError:
            print(f"\r⚠️ La respuesta no es un JSON válido.", end='', flush=True)
            return None, 0

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None, 0

    finally:
        conn.close()



def actualizar_canvas_y_extraer_id(session_cookie, project_id, asset_id):
    host = "magi.sand.ai"
    url_path = f"/api/v1/projects/{project_id}/canvas"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-eba42b4ff93d4e38a5b4a8995cb93844-d5d18bcb04694464-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    # Cuerpo de la solicitud (ajustado con el asset_id dinámico)
    body = {
        "version": "1",
        "snapshot": {
            "store": {
                "document:document": {
                    "gridSize": 10,
                    "name": "",
                    "meta": {},
                    "id": "document:document",
                    "typeName": "document"
                },
                "page:page": {
                    "meta": {},
                    "id": "page:page",
                    "name": "Page 1",
                    "index": "a1",
                    "typeName": "page"
                },
                "shape:WqIPPiXZbC--eZ2s6Fgh6": {
                    "x": 1068.666748046875,
                    "y": 317.00004069010413,
                    "rotation": 0,
                    "isLocked": False,
                    "opacity": 1,
                    "meta": {},
                    "id": "shape:WqIPPiXZbC--eZ2s6Fgh6",
                    "type": "start-frame",
                    "props": {
                        "magiAssetId": asset_id,
                        "w": 352,
                        "h": 458.6666666666667,
                        "scale": 1,
                        "isVideo": False,
                        "size": {"width": 768, "height": 1024},
                        "cropArea": {"x": 0, "y": 0, "width": 768, "height": 1024},
                        "aspectRatio": "768:1024"
                    },
                    "parentId": "page:page",
                    "index": "a1",
                    "typeName": "shape"
                }
            },
            "schema": {
                "schemaVersion": 2,
                "sequences": {
                    "com.tldraw.store": 4,
                    "com.tldraw.asset": 1,
                    "com.tldraw.camera": 1,
                    "com.tldraw.document": 2,
                    "com.tldraw.instance": 25,
                    "com.tldraw.instance_page_state": 5,
                    "com.tldraw.page": 1,
                    "com.tldraw.instance_presence": 6,
                    "com.tldraw.pointer": 1,
                    "com.tldraw.shape": 4,
                    "com.tldraw.asset.bookmark": 2,
                    "com.tldraw.asset.image": 5,
                    "com.tldraw.asset.video": 5,
                    "com.tldraw.shape.group": 0,
                    "com.tldraw.shape.text": 2,
                    "com.tldraw.shape.bookmark": 2,
                    "com.tldraw.shape.draw": 2,
                    "com.tldraw.shape.geo": 9,
                    "com.tldraw.shape.note": 8,
                    "com.tldraw.shape.line": 5,
                    "com.tldraw.shape.frame": 0,
                    "com.tldraw.shape.arrow": 5,
                    "com.tldraw.shape.highlight": 1,
                    "com.tldraw.shape.embed": 4,
                    "com.tldraw.shape.image": 4,
                    "com.tldraw.shape.video": 2,
                    "com.tldraw.shape.video-generation": 0,
                    "com.tldraw.shape.start-frame": 0,
                    "com.tldraw.shape.curve-arrow": 0,
                    "com.tldraw.binding.arrow": 0,
                    "com.tldraw.binding.curve-arrow": 0
                }
            }
        }
    }

    body_json = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("PATCH", url_path, body=body_json, headers=headers)

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
            project_id_response = json_response.get("id")
            #print("ID del proyecto actualizado:", project_id_response)
            return project_id_response

        except json.JSONDecodeError:
            print(f"\r⚠️ No se pudo parsear el JSON..", end='', flush=True)
            return None

    except Exception as e:
        #print("❌ Error al hacer la solicitud:", e)
        print(f"\r⚠️ Error al hacer la solicitud:", end='', flush=True)
        return None

    finally:
        conn.close()




def obtener_datos_del_proyecto(session_cookie, project_id):
    host = "magi.sand.ai"
    url_path = f"/api/v1/projects/{project_id}"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "traceparent": "00-3972a65e438a480785c9fa3a781ccd74-1f73ab6124d1ebaf-01",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", url_path, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        # Descomprimir si es necesario
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Parsear JSON
        try:
            json_response = json.loads(data)

            # Extraer los datos requeridos
            project_data = {
                "id": json_response.get("id"),
                "userId": json_response.get("userId"),
                "posterUrl": json_response.get("posterUrl"),
                "posterAssetId": json_response.get("posterAssetId")
            }

            #print("Datos del proyecto:")
            #for key, value in project_data.items():
            #    print(f"{key}: {value}")

            return project_data

        except json.JSONDecodeError:
            print(f"\r⚠️  No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("⚠️ Error al hacer la solicitud:", e)
        print(f"\r⚠️ Error al hacer la solicitud:", end='', flush=True)
        return None

    finally:
        conn.close()




def obtener_id_y_url_imagen(session_cookie, asset_id, project_id):
    host = "magi.sand.ai"
    url_path = f"/api/v1/assets/mget?ids={asset_id}"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "traceparent": "00-834a648063db45db8aa813f33e9d9431-31d5b449f5aaf6ab-01",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", url_path, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        # Descomprimir si es necesario
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Parsear JSON
        try:
            json_response = json.loads(data)
            asset_data = json_response.get(str(asset_id))

            if asset_data:
                asset_id_found = asset_data.get("id")
                image_url = asset_data.get("url")

                #print(f"ID encontrado: {asset_id_found}")
                #print(f"URL de la imagen: {image_url}")

                return {
                    "id": asset_id_found,
                    "url": image_url
                }
            else:
                #print("No se encontró el activo en la respuesta.")
                print(f"\r⚠️ No se encontró el activo en la respuesta.", end='', flush=True)
                return None

        except json.JSONDecodeError:
            #print("❌ No se pudo parsear el JSON.")
            print(f"\r⚠️ No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("⚠️ Error al hacer la solicitud:", e)
        print(f"\r⚠️ Error al hacer la solicitud:", end='', flush=True)
        return None

    finally:
        conn.close()




def actualizar_proyecto_con_imagen(session_cookie, project_id, asset_id):
    host = "magi.sand.ai"
    url_path = f"/api/v1/projects/{project_id}"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-afd0d1cd2175437399c5b38f31c6e239-17d6281dcb06b69b-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate"
    }

    body = {
        "poster_asset_id": asset_id
    }

    body_json = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("PUT", url_path, body=body_json, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        #print("Estado:", response.status)

        # Descomprimir si es necesario
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8')

        # Parsear JSON y extraer ID
        try:
            json_response = json.loads(data)
            returned_id = json_response.get("id")
            #print("ID devuelto por el servidor:", returned_id)
            return returned_id
        except json.JSONDecodeError:
            #print("La respuesta no es un JSON válido.")
            print(f"\r⚠️ La respuesta no es un JSON válido.", end='', flush=True)
            return None

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None

    finally:
        conn.close()



def subir_imagen(session_cookie, project_id, file_path, boundary="----WebKitFormBoundary8m79y2pPrrKDtIje"):
    host = "magi.sand.ai"
    url_path = "/api/v1/assets?isArtifacts=true"

    # Leer archivo de imagen
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
    except Exception as e:
        #print("Error al leer el archivo:", e)
        print(f"\r⚠️ Error al leer el archivo:", end='', flush=True)
        return None

    # Nombre del archivo
    filename = file_path.split("/")[-1]

    # Construir cuerpo multipart/form-data manualmente
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-3d813a4ba22b4eb597411865d508a733-2e5ca7a09a6b7594-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://magi.sand.ai/app/projects/ {project_id}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"session={session_cookie}",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": str(len(body))
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", url_path, body=body, headers=headers)

        response = conn.getresponse()
        raw_data = response.read()

        #print("Estado:", response.status)

        # Descomprimir solo si es gzip
        content_encoding = response.getheader('Content-Encoding')
        if content_encoding == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as gz:
                data = gz.read().decode('utf-8')
        else:
            data = raw_data.decode('utf-8', errors='ignore')

        #print("Respuesta del servidor:")
        #print(data)

        # Parsear JSON y extraer ID
        try:
            json_response = json.loads(data)
            asset_id = json_response.get("id")
            #print("ID del recurso subido:", asset_id)
            return asset_id  # Devolvemos solo el ID
        except json.JSONDecodeError:
            #print("La respuesta no es un JSON válido.")
            print(f"\r⚠️ La respuesta no es un JSON válido.", end='', flush=True)
            return None

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None

    finally:
        conn.close()



def crear_proyecto(session_cookie, titulo="New Project"):
    host = "magi.sand.ai"
    url_path = "/api/v1/projects"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-d1f4378618d14486ab467849b6a29efd-0b0a70c1caad9854-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&acb6a260393e4724b1a567fda82e74f4&uid_49kbhl6q9xes78qu',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://magi.sand.ai/app/projects ",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": f"session={session_cookie}"
    }

    body = {
        "title": titulo
    }

    body_json = json.dumps(body)

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", url_path, body=body_json, headers=headers)

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
            project_id = json_response.get("id")
            #print("ID del proyecto:", project_id)
            return project_id  # Devolvemos solo el ID

        except json.JSONDecodeError:
            #print("No se pudo parsear el JSON.")
            print(f"\r⚠️ No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None

    finally:
        conn.close()


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
            #print("Crédito disponible:", {credit_amount})
            print(f"\r✅ Crédito disponible: {credit_amount}", end='', flush=True)
            return credit_amount  # Devolvemos solo el crédito

        except json.JSONDecodeError:
            #print("No se pudo parsear el JSON.")
            print(f"\r⚠️ No se pudo parsear el JSON.", end='', flush=True)
            return None

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None

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

def iniciar_sesion(email, password):
    host = "magi.sand.ai"
    url_path = "/api/v1/user/login"

    headers = {
        "Host": host,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-d22fd5bef59d4276a7b67b3d1bd6606f-e3c3465b8d28c349-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": 'rum=v2&browser&fa6f9pxqjp@7d3c1bebf3d8197&3191f013129a486ab3e907a369db93d4&uid_63h786x7tyczgquf',
        "Origin": "https://magi.sand.ai ",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://magi.sand.ai/app/login/email ",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    body = {
        "email": email,
        "password": password
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

        #print("Set-Cookie:", set_cookie)
        #print("Trace-ID:", trace_id)

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
                print(f"\r⚠️ Respuesta no es JSON:", end='', flush=True)
                return {
                    "cookie": set_cookie,
                    "trace_id": trace_id,
                    "raw_response": data
                }
        else:
            #print("No hubo cuerpo en la respuesta.")
            print(f"\r⚠️ No hubo cuerpo en la respuesta.", end='', flush=True)
            return {
                "cookie": set_cookie,
                "trace_id": trace_id
            }

    except Exception as e:
        #print("Error:", e)
        print(f"\r⚠️ Error.", end='', flush=True)
        return None

    finally:
        conn.close()

# Ejemplo de uso
def generate(text_prompt, model_original, Enhance_Prompt, duration):
    session_value = os.environ.get("SESSION_VALL")
    if not session_value:
      credited()

    if session_value:

        # Ejemplo de uso
        credito = int(obtener_creditos(session_value))
        #print("Crédito devuelto:", credito)
        print(f"\r✅ Crédito devuelto: {credito}", end='', flush=True)
        incrediited = int(f"{duration}0")

        if credito >= incrediited:
            #print(f"Es mayor o igual a {duration}0")
            print(f"\r✅ Es mayor o igual a {duration}0", end='', flush=True)
            text_project = "streaming talking1"
            # Ejemplo de uso
            session_value = os.environ.get("SESSION_VALL")
            project_id = crear_proyecto(session_value, text_project)
            #print("ID devuelto por la función:", project_id)

            if project_id:
                os.environ["PROJECT_ID"] = str(project_id)
                # Ejemplo de uso
                session_value = os.environ.get("SESSION_VALL")
                #project_id = "675334509154757"
                ruta_de_imagen = os.environ.get("RUTA_TMP")

                asset_id = subir_imagen(session_value, project_id, ruta_de_imagen)
                #print("ID devuelto por la función:", asset_id)
                if asset_id:
                    os.environ["ASSET_ID"] = str(asset_id)

                    # Ejemplo de uso
                    session_value = os.environ.get("SESSION_VALL")
                    project_id = os.environ.get("PROJECT_ID")
                    #asset_id = 675341047624197  # Este es el ID de la imagen subida

                    resultado = actualizar_proyecto_con_imagen(session_value, project_id, asset_id)
                    #print("Resultado final - ID del proyecto actualizado:", resultado)
                    if resultado:
                        #print("El proyecto se actualizó correctamente.")

                        print(f"\r✅ El proyecto se actualizó correctamente.", end='', flush=True)

                        # Datos de prueba
                        session_value = os.environ.get("SESSION_VALL")
                        asset_id = os.environ.get("ASSET_ID")
                        project_id = os.environ.get("PROJECT_ID")

                        # Llamada a la función
                        resultado = obtener_id_y_url_imagen(session_value, asset_id, project_id)

                        if resultado:
                            #print("\nDatos extraídos:")
                            #print("ID:", resultado["id"])
                            #print("URL:", resultado["url"])

                            # Datos de prueba
                            session_value = os.environ.get("SESSION_VALL")
                            project_id = os.environ.get("PROJECT_ID")

                            # Llamada a la función
                            resultado = obtener_datos_del_proyecto(session_value, project_id)

                            if resultado:
                                #print("\nDatos extraídos:")
                                #print("ID:", resultado["id"])
                                #print("UserID:", resultado["userId"])
                                #print("Poster URL:", resultado["posterUrl"])
                                #print("Poster Asset ID:", resultado["posterAssetId"])

                                # Datos de ejemplo
                                session_value = os.environ.get("SESSION_VALL")
                                asset_id = os.environ.get("ASSET_ID")
                                project_id = os.environ.get("PROJECT_ID")

                                # Llamar a la función
                                resultado_id = actualizar_canvas_y_extraer_id(session_value, project_id, asset_id)

                                if resultado_id:
                                    #print("\n✅ ID devuelto por el servidor:", resultado_id)

                                    ancho = os.environ.get("ANCHO")
                                    alto = os.environ.get("ALTO")

                                    aspect_ratio_id = f"{ancho}:{alto}"

                                    model_originals = {
                                        "SD": "magi-v2-distill-fp8-s16",
                                        "HD": "magi-v2-distill-fp8-s32",
                                    }

                                    # Selecciona el nombre mediante un combolist

                                    # Parámetros editables
                                    ai_model_id = model_originals.get(model_original)

                                    if model_original == "SD":
                                        calidad = 16
                                    elif model_original == "HD":
                                        calidad = 32





                                    if Enhance_Prompt:
                                        enhanceprompt = "true"
                                    else:
                                        enhanceprompt = "false"


                                    # Ejemplo de uso
                                    session_value = os.environ.get("SESSION_VALL")
                                    asset_id = os.environ.get("ASSET_ID")
                                    project_id = os.environ.get("PROJECT_ID")

                                    dura = int(duration)

                                    resultado, contador_segundos = iniciar_generacion(text_prompt, session_value, project_id, asset_id, ai_model_id, calidad, enhanceprompt, aspect_ratio_id, dura)
                                    #print("ID devuelto por la función:", resultado)

                                    if resultado:
                                        #print("La generación se inició correctamente.")
                                        print(f"\r✅ La generación se inició correctamente.", end='', flush=True)

                                        # Ejemplo de uso

                                        session_value = os.environ.get("SESSION_VALL")
                                        project_id = os.environ.get("PROJECT_ID")
                                        generation_id = resultado
                                        
                                        # Ruta de la carpeta a verificar
                                        folder_path = '/content/videos'

                                        # Verificar si la carpeta existe
                                        if not os.path.exists(folder_path):
                                            # Si no existe, la creamos
                                            os.makedirs(folder_path)
                                            #print(f'Carpeta creada: {folder_path}')
                              

                                        id_unico = uuid.uuid4()
                                        output_video_file = f"/content/videos/{id_unico}.mp4"

                                        os.environ["VIDEO_FILE"] = output_video_file

                                        # Iniciar verificación periódica y descargar cuando esté listo
                                        verificar_estado_y_descargar_video(session_value, generation_id, project_id, output_video_file, contador_segundos)








        else:
            #print("Es menor que 30")
            credited()
            time.sleep(1)
            generate(text_prompt, model_original, Enhance_Prompt, duration)

    else:
        #print("No se pudo extraer el valor de session.")
        credited()
        time.sleep(1)
        generate(text_prompt, model_original, Enhance_Prompt, duration)