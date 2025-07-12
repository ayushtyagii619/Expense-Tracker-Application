from django.shortcuts import render
from django.db.models import Sum,Avg
from django.db.models.functions import TruncDay,TruncWeek,TruncMonth
from .models import User,Expense
from .serializers import RegisterSerializer, LoginSerializer,ExpenseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from datetime import datetime

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class RegisterApiView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'Registraion Success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens(user)
                return Response({'token':token,'msg':'Login Successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseCreateListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        expenses = Expense.objects.filter(user=request.user)

        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseAnalyticsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        expenses = Expense.objects.filter(user=request.user)

        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])

        # Total Expenses
        total = expenses.aggregate(total_expense=Sum('amount'))['total_expense'] or 0

        # Category-wise Breakdown
        category_breakdown = expenses.values('category').annotate(total=Sum('amount'))

        # Trends
        trend_type = request.GET.get('trend', 'monthly')  # daily, weekly, monthly
        if trend_type == 'daily':
            trend_data = expenses.annotate(period=TruncDay('date'))
        elif trend_type == 'weekly':
            trend_data = expenses.annotate(period=TruncWeek('date'))
        else:
            trend_data = expenses.annotate(period=TruncMonth('date'))

        trend_summary = trend_data.values('period').annotate(
            total=Sum('amount'),
            average=Avg('amount')
        ).order_by('period')

        return Response({
            'total_expenses': total,
            'category_breakdown': category_breakdown,
            'trends': trend_summary
        }, status=status.HTTP_200_OK)
# Create your views here.
