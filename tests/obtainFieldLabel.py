from shopping_registry.models import Purchase

def obtainFieldLabel(label, object):
    field_label = object._meta.get_field(label).verbose_name

    return field_label
