import django_filters
from .models import Company


class CompanyFilter(django_filters.FilterSet):
    """
    Filter set for Company model with various filtering options
    """

    name = django_filters.CharFilter(
        lookup_expr="icontains", help_text="Filter by company name (case-insensitive)"
    )
    country = django_filters.CharFilter(
        field_name="country_of_origin",
        lookup_expr="icontains",
        help_text="Filter by country",
    )
    sector = django_filters.CharFilter(
        field_name="economic_sector",
        lookup_expr="icontains",
        help_text="Filter by economic sector",
    )
    description = django_filters.CharFilter(
        lookup_expr="icontains", help_text="Search in description"
    )

    # Exact matches
    country_exact = django_filters.CharFilter(
        field_name="country_of_origin",
        lookup_expr="exact",
        help_text="Exact country match",
    )
    sector_exact = django_filters.CharFilter(
        field_name="economic_sector",
        lookup_expr="exact",
        help_text="Exact sector match",
    )

    # Multiple choice filters
    countries = django_filters.CharFilter(
        field_name="country_of_origin",
        lookup_expr="in",
        help_text="Multiple countries (comma-separated)",
    )
    sectors = django_filters.CharFilter(
        field_name="economic_sector",
        lookup_expr="in",
        help_text="Multiple sectors (comma-separated)",
    )

    class Meta:
        model = Company
        fields = [
            "name",
            "country",
            "sector",
            "description",
            "country_exact",
            "sector_exact",
        ]
