from django.urls import resolve, reverse

from .. import views
from .test_recipes_base import RecipesTestBase


class RecipesViewsTest(RecipesTestBase):
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
