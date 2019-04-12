import bisect

class AlumniComponentMixin:
    """ Mixin representing a component """

    SETUP_COMPONENT_NAME = None
    COMPONENT_SETUP_URL = None


    @classmethod
    def component_exists(cls, alumni):
        """ Checks if an alumni has this component set """

        return cls.objects.filter(member=alumni).exists()
    
    @classmethod
    def component_name(cls):
        """ Gets the component name """
        name = cls.SETUP_COMPONENT_NAME
        if name is not None:
            return name
        
        return cls.member.field.remote_field.name
    
    @classmethod
    def component_setup_url(cls):
        url = cls.COMPONENT_SETUP_URL
        if url is not None:
            return url, False

        return 'setup_{}'.format(cls.component_name()), True


class AlumniRegistryMixin:
    components = [] # the list of components used by the alumni model
    component_prios = [] # the corresponding alumni priority mixin

    @classmethod
    def register_component(cls, prio):
        """ A decorator to add a component to the list of components """
        
        def decorator(f):

            # raise an error for the component
            if not issubclass(f, AlumniComponentMixin):
                raise TypeError('can only register subclass of AlumniComponentMixin')

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
        
        if issubclass(component, AlumniComponentMixin):
            return component.component_exists(self)
        else:
            raise TypeError("expected 'component' to be a subclass of AlumniComponentMixin")

    def get_first_unset_component(self):
        """ Gets the first unset component or returns None if it
        already exists. """

        for component in self.__class__.components:
            if not self.has_component(component):
                return component
        
        return None
    
    @property
    def setup_completed(self):
        """ Checks if a user has completed setup """
        return self.get_first_unset_component() is None