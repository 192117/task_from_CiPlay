from .models import Event
from rest_framework import serializers
import re

class SaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['date', 'views', 'clicks', 'cost']

    def validate(self, data):
        if not re.match(r'([12][09][0-9][0-9])\-(0[1-9]|1[0-2])\-(0[1-9]|[12][0-9]|3[01])',
                        data['date'].strftime('%Y-%m-%d')):
            raise serializers.ValidationError({'date': 'Incorrect date!'})
        if data['views'] or data['clicks'] or data['cost']:
            if data['views'] < 0 or data['clicks'] < 0 or data['cost'] < 0:
                raise serializers.ValidationError({'views/clicks/cost': 'Must be non-negative'})
        return data


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['date', 'views', 'clicks', 'cost', 'cpc', 'cpm']
