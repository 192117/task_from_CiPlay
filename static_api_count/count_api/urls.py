from django.urls import path, register_converter
from datetime import datetime
from .views import StaticSaveView, StaticListView, StaticClearView

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('save/', StaticSaveView.as_view(), name='save'),
    path('show/<yyyy:from_data>/<yyyy:to_data>/', StaticListView.as_view(), name='show'),
    path('clear/', StaticClearView.as_view(), name='clear')
]