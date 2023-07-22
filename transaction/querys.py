from transaction.models import Transaction
from django.db.models import Sum,Count,Case,When,Value


# in case than you want to use the querys instead of Amount model 
# that is updated by signals.py you can use this querys.
# but if transactions table is too big, this querys can be slow
def get_balance_by_aggregation(user):
    
    aggregated_data = Transaction.objects.filter(user=user).aggregate(
    income_sum=Sum(Case(When(Type='I', then='Amount'), default=Value(0))),
    expense_sum=Sum(Case(When(Type='E', then='Amount'), default=Value(0))))

    return aggregated_data['income_sum'] - aggregated_data['expense_sum']

# def get_transactions_by_category(user,start_date,end_date):
#     return Transaction.objects.filter(
#         user=user,date__range=[start_date,end_date]
#         ).values('Category__name').annotate(
#         income_sum=Sum(Case(When(Type='I', then='Amount'), default=Value(0))),
#         expense_sum=Sum(Case(When(Type='E', then='Amount'), default=Value(0))))


