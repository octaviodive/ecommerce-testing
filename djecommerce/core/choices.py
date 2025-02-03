# myapp/choices.py
from enum import Enum

class CategoryChoices(Enum):
    SHIRT = 'S', 'Shirt'
    SPORT_WEAR = 'SW', 'Sport wear'
    OUTWEAR = 'OW', 'Outwear'

class LabelChoices(Enum):
    PRIMARY = 'P', 'Primary'
    SECONDARY = 'S', 'Secondary'
    DANGER = 'D', 'Danger'

class AddressChoices(Enum):
    BILLING = 'B', 'Billing'
    SHIPPING = 'S', 'Shipping'

def enum_to_choices(enum_cls):
    return [(choice.value[0], choice.value[1]) for choice in enum_cls]



