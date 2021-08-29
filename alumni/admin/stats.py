
from alumni.fields.major import MajorField
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import QuerySet
from typing import Any
import json

from ..fields.custom import CustomChoiceFieldMixin
from ..fields import AlumniCategoryField, TierField, DegreeField, ClassField, GenderField, CollegeField

from typing import TYPE_CHECKING
from typing import Any, Dict, Callable, List, Tuple

CHOICE_DICT = Dict[str, Callable[[QuerySet], QuerySet]]


def render_stats(request: HttpRequest, queryset: QuerySet, alumni_qualifer_text: str = "") -> HttpResponse:
    """ Renders the statistics page """

    stats = _make_stats(queryset)
    return render(request, 'stats/index.html', {"stats": json.dumps(stats), "alumni_qualifer_text": alumni_qualifer_text})


def _make_stats(queryset: QuerySet) -> Any:
    """ Generates stats for the frontend to render """

    # The return value of this function should be kept in sync with
    # the 'PortalStats' interface in assets/src/registry/stats/_view.d.ts.

    dicts = {k: _compute_stats(queryset, v) for (k, v) in stat_dicts.items()}

    return {'total': queryset.count(), **dicts}


def _compute_stats(queryset: QuerySet, choices: CHOICE_DICT) -> Dict[str, int]:
    return {k: q(queryset).count() for (k, q) in choices.items()}


def _make_choice_dict(field: str, **values: Dict[str, Any]) -> CHOICE_DICT:
    """ Creates a simple CHOICE_DICT """
    return {k: _make_filter_query(field, v) for (k, v) in values.items()}

def _make_choice_dict_from_choices(field: str, choices: CustomChoiceFieldMixin):
    """ Makes a choice dict from a list of field choices """
    ## Uncomment this to generate type definitions for the .ts file
    # TYPE = " | ".join(["'" + v + "'" for (_, v) in choices.CHOICES])
    # print("{}: _Stat< {} >;".format(field, TYPE))

    the_choices = {v: k for (k, v) in choices.CHOICES }
    return _make_choice_dict(field, **the_choices)


def _make_filter_query(field: str, value: Any):
    return lambda q: q.filter(**{field: value})

yes_no_stat = { 'yes': True, 'no': False }

stat_dicts: Dict[str, CHOICE_DICT] = {
    'approval': _make_choice_dict("approval__approval", **yes_no_stat),
    'setup': _make_choice_dict("setup__isnull", yes = False, no = True),
    'autocreated': _make_choice_dict("approval__autocreated", **yes_no_stat),
    'category': _make_choice_dict_from_choices('category', AlumniCategoryField),
    'tier': _make_choice_dict_from_choices('membership__tier', TierField),
    'atlas': _make_choice_dict('atlas__included', **yes_no_stat ),
    'degree': _make_choice_dict_from_choices('jacobs__degree', DegreeField),
    'graduation': _make_choice_dict_from_choices('jacobs__graduation', ClassField),
    'major': _make_choice_dict_from_choices('jacobs__major', MajorField),
    'gender': _make_choice_dict_from_choices('sex', GenderField),
    'college': _make_choice_dict_from_choices('jacobs__college', CollegeField),
}

__all__ = ["render_stats"]
