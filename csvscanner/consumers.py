import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Cada cliente que se conecte se le asigna un id o se conecta con un id
        # Revisar variables de sesion por un id
        self.id_proceso = self.scope['url_route']['kwargs']['id_proceso']
        self.room_group_name = f'progreso_{self.id_proceso}'
        
        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        
        # Aceptar conexion
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def recibir_logs(self, event):
        await self.send(text_data=json.dumps({
            'mensaje': event['mensaje']
        }))