from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    name = "Demo REST API Item Operations"
    
    def get_item_by_id(self, item_id):
        """Busca un elemento por su ID"""
        for item in data_list:
            if item.get('id') == item_id and item.get('is_active', False):
                return item
        return None
    
    def put(self, request, id):
        """Reemplaza completamente los datos de un elemento"""
        data = request.data
        
        # Validación: el ID es obligatorio
        if 'id' not in data:
            return Response(
                {'error': 'El campo ID es obligatorio para la operación PUT.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validación: el ID del cuerpo debe coincidir con el ID de la URL
        if data['id'] != id:
            return Response(
                {'error': 'El ID del cuerpo de la solicitud debe coincidir con el ID de la URL.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar el elemento existente
        existing_item = self.get_item_by_id(id)
        if not existing_item:
            return Response(
                {'error': 'Elemento no encontrado o inactivo.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Reemplazar completamente los datos
        new_data = data.copy()
        new_data['is_active'] = True  # Mantener activo
        
        # Actualizar en la lista
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                data_list[i] = new_data
                break
        
        return Response(
            {'message': 'Elemento actualizado completamente.', 'data': new_data}, 
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, id):
        """Actualiza parcialmente los campos de un elemento"""
        data = request.data
        
        # Buscar el elemento existente
        existing_item = self.get_item_by_id(id)
        if not existing_item:
            return Response(
                {'error': 'Elemento no encontrado o inactivo.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Actualizar solo los campos proporcionados
        updated_item = existing_item.copy()
        for key, value in data.items():
            if key != 'id':  # No permitir cambiar el ID
                updated_item[key] = value
        
        # Actualizar en la lista
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                data_list[i] = updated_item
                break
        
        return Response(
            {'message': 'Elemento actualizado parcialmente.', 'data': updated_item}, 
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, id):
        """Elimina lógicamente un elemento (marca como inactivo)"""
        # Buscar el elemento existente
        existing_item = self.get_item_by_id(id)
        if not existing_item:
            return Response(
                {'error': 'Elemento no encontrado o ya inactivo.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Marcar como inactivo (eliminación lógica)
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                data_list[i]['is_active'] = False
                break
        
        return Response(
            {'message': 'Elemento eliminado lógicamente.'}, 
            status=status.HTTP_200_OK
        )
