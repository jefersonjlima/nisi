import numpy as np

class Particle:
    def __init__(self, params):
        self._params = params['optmizer']
        self.nVar = self._params['nVar']
        self.nPop = self._params['nPop']
        self.cognitive_weight = self._params['cognitive_weight']
        self.social_weight = self._params['social_weight']
        self.w = self._params['w']
        self.w_damping = self._params['w_damping']
        self.minVelocity = self._params['minVelocity']
        self.maxVelocity = self._params['maxVelocity']
        self.beta = self._params['beta']
        self.escape_min_vel = self._params['escape_min_vel']
        self.escape_min_error = self._params['escape_min_error']

        self.lowBound = np.empty([self.nPop, self.nVar])
        self.upBound = np.empty([self.nPop, self.nVar])
        self.p_position_ = np.empty([self.nPop, self.nVar])
        self.p_velocity_ = np.empty([self.nPop, self.nVar])
        self.pb_position_ = np.empty([self.nPop, self.nVar])

        self.pbg_position = np.empty([1, self.nVar])
        self.particles_initializer()

    def particles_initializer(self) -> None:
        self.lowBound = np.ones([self.nPop, self.nVar]) * np.array(self._params['lowBound'])
        self.upBound =  np.ones([self.nPop, self.nVar]) * np.array(self._params['upBound'])
        self.p_position_ = (self.upBound - self.lowBound) * np.random.rand(self.nPop, self.nVar) + self.lowBound
        self.p_velocity_ = np.zeros([self.nPop, self.nVar])

    def limits(self, values, state=None):
        if state == 'velocity':
            values[values < self.minVelocity] = self.minVelocity
            values[values > self.maxVelocity] = self.maxVelocity
        elif state == 'position':
            values[values < self.lowBound] = self.lowBound[values < self.lowBound]
            values[values > self.upBound] = self.upBound[values > self.upBound]
        return values

    def update_particle(self):
        # update velocity
        up_vel = self.w * self.p_velocity_ \
                 + self.cognitive_weight * np.random.rand(self.nPop, self.nVar) * (self.pb_position_ - self.p_position_) \
                 + self.social_weight * np.random.rand(self.nPop,  self.nVar) * (self.pbg_position - self.p_position_)
        self.p_velocity_ = self.limits(up_vel, state='velocity')
        # update position
        up_pos = self.p_position_ + self.beta*self.p_velocity_
        self.p_position_ = self.limits(up_pos, state='position')


class PSO(Particle):
    def __init__(self, eq_system, params=None):
        super(PSO, self).__init__(params)
        if params is None:
            raise Exception('Please provide Params')
        self._params = params['optmizer']
        self._fitness = eq_system
        self.p_cost_ = np.empty([self.nPop, 1])
        self.pb_cost_ = np.empty([self.nPop, 1])
        self.pbg_cost = np.empty(1)
        self.cost_tmp = np.empty(1)
        self.pso_initializer()

    def pso_initializer(self):
        self.pbg_cost = float('inf')
        self.cost_tmp = self.pbg_cost
        for i in range(self.nPop):
            self.p_cost_[i], self.y, self.y_hat = self._fitness.evaluate(self.p_position_[i, :])
            self.pb_position_[i, :] = self.p_position_[i, :]
            self.pb_cost_[i] = self.p_cost_[i]
        self.pbg_position = self.pb_position_[self.pb_cost_.argmin(), :]
        self.pbg_y_hat = self.y_hat

    def update_cost(self):
        for i in range(self.nPop):
            self.p_cost_[i], self.y, self.y_hat = self._fitness.evaluate(self.p_position_[i, :])
            if self.p_cost_[i] < self.pb_cost_[i]:
                # update best particle values
                self.pb_position_[i, :] = self.p_position_[i, :]
                self.pb_cost_[i] = self.p_cost_[i]
                # update best global particle values
            if self.pb_cost_[i] < self.pbg_cost:
                self.pbg_cost = self.pb_cost_[i]
                self.pbg_position = self.p_position_[i, :]
                self.pbg_y_hat = self.y_hat
        self.w *= self.w_damping
        self.cost_tmp = self.pbg_cost

    def run(self):
        self.update_particle()
        self.update_cost()
        # Escape local mininal
        if self.pbg_cost > self.escape_min_error:
            if (abs(self.p_velocity_).mean() < self.maxVelocity * self.escape_min_vel):
                self.particles_initializer()
        else:
            if (abs(self.p_velocity_).mean() < self.maxVelocity * self.escape_min_vel):
                self.w_damping = 1.01
                self.w = 1.0
            else:
                self.w = self._params['w']
                self.w_damping = self._params['w_damping']






