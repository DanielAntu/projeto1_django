from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'Recipe Preparation steps',
        )
        return recipe
    
#     def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
#         self.recipe.title = 'A'*70
#         with self.assertRaises(ValidationError):
#             self.recipe.full_clean()

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_step_is_html, msg='Recipe preparation_step_is_html is not false')

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published, msg='Recipe is_published is not false')

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed, msg=f'Recipe string representation need to be the same as "{needed}"')