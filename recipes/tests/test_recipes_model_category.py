from django.core.exceptions import ValidationError

from .test_recipes_base import RecipesTestBase


class CategoryModelTest(RecipesTestBase):
    def setUp(self) -> None:
        self.category = self.create_category(name='Category Testing')
        return super().setUp()

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_name_max_length(self):
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
