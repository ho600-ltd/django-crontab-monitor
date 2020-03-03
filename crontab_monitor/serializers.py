from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer

from crontab_monitor.models import SelectOption, Inspection, AlertLog



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']



class SelectOptionSerializer(ModelSerializer):
    resource_uri = HyperlinkedIdentityField(view_name="crontab_monitor_api_root:select_option-detail",
                                            lookup_field='pk')

    class Meta:
        model = SelectOption
        fields = '__all__'



class InspectionSerializer(ModelSerializer):
    resource_uri = HyperlinkedIdentityField(view_name="crontab_monitor_api_root:inspection-detail",
                                            lookup_field='pk')
    function_option = SelectOptionSerializer(read_only=True)

    class Meta:
        model = Inspection
        fields = '__all__'



class AlertLogSerializer(ModelSerializer):
    resource_uri = HyperlinkedIdentityField(view_name="crontab_monitor_api_root:alert_log-detail",
                                            lookup_field='pk')
    inspection = InspectionSerializer(read_only=True)
    status = SelectOptionSerializer()
    receivers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = AlertLog
        fields = '__all__'