from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,BasePermission,SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction,Category
from .serializers import TransactionSerializer,CategorySerializer


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only permissions to any user (GET, HEAD, OPTIONS requests)
        if request.method in SAFE_METHODS:
            return True

        # Allow POST, PUT, PATCH, DELETE methods only for admin users
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the transaction.
        return obj.user == request.user

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner]
    # queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    model = Transaction
    queryset = Transaction.objects.all()
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     # Additional logic or customization before creating the transaction
    #     # For example, you can modify the request data before saving it to the database.
    #     # Here, we'll set the user to the authenticated user making the request.
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)  # Set the user to the authenticated user

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# {"username":"abc2","token":
#  {"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5ODgxNzI4LCJpYXQiOjE2ODk4Nzg3MjgsImp0aSI6IjllOTQzZWQ0MGJlMDQ4NGM5NWFmMmRmY2M0MDJiOTBkIiwidXNlcl9pZCI6NH0.SOiM_0KQPcOm5S4K_1_KobRAcOj2P5yHrToJZWcRzfE",
# "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTk2NTEyOCwiaWF0IjoxNjg5ODc4NzI4LCJqdGkiOiI4YmE0NDNhMjA1ZTM0MmI3YjY1ZTdhMTI3YjcwOTU1NSIsInVzZXJfaWQiOjR9.p4Gjbo35okBog-2KR8jrO861kbexs8nXHBvgL7Zithg"}}