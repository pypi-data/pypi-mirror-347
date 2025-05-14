from typing import Any

from ..schema import Operator, LogicalOperator
from abs_exception_core.exceptions import BadRequestError

logical_operator_map = {
    LogicalOperator.AND: "$and",
    LogicalOperator.OR: "$or",
}

def apply_condition(model, operator: Operator, field: str, value: Any, is_expr: bool = False):
    print("operator", operator)
    print("field", field)
    print("value", value)

    if is_expr:
        field = f"$$item.{field}"

        if operator in {Operator.EQ, Operator.NE, Operator.GT, Operator.GTE, Operator.LT, Operator.LTE, Operator.IN, Operator.NIN}:
            return {f"${operator.value}": [field, value]}

        elif operator == Operator.BETWEEN:
            if isinstance(value, list) and len(value) == 2:
                return {
                    "$and": [
                        {"$gte": [field, value[0]]},
                        {"$lte": [field, value[1]]}
                    ]
                }
            raise BadRequestError("BETWEEN operator requires a list of two values.")

        elif operator == Operator.LIKE:
            return {
                "$regexMatch": {
                    "input": field,
                    "regex": f".*{value}.*"
                }
            }

        elif operator == Operator.ILIKE:
            return {
                "$regexMatch": {
                    "input": field,
                    "regex": f".*{value}.*",
                    "options": "i"
                }
            }

        elif operator == Operator.IS_NULL:
            return {"$eq": [field, None]}
        elif operator == Operator.IS_NOT_NULL:
            return {"$ne": [field, None]}

    else:
        mongo_ops = {
            Operator.EQ: "$eq",
            Operator.NE: "$ne",
            Operator.GT: "$gt",
            Operator.GTE: "$gte",
            Operator.LT: "$lt",
            Operator.LTE: "$lte",
            Operator.IN: "$in",
            Operator.NIN: "$nin",
            Operator.IS_NULL: "$eq",
            Operator.IS_NOT_NULL: "$ne"
        }

        if operator in mongo_ops:
            val = None if operator in {Operator.IS_NULL, Operator.IS_NOT_NULL} else value
            return {field: {mongo_ops[operator]: val}}

        elif operator == Operator.LIKE:
            return {field: {"$regex": f".*{value}.*"}}
        elif operator == Operator.ILIKE:
            return {field: {"$regex": f".*{value}.*", "$options": "i"}}
        elif operator == Operator.BETWEEN:
            if isinstance(value, list) and len(value) == 2:
                return {field: {"$gte": value[0], "$lte": value[1]}}
            raise BadRequestError("BETWEEN operator requires a list of two values.")


    raise BadRequestError(f"Unsupported operator: {operator}")