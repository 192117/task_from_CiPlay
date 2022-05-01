from rest_framework import generics, filters

from .serializers import *

class StaticSaveView(generics.CreateAPIView):
    serializer_class = SaveSerializer

class StaticListView(generics.ListAPIView):
    serializer_class = ListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'views', 'clicks', 'cost', 'cpc', 'cpm']
    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=self.request.parser_context['kwargs']['from_data'],
                                        date__lte=self.request.parser_context['kwargs']['to_data'])
        return queryset

class StaticClearView(generics.ListAPIView):
    serializer_class = ListSerializer
    queryset = Event.objects.all().delete()
    def get_queryset(self):
        queryset = Event.objects.all().delete()
        return []
