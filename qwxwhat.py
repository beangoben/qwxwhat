__version__ = "0.1.6"

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


@state_dec
def check_numpy_array(name, state=None):
    """Test a numpy array object. Return that object.

    Args:
        name: name of the object to be tested.
    """
    # check if is defined
    obj = Ex(state).check_object(name)

    # Check is a numpy array
    obj.is_instance(np.ndarray)
    # check if it has equal
    #obj.has_equal_value(expr_code=TYPE_EXPR.format(key), incorrect_msg=TYPE_MSG)
    # check if it has the same shape
    obj.has_equal_value(expr_code=SHAPE_EXPR.format(name),
                        incorrect_msg=SHAPE_MSG)
    # check if it has the same value
    obj.has_equal_value(expr_code=CONTENTS_EXPR.format(name),
                        incorrect_msg=CONTENTS_MSG)

    # return object state for chaining
    return obj


@state_dec
def check_exercise(arrays, state=None):
    for name in arrays:
        Ex(state) >> check_numpy_array(name)
    return


def test_exercise(arrays, state=None):
    for name in arrays:
        Ex(state) >> check_numpy_array(name)
    return
# def check_function_call(name, state=None):
#     Ex(state).test_student_typed("{}\s*\(".format(name), not_typed_msg=func_msg.format(func))
#     return

# # check function definitions
# for i, v in func_defs.items():
#     Ex().test_function_definition(i, results=v)
# # floating values
# for i in float_vars:
#     Ex().check_object(i).has_equal_value(expr_code=contents_expr.format(
#         i), incorrect_msg='Contents differ from solution.')
# # check numpy vars
# for key in numpy_vars:
#     Ex().check_object(key)  \
#         .has_equal_value(expr_code=type_expr.format(key), incorrect_msg=type_msg)  \
#         .has_equal_value(expr_code=shape_expr.format(key), incorrect_msg=shape_msg) \
#         .has_equal_value(expr_code=contents_expr.format(key), incorrect_msg=contents_msg)
# # function calls via re
# for func in func_calls:


# def test_numpy(state, key):

#     return state
