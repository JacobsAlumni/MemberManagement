import bisect

from django.db import models

class AlumniRegistryMixin:
    components = [] # the list of components used by the alumni model
    component_prios = [] # the corresponding alumni priority mixin

    @classmethod
    def register_component(cls, prio):
        """ A decorator to add a component to the list of components """
        
        def decorator(f):
            # Find the insertion point within the priority list
            insertion = bisect.bisect_left(cls.component_prios, prio)

            # Insert into (components, component_prios)
            cls.components.insert(insertion, f)
            cls.component_prios.insert(insertion, prio)

            # and return the original function
            return f
        return decorator

    def has_component(self, component):
        """ Checks if this alumni has a given component"""
        
        if issubclass(component, models.Model):
            return component.objects.filter(member=self).exists()
        else:
            raise TypeError("expected 'component' to be a subclass of model")

    def get_first_unset_component(self):
        """ Gets the first unset component or returns None if it
        already exists. """

        for c in self.__class__.components:
            if not self.has_component(c):
                if hasattr(c, 'SETUP_COMPONENT_NAME'):
                    return c.SETUP_COMPONENT_NAME
                else:
                    return c.member.field.remote_field.name
        return None
    
    @property
    def setup_completed(self):
        """ Checks if a user has completed setup """
        return self.get_first_unset_component() is None