"""
.. module:: sde.py
   :synopsis: Numerical integration techniques
.. moduleauthor:: Jonathan Gross <jarthurgross@gmail.com>

"""

import numpy as np

def milstein(drift, diffusion, diffusion_prime, X0, ts, dws):
    r"""Integrate a system of ordinary stochastic differential equations:

    .. math::

        d\vec{X}=a(X,t)\,dt+b(X,t)\,dW_t

    Uses the Milstein method:

    .. math::

        w_{i+1}=w_i+a(w_i,t_i)\Delta t_i+b(w_i,t_i)\Delta W_i+
        \frac{1}{2}b(w_i,t_i)\frac{\partial b}{\partial X}(w_i,t_i)
        ((\Delta W_i)^2-\Delta t_i)

    :param drift:           Computes the drift term :math:`a(t,X)` at t0
    :type drift:            callable(X, t0)
    :param diffusion:       Computes the diffusion term :math:`b(t,X)` at t0
    :type diffusion:        callable(X, t0)
    :param diffusion_prime: Computes the diffusion term :math:`b_X(t,X)` at t0
                            (for systems of equations computes
                            :math:`\vec{\nabla}_{\vec{X}}\cdot\vec{b}`
    :type diffusion_prime:  callable(X, t0)
    :param X0:              Initial condition on X (can be a vector)
    :type X0:               array
    :param ts:              A sequence of time points for which to solve for y.
                            The
                            initial value point should be the first element of
                            this sequence.
    :type ts:               array
    :param dws:             Normalized Weiner increments for each time step
                            (i.e. samples from a Gaussian distribution with mean
                            0 and variance 1).
    :type dws:              array, shape (len(t) - 1)
    :return:                Array containint the value of X for each desired
                            time in t, with the initial value `X0` in the first
                            row.
    :rtype:                 numpy.array, shape (len(t), len(X0))

    """

    dts = [tf - ti for tf, ti in zip(t[1:], t[:-1])]
    # Scale the Weiner increments to the time increments.
    sqrtdts = np.sqrt(dts)
    dWs = np.product(np.array([sqrtdt, dws]), axis=0)

    X = [np.array(X0)]

    for t, dt, dW in zip(ts[:-1], dts, dWs):
        X.append(X[-1] + drift(X[-1], t)*dt + diffusion(X[-1], t)*(dW +
            0.5*diffusion_prime(X[-1], t)*(dW**2 - dt)))

    return X
