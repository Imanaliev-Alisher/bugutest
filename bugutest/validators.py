import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:

    def validate(self, password, user=None):
        if not re.findall(r'[A-Za-z]', password):
            raise ValidationError(
                _("The password must contain at least one letter."),
                code='password_no_letter',
            )
        if not re.findall(r'\d', password):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one letter and one digit."
        )
