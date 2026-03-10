from django.db import models


class UpperCaseCharField(models.CharField):
    """Custom CharField that automatically converts string values to uppercase
    before saving to the database
    """

    def get_prep_value(self, value) -> str:
        """Prepare the value before saving to the database
        """
        value = super().get_prep_value(value)

        if isinstance(value, str):
            return value.upper()

        return value
