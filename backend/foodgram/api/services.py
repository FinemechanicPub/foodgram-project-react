from django.core.files.base import ContentFile

LIST_ITEM = '- {name}: {amount} {unit}'
LIST = """
           Ваш список покупок

{ingredients}
"""


def render_txt(shopping_list: list, filename: str):
        ingredient_text = '\n'.join(
            LIST_ITEM.format(
                name =item['ingredient_name'],
                unit=item['unit'],
                amount=item['total_amount']
            ) for item in shopping_list
        )
        return ContentFile(
            LIST.format(
                ingredients=ingredient_text
            ).encode(encoding='utf-8'),
            f'{filename}.txt'
        )