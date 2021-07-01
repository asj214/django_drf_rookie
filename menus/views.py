from rest_framework import status, viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuSerializer
from pages.serializers import PageSerializer


class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = MenuSerializer
    queryset = Menu.objects.prefetch_related('page')

    def get_queryset(self):
        return self.queryset

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Menu.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'parent_id': request.data.pop('parent_id', None),
            'page_id': request.data.pop('page_id', None)
        }
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        menu = self.get_object(pk)
        context = {
            'parent_id': request.data.pop('parent_id', None),
            'page_id': request.data.pop('page_id', None)
        }

        serializer = self.serializer_class(
            menu,
            data=request.data,
            context=context,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        menu = self.get_object(pk)
        menu.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuTreeView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Menu.objects.prefetch_related('page')

    def list(self, request, *args, **kwargs):
        qs = self.queryset.all()
        menus = self._build(rows=qs)
        return Response(menus)

    def _build(self, rows=[], depth=0, parent_id=None):
        ret = []
        for row in rows:
            if row.depth != depth:
                continue
            if parent_id is not None and row.parent_id != parent_id:
                continue

            add = {
                'id': row.id,
                'parent_id': row.parent_id,
                'name': row.name,
                'depth': row.depth,
                'order': row.order,
                'page': PageSerializer(row.page).data,
                'is_published': row.is_published,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'children': self._build(rows=rows, parent_id=row.id, depth=row.depth + 1)
            }

            if len(add['children']) == 0:
                add.pop('children')

            ret.append(add)

        return ret