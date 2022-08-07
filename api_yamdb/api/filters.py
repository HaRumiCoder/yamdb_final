from rest_framework import filters


class TitleFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        genre_slug = request.query_params.get('genre')
        category_slug = request.query_params.get('category')
        name = request.query_params.get('name')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
