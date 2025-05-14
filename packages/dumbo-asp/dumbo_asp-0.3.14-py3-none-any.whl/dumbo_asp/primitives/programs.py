import base64
import dataclasses
from collections import defaultdict
from dataclasses import InitVar
from functools import cached_property, cache
from typing import Optional, Iterable, Dict, List

import clingo
import clingo.ast
import typeguard
from dumbo_utils.primitives import PrivateKey
from dumbo_utils.validation import validate

from dumbo_asp import utils
from dumbo_asp.primitives.atoms import GroundAtom, SymbolicAtom
from dumbo_asp.primitives.models import Model
from dumbo_asp.primitives.parsers import Parser
from dumbo_asp.primitives.predicates import Predicate
from dumbo_asp.primitives.rules import SymbolicRule
from dumbo_asp.primitives.terms import SymbolicTerm


@typeguard.typechecked
@dataclasses.dataclass(frozen=True)
class SymbolicProgram:
    __rules: tuple[SymbolicRule, ...]
    __parsed_string: Optional[str]

    key: InitVar[PrivateKey]
    __key = PrivateKey()

    def __post_init__(self, key: PrivateKey):
        self.__key.validate(key)

    @staticmethod
    def of(*args: SymbolicRule | Iterable[SymbolicRule]) -> "SymbolicProgram":
        rules = []
        for arg in args:
            if type(arg) is SymbolicRule:
                rules.append(arg)
            else:
                rules.extend(arg)
        return SymbolicProgram(tuple(rules), None, key=SymbolicProgram.__key)

    @staticmethod
    def parse(string: str) -> "SymbolicProgram":
        rules = tuple(SymbolicRule.parse(utils.extract_parsed_string(string, rule.location))
                      for rule in Parser.parse_program(string))
        return SymbolicProgram(rules, string, key=SymbolicProgram.__key)

    def __str__(self):
        return '\n'.join(str(rule) for rule in self.__rules) if self.__parsed_string is None else self.__parsed_string

    def __len__(self):
        return len(self.__rules)

    def __getitem__(self, item: int):
        return self.__rules[item]

    def __iter__(self):
        for rule in self.__rules:
            yield rule

    @cached_property
    def with_named_anonymous_variables(self) -> "SymbolicProgram":
        return SymbolicProgram.of(rule.with_named_anonymous_variables for rule in self)

    @cached_property
    def herbrand_universe(self) -> set[SymbolicTerm]:
        res = set()

        def get_arguments(term):
            for argument in term.arguments:
                if argument.type == clingo.SymbolType.Function and argument.arguments:
                    get_arguments(argument)
                else:
                    res.add(SymbolicTerm.parse(str(argument)))

        for atom in self.herbrand_base:
            get_arguments(atom)
        return res

    @cached_property
    def herbrand_base(self) -> Model:
        control = clingo.Control()
        control.add(
            '\n'.join(f"{atom} :- {rule.body_as_string(drop_negative_literals=True)}."
                      for rule in self for atom in rule.head_elements)
        )
        control.ground([("base", [])])
        return Model.of_atoms(atom.symbol for atom in control.symbolic_atoms)

    @cached_property
    def herbrand_base_without_false_predicate(self) -> Model:
        return self.herbrand_base.drop(Predicate.false())

    @cached_property
    def herbrand_base_false_predicate_only(self) -> Model:
        return self.herbrand_base.filter(when=lambda at: at.predicate == Predicate.false().with_arity(2))

    @cached_property
    def rules_grouped_by_false_predicate(self):
        atoms = self.herbrand_base_false_predicate_only
        res = defaultdict(list)
        variables = {}
        for atom in atoms:
            key = base64.b64decode(atom.arguments[0].arguments[0].string.encode()).decode()
            res[key].append(atom.arguments[1])
            variables[key] = {arg.string: index for index, arg in enumerate(atom.arguments[0].arguments[1].arguments)}
        return res, variables

    def serialize(self, *, base64_encode: bool = True) -> tuple[GroundAtom, ...]:
        return tuple(GroundAtom.parse(atom) for atom in self.serialize_as_strings(base64_encode=base64_encode))

    def serialize_as_strings(self, *, base64_encode: bool = True) -> List[str]:
        res = []
        for rule in self:
            res.extend(rule.serialize_as_strings(base64_encode=base64_encode))
        return res

    @cached_property
    def predicates(self) -> tuple[Predicate, ...]:
        res = set()
        for rule in self:
            res.update(rule.predicates)
        return tuple(res)

    @cache
    def process_constants(self) -> "SymbolicProgram":
        rules = []
        constants = {}
        for rule in self:
            if rule.is_fact:
                head_atom = rule.head_atom
                if head_atom.predicate_name == "__const__":
                    validate("arity", head_atom.predicate_arity, equals=2, help_msg="Error in defining constant")
                    name, value = head_atom.arguments
                    constants[str(name)] = value
                    rules.append(rule.disable())
                    continue
            rules.append(rule.apply_term_substitution(**constants))

        return SymbolicProgram.of(rules)

    @cache
    def process_with_statements(self) -> "SymbolicProgram":
        rules = []
        statements_queue = []
        for rule in self:
            if rule.is_fact:
                head_atom = rule.head_atom
                if head_atom.predicate_name == "__with__":
                    statements_queue.append(tuple(SymbolicAtom.parse(str(argument))
                                                  for argument in head_atom.arguments))
                    rules.append(rule.disable())
                    continue
                if head_atom.predicate_name == "__end_with__":
                    validate("no arguments", head_atom.arguments, length=0)
                    statements_queue.pop()
                    rules.append(rule.disable())
                    continue
            for statement in statements_queue:
                for literal in statement:
                    rule = rule.with_extended_body(literal)
            rules.append(rule)
        validate("all __with__ are terminated", statements_queue, length=0,
                 help_msg=f"{len(statements_queue)} unterminated __with__ statements")

        return SymbolicProgram.of(rules)

    def apply_predicate_renaming(self, **kwargs: Predicate) -> "SymbolicProgram":
        return SymbolicProgram.of(rule.apply_predicate_renaming(**kwargs) for rule in self)

    def expand_global_safe_variables(self, *, rule: SymbolicRule, variables: Iterable[str],
                                     herbrand_base: Optional[Model] = None) -> "SymbolicProgram":
        rules = []
        for __rule in self.__rules:
            if rule != __rule:
                rules.append(__rule)
            else:
                rules.extend(__rule.expand_global_safe_variables(
                    variables=variables,
                    herbrand_base=self.herbrand_base if herbrand_base is None else herbrand_base
                ))
        return SymbolicProgram.of(rules)

    def expand_global_safe_variables_in_rules(
            self,
            rules_to_variables: Dict[SymbolicRule, Iterable[str]],
            herbrand_base: Optional[Model] = None,
    ) -> "SymbolicProgram":
        if not rules_to_variables:
            return self
        rules = []
        for __rule in self.__rules:
            if __rule in rules_to_variables.keys():
                rules.extend(__rule.expand_global_safe_variables(
                    variables=rules_to_variables[__rule],
                    herbrand_base=self.herbrand_base if herbrand_base is None else herbrand_base,
                ))
            else:
                rules.append(__rule)
        return SymbolicProgram.of(rules)

    def expand_global_and_local_variables(self, *, expand_also_disabled_rules: bool = False,
                                          herbrand_base: Optional[Model] = None) -> "SymbolicProgram":
        rules = []
        for rule in self.__rules:
            if not rule.disabled or expand_also_disabled_rules:
                rules.extend(
                    rule.expand_global_and_local_variables(
                        herbrand_base=self.herbrand_base if herbrand_base is None else herbrand_base
                    )
                )
            else:
                rules.append(rule)
        return SymbolicProgram.of(rules)

    def move_before(self, *pattern: SymbolicAtom) -> "SymbolicProgram":
        def key(rule: SymbolicRule):
            return 0 if rule.match(*pattern) else 1
        return SymbolicProgram.of(sorted([rule for rule in self.__rules], key=key))

    def to_zero_simplification_version(self, *, extra_atoms: Iterable[GroundAtom] = (), 
                                       compact=False) -> "SymbolicProgram":
        false_predicate = Predicate.false().name
        return SymbolicProgram.of(
            [rule.to_zero_simplification_version(compact=compact) for rule in self],
            SymbolicRule.parse('{' + '; '.join(str(atom) for atom in extra_atoms) + f"}} :- {false_predicate}.")
            if extra_atoms else [],
            SymbolicRule.parse(f"{{{false_predicate}}}."),
            SymbolicRule.parse(f":- {false_predicate}.") if compact else
            SymbolicRule.parse(f":- #count{{0 : {false_predicate}; "
                               f"RuleID, Substitution "
                               f": {false_predicate}(RuleID, Substitution)}} > 0."),
        )
