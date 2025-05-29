from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company
from .serializers import CompanySerializer, CompanyListSerializer


class HelloWorldAPI(APIView):
    """
    A simple API view that returns a greeting
    """

    permission_classes = []  # Allow anyone to access

    def get(self, request):
        return Response({"message": "Hello from the Django API!", "status": "success"})


class CurrentTimeAPI(APIView):
    """
    An API view that returns the current server time
    """

    permission_classes = []  # Allow anyone to access

    def get(self, request):
        from datetime import datetime

        now = datetime.now()
        return Response(
            {"current_time": now.strftime("%Y-%m-%d %H:%M:%S"), "status": "success"}
        )


class CompanyListCreateAPI(generics.ListCreateAPIView):
    """
    API view to list all companies or create a new company
    Supports searching and ordering
    """

    queryset = Company.objects.all()
    permission_classes = []  # Allow anyone to access

    # Add searching and ordering
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "country_of_origin", "economic_sector"]
    ordering_fields = ["name", "country_of_origin", "economic_sector", "id"]
    ordering = ["name"]  # Default ordering

    def get_serializer_class(self):
        """
        Use different serializers for list vs create operations
        """
        if self.request.method == "GET":
            return CompanyListSerializer
        return CompanySerializer


class CompanyDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a specific company
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []  # Allow anyone to access


class CompanyStatsAPI(APIView):
    """
    API view to get company statistics and summaries
    """

    permission_classes = []  # Allow anyone to access

    def get(self, request):
        from django.db.models import Count

        # Basic counts
        total_companies = Company.objects.count()

        # Count by country
        countries = (
            Company.objects.values("country_of_origin")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Count by sector
        sectors = (
            Company.objects.values("economic_sector")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Recent companies (latest 5)
        recent_companies = Company.objects.all().order_by("-id")[:5]
        recent_data = CompanyListSerializer(recent_companies, many=True).data

        return Response(
            {
                "total_companies": total_companies,
                "companies_by_country": list(countries),
                "companies_by_sector": list(sectors),
                "recent_companies": recent_data,
                "unique_countries": Company.objects.values_list(
                    "country_of_origin", flat=True
                )
                .distinct()
                .count(),
                "unique_sectors": Company.objects.values_list(
                    "economic_sector", flat=True
                )
                .distinct()
                .count(),
            }
        )


class CompanySearchAPI(APIView):
    """
    Advanced search API for companies
    """

    permission_classes = []  # Allow anyone to access

    def get(self, request):
        query = request.query_params.get("q", "")

        if not query:
            return Response(
                {"error": "Please provide a search query using 'q' parameter"},
                status=400,
            )

        # Search across multiple fields
        from django.db.models import Q

        companies = Company.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(country_of_origin__icontains=query)
            | Q(economic_sector__icontains=query)
        ).distinct()

        serializer = CompanyListSerializer(companies, many=True)

        return Response(
            {"query": query, "count": companies.count(), "results": serializer.data}
        )
