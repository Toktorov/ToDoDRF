from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.todo.models import ToDo
from apps.todo.serializers import ToDoSerializer, ToDoCreateSerializer
from apps.todo.permissions import IsOwnerPermissions
from rest_framework import filters

# Create your views here.
class TodoAPIView(ListAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAdminUser, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('title', 'description')

class ToDoCreateAPIView(CreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoCreateSerializer
    permission_classes = (IsOwnerPermissions, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if self.request.user.id == int(serializer.initial_data['user']):
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TodoUpdateAPIView(UpdateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsOwnerPermissions, )

class ToDoDestroyAPIView(DestroyAPIView):
    queryset = ToDo.objects.all()
    permission_classes = (IsOwnerPermissions, )

class ToDoAllDestroyAPIView(DestroyAPIView):
    queryset = ToDo.objects.all()
    permission_classes = (IsOwnerPermissions, )

    def delete(self, request, *args, **kwargs):
        todo = ToDo.objects.filter(user=request.user)
        todo = [t for t in todo.delete()]
        return Response({'delete' : 'Все такски удалены'})