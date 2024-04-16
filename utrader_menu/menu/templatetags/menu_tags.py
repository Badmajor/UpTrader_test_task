from django import template
from django.db.models import Prefetch

from menu.models import Menu, MenuItem

register = template.Library()


def build_menu_structure(menu: Menu, named_url: str) -> dict:
    menu_structure = dict()
    items = menu.items.all()
    for item in items:
        if item.named_url == named_url:
            menu_structure[item.id] = list(item.children.all())
            if hasattr(item.parent, 'named_url'):
                menu_structure.update(
                    build_menu_structure(menu, item.parent.named_url)
                )
    menu_structure[None] = [item for item in items if not item.parent_id]
    return menu_structure


def render_menu_html(menu_structure: dict,
                     named_url: str,
                     parent=None) -> str:
    html = '<ul>'
    for item in menu_structure.get(parent, []):
        active = 'active' if named_url == item.named_url else ''
        html += (f'<li class="{active}">'
                 f'<a href="{item.named_url}">{item.name}</a>')
        if item.id in menu_structure:
            html += render_menu_html(menu_structure, named_url, item.id)
        html += '</li>'
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name) -> str:
    try:
        path = context['request'].path
        named_url = path.replace('/', '')
        menu = Menu.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=MenuItem.objects.select_related(
                    'parent',
                ).prefetch_related(
                    'children'
                )
            )
        ).get(name=menu_name)

        current_structure = build_menu_structure(menu, named_url)
        return render_menu_html(current_structure, named_url)
    except (Menu.DoesNotExist, KeyError):
        return ''
