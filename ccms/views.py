import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from ccms.permissions import IsAnyEmployee, IsSuperUser
from ccms.serializers import *


@api_view(['GET'])
@permission_classes((IsAnyEmployee or IsSuperUser,))
def citizens_list(request):
    if request.method == 'GET':
        users = CCMSUser.objects.filter(is_employee=False)
        users_serializer = CCMSUserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes((IsAnyEmployee or IsSuperUser,))
def employees_list(request):
    if request.method == 'GET':
        users = CCMSUser.objects.filter(is_employee=True)
        users_serializer = CCMSUserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)


@api_view(['GET', 'DELETE'])
@permission_classes((IsAnyEmployee or IsSuperUser,))
def users_list(request):
    if request.method == 'GET':
        users = CCMSUser.objects.all()
        users_serializer = CCMSUserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            deleted_items = CCMSUser.objects.all().delete()
            return JsonResponse({'message': 'Deleted all'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def user_details(request, pk):
    user_permitted = (not request.user.is_employee) and int(request.user.user_id) == int(pk) and request.method != 'DELETE'
    employee_permitted = request.user.is_employee and request.method != 'DELETE'
    if not (user_permitted or employee_permitted or request.user.is_superuser):
        raise PermissionError
    try:
        user = CCMSUser.objects.get(pk=pk)
    except CCMSUser.DoesNotExist:
        return JsonResponse({'message': 'Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = CCMSUserSerializer(user)
        return JsonResponse(user_serializer.data)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = CCMSUserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAnyEmployee or IsSuperUser,))
def categories_list(request):
    if request.method == 'GET':
        categories = Categories.objects.all()
        categories_serializer = CategoriesSerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)
    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategoriesSerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        deleted_items = Categories.objects.all().delete()
        return JsonResponse({'message': 'Deleted all'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAnyEmployee or IsSuperUser,))
def categories_details(request, pk):
    try:
        category = Categories.objects.get(pk=pk)
    except Categories.DoesNotExist:
        return JsonResponse({'message': 'Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        category_serializer = CategoriesSerializer(category)
        return JsonResponse(category_serializer.data)
    elif request.method == 'PUT':
        category_data = JSONParser().parse(request)
        category_serializer = CategoriesSerializer(category, data=category_data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(category_serializer.data)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def complaints_list(request):
    cs = request.GET.get('cs')
    if request.method == 'GET':
        if not (request.user.is_employee or request.user.is_superuser):
            raise PermissionError("You are not permitted")
        if cs is None:
            complaints = Complaints.objects.all()
        else:
            complaints = Complaints.objects.filter(status=cs)
        complaints_serializer = ComplaintsSerializer(complaints, many=True)
        return JsonResponse(complaints_serializer.data, safe=False)
    elif request.method == 'POST':
        complaint_data = JSONParser().parse(request)
        complaint_data["citizen_id"] = request.user.user_id
        complaint_data["category_id"] = search_for_category(complaint_data["description"])
        complaint_serializer = ComplaintsSerializer(data=complaint_data)
        if complaint_serializer.is_valid():
            complaint_serializer.save()
            return JsonResponse(complaint_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(complaint_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            raise PermissionError
        deleted_items = Complaints.objects.all().delete()
        return JsonResponse({'message': 'Deleted all'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def complaints_details(request, pk):
    user_permitted = (not request.user.is_employee) and int(request.user.user_id) == int(pk) and request.method in SAFE_METHODS
    employee_permitted = request.user.is_employee and request.method != 'DELETE'
    if not (user_permitted or employee_permitted or request.user.is_superuser):
        raise PermissionError
    try:
        complaint = Complaints.objects.get(pk=pk)
    except Complaints.DoesNotExist:
        return JsonResponse({'message': 'Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        complaint_serializer = ComplaintsSerializer(complaint)
        return JsonResponse(complaint_serializer.data)
    elif request.method == 'PUT':
        complaint_data = JSONParser().parse(request)
        complaint_serializer = ComplaintsSerializer(complaint, data=complaint_data, partial=True)
        if complaint_serializer.is_valid():
            complaint_serializer.save()
            return JsonResponse(complaint_serializer.data)
        return JsonResponse(complaint_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        complaint.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def complaints_of_citizen(request, cid):
    if request.user.is_superuser or request.user.is_employee or int(request.user.user_id) == int(cid):
        try:
            complaint = Complaints.objects.filter(citizen_id=cid)
        except Complaints.DoesNotExist:
            return JsonResponse({'message': 'Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        complaint_serializer = ComplaintsSerializer(complaint, many=True)
        return JsonResponse(complaint_serializer.data, safe=False)


def search_for_category(description):
    categories_serializer = CategoriesSerializer(Categories.objects.all(), many=True)
    categories_json = json.dumps(categories_serializer.data)
    categories_json = json.loads(categories_json)
    for categories in categories_json:
        if categories["keyword"] in description:
            return categories["category_id"]
    return 1
