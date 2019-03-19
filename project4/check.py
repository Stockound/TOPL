from el import *

def check(e):
    assert type(e) is Expr
    if e.type:
        return e.type
    e.type = do_check(e)
    return e.type

def do_check(e):
    #type checks
    if type(e) is BoolExpr:
        return check_bool(e)
    if type(e) is IntExpr:
        return check_int(e)
    #bool expr checks
    if type(e) is AndExpr:
        return check_and(e)
    if type(e) is OrExpr:
        return check_or(e)
    if type(e) is NotExpr:
        return check_not(e)
    if type(e) is IfExpr:
        return check_if(e)
    #bool comp checks
    if type(e) is LtExpr:
        return check_lt(e)
    if type(e) is GtExpr:
        return check_gt(e)
    if type(e) is LeExpr:
        return check_le(e)
    if type(e) is GeExpr:
        return check_ge(e)
    #numeric expr checks
    if type(e) is AddExpr:
        return check_add(e)
    if type(e) is SubExpr:
        return check_sub(e)
    if type(e) is MulExpr:
        return check_mul(e)
    if type(e) is DivExpr:
        return check_div(e)
    if type(e) is ModExpr(e):
        return check_mod(e)
    if type(e) is NegExpr:
        return check_neg(e)
    #lambda check
    if type(e) is IdExpr:
        return check_id(e)
    if type(e) is AppExpr:
        return check_app(e)
    if type(e) is AbsExpr:
        return check_abs(e)
    if type(e) is LambdaExpr:
        return check_lambda(e)
    assert false

#type checks
def check_bool(e):
    return boolType

def check_int(e):
    return intType

#bool expr checks
def check_and(e):
    t1 = check(e.lhs)
    t2 = check(e.rhs)
    if type(t1) is BoolType and type(t2) is BoolType:
        return BoolType()
    raise Exception("invalid operands to 'and'")

def check_or(e):
    t1 = check(e.lhs)
    t2 = check(e.rhs)
    if type(t1) is BoolType and type(t2) is BoolType:
        return BoolType()
    raise Exception("invalid operands to 'or'")

def check_not(e):
    if type(e.vakue) is BoolType:
        return BoolType()
    raise Exception("invalid operand to 'not'")
    
def check_if(e):
    t1 = check(e.eIf)
    t2 = check(e.eTh)
    t3 = check(e.eEl)
    if type(t2) is type(t3):
        return type(t1)
    raise Exception("invalid operands to 'if'")

#bool comp check
def check_comp(e, op):
    if has_same_type(e.lhs, e.rhs):
        return boolType
    raise Exception(f"invalid operands to '{op}'")  

def check_lt(e):
    return check_comp(e, "<")

def check_gt(e):
    return check_comp(e, ">")

def check_le(e):
    return check_comp(e, "=<")

def check_ge(e):
    return check_comp(e, "=<")

#numeric check
def check_num(e, op):
    if is_int(e.op1) and is_int(e.op2):
        return intType
    raise Exception(f"invalid operands to '{op}'")  

def check_add(e):
    return check_num(e, "+")

def check_sub(e):
    return check_num(e, "-")

def check_mul(e):
    return check_num(e, "*")

def check_div(e):
    return check_num(e, "/")

def check_mod(e):
    return check_num(e, "%")

def check_add(e):
    return check_num(e, "+")

#lambda check
def check_id(e):
    return e.ref.type

def check_abs(e):
    t1 = e.var.type
    t2 = check(e.expr)
    return ArrowType(t1, t2)

def check_app(e):
    t1 = check(e.lhs)
    if type(t1) is not ArrowType:
        raise Exception("application to non-abstraction")
    if not is_same(t1.parm, t2):
        raise Exception("invalid operand to abstraction")
    return t2

#helpers I stole
def is_bool(x):
    if isinstance(x, Type):
        return x == boolType
    if isinstance(x, Expr):
        return is_bool(check(x))

def is_int(x):
    if isinstance(x, Type):
        return x == intType
    if isinstance(x, Expr):
        return is_int(check(x))

def is_same_type(t1, t2):
    if type(t1) is not type(t2):
        return False
    if type(t1) is BoolType:
        return True
    if type(t1) is IntType:
        return True

    assert False

def has_same_type(e1, e2):
    return is_same_type(check(e1), check(e2))