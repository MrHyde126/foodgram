import os
from io import BytesIO

from django.db.models import Sum
from django.db.models.expressions import Exists, OuterRef, Value
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

# from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import BASE_DIR
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    ShoppingCart,
    Tag,
)
from .permissions import IsAdminOwnerOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeRetrieveSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOwnerOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeRetrieveSerializer
        return RecipeCreateUpdateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(
                    Favorite.objects.filter(
                        user=self.request.user, recipe=OuterRef('id')
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        user=self.request.user, recipe=OuterRef('id')
                    )
                ),
            ).select_related('author')
        return Recipe.objects.annotate(
            is_in_shopping_cart=Value(False),
            is_favorited=Value(False),
        ).select_related('author')

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        user = request.user
        serializer = FavoriteSerializer(
            data={'user': user.id, 'recipe': pk}, context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if favorite:
            favorite.delete()
            return Response(
                {'detail': 'Рецепт удален из избранного'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'detail': 'Ошибка удаления из избранного'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        user = request.user
        serializer = ShoppingCartSerializer(
            data={'user': user.id, 'recipe': pk}, context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, id=pk)
        shopping = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if shopping:
            shopping.delete()
            return Response(
                {'detail': 'Рецепт удален из списка покупок'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'detail': 'Ошибка удаления из списка покупок'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredientAmount.objects.select_related('recipe')
            .filter(recipe__shopping_cart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(total_amount=Sum('amount'))
        )
        today = timezone.now().today()
        buffer = BytesIO()
        offset = 700
        pdf = Canvas(buffer)
        font_path = os.path.join(BASE_DIR, 'fonts/arial.ttf')
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdf.setFont('Arial', 18)
        pdf.drawString(150, 750, f'Список покупок для {request.user.username}')
        pdf.setFontSize(14)
        for index, ingredient in enumerate(ingredients, start=1):
            pdf.drawString(
                80,
                offset,
                (
                    f'{index}) {ingredient["ingredient__name"]} -'
                    f' {ingredient["total_amount"]}'
                    f' {ingredient["ingredient__measurement_unit"]}'
                ),
            )
            offset -= 30
            if offset < 80:
                pdf.showPage()
                pdf.setFont('Arial', 14)
                offset = 750
        pdf.drawString(130, 50, f'Файл сгенерирован Foodgram {today:%d.%m.%Y}')
        pdf.save()
        buffer.seek(0)
        # filename = f'{slugify(request.user.username)}\'s_shopping_list.pdf'
        return FileResponse(buffer, as_attachment=True, filename='123.pdf')


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
