from rest_framework import viewsets, filters


class AbstractViewset(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated', 'created']
    ordering = ['-updated'] 