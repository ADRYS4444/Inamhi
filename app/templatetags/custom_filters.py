from django import template
from app.models import Chofer

register = template.Library()

@register.filter
def get_item(choferes, chofer_id):
    return choferes.get(id=chofer_id).nombre