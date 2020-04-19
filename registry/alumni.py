from __future__ import annotations

import bisect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List, Type, Callable, Optional
    from alumni.models import Alumni


class AlumniComponentMixin:
    """ Mixin representing a component """

    SETUP_COMPONENT_NAME: str = None
    COMPONENT_SETUP_URL: Optional[str] = None

    @classmethod
    def component_exists(cls, alumni: Alumni) -> bool:
        """ Checks if an alumni has this component set """

        return cls.objects.filter(member=alumni).exists()

    @classmethod
    def component_name(cls) -> str:
        """ Gets the component name """
        name = cls.SETUP_COMPONENT_NAME
        if name is not None:
            return name

        return cls.member.field.remote_field.name

    @classmethod
    def component_setup_url(cls) -> (str, bool):
        url = cls.COMPONENT_SETUP_URL
        if url is not None:
            return url, False

        return 'setup_{}'.format(cls.component_name()), True

    def is_filled(self) -> Optional[bool]:
        """ Checks if the user has filled out this component """
        return None


class AlumniRegistryMixin:
    components: List[Type[AlumniComponentMixin]] = []  # the list of components used by the alumni model
    component_prios: List[int] = []  # the corresponding alumni priority mixin

    @classmethod
    def register_component(cls, prio: int) -> Callable[[Type[AlumniComponentMixin]], Type[AlumniComponentMixin]]:
        """ A decorator to add a component to the list of components """

        def decorator(f: Type[AlumniComponentMixin]) -> Type[AlumniComponentMixin]:

            # raise an error for the component
            if not issubclass(f, AlumniComponentMixin):
                raise TypeError(
                    'can only register subclass of AlumniComponentMixin')

            # Find the insertion point within the priority list
            insertion = bisect.bisect_left(cls.component_prios, prio)

            # Insert into (components, component_prios)
            cls.components.insert(insertion, f)
            cls.component_prios.insert(insertion, prio)

            # and return the original function
            return f
        return decorator

    def has_component(self, component: Type[AlumniComponentMixin]) -> bool:
        """ Checks if this alumni has a given component"""

        if issubclass(component, AlumniComponentMixin):
            return component.component_exists(self)
        else:
            raise TypeError(
                "expected 'component' to be a subclass of AlumniComponentMixin")

    def get_first_unset_component(self) -> Optional[Type[AlumniComponentMixin]]:
        """ Gets the first unset component or returns None if it
        already exists. """

        for component in self.__class__.components:
            if not self.has_component(component):
                return component

        return None

    @property
    def setup_completed(self) -> bool:
        """ Checks if a user has completed setup """
        return self.get_first_unset_component() is None
