from el import *
from operation import *
from evaluate import *

test = resolve(UniType(["X", "Y"], FnType(["X"], "X")))
print(test)
