import django_filters
from django.db.models import Q
from api.models import User


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["search", "city"]
