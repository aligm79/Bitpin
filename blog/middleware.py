from django.db import connection
import logging

logger = logging.getLogger(__name__)

class QueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        connection.queries.clear()
        
        response = self.get_response(request)

        self.print_queries()

        return response

    def print_queries(self):
        if connection.queries:
            print(f"Executed SQL Queries:")
            for query in connection.queries:
                print(query['sql'])
                print()