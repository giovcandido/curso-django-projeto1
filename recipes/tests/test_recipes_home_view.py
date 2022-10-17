from django.urls import resolve, reverse

from .. import views
from .test_recipes_base import RecipesTestBase


class RecipesHomeViewTest(RecipesTestBase):
    def test_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_returns_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found.', response.content.decode('utf-8'))

    def test_home_template_loads_recipes(self):
        self.create_recipe()

        response = self.client.get(reverse('recipes:home'))

        content = response.content.decode('utf-8')
        context_recipes = response.context['recipes']

        self.assertIn('Recipe title', content)
        self.assertEqual(len(context_recipes), 1)

    def test_home_template_doesnt_load_unpublished_recipes(self):
        self.create_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found.', response.content.decode('utf-8'))
