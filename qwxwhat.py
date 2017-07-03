__version__ = "0.4.1"

from pythonwhat.check_syntax import state_dec, Ex
import numpy as np

# ERROR messages
TYPE_MSG = "__JINJA__: **type** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
TYPE_EXPR = 'type({:s})'
SHAPE_MSG = "__JINJA__: **shape** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
SHAPE_EXPR = '{:s}.shape'
CONTENTS_MSG = "__JINJA__: **solution** **contents** are different acoording to numpy.allclose. We expected `{{sol_eval}}`, but got `{{stu_eval}}`."
#CONTENTS_EXPR = 'np.round({:s}, decimals = 4)'
FUNC_CALL_MSG = "Did you forget to use `{}`?"
FLOAT_MSG = "__JINJA__: **solution** **contents** for {:s} are different acoording to numpy.allclose.`."
FUNC_TEST_MSG = "FMT:Calling it with arguments `({:s})` should result in `{{str_sol}}`, instead got `{{str_stu}}`."
CHEAT_MSG = "You cannot use the provided test function `{}` in your solution!"


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
    obj.has_equal_value(func=lambda x, y: np.allclose(
        x, y, rtol=1e-04, atol=1e-05),
        incorrect_msg=CONTENTS_MSG)

    # return object state for chaining
    return obj


@state_dec
def check_float_value(name, state=None):
    """Test a float.

     Args:
         name: name of the object to be tested.
     """
    # check if is defined
    obj = Ex(state).check_object(name)
    # check if it has same type of variable
    obj.has_equal_value(expr_code=TYPE_EXPR.format(name),
                        incorrect_msg=TYPE_MSG)
    # check if it has the same value
    obj.has_equal_value(func=lambda x, y: np.allclose(x, y, rtol=1e-04, atol=1e-05),
                        incorrect_msg=FLOAT_MSG.format(name))
    return obj


@state_dec
def check_function_call(name, state=None):
    obj = Ex(state).test_student_typed(
        "{}\s*\(".format(name), not_typed_msg=FUNC_CALL_MSG.format(name))
    return obj


@state_dec
def check_testfunction_call(name, state=None):
    obj = Ex(state).test_not(test_student_typed(
        "{:s}\s*\(".format(name)), msg=CHEAT_MSG)

    return obj


@state_dec
def check_function_definition(name, v, state=None):

    Ex(state).test_function_definition(name)

    obj = Ex(state).check_function_def(name)
    for vi in v:
        arg_string = str(vi).replace("[", "").replace("]", "")
        obj.call(vi).has_equal_value(func=lambda x,
                                     y: np.allclose(x, y, rtol=1e-04, atol=1e-05),
                                     incorrect_msg=FUNC_TEST_MSG.format(arg_string))
    return obj


def test_exercise(func_defs={}, arrays=[], floats=[], func_calls=[],
                  state=None):
    # check function definitions
    for i, v in func_defs.items():
        Ex(state) >> check_function_definition(i, v)

    # numpy arrays
    for name in arrays:
        Ex(state) >> check_numpy_array(name)

    # floating values
    for name in floats:
        Ex(state) >> check_float_value(name)

    # function calls via re
    for func in func_calls:
        Ex(state) >> check_function_call(func)

    for indx in range(len(func_defs)):
        name = 'test_function{:d}'.format(indx + 1)
        Ex(state) >> check_testfunction_call(name)

    return
