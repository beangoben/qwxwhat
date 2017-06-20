__version__ = "0.1"

from pythonwhat.sct_syntax import *


@state_dec
def check_exercise(state, float_vars, numpy_vars, func_calls, func_defs):
    # error messages
    type_msg = "__JINJA__: **type** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
    type_expr = 'type({:s})'
    shape_msg = "__JINJA__: **shape** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
    shape_expr = '{:s}.shape'
    contents_msg = "__JINJA__: **solution** **contents** are different. Rounded to 4 decimal places, we expected `{{sol_eval}}`, got `{{stu_eval}}`."
    contents_expr = 'np.round({:s}, decimals = 4)'
    func_msg = "Did you forget to use `{}`?"
    # check function definitions
    for i, v in func_defs.items():
        test_function_definition(i, results=v)
    # floating values
    for i in float_vars:
        test_object(i, do_eval=True)
    # check numpy vars
    for key in numpy_vars:
        check_object(key)  \
            .has_equal_value(expr_code=type_expr.format(key), incorrect_msg=type_msg)  \
            .has_equal_value(expr_code=shape_expr.format(key), incorrect_msg=shape_msg) \
            .has_equal_value(expr_code=contents_expr.format(key), incorrect_msg=contents_msg)
    # function calls via re
    for func in func_calls:
        test_student_typed(
            "{}\s*\(".format(func), not_typed_msg=func_msg.format(func))
    return state


@state_dec
def check_numpy(state, key):
    # error messages
    type_msg = "__JINJA__: **type** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
    type_expr = 'type({:s})'
    shape_msg = "__JINJA__: **shape** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
    shape_expr = '{:s}.shape'
    contents_msg = "__JINJA__: **solution** **contents** are different. Rounded to 4 decimal places, we expected `{{sol_eval}}`, got `{{stu_eval}}`."
    contents_expr = 'np.round({:s}, decimals = 4)'
    check_object(key)  \
        .has_equal_value(expr_code=type_expr.format(key), incorrect_msg=type_msg)  \
        .has_equal_value(expr_code=shape_expr.format(key), incorrect_msg=shape_msg) \
        .has_equal_value(expr_code=contents_expr.format(key), incorrect_msg=contents_msg)
    return state