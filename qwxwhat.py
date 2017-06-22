__version__ = "0.3.1"

from pythonwhat.check_syntax import state_dec, Ex
import numpy as np

# ERROR messages
TYPE_MSG = "__JINJA__: **type** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
TYPE_EXPR = 'type({:s})'
SHAPE_MSG = "__JINJA__: **shape** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
SHAPE_EXPR = '{:s}.shape'
CONTENTS_MSG = "__JINJA__: **solution** **contents** are different. Rounded to 4 decimal places, we expected `{{sol_eval}}`, got `{{stu_eval}}`."
CONTENTS_EXPR = 'np.round({:s}, decimals = 4)'
FUNC_MSG = "Did you forget to use `{}`?"
FLOAT_MSG = 'Contents differ from solution.'


@state_dec
def check_numpy_array(name, state=None):
    """Test a numpy array object. Return that object.

    Args:
        name: name of the object to be tested.
    """
    # check if is defined
    obj = Ex(state).check_object(name)
    # check if it has same type of variable
    obj.has_equal_value(expr_code=TYPE_EXPR.format(name),
                        incorrect_msg=TYPE_MSG)
    # check if it has the same shape
    obj.has_equal_value(expr_code=SHAPE_EXPR.format(name),
                        incorrect_msg=SHAPE_MSG)
    # check if it has the same value
    obj.has_equal_value(expr_code=CONTENTS_EXPR.format(name),
                        incorrect_msg=CONTENTS_MSG)

    # return object state for chaining
    return obj


@state_dec
def check_function_call(name, state=None):
    obj = Ex(state).test_student_typed(
        "{}\s*\(".format(name), not_typed_msg=FUNC_MSG.format(name))
    return obj


def test_exercise(func_defs={}, arrays=[], floats=[], func_calls=[],
                  state=None):
    # check function definitions
    for i, v in func_defs.items():
        Ex(state).test_function_definition(i, results=v)

    # numpy arrays
    for name in arrays:
        Ex(state) >> check_numpy_array(name)

    # floating values
    for name in floats:
        Ex(state).check_object(name).has_equal_value(
            expr_code=CONTENTS_EXPR.format(name), incorrect_msg=FLOAT_MSG)

    # function calls via re
    for func in func_calls:
        Ex(state) >> check_function_call(func)
    return
