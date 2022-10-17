from django.urls import resolve, reverse

from .. import views
from .test_recipes_base import RecipesTestBase


class RecipesCategoryViewTest(RecipesTestBase):
    def test_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_category_view_returns_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:category', args=(1000,)))
        self.assertEqual(response.status_code, 404)

    def test_category_template_loads_recipes(self):
        title = 'This is a category test'

        self.create_recipe(title=title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_category_template_doesnt_load_unpublished_recipes(self):
        category_id = self.create_recipe(is_published=False).category.id

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id': category_id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
