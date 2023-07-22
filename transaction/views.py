from datetime import datetime, timedelta
from django.db.models import Sum,Q
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,BasePermission,SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary_report(request):
    # Get the current month's first day and last day
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Retrieve transactions for the current month for the logged-in user
    user_transactions = Transaction.objects.filter(
        user=request.user,
        Date__range=[first_day_of_month, last_day_of_month]
    )


    # Calculate total income and total expenses for the month using database-level aggregations
    summary_data = user_transactions.aggregate(
        total_income=Sum('Amount', filter=Q(Type='I')),
        total_expenses=Sum('Amount', filter=Q(Type='E')),
        net_cash_flow=Sum('Amount', filter=Q(Type='I')) - Sum('Amount', filter=Q(Type='E'))
    )


    report_data = {
        'user': request.user.username,
        'month': today.strftime('%B %Y'),
        'total_income': summary_data['total_income'] or 0,
        'total_expenses': summary_data['total_expenses'] or 0,
        'net_cash_flow': summary_data['net_cash_flow'] or 0,
    }

    return Response(report_data)