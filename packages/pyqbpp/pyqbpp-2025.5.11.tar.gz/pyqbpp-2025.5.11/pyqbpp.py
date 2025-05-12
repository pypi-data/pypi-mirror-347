# @file pyqbpp.py
#  @brief Python version of QUBO++
#  @details This file contains the implementation of a Python version of QUBO++.
#  @copyright Copyright (c) 2025 Koji Nakano
#  @license Following the QUBO++ license
#  @author Koji Nakano
#  @version 2025.05.11
#  @note This program is under development and compatibility with QUBO++ is limited.
#  @date 2025-05-11


class Var:
    num = 0
    unnamed_num = 0

    def __init__(self, *args):
        if len(args) == 0:
            self.name = f"{{{Var.num}}}"
            self.index = Var.num
            self.unnamed_index = Var.unnamed_num
            Var.num += 1
            Var.unnamed_num += 1
        elif len(args) == 1:
            self.name = args[0]
            self.index = Var.num
            Var.num += 1
        else:
            raise ValueError("Var has at most one argument")

    def __eq__(self, other):
        return isinstance(other, Var) and self.index == other.index

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Expr(self, other)

    def __radd__(self, other):
        return Expr(other, self)

    def __sub__(self, other):
        return Expr(self, Term(-1, other))

    def __rsub__(self, other):
        return Expr(other, Term(-1, self))

    def __mul__(self, other):
        if isinstance(other, int):
            return Term(other, self)
        elif isinstance(other, Var):
            return Term(self, other)
        elif isinstance(other, Term):
            return Term(*([self] + other.var), other.coeff)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        return self.index < other.index

    def __str__(self):
        return self.name


def var(*args):
    if len(args) == 0:
        return Var()

    if isinstance(args[0], str):
        var_name = args[0]
        dims = args[1:]
    else:
        var_name = None
        dims = args

    if len(dims) == 0:
        return Var(var_name)

    return Vector([
        var(
            f"{var_name}[{i}]" if var_name is not None else None,
            *dims[1:]
        )
        for i in range(dims[0])
    ])


class Term:
    def __init__(self, *args):
        self.coeff = 1
        self.vars = []
        for arg in args:
            if isinstance(arg, int):
                self.coeff *= arg
            elif isinstance(arg, Var):
                self.vars.append(arg)
            else:
                raise ValueError("Term can only have int or Var arguments")

    def __str__(self):
        if not self.vars:
            return str(self.coeff)
        var_str = "*".join(str(v) for v in self.vars)
        if self.coeff == 1:
            return var_str
        elif self.coeff == -1:
            return "-" + var_str
        else:
            return str(self.coeff) + "*" + var_str

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Expr(self, other)

    def __radd__(self, other):
        return Expr(other, self)

    def __sub__(self, other):
        if isinstance(other, Term):
            return Expr(self, Term(-other.coeff, *other.var))
        return Expr(self, Term(-1, other))

    def __rsub__(self, other):
        return Expr(other, Term(-1, *self.vars)).__add__(Term(-self.coeff + 1))

    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            return NotImplemented
        return Term(self.coeff * scalar, *self.vars)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __lt__(self, other):
        if len(self.vars) != len(other.vars):
            return len(self.vars) < len(other.vars)
        else:
            return self.vars < other.vars

    def simplify_as_binary(self):
        if len(self.vars) <= 1:
            return self
        else:
            seen = set()
            unique_vars = []
            for v in sorted(self.vars, key=lambda v: v.index):
                if v.index not in seen:
                    seen.add(v.index)
                    unique_vars.append(v)
            return Term(self.coeff, *unique_vars)


class Expr:
    def __init__(self, *args):
        self.const = 0
        self.terms = []
        for arg in args:
            if isinstance(arg, int):
                self.const += arg
            elif isinstance(arg, Term):
                self.terms.append(arg)
            elif isinstance(arg, Var):
                self.terms.append(Term(arg))
            elif isinstance(arg, Expr):
                self.const += arg.const
                self.terms += arg.terms
            else:
                raise ValueError(
                    "Expr can only have int, Var, Term, or Expr arguments")

    def __add__(self, other):
        return Expr(self, other)

    def __radd__(self, other):
        return Expr(other, self)

    def __str__(self):
        first = True
        string = ""
        if self.const != 0:
            string = str(self.const)
            first = False
        elif len(self.terms) == 0:
            return "0"
        for term in self.terms:
            if first:
                string += str(term)
                first = False
            else:
                if (term.coeff < 0):
                    string += " " + str(term)
                else:
                    string += " +" + str(term)
        return string

    def __sub__(self, other):
        if isinstance(other, Expr):
            negated = Expr()
            negated.const = -other.const
            negated.terms = [Term(-t.coeff, *t.vars) for t in other.terms]
            return Expr(self, negated)
        elif isinstance(other, Term):
            return Expr(self, Term(-other.coeff, *other.vars))
        elif isinstance(other, Var):
            return Expr(self, Term(-1, other))
        elif isinstance(other, int):
            return Expr(self, -other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        return Expr(other).__sub__(self)

    def __mul__(self, other):
        if isinstance(other, int):
            return Expr(self.const * other,
                        *[Term(t.coeff * other, *t.vars) for t in self.terms])

        elif isinstance(other, Expr):
            result_terms = []

            const_part = self.const * other.const

            for t in other.terms:
                result_terms.append(Term(t.coeff * self.const, *t.vars))
            for t in self.terms:
                result_terms.append(Term(t.coeff * other.const, *t.vars))

            for t1 in self.terms:
                for t2 in other.terms:
                    coeff = t1.coeff * t2.coeff
                    vars_combined = t1.vars + t2.vars
                    result_terms.append(Term(coeff, *vars_combined))

            return Expr(const_part, *result_terms)

        elif isinstance(other, Term):
            return self * Expr(other)

        elif isinstance(other, Var):
            return self * Expr(other)

        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __eq__(self, other):
        return sqr(self - other)

    def __repr__(self):
        return str(self)

    def simplify_as_binary(self):
        simplified_terms = sorted(
            [term.simplify_as_binary() for term in self.terms if term.coeff != 0])
        new_terms = []
        for i in range(len(simplified_terms)):
            if len(simplified_terms[i].vars) == 0:
                self.const += simplified_terms[i].coeff
            elif len(new_terms) == 0 or new_terms[-1].vars != simplified_terms[i].vars:
                new_terms.append(simplified_terms[i])
            else:
                new_terms[-1].coeff += simplified_terms[i].coeff
        self.terms = new_terms
        return self


def sqr(arg):
    if isinstance(arg, Vector):
        return Vector([sqr(item) for item in arg])
    else:
        return arg * arg


def is_nested_list(obj):
    return (
        isinstance(obj, Vector) and
        any(isinstance(item, Vector) for item in obj)
    )


def total_sum(arg):
    if not is_nested_list(arg):
        raise ValueError("Argument must be a nested list")
    return total_sum_impl(arg)


def total_sum_impl(arg):
    result = 0
    for item in arg:
        if isinstance(item, (int, Var, Term, Expr)):
            result += item
        else:
            result += total_sum_impl(item)
    return result


def vector_sum(arg):
    if not is_nested_list(arg):
        raise ValueError("Argument must be a nested list")
    return vector_sum_impl(arg)


def vector_sum_impl(arg):
    if isinstance(arg[0], (int, Var, Term, Expr)):
        return sum(arg)
    else:
        return Vector([vector_sum_impl(item) for item in arg])


def transpose(arg):
    if not is_nested_list(arg):
        raise ValueError("Argument must be a nested list")
    return Vector([
        Vector([arg[i][j] for i in range(len(arg))])
        for j in range(len(arg[0]))
    ])


class Vector:
    def __init__(self, data):
        self.data = [
            Vector(x) if isinstance(
                x, list) and not isinstance(x, Vector) else x
            for x in data
        ] if isinstance(data, list) else data

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data) if isinstance(self.data, list) else 1

    def __iter__(self):
        if isinstance(self.data, list):
            return iter(self.data)
        else:
            return iter([self.data])

    def __eq__(self, other):

        if isinstance(other, int):
            return [x == other for x in self.data]
        else:
            raise ValueError("Comparison with non-integer is not supported")

    def __repr__(self):
        return f"Vector({self.data})"
