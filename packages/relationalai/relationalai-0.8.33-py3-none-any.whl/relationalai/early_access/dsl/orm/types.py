from typing import Any, Optional

from relationalai.early_access.builder import Concept as QBConcept


class Concept(QBConcept):

    def __init__(self, model, name: str, extends: list[Any] = []):
        super().__init__(name, extends, model.qb_model())
        self._dsl_model = model

    def _is_value_type(self) -> bool:
        if len(self._extends) == 1:
            ext_concept = self._extends[0]
            if ext_concept._is_primitive():
                return True
            else:
                return ext_concept._is_value_type()
        return False

    def __eq__(self, other):
        return isinstance(other, Concept) and self._name == other._name

    def __hash__(self):
        return hash(self._name)


class EntityType(Concept):

    def __init__(self, model, nm, extends: list[Concept] = [], ref_schema_name: Optional[str] = None):
        self._domain = extends
        super().__init__(model, nm, extends)
        self.__ref_schema_name = ref_schema_name

    def _qualified_name(self):
        return self._name

    def _is_composite(self):
        return len(self._domain) > 1

    def _ref_schema_name(self):
        return self.__ref_schema_name

    def _is_value_type(self) -> bool:
        return False


class ValueType(Concept):

    def __init__(self, model, nm, extends: Optional[Concept] = None):
        super().__init__(model, nm, [extends] if extends is not None else [])

    def _is_value_type(self) -> bool:
        return True