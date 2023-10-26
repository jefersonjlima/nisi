import numpy as np
import pytest
from nisi import PSO, Model

class EqSystem(Model):
    def __init__(self, params=None):
        super().__init__(params)
        self._params = params

    def model(self, t, y, *args):
        def delta(vel):
            if abs(vel) > 0.1:
                d = 5.0
            else:
                d = 0.5
            return d
        k = self.unknown_const
        ks   = k[0]
        c    = k[1]
        w    = 0.5
        m    = 1
        wn   = np.sqrt(ks/m)
        zeta = c/(2*m*wn)
        dy = np.zeros(len(self.x0),)
        dy[0] = y[1]
        dy[1] = -2 * zeta * wn * delta(y[1])*y[1] - wn ** 2 * y[0] + 4*np.sin(2*np.pi*w*t)
        return dy


@pytest.fixture
def fixture_sys_a():
    params = {'optmizer': {'lowBound': [1.0 , 1.0],
                            'upBound': [8,  8],
                            'maxVelocity':  2, 
                            'minVelocity': -2,
                            'nPop': 10,
                            'nVar': 2,
                            'social_weight': 2.0,
                            'cognitive_weight': 1.0,
                            'w': 0.9,
                            'beta': 0.1,
                            'w_damping': 0.999,
                            'escape_min_vel': 0.05,
                            'escape_min_error': 0.5},
                'dyn_system': {'model_path': 'test/test1.dat',
                                'external': None,
                                'state_mask' : [True, False],
                                'loss': 'rmse',
                                'x0': [0., 0.],
                                't': [0,6,1000]
                                }
                }
    return params

def test_error(fixture_sys_a):
    f_fit = EqSystem(fixture_sys_a)
    k = np.array([2.5,5.1])
    f_fit.y = f_fit.simulation(k)
    pso = PSO(f_fit, fixture_sys_a)

    for _ in range(50):
        pso.run()
    assert pso.pbg_cost < 0.001
