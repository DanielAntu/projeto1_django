from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Recipe
from ..serializers import RecipeSerializer
from tag.models import Tag
from ..serializers import TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from ..permisions import IsOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import status

# http_method_names=['get', 'post']

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10

class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')
        if category_id is not '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs
    
    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(),]
        
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )

# class RecipeAPIv2List(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination
    # def get(self, request):
    #     recipes = Recipe.objects.get_published()[:10]
    #     serializer = RecipeSerializer(instance=recipes, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = RecipeSerializer(data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() 
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv2Pagination

    # def get_recipe(self, pk):
    #     recipe = get_object_or_404(
    #         Recipe.objects.get_published(),
    #         pk=pk
    #     )

    #     return recipe
        
    # def get(self, request, pk):
    #     recipe = self.get_recipe(pk)

    #     serializer = RecipeSerializer(instance=recipe, many=False, context={'request': request})
    #     return Response(serializer.data)

    # def patch(self, request, pk):
    #     recipe = self.get_recipe(pk)

    #     serializer = RecipeSerializer(
    #         instance=recipe, 
    #         data=request.data, 
    #         many=False, 
    #         context={'request': request},
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def delete(self, request, pk):
    #     recipe = self.get_recipe(pk)

    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(http_method_names=['get', 'post'])
# def recipe_api_list(request):
#     if request.method == 'GET':
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(instance=recipes, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = RecipeSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save(
#             author_id=1, category_id=1, tags=[1, 2]
#         ) 
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['get', 'patch', 'delete'])
# def recipe_api_detail(request, pk):
#     recipe = get_object_or_404(
#         Recipe.objects.get_published(),
#         pk=pk
#     )
#     if request.method == 'GET':
#         serializer = RecipeSerializer(instance=recipe, many=False, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PATCH':
#         serializer = RecipeSerializer(
#             instance=recipe, 
#             data=request.data, 
#             many=False, 
#             context={'request': request},
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "detail": "Eita"
    #     }, status=status.HTTP_404_NOT_FOUND)

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)