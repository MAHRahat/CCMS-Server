from django.contrib.auth import get_user_model
from rest_framework import serializers

from ccms.models import Complaints, Categories

CCMSUser = get_user_model()


class CCMSUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom user model of the City Complaints Management System.
    """

    class Meta:
        model = CCMSUser
        fields = (
            "user_id",
            "email",
            "cell_no",
            "name",
            "address",
            "is_employee",
            "date_joined",
            "last_login",
        )
        extra_kwargs = {
            "email": {
                "read_only": True
            },
            "password": {
                "write_only": True
            }
        }


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = "__all__"
