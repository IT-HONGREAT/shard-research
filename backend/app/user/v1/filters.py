from django_filters import CharFilter
from django_filters.rest_framework import FilterSet


class UserFilter(FilterSet):
    location = CharFilter(field_name="location")
