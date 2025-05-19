import requests
import sys
import time

API_KEY = "e0dd8b18-f259-4c21-b7e4-38a4fb560165"
BASE_URL = "https://graphhopper.com/api/1/route"

def obtener_coordenadas(ciudad, pais="Chile"):
   url = "https://nominatim.openstreetmap.org/search"
   params = {
       "q": f"{ciudad}, {pais}",
       "format": "json",
       "limit": 1
   }
   headers = {
       "User-Agent": "DEVASC-Evaluation-Script/1.0"
   }
  
   try:
       response = requests.get(url, params=params, headers=headers)
       response.raise_for_status()
       data = response.json()
       if data:
           return float(data[0]["lat"]), float(data[0]["lon"])
       else:
           print(f"No se encontraron coordenadas para {ciudad}, {pais}")
           return None
   except Exception as e:
       print(f"Error al obtener coordenadas: {e}")
       return None

def calcular_ruta(origen, destino, vehiculo):
   coord_origen = obtener_coordenadas(origen)
   if not coord_origen:
       return None
  
   coord_destino = obtener_coordenadas(destino)
   if not coord_destino:
       return None
  
   params = {
       "point": [f"{coord_origen[0]},{coord_origen[1]}", f"{coord_destino[0]},{coord_destino[1]}"],
       "vehicle": vehiculo,
       "locale": "es",
       "instructions": "true",
       "calc_points": "true",
       "key": API_KEY
   }
  
   try:
       response = requests.get(BASE_URL, params=params)
       response.raise_for_status()
       return response.json()
   except Exception as e:
       print(f"Error al calcular la ruta: {e}")
       return None

def mostrar_resultado(datos_ruta, origen, destino, vehiculo):
   if not datos_ruta or "paths" not in datos_ruta or not datos_ruta["paths"]:
       print("No se pudo calcular la ruta.")
       return
  
   ruta = datos_ruta["paths"][0]
   distancia_km = ruta["distance"] / 1000  
   tiempo_total_seg = ruta["time"] / 1000  
  
   horas = int(tiempo_total_seg // 3600)
   minutos = int((tiempo_total_seg % 3600) // 60)
   segundos = int(tiempo_total_seg % 60)
  
   print("\n" + "="*50)
   print(f"RUTA: {origen.upper()} → {destino.upper()}")
   print("="*50)
   print(f"Distancia: {distancia_km:.2f} km")
   print(f"Duración: {horas} horas, {minutos} minutos, {segundos} segundos")
   print("="*50)

def seleccionar_vehiculo():
   opciones = {
       "1": "car",
       "2": "bike",
       "3": "foot",
       "4": "small_truck",
       "5": "truck"
   }
  
   print("\nSeleccione un tipo de vehículo:")
   print("1. Automóvil")
   print("2. Bicicleta")
   print("3. A pie")
   print("4. Camioneta")
   print("5. Camión")
  
   while True:
       opcion = input("Ingrese el número de su elección: ")
       if opcion in opciones:
           return opciones[opcion]
       print("Opción inválida, intente nuevamente.")

def main():
   print("\n" + "*"*60)
   print("*" + " "*19 + "CALCULADORA DE RUTAS" + " "*19 + "*")
   print("*" + " "*21 + "API GRAPHHOPPER" + " "*22 + "*")
   print("*"*60)
  
   vehiculo = seleccionar_vehiculo()
  
   print("\nIndique la ciudad de origen y destino para medir la distancia:")
   origen_req = ""
   destino_req = ""
  
   while origen_req.lower() != "santiago":
       origen_req = input("Indique la ciudad de origen: ")
       if origen_req.lower() != "santiago":
           print("Para este cálculo específico, debe ingresar 'Santiago' como origen.")
  
   while destino_req.lower() != "ovalle":
       destino_req = input("Indique la ciudad de destino: ")
       if destino_req.lower() != "ovalle":
           print("Para este cálculo específico, debe ingresar 'Ovalle' como destino.")
  
   print("\nCalculando ruta, por favor espere...")
   ruta_santiago_ovalle = calcular_ruta("Santiago", "Ovalle", vehiculo)
   if ruta_santiago_ovalle:
       mostrar_resultado(ruta_santiago_ovalle, "Santiago", "Ovalle", vehiculo)
   else:
       print(f"No se pudo calcular la ruta entre Santiago y Ovalle.")
  
   while True:
       print("\n" + "-"*60)
       print("Ingrese 'q' para salir o presione ENTER para continuar")
       opcion = input("> ")
      
       if opcion.lower() == 'q':
           print("\n¡Gracias por usar el programa!")
           break
      
       origen = input("\nCiudad de origen: ")
       destino = input("Ciudad de destino: ")
      
       if origen and destino:
           cambiar = input("\n¿Desea cambiar el tipo de vehículo? (s/n): ")
           if cambiar.lower() == 's':
               vehiculo = seleccionar_vehiculo()
          
           print("\nCalculando ruta, por favor espere...")
           ruta = calcular_ruta(origen, destino, vehiculo)
           if ruta:
               mostrar_resultado(ruta, origen, destino, vehiculo)
           else:
               print(f"No se pudo calcular la ruta entre {origen} y {destino}.")
       else:
           print("Debe ingresar ciudades válidas.")

if __name__ == "__main__":
   main()
