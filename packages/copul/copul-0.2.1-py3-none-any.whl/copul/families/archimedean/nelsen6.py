import numpy as np
import sympy

from copul.families.archimedean.biv_archimedean_copula import BivArchimedeanCopula
from copul.families.archimedean.heavy_compute_arch import HeavyComputeArch
from copul.families.other.biv_independence_copula import BivIndependenceCopula
from copul.wrapper.sympy_wrapper import SymPyFuncWrapper


class Joe(HeavyComputeArch):
    ac = BivArchimedeanCopula
    theta = sympy.symbols("theta", positive=True)
    theta_interval = sympy.Interval(1, np.inf, left_open=False, right_open=True)
    special_cases = {1: BivIndependenceCopula}

    @property
    def is_absolutely_continuous(self) -> bool:
        return True

    @property
    def _raw_generator(self):
        return -sympy.log(1 - (1 - self.t) ** self.theta)

    @property
    def _raw_inv_generator(self):
        return 1 - (1 - sympy.exp(-self.y)) ** (1 / self.theta)

    @property
    def _cdf_expr(self):
        theta = self.theta
        return 1 - (-((1 - self.u) ** theta - 1) * ((1 - self.v) ** theta - 1) + 1) ** (
            1 / theta
        )

    def cond_distr_1(self, u=None, v=None):
        theta = self.theta
        cond_distr_1 = (
            -((1 - self.u) ** theta)
            * ((1 - (1 - self.u) ** theta) * ((1 - self.v) ** theta - 1) + 1)
            ** (1 / theta)
            * ((1 - self.v) ** theta - 1)
            / (
                (1 - self.u)
                * ((1 - (1 - self.u) ** theta) * ((1 - self.v) ** theta - 1) + 1)
            )
        )
        return SymPyFuncWrapper(cond_distr_1)(u, v)

    def cond_distr_2(self, u=None, v=None):
        theta = self.theta
        cond_distr_2 = (
            (1 - self.v) ** theta
            * (1 - (1 - self.u) ** theta)
            * ((1 - (1 - self.u) ** theta) * ((1 - self.v) ** theta - 1) + 1)
            ** (1 / theta)
            / (
                (1 - self.v)
                * ((1 - (1 - self.u) ** theta) * ((1 - self.v) ** theta - 1) + 1)
            )
        )
        return SymPyFuncWrapper(cond_distr_2)(u, v)

    def lambda_L(self):
        return 0

    def lambda_U(self):
        return 2 - 2 ** (1 / self.theta)


Nelsen6 = Joe

# B5 = Joe
