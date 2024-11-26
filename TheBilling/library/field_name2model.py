from django.db import models
from django.db.models.fields.related import ForeignKey
from typing import Optional, Type, Literal

from orgsandpeople.models import Account


def field_name2model(model: Type[models.Model], field_name: str) -> Optional[Type[models.Model] | Literal["self"]]:
    """
    Retrieve the related model class for a given ForeignKey field in a Django model.

    This function takes a Django model class and the name of a field as input, and returns
    the related model class if the field is a ForeignKey. If the ForeignKey is self-referential,
    it returns the string "self". If the field is not a ForeignKey or is not a related field,
    the function returns None.

    Parameters:
    -----------
    model : Type[models.Model]
        The Django model class containing the field. This should be a subclass of `models.Model`.

    field_name : str
        The name of the field for which the related model is to be retrieved.

    Returns:
    --------
    Optional[Union[Type[models.Model], Literal["self"]]]
        - If the field is a ForeignKey pointing to another model, returns the class of the related model.
        - If the ForeignKey is self-referential, returns the string `"self"`.
        - If the field is not a ForeignKey or is not a related field, returns `None`.

    Raises:
    -------
    FieldDoesNotExist
        If the specified field name does not exist in the model.

    Example:
    --------
    >>> from orgsandpeople.models import Account
    >>> field_name2model(Account, 'business_unit')
    <class 'orgsandpeople.models.BusinessUnit'>

    >>> field_name2model(Account, 'non_existent_field')
    FieldDoesNotExist: Account has no field named 'non_existent_field'

    >>> field_name2model(Account, 'business_unit')
    "self"  # If the ForeignKey is self-referential

    Notes:
    ------
    This function utilizes Django's `_meta.get_field()` to access the field definition, and
    checks whether the field is a ForeignKey and a relation field. If the ForeignKey is self-referential,
    the literal `"self"` will be returned.
    """
    field = model._meta.get_field(field_name)
    if field.is_relation and isinstance(field, ForeignKey):
        return field.related_model  # Get the related model class or "self" if self-referential
    return None


if __name__ == "__main__":
    field_name = 'business_unit'
    model = Account
    related_model = field_name2model(model, field_name)
    if related_model:
        if related_model == "self":
            print("The ForeignKey is self-referential.")
        else:
            print(f"Related model: {related_model.__name__}")
    else:
        print("No related model found.")
