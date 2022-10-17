from django.urls import resolve, reverse

from .. import views
from .test_recipes_base import RecipesTestBase


class RecipesSearchViewTest(RecipesTestBase):
    def test_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<test>')
        self.assertIn('Search for &quot;&lt;test&gt;&quot;',
                      response.content.decode('utf-8'))

    def test_search_can_find_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.create_recipe(
            slug='one', title=title1, author={'username': 'one'})
        recipe2 = self.create_recipe(
            slug='two', title=title2, author={'username': 'two'})

        search_url = reverse('recipes:search')

        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response3 = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response3.context['recipes'])
        self.assertIn(recipe2, response3.context['recipes'])
