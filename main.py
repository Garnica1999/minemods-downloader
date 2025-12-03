import zipfile
import os
import shutil
import gdown

def download_file(archivo_id, nombre_destino):
    try:
        print(f"Descargando archivo con ID: {archivo_id}...")
        
        # gdown.download utiliza el ID, y el 'output' es el nombre del archivo local
        # 'quiet=False' para ver el progreso de la descarga
        gdown.download(id=archivo_id, output=nombre_destino, quiet=False)

        print(f"Descarga completa. Archivo guardado en: {os.path.abspath(nombre_destino)}")

    except Exception as e:
        print(f"Error en la descarga de Drive: {e}")

def main_app(archivo_zip, directorio_destino):
    # Crea el directorio de destino si no existe
    # Si no, borra su contenido
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    else:
        limpiar_carpeta(directorio_destino)

    # 2. Abre el archivo .zip y extráelo
    try:
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            # 'zip_ref' es el objeto que representa el archivo .zip abierto
            # El método .extractall() extrae todo el contenido
            print(f"Extrayendo todo el contenido a: {directorio_destino}...")
            zip_ref.extractall()
        print("¡Extracción completa!")

    except FileNotFoundError:
        print(f"Error: El archivo {archivo_zip} no fue encontrado.")
    except zipfile.BadZipFile:
        print(f"Error: El archivo {archivo_zip} no es un archivo ZIP válido o está corrupto.")


def limpiar_carpeta(ruta_carpeta):
    """Elimina todos los archivos y subcarpetas dentro de la ruta dada."""
    
    if not os.path.exists(ruta_carpeta):
        print(f"Error: La carpeta '{ruta_carpeta}' no existe.")
        return

    print(f"Limpiando el contenido de: {ruta_carpeta}...")
    
    # Itera sobre todos los elementos (archivos y directorios) dentro de la carpeta
    for elemento in os.listdir(ruta_carpeta):
        # Combina la ruta de la carpeta con el nombre del elemento para obtener su ruta completa
        ruta_completa = os.path.join(ruta_carpeta, elemento)
        
        try:
            # Si el elemento es un directorio (carpeta), usa shutil.rmtree para borrarlo
            if os.path.isdir(ruta_completa):
                print(f"Borrando directorio: {ruta_completa}")
                shutil.rmtree(ruta_completa)
            # Si es un archivo, usa os.remove para borrarlo
            elif os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                print(f"Borrando archivo: {ruta_completa}")
                os.remove(ruta_completa)
            
        except Exception as e:
            # Manejo de errores, por ejemplo, si no hay permisos
            print(f"No se pudo borrar {ruta_completa}. Razón: {e}")

    print("Limpieza completada.")
import os

def check_minecraft_installation():
    """Verifica si existe la carpeta de datos de Minecraft en el sistema."""

    # 1. Windows: %APPDATA%\.minecraft
    if os.name == 'nt':
        minecraft_path = os.path.join(os.getenv('APPDATA'), '.minecraft')
    # 2. macOS/Linux: ~/Library/Application Support/minecraft / ~/.minecraft
    else:
        # Esto cubre la ubicación común en Linux (~/.minecraft) y macOS
        # (~/Library/Application Support/minecraft) al usar 'expanduser'
        minecraft_path = os.path.expanduser('~/.minecraft')
        
        # En macOS, la ubicación más precisa para el launcher es:
        # minecraft_macos_path = os.path.expanduser('~/Library/Application Support/minecraft')
        if os.path.exists(minecraft_macos_path):
            return True

    if os.path.exists(minecraft_path):
        print(f"¡Minecraft parece estar instalado! Carpeta encontrada en: {minecraft_path}")
        return (True, minecraft_path)
    else:
        print("No se encontró la carpeta de instalación estándar de Minecraft.")
        return (False, None)

def copy_content(carpeta_origen, carpeta_destino):
    # 1. Asegurarse de que la carpeta de destino exista
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino) # Crea la carpeta de destino si no existe

    # 2. Iterar sobre todos los elementos dentro de la carpeta de origen
    for elemento in os.listdir(carpeta_origen):
        ruta_origen = os.path.join(carpeta_origen, elemento)
        ruta_destino = os.path.join(carpeta_destino, elemento)

        try:
            # Si es un directorio, usa copytree() para copiarlo recursivamente
            if os.path.isdir(ruta_origen):
                # copytree requiere que el destino no exista
                if os.path.exists(ruta_destino):
                    print(f"Advertencia: Subcarpeta '{elemento}' ya existe en el destino, se omite.")
                    continue # O podrías implementar lógica para sobrescribir/fusionar
                shutil.copytree(ruta_origen, ruta_destino)
                print(f"Subcarpeta '{elemento}' copiada.")

            # Si es un archivo, usa copy2()
            elif os.path.isfile(ruta_origen):
                shutil.copy2(ruta_origen, ruta_destino) # copy2 también copia metadatos (permisos, etc.)
                print(f"Archivo '{elemento}' copiado.")

        except Exception as e:
            print(f"Ocurrió un error al copiar '{elemento}': {e}")

    print("\nCopia de contenido completada.")

initial_text = """ Bienvenido al script de instalacion de mods. 
Advertencia: RECOMENDAMOS LEER LOS SIGUIENTES PASOS LETRA POR LETRA. Este proceso es automático pero el script
está en versión beta y elimina ciertos mods de la carpeta de instalacion de minecraft. Es probable que este script
no funcione con launchers personalizados, ya que suelen instalar minecraft en rutas diferentes al launcher original.

Este script hará los siguientes pasos para la instalación/actualizacion de mods.
    1. Validaremos si tiene Minecraft en su versión java instalado. 
    Si no lo tiene detenga este script e instale la versión Minecraft java 1.21.1.
    Recuerde que posteriormente debe tener NeoForge instalado.
    2. Descargaremos un archivo comprimido de los mods necesarios para la instalacion
    en una carpeta compartida de drive. Si desea descargarlo manualmente para verificar
    su contenido lo puede hacer mediante el siguiente enlace:
    https://drive.google.com/file/d/1ymiW0Xk1Y_9O-JA-Vf_w147LX04PT0gw/view?usp=drive_link
    3. Se descomprime este archivo y se guarda todo su contenido en una carpeta llamada 'mods'
    4. Posteriormente se borra la carpeta de mods de minecraft y se copia todo el contenido ahí.
    Si tiene muchos mods, u otros mods que desea conservar, puede saltarte este proceso posteriormente
    y hacerlo de manera manual.
    5. Abre el minecraft con NeoForge y abre el servidor 'chill-nAo9.aternos.me'. Este es el host de acceso.
    Con esto estás dentro automáticamente :D

    Este script se irá actualizando. De momento se dará aviso para que descarguen el nuevo script si es necesario.

    Pulsa una tecla para continuar!

"""
print(initial_text)
input("\n")

# Ejecutar la verificación
is_mine_installed, minecraft_path = check_minecraft_installation()

# 1. Define las rutas
archivo_zip = 'mods.zip'
directorio_destino = 'mods'
archivo_id = '1ymiW0Xk1Y_9O-JA-Vf_w147LX04PT0gw' 
nombre_destino = archivo_zip

download_file(archivo_id, nombre_destino)
main_app(archivo_zip, directorio_destino)

if(is_mine_installed):
    partial_mods_route = "\\mods"
    complete_minemods_path = f"{minecraft_path}{partial_mods_route}"
    decision_text = f"Desea borrar los mods contenidos dentro de la carpeta {complete_minemods_path}? (S/N): "
    input_clean_mods = str(input(decision_text))
    if(input_clean_mods.lower() == 's'):
        print(f"Se borraran todos los mods de la carpeta {complete_minemods_path}")
        limpiar_carpeta(complete_minemods_path)
        copy_content(directorio_destino, complete_minemods_path)
    else:
        print("Saliendo del script. Hasta luego!")
input("Presione una tecla para salir!")