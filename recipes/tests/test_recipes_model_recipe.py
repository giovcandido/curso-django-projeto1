from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipes_base import Recipe, RecipesTestBase


class RecipeModelTest(RecipesTestBase):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

    def create_recipe_filling_fields_without_default(self):
        recipe = Recipe(
            category=self.create_category(name='Category'),
            author=self.create_author(username='newuser'),
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Servings',
            preparation_steps='Recipe preparation steps'
        )
        recipe.full_clean()
        recipe.save()

        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_false_by_default(self):
        recipe = self.create_recipe_filling_fields_without_default()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_false_by_default(self):
        recipe = self.create_recipe_filling_fields_without_default()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.assertEqual(str(self.recipe), self.recipe.title)
