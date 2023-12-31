import matplotlib.pyplot as plt
import numpy as np
from nisi import PSO, Model

class EqSystem(Model):
    def __init__(self, params=None):
        super(EqSystem, self).__init__(params)
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
        w    = k[2]
        m    = 1
        wn   = np.sqrt(ks/m)
        zeta = c/(2*m*wn)
        dy = np.zeros(len(self.x0),)
        dy[0] = y[1]
        dy[1] = -2 * zeta * wn * delta(y[1])*y[1] - wn ** 2 * y[0] + 4*np.sin(2*np.pi*w*t)
        return dy


def main():
    params = {'optmizer': {'lowBound': [1.0 , 1.0 ,0.1],
                            'upBound': [8,  8, 5],
                            'maxVelocity':  5, 
                            'minVelocity': -5,
                            'nPop': 10,
                            'nVar': 3,
                            'social_weight': 2.0,
                            'cognitive_weight': 2.0,
                            'w': 0.9,
                            'beta': 0.1,
                            'w_damping': 0.999,
                            'escape_min_vel': 0.05,
                           'escape_min_error': 0.001},
                'dyn_system': {'model_path': '',
                                'external': None,
                                'state_mask' : [True, False],
                               'loss': 'rmse',
                                'x0': [0., 0.],
                                't': [0,6,1000]
                                }
                }
    # suface_plot(params)
    f_fit = EqSystem(params)
    k = np.array([2.5,5.1,0.54])
    f_fit.y = f_fit.simulation(k)
    pso = PSO(f_fit, params)
    cost = []
    position = []
    fig = plt.figure(figsize=(12, 4), facecolor='white')
    particle = fig.add_subplot(221, frameon=False)
    graph_cost = fig.add_subplot(222, frameon=False)
    func1  = fig.add_subplot(223, frameon=False)
    func2  = fig.add_subplot(224, frameon=False)
    plt.show(block=False)

    for i in range(500):
        print(f'i: {i}, e: {pso.pbg_cost}, predict: {pso.pbg_position}')
        particle.cla()
        for j in range(params['optmizer']['nPop']):
            particle.plot(pso.p_position_[j, 0], pso.p_position_[j, 1], '.')
        particle.set_xlim(params['optmizer']['lowBound'][0], params['optmizer']['upBound'][0], )
        particle.set_ylim(params['optmizer']['lowBound'][1], params['optmizer']['upBound'][1], )
        particle.plot(pso.pbg_position[0], pso.pbg_position[1], 'x')
        particle.plot(k[0],k[1], 'o')
#        particle.grid()


        if pso.pbg_cost != float('inf'):
            cost.append(pso.pbg_cost[0])
            position.append(pso.pbg_position[0])
        graph_cost.cla()
        graph_cost.plot(cost)
        graph_cost.set_xlim(0, 500)
        graph_cost.set_title('Error')

        func1.cla()
        func1.plot(pso.y[:,0])
        func1.plot(pso.pbg_y_hat[:,0],'--')
        func1.plot(pso.y[:,1])
        func1.plot(pso.pbg_y_hat[:,1],'--')
        func1.legend(['y0','y0_hat','y1','y1_hat'])

        func2.cla()
        func2.plot(pso.y[:,0],pso.y[:,1])
        func2.plot(pso.pbg_y_hat[:,0], pso.pbg_y_hat[:,1],'--')
        func2.legend(['y','y_hat'])
        func2.set_xlabel('y')
        func2.set_ylabel('dot_y')

        plt.draw()
        plt.pause(0.01)
        pso.run()

if __name__ == "__main__":
    main()
