from typing import TYPE_CHECKING
from typing import Callable, List, Any, Dict, Set, Tuple, Optional


class CSVParser(object):
    """ CSVParser can parse a list of lists into a parsed set of JSON values """

    def __init__(self) -> None:
        super().__init__()

        # internal id for groups
        self._counter = 0

        # contains a list of mappings from group id to required field ids
        self._groups: Dict[int, List[str]] = {}

        # contains a list of mappings from field id -> group id
        self._fieldmap: Dict[str, int] = {}

        # names of the targeted fields
        self._targets: Dict[int, str] = {}

        # contains a mapping from group id -> mapping function
        self._mappers: Dict[int, Callable[[List[str]], Any]] = {}

    def register(self, fields: List[str], target: str, map: Callable[[List[str]], Any]):
        """ Register a new field that can be loaded """
        if target == "" or "" in fields:
            raise Exception('Target and Fields must not be the empty')

        # get a new group id
        group_id: int = self._counter
        self._counter += 1

        # check that none of the field ids are used
        for field in fields:
            if field in self._fieldmap:
                raise Exception('Field {} already used by group'.format(field))

        # store the group ids for all the fields
        for field in fields:
            self._fieldmap[field] = group_id

        # store the required fields and map
        self._groups[group_id] = [f for f in fields]
        self._mappers[group_id] = map
        self._targets[group_id] = target

    def prepare(self, fields: List[str], required: Optional[List[str]] = None) -> Tuple[Dict[str, List[int]], Dict[str, Callable[[List[str]], Any]]]:
        """ Parses a list of fields into a list of indexes """

        # check that fields are unique!
        non_empty_fields = list(filter(lambda f: f != '', fields))
        if len(non_empty_fields) != len(set(non_empty_fields)):
            raise Exception('fields contain duplicate field')

        # check that all the fields exist
        # and keep track of referenced groups and targets!
        groups: Set[int] = set()
        targets: Set[str] = set()
        for field in fields:
            # ignore empty field
            if field == '':
                continue

            if field not in self._fieldmap:
                raise Exception('Unknown field {}'.format(field))

            group = self._fieldmap[field]
            groups.add(group)
            targets.add(self._targets[group])

        if required is None:
            required = list()
        for target in required:
            if target not in targets:
                raise Exception(
                    'Target {} is required, but not provided by any field. '.format(target))

        # check that all the groups have all the requirements!
        # also track which group has which index!
        indexes: Dict[str, List[int]] = {}
        mappers: Dict[str, Callable[[List[str]], Any]] = {}
        for group in groups:
            # check that all the fields are there
            for field in self._groups[group]:
                if field not in fields:
                    raise Exception(
                        'Group {} requires field {}, but it is not provided'.format(group, field))

            # store all the indexes for the target
            target = self._targets[group]
            indexes[target] = [fields.index(field)
                               for field in self._groups[group]]
            mappers[target] = self._mappers[group]

        # and return
        return indexes, mappers

    def parse(self, fields: List[str], values: List[List[Any]], required: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """ Parses a list of fields and values """

        # check that the values are of the correct length
        count = len(fields)
        for (i, v) in enumerate(values):
            if len(v) != count:
                raise Exception(
                    'Malformed values: Index {} is not of expected length'.format(i))

        # figure out which indexes everything is at
        indexes, mappers = self.prepare(fields, required=required)

        # prepare a list of results
        results: List[Dict[str, Any]] = [{} for _ in values]

        for (target, idxs) in indexes.items():
            mapper = mappers[target]

            # apply the mapper to each target and save it!
            for (index, value) in enumerate(values):
                params: List[str] = list(map(lambda i: value[i], idxs))
                results[index][target] = mapper(params)

        # and done!
        return results
