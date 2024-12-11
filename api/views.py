from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer
from todo.models import Todo


class TodoList(generics.ListAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        user  = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

class TodoListCreate(generics.ListCreateAPIView):
    # ListAPIView requires two mandatory attributes, serializer_class and
    # queryset.
    # We specify TodoSerializer which we have earlier implemented
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')
    
    # Perform_create personaliza la lógica de la creación de un objeto antes de que sea guardado en la db
    # En este caso se personaliza el método ya que se necesita especificar qué usuario ha creado el todo
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)