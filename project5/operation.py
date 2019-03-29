from el import *

def is_value(e):
    assert isinstance(e, Expr)
    return type(e) in (BoolExpr, IdExpr, AbsExpr, LambdaExpr)

def is_reducible(e):
    assert isinstance(e, Expr)
    return not is_value(e)

def size(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
        return 1
    if type(e) is NotExpr:
        return 1 + size(e.expr)
    if isinstance(e, BinaryExpr):
        return 1 + size(e.lhs) + size(e.rhs)
    assert False

def height(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
        return 0
    if type(e) is NotExpr:
        return 1 + height(e.expr)
    if isinstance(e, BinaryExpr):
        return 1 + max(height(e.lhs), height(e.rhs))
    assert False

def same(e1, e2):
    assert isinstance(e1, Expr)
    assert isinstance(e2, Expr)
    if type(e1) == type(e2):
        if type(e1) is BoolExpr:
            return e1.value == e2.value
        elif type(e1) is NotExpr:
            return same(e1.expr, e2.expr)
        elif type(e1) is AndExpr:
            return same(e1.rhs, e2.rhs) and same(e1.lhs, e2.lhs)
        elif type(e1) is OrExpr:
            return same(e1.rhs, e2.rhs) or same(e1.lhs, e2.lhs)
    else:
        return False

def value(e):
    assert isinstance(e, Expr)
    if type(e) is BoolExpr:
        return e.value
    if type(e) is NotExpr:
        return not value(e.expr)
    if type(e) is AndExpr:
        return value(e.lhs) and value(e.rhs)
    if type(e) is OrExpr:
        return value(e.lhs) or value(e.rhs)
    assert False

#Mine was wrong, so I copied yours
def subst(e, s):
    # Rewrite the expression 'e' by substituting references to variables
    # in 's' with their corresponding value.

    if type(e) is BoolExpr:
        # [x->s]b = b
        return e

    if type(e) is AndExpr:
        # [x->s](e1 and e2) = [x->s]e1 and [x->s]e2
        e1 = subst(e.lhs, s)
        e2 = subst(e.rhs, s)
        return AndExpr(e1, e2)

    if type(e) is OrExpr:
        # [x->s](e1 or e2) = [x->s]e1 or [x->s]e2
        e1 = subst(e.lhs, s)
        e2 = subst(e.rhs, s)
        return OrExpr(e1, e2)

    if type(e) is NotExpr:
        # [x->s](not e1) = not [x->s]e1
        e1 = subst(e.expr, s)
        return NotExpr(e1)

    if type(e) is IfExpr:
        # [x->s](if e1 then e2 else e3) = if [x->s]e1 then [x->s]e2 else [x->s]e3
        e1 = subst(e.cond, s)
        e2 = subst(e.true, s)
        e3 = subst(e.false, s)
        return IfExpr(e1, e2, e3)

    if type(e) is IdExpr:
        # [x->s]x = v
        # [x->s]y = y (y != x)
        if e.ref in s:
            return s[e.ref]
        else:
            return e

    if type(e) is AbsExpr:
        # [x->s] \x.e1 = \x.[x->s]e1
        #
        # Note that references to var  will never be replaced, so the
        # binding will be preserved when we create the expression.
        #
        # Alternatively, we could create a new variable and redo 
        # resolution on the resulting expression.
        e1 = subst(e.expr, s)
        return AbsExpr(e.var, e1)

    if type(e) is AppExpr:
        # [x->s](e1 e2) = [x->s]e1 [x->s]e2
        e1 = subst(e.lhs, s)
        e2 = subst(e.rhs, s)
        return AppExpr(e1, e2)

    if type(e) is LambdaExpr:
        # [x->s]\(x1, x2, ...).e1 = \(x1, x2, ...).[x->s]e1
        e1 = subst(e.expr, s)
        return LambdaExpr(e.vars, e1)

    if type(e) is CallExpr:
        # [x->s]e0(e1, e2, ...)
        e0 = subst(e.fn, s)
        args = list(map(lambda x: subst(x, s), e.args))
        return CallExpr(e0, args)

    assert False

#copied and modified yours as mine were wronh
def lookup(id, stk):
    # Perform name lookup. Search the scope stack for the first
    # declaration of `id`. Returns the declaration or None if 
    # the name is undeclared.
    for scope in reversed(stk):
        if id in scope:
            return scope[id]
    return None

def resolve(e, stk = []):
    # Resolve references to declared variables. This requires a scope
    # stack. A scope is a mappings from names to their declarations.
    #
    # Returns the modified tree.

    if type(e) is BoolExpr:
        # No ids here.
        return e

    if type(e) is AndExpr:
        # Recursively resolve in subexpressions.
        resolve(e.lhs, stk)
        resolve(e.rhs, stk)
        return e 

    if type(e) is OrExpr:
        # Recursively resolve in subexpressions.
        resolve(e.lhs, stk)
        resolve(e.rhs, stk)
        return e 

    if type(e) is NotExpr:
        # Recursively resolve in subexpressions.
        resolve(e.expr, stk)
        return e

    if type(e) is IfExpr:
        # Recursively resolve in subexpressions.
        resolve(e.cond, stk)
        resolve(e.true, stk)
        resolve(e.false, stk)
        return e

    if type(e) is IdExpr:
        # Perform name lookup.
        decl = lookup(e.id, stk)
        if not decl:
            raise Exception("name lookup error")

        # Bind the expression to its declaration.
        e.ref = decl
        return e

    if type(e) is AbsExpr:
        # Declare the variable by defining a new scope.
        # We could alternatively push the scope here and
        # then pop the scope after the recursive call (i.e.,
        # bracket the call with push/pop).
        resolve(e.expr, stk + [{e.var.id : e.var}])
        return e

    if type(e) is AppExpr:
        # Recursively resolve in subexpressions.
        resolve(e.lhs, stk)
        resolve(e.rhs, stk)
        return e

    if type(e) is LambdaExpr:
        # Do the same as with abstractions, but declare
        # all variables simultaneously.
        resolve(e.expr, stk + [{var.id : var for var in e.vars}])
        return e

    if type(e) is CallExpr:
        # Recursively resolve in each subexpression.
        resolve(e.fn, stk)
        for a in e.args:
            resolve(e.fn, stk)
        return e

    if type(e) is TupleExpr:
        # TODO: Need to resolve all subexpression
        return e

    assert False


def step(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
        return e
    #boolean logic
    elif type(e) is NotExpr:
        if is_reducible(e.expr):
            return NotExpr(step(e.expr))
        return BoolExpr(not e.expr.value)
    elif type(e) is AndExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value and e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return AndExpr(step(e.lhs), e.rhs)
        else:
            return AndExpr(e.lhs, step(e.rhs))
    elif type(e) is OrExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value or e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return OrExpr(step(e.lhs), e.rhs)
        else:
            return OrExpr(e.lhs, step(e.rhs))
    elif type(e) is IfExpr:
        if is_reducible(e.eIf):
            return IfExpr(step(e.eIf), e.eTh, e.eEl)
        if e.eIf.value:
            return e.eTh
        else:
            return e.eEl
    #Application of lambda
    elif type(e) is AppExpr:
        if is_reducible(e.lhs):
            return AppExpr(step(e.lhs), e.rhs)
        if type(e.lhs) is not AbsExpr:
            raise Exception("attempted to apply non-lambda")
        if is_reducible(e.rhs):
            return AppExpr(e.lhs, step(e.rhs))
        #lhs is a lambda, rhs is non-reducible
        sub = {e.lhs.var: e.rhs}
        return subst(e.lhs.expr, sub)
    #call expression
    #Mine was wrong, so I copied yours
    elif type(e) is CallExpr: 
        if is_reducible(e.fn):
            return CallExpr(step(e.fn), e.args)

        if len(e.args) < len(e.fn.vars):
            raise Exception("too few arguments")
        if len(e.args) > len(e.fn.vars):
            raise Exception("too many arguments")

        for i in range(len(e.args)):
            if is_reducible(e.args[i]):
                return CallExpr(e.fn, e.args[:i] + [step(e.args[i])] + e.args[i+1:])

        # Map parameters to arguments.
        s = {}
        for i in range(len(e.args)):
            s[e.fn.vars[i]] = e.args[i]

        # Substitute through the definition.
        return subst(e.fn.expr, s)
    assert False

def reduce(e):
    while not is_value(e):
        e = step(e)
        print(e)
    return e
