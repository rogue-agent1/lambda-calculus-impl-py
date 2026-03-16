#!/usr/bin/env python3
"""Lambda calculus — parser and beta-reduction evaluator."""
class Var:
    def __init__(self,name):self.name=name
    def __repr__(self):return self.name
    def __eq__(self,o):return isinstance(o,Var) and self.name==o.name
class Lam:
    def __init__(self,param,body):self.param=param;self.body=body
    def __repr__(self):return f"(λ{self.param}.{self.body})"
class App:
    def __init__(self,fn,arg):self.fn=fn;self.arg=arg
    def __repr__(self):return f"({self.fn} {self.arg})"
_counter=[0]
def fresh():_counter[0]+=1;return f"_{_counter[0]}"
def subst(expr,name,val):
    if isinstance(expr,Var):return val if expr.name==name else expr
    if isinstance(expr,Lam):
        if expr.param==name:return expr
        if isinstance(val,Var) and val.name==expr.param:
            new_name=fresh();new_body=subst(expr.body,expr.param,Var(new_name))
            return Lam(new_name,subst(new_body,name,val))
        return Lam(expr.param,subst(expr.body,name,val))
    if isinstance(expr,App):return App(subst(expr.fn,name,val),subst(expr.arg,name,val))
def beta_reduce(expr,max_steps=100):
    for _ in range(max_steps):
        new=_step(expr)
        if new is None:return expr
        expr=new
    return expr
def _step(expr):
    if isinstance(expr,App):
        if isinstance(expr.fn,Lam):return subst(expr.fn.body,expr.fn.param,expr.arg)
        new_fn=_step(expr.fn)
        if new_fn:return App(new_fn,expr.arg)
        new_arg=_step(expr.arg)
        if new_arg:return App(expr.fn,new_arg)
    if isinstance(expr,Lam):
        new_body=_step(expr.body)
        if new_body:return Lam(expr.param,new_body)
    return None
def main():
    # (λx.x) y → y
    expr=App(Lam("x",Var("x")),Var("y"))
    print(f"{expr} → {beta_reduce(expr)}")
    # (λx.λy.x) a b → a
    expr2=App(App(Lam("x",Lam("y",Var("x"))),Var("a")),Var("b"))
    print(f"{expr2} → {beta_reduce(expr2)}")
if __name__=="__main__":main()
