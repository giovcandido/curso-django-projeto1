from django.test import TestCase

from ..models import Category, Recipe, User


class RecipesTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def create_category(self, name='Category'):
        return Category.objects.create(name=name)

    def create_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='12345678',
        email='username@email.com'
    ):
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def create_recipe(
        self,
        category={},
        author={},
        title='Recipe title',
        description='Recipe description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutes',
        servings=5,
        servings_unit='Servings',
        preparation_steps='Recipe preparation steps',
        preparation_steps_is_html=False,
        is_published=True
    ):
        return Recipe.objects.create(
            category=self.create_category(**category),
            author=self.create_author(**author),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
