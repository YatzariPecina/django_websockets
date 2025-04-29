from django.shortcuts import render
import csv, io
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def calcular_edad(fecha_str):
        try:
            fecha_nac = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hoy = datetime.now().date()
            return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        except ValueError:
            return 'N/A'

def blog_load(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        id_proceso = request.POST.get('id_proceso')
        print(f"id proceso: {id_proceso}")

        if not csv_file.name.endswith('.csv'):
            return render(request, 'csvscanner/load.html', {'mensaje': 'El archivo no es un CSV'})

        #Extraer datos del csv y leerlo
        contenido = csv_file.read().decode('utf-8')
        lector = csv.reader(io.StringIO(contenido))
        
        # Preparar para enviar mensajes
        channel_layer = get_channel_layer()

        filas = list(lector)  # convierte a lista para poder usarla varias veces
        encabezados = filas[0] + ['dominio_correo', 'nombre_pila', 'apellido', 'longitud_nombre', 'usuario_correo', 'edad'] if filas else []
        #Generar los otros datos
        datos = []
        for fila in filas[1:]:
            id_, nombre, correo, ciudad, fecha_registro, estatus = fila[:6]
            
            # Calcula nuevas columnas
            dominio_correo = correo.split('@')[1]
            nombre_pila = nombre.split()[0]
            apellido = nombre.split()[-1]
            longitud_nombre = len(nombre)
            usuario_correo = correo.split('@')[0]
            try:
                edad = calcular_edad(fecha_registro)
            except:
                edad = 'N/A'
                
            nueva_fila = fila + [dominio_correo, nombre_pila, apellido, longitud_nombre, usuario_correo, edad]
            datos.append(nueva_fila)
            
            async_to_sync(channel_layer.group_send)(
                f'progreso_{id_proceso}',
                {
                    'type': 'recibir_logs',
                    'mensaje': f"Se proceso la fila {id_}"
                }
            )

        return render(request, 'csvscanner/load.html', {
            'encabezados': encabezados,
            'datos': datos
        })
    else:
        return render(request, 'csvscanner/load.html', {})
