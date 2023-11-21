import matplotlib.pyplot as plt
import numpy as np
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

        dy = np.zeros(len(self.x0),)
        dy[0] = y[1]
        dy[1] = -alpha*y[1] -delta*y[0] -beta*y[0]**3 + F*np.cos(y[2])
        dy[2] = omega
        return dy

def main():
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
                            'escape_min_vel_percent': 0.001,
                           'escape_min_error': 5e-6},
                'dyn_system': {'model_path': '',
                                'external': None,
                                'state_mask' : [True, False, False],
                               'loss': 'rmse',
                                'x0': [0., 0., 0.],
                                't': [0,50,500]
                                }
                }
    f_fit = EqSystem(params)
    k = np.array([1.,0.385])
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
        graph_cost.semilogy(cost)
        graph_cost.set_xlim(0, 500)
        graph_cost.set_ylim(0, 1)
        graph_cost.set_title('Error')

        func1.cla()
        func1.plot(pso.y[:,0])
        func1.plot(pso.pbg_y_hat[:,0],'--')
        func1.plot(pso.y[:,1])
        func1.plot(pso.pbg_y_hat[:,1],'--')
        func1.legend([r'$y_0$',r'$\hat{y_0}$',r'$y_1$','$\hat{y_1}$'])

        func2.cla()
        func2.plot(pso.y[:,0],pso.y[:,1])
        func2.plot(pso.pbg_y_hat[:,0], pso.pbg_y_hat[:,1],'--')
        func2.legend(['y',r'$\hat{y}$'])
        func2.set_xlabel('y')
        func2.set_ylabel('dot_y')

        plt.draw()
        plt.pause(0.01)
        pso.run()

if __name__ == "__main__":
    main()
