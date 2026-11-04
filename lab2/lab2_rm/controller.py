'''
Adaptación del Nodo PIDController visto en clases para poder instanciarlo directamente
'''

import time

class PIDController:

    def __init__(self, kp, ki=0.0, kd=0.0, sat=0.2):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sat = sat
        self.setpoint = None
        self.state = None
        self.proportional_action = None

        self.error_i = 0.0
        self.last_time = time.time()

    def set_target(self, target):
        print(f'[PICTRL] new setpoint received: %.2f' % (target) )
        self.setpoint = target
        self.last_time = time.time()
        self.error_i = 0.0

    def set_state(self, current_state):
        if self.setpoint == None:
            return

        current_time = time.time()
        dt = (current_time - self.last_time)
        self.last_time = time.time()

        self.state = current_state
        error = self.setpoint - current_state

        # Proportional
        p_actuation = self.kp*error

        # Integrative
        self.error_i += error*dt
        i_actuation = self.ki*self.error_i

        # Derivative
        d_actuation = self.kd*0

        # Actuation
        actuation = p_actuation + i_actuation + d_actuation

        # Velocidad
        if actuation > self.sat:
            actuation = self.sat

        elif actuation < -self.sat:
            actuation = -self.sat

        return actuation

    def reset(self):
        self.setpoint = None
        self.last_time = time.time()
        self.error_i = 0.0
        self.state = None