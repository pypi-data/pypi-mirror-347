from ortools.sat.python.cp_model import (
    FEASIBLE,
    INFEASIBLE,
    INT_MAX,
    INT_MIN,
    MODEL_INVALID,
    OPTIMAL,
    UNKNOWN,
)

from .. import SolverStatus


class CpSatStatus:
    cpsat_status_dict = {
        UNKNOWN: SolverStatus.UNKNOWN,
        MODEL_INVALID: SolverStatus.MODEL_INVALID,
        FEASIBLE: SolverStatus.FEASIBLE,
        INFEASIBLE: SolverStatus.INFEASIBLE,
        OPTIMAL: SolverStatus.OPTIMAL,
    }
    """Map: ortools.sat.python.cp_model status codes -> string"""

    feasible_cpsat_status_set = frozenset({FEASIBLE, OPTIMAL})
    """Set of status codes indicating a feasible solution was found."""

    @staticmethod
    def get_status_string(cpsat_status: int) -> str:
        """Returns the status string corresponding to the given status code."""
        return CpSatStatus.cpsat_status_dict.get(cpsat_status, "UNKNOWN")

    @staticmethod
    def found_feasible_solution(cpsat_status: int) -> bool:
        """Checks if a feasible solution was found based on the status code."""
        return cpsat_status in CpSatStatus.feasible_cpsat_status_set

    @staticmethod
    def get_obj_value_and_bound_for_infeasible_maximize() -> tuple[int, int]:
        """Returns the upper and lower bounds for maximization problems."""
        return INT_MIN, INT_MIN

    @staticmethod
    def get_obj_value_and_bound_for_infeasible_minimize() -> tuple[int, int]:
        """Returns the upper and lower bounds for minimization problems."""
        return INT_MAX, INT_MAX

    @staticmethod
    def get_obj_value_and_bound_for_infeasible(is_maximize: bool) -> tuple[int, int]:
        """Returns the upper and lower bounds for infeasible problems."""
        if is_maximize:
            return CpSatStatus.get_obj_value_and_bound_for_infeasible_maximize()
        else:
            return CpSatStatus.get_obj_value_and_bound_for_infeasible_minimize()
