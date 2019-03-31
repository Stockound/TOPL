from el import *
from operation import *

import copy

clone = copy.deepcopy

class Closure:
    def __init__(self, abs, env):
        self.abs = abs
        self.env = clone(env)

def eval_bool(e, store):
    return e.value

def eval_and(e, store):
    return evaluate(e.lhs, store) and evaluate(e.rhs, store)

def eval_or(e, store):
    return evaluate(e.lhs, store) or evaluate(e.rhs, store)

def eval_not(e, store):
    return not evaluate(e.expr, store)

def eval_cond(e, store):
    if evaluate(e.cond):
        return evaluate(e.true)
    else:
        return evaluate(e.false)

def eval_id(e, store):
    return store[e.ref]

def eval_abs(e, store):
    return Closure(e, store)

def eval_app(e, store):
    c = evaluate(e.lhs, store)

    if type(c) is not Closure:
        raise Exception("cannot apply a non-closure to an argument")

    v = evaluate(e.rhs, store)

    return evaluate(c.abs.expr, c.env + {c.abs.var: v})

def eval_lambda(e, store):
    return Closure(e, store)

def eval_call(e, store):
    c = evaluate(e.fn, store)

    if type(c) is not Closure:
        raise Exception("cannot apply a non-closure to an argument")

    args = []
    for a in e.args:
        args += [evaluate(a, store)]

    env = clone(c.env)
    for i in range(len(args)):
        env[c.abs.vars[i]] = args[i]

    return evaluate(c.abs.expr, env)

#no idea what tuples and records evaluate to other than a list of evaluated 
#stuff so thats what they are
def eval_tuple(e, store):
    return list(evaluate(var, store) for var in e.vars)

def eval_record(e, store):#i hope this syntax works because it's really cool
    return {key: (evaluate(value, store)) for key, value in e.vars.items()}

def eval_variant(e, store):
    if(evaluate(e.tag, store)):
        return evaluate(e.lhs, store)
    else:
        return evaluate(e.rhs, store)

def evaluate(e, store = {}):
    if type(e) is BoolExpr:
        return eval_bool(e, store)

    if type(e) is AndExpr:
        return eval_and(e, store)

    if type(e) is OrExpr:
        return eval_or(e, store)

    if type(e) is NotExpr:
        return eval_not(e, store)

    if type(e) is IdExpr:
        return eval_id(e, store)

    if type(e) is AbsExpr:
        return eval_abs(e, store)

    if type(e) is AppExpr:
        return eval_app(e, store)

    if type(e) is LambdaExpr:
        return eval_lambda(e, store)

    if type(e) is CallExpr:
        return eval_call(e, store)
    
    if type(e) is TupleExpr:
        return eval_tuple(e, store)
    
    if type(e) is RecordExpr:
        return eval_record(e, store)
    if type(e) is VariantExpr:
        return eval_variant(e, store)
