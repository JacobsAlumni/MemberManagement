from django.db import models

__all__ = ['CustomTextChoiceField', 'CustomIntegerChoiceField']

class CustomChoiceFieldMixin:
    """ A mixin for custom choice fields """

    CHOICES = []
    @classmethod
    def get_class_choices(cls):
        """ Returns the choices used by this class """

        return cls.CHOICES

    DEFAULT_CHOICE = None # the default choice
    @classmethod
    def get_class_default(cls):
        """ Returns the default choice of this class """

        return cls.DEFAULT_CHOICE

class CustomTextChoiceField(CustomChoiceFieldMixin, models.CharField):
    """ A Custom Choice Field for Text """

    @classmethod
    def get_class_max_length(cls):
        """ Returns the maximum length of this class """
        choices = cls.get_class_choices()
        return max([len(k) for (k, v) in choices])

    def __init__(self, **kwargs):
        kwargs['max_length'] = self.get_class_max_length()
        kwargs['choices'] = self.get_class_choices()
        kwargs['default'] = self.get_class_default()
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['choices']
        del kwargs['default']
        return name, path, args, kwargs

class CustomIntegerChoiceField(CustomChoiceFieldMixin, models.IntegerField):
    """ A Custom Choice Field for Integers """

    def __init__(self, **kwargs):
        kwargs['choices'] = self.get_class_choices()
        kwargs['default'] = self.get_class_default()
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['choices']
        del kwargs['default']
        return name, path, args, kwargs
