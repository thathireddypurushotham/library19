import django_filters
from .models import *

class Search_book(django_filters.filterset):
	class Meta:
		model = Search
		fields = '__all__'