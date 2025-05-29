from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company
from .serializers import CompanySerializer, CompanyListSerializer
from .scrapers import ScraperManager


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


class CompanyScraperAPI(APIView):
    """
    API endpoint to trigger data scraping from external sources
    """

    permission_classes = []  # Allow anyone to access for demo

    def post(self, request):
        """Trigger data scraping"""
        source = request.data.get("source", "all")
        query = request.data.get("query", None)
        limit = request.data.get("limit", 10)

        # Validate source
        valid_sources = ["mock", "crunchbase", "opencorporates", "all"]
        if source not in valid_sources:
            return Response(
                {"error": f"Invalid source. Must be one of: {valid_sources}"},
                status=400,
            )

        try:
            scraper_manager = ScraperManager()

            if source == "all":
                companies = scraper_manager.fetch_from_all_sources(query, limit)
                message = "Fetched from all sources"
            else:
                companies = scraper_manager.fetch_from_source(source, query, limit)
                message = f"Fetched from {source}"

            # Serialize the companies for response
            from .serializers import CompanyListSerializer

            serializer = CompanyListSerializer(companies, many=True)

            return Response(
                {
                    "message": message,
                    "companies_fetched": len(companies),
                    "query": query,
                    "source": source,
                    "companies": serializer.data,
                }
            )

        except Exception as e:
            return Response({"error": f"Error during scraping: {str(e)}"}, status=500)

    def get(self, request):
        """Get information about available scrapers"""
        return Response(
            {
                "available_sources": [
                    {"name": "mock", "description": "Mock API data for testing"},
                    {
                        "name": "crunchbase",
                        "description": "Crunchbase company data (requires API key)",
                    },
                    {
                        "name": "opencorporates",
                        "description": "OpenCorporates public company data",
                    },
                    {"name": "all", "description": "Fetch from all available sources"},
                ],
                "usage": {
                    "POST": {
                        "source": "string (optional, default: 'all')",
                        "query": "string (optional, search query)",
                        "limit": "integer (optional, default: 10)",
                    }
                },
            }
        )


class CompanyDataSourcesAPI(APIView):
    """
    API to get statistics about data sources and last fetch times
    """

    permission_classes = []

    def get(self, request):
        """Get data source statistics"""
        from django.db.models import Count

        # Get companies created in the last 24 hours (assuming they're from scrapers)
        recent_companies = Company.objects.filter(
            id__gte=1  # This is a simple way, you might want to add a 'created_at' field
        )

        return Response(
            {
                "total_companies": Company.objects.count(),
                "recent_companies": recent_companies.count(),
                "companies_by_country": list(
                    Company.objects.values("country_of_origin")
                    .annotate(count=Count("id"))
                    .order_by("-count")[:10]
                ),
                "companies_by_sector": list(
                    Company.objects.values("economic_sector")
                    .annotate(count=Count("id"))
                    .order_by("-count")[:10]
                ),
                "scraper_info": {
                    "last_run": "Not tracked yet (add timestamp fields to track this)",
                    "available_sources": ["mock", "crunchbase", "opencorporates"],
                },
            }
        )
