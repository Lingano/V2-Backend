"""
Simple database browser views for PostgreSQL inspection
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import json


class DatabaseBrowserView(View):
    """Simple web-based PostgreSQL browser"""

    def get(self, request):
        """Display database browser interface"""
        return render(request, "database_browser.html")


class DatabaseTablesAPI(View):
    """API to list all database tables"""

    def get(self, request):
        with connection.cursor() as cursor:
            # Get all tables in the database
            cursor.execute("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)

            tables = []
            for row in cursor.fetchall():
                table_name, table_type = row

                # Get row count for each table
                cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                row_count = cursor.fetchone()[0]

                tables.append(
                    {"name": table_name, "type": table_type, "row_count": row_count}
                )

        return JsonResponse({"tables": tables})


class DatabaseTableDataAPI(View):
    """API to view data from a specific table"""

    def get(self, request, table_name):
        limit = int(request.GET.get("limit", 100))
        offset = int(request.GET.get("offset", 0))

        with connection.cursor() as cursor:
            # Get column information
            cursor.execute(
                """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """,
                [table_name],
            )

            columns = []
            for row in cursor.fetchall():
                columns.append(
                    {"name": row[0], "type": row[1], "nullable": row[2] == "YES"}
                )

            # Get table data
            cursor.execute(
                f'''
                SELECT * FROM "{table_name}" 
                ORDER BY 1 
                LIMIT %s OFFSET %s
            ''',
                [limit, offset],
            )

            rows = []
            for row in cursor.fetchall():
                # Convert each row to a list, handling special types
                row_data = []
                for item in row:
                    if item is None:
                        row_data.append(None)
                    else:
                        row_data.append(str(item))
                rows.append(row_data)

            # Get total count
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            total_count = cursor.fetchone()[0]

        return JsonResponse(
            {
                "table_name": table_name,
                "columns": columns,
                "rows": rows,
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
            }
        )


class DatabaseQueryAPI(View):
    """API to execute custom SQL queries"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get("query", "").strip()

            if not query:
                return JsonResponse({"error": "No query provided"}, status=400)

            # Only allow SELECT queries for safety
            if not query.upper().startswith("SELECT"):
                return JsonResponse(
                    {"error": "Only SELECT queries are allowed"}, status=400
                )

            with connection.cursor() as cursor:
                cursor.execute(query)

                if cursor.description:
                    # Query returned results
                    columns = [col[0] for col in cursor.description]
                    rows = []
                    for row in cursor.fetchall():
                        row_data = []
                        for item in row:
                            if item is None:
                                row_data.append(None)
                            else:
                                row_data.append(str(item))
                        rows.append(row_data)

                    return JsonResponse(
                        {
                            "success": True,
                            "columns": columns,
                            "rows": rows,
                            "row_count": len(rows),
                        }
                    )
                else:
                    return JsonResponse(
                        {"success": True, "message": "Query executed successfully"}
                    )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
