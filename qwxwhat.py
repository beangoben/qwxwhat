__version__ = "0.1.3"

from sqlwhat.check_syntax import *


# error messages
type_msg = "__JINJA__: **type** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
type_expr = 'type({:s})'
shape_msg = "__JINJA__: **shape** **mismatch**: expected `{{sol_eval}}`, got `{{stu_eval}}`."
shape_expr = '{:s}.shape'
contents_msg = "__JINJA__: **solution** **contents** are different. Rounded to 4 decimal places, we expected `{{sol_eval}}`, got `{{stu_eval}}`."
contents_expr = 'np.round({:s}, decimals = 4)'

@state_dec
def test_numpy(state, key):

    check_object(key)  \
        .has_equal_value(expr_code=type_expr.format(key), incorrect_msg=type_msg)  \
        .has_equal_value(expr_code=shape_expr.format(key), incorrect_msg=shape_msg) \
        .has_equal_value(expr_code=contents_expr.format(key), incorrect_msg=contents_msg)

    return state
