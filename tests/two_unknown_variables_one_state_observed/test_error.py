import numpy as np
import pytest
from nisi import PSO, Model

class EqSystem(Model):
    def __init__(self, params=None):
        super().__init__(params)
        self._params = params

    def model(self, t, y, *args):
        k = self.unknown_const
        alpha = 0.5
        beta  = 1
        delta = -1
        omega = k[0]
        F     = k[1]
        # non-ideal coeff [1]
        a_0 = 2.0
        b_0 = 0.01
        c_0 = 0.0

        dy = np.zeros(len(self.x0),)
        dy[0] = y[1]
        dy[1] = -alpha*y[1] -delta*y[0] -beta*y[0]**3 + F*np.cos(y[2]  + a_0*np.sin(b_0*y[2]+c_0))
        dy[2] = omega
        return dy

@pytest.fixture
def fixture_sys_a():
    params = {'optmizer': {'lowBound': [0.1 , 0.1],
                            'upBound': [5.0,  0.5],
                            'maxVelocity':  2, 
                            'minVelocity': -2,
                            'nPop': 10,
                            'nVar': 2,
                            'social_weight': 2.0,
                            'cognitive_weight': 1.0,
                            'w': 0.9,
                            'beta': 0.1,
                            'w_damping': 0.999,
                            'escape_min_vel_percent': 0.0005,
                           'escape_min_error': 2e-3},
                'dyn_system': {'model_path': '',
                                'external': None,
                                'state_mask' : [True, False, False],
                               'loss': 'rmse',
                                'x0': [0., 0., 0.],
                                't': [0,50,500]
                                }
                }
    return params

def test_error(fixture_sys_a):
    f_fit = EqSystem(fixture_sys_a)
    k = np.array([1.,0.385])
    f_fit.y = f_fit.simulation(k)
    pso = PSO(f_fit, fixture_sys_a)

    for i in range(500):
        pso.run()
    print("\n============== Final report: ==================")
    print(f'e: {pso.pbg_cost}, predict: {pso.pbg_position}')
    assert pso.pbg_cost < 0.01
