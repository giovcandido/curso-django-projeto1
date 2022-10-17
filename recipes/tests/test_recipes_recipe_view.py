from django.urls import resolve, reverse

from .. import views
from .test_recipes_base import RecipesTestBase


class RecipesRecipeViewTest(RecipesTestBase):
    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_returns_status_code_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_view_loads_correct_recipe(self):
        title = 'This is a recipe page'

        self.create_recipe(title=title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_template_doesnt_load_unpublished_recipes(self):
        recipe_id = self.create_recipe(is_published=False).id

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe_id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
