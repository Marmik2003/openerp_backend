from rest_framework import serializers

from users.models import Business, Employee, EmployeeType, EmployeeTypePermission, EmployeeGroup, Subscription


class FullBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'name', 'address', 'phone', 'email', 'avatar', 'description', 'subscription')


