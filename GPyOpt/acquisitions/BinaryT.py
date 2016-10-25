# Copyright (c) 2016, the GPyOpt Authors
# Licensed under the BSD 3-clause license (see LICENSE.txt)

from .base import AcquisitionBase
from ..util.general import get_quantiles

class AcquisitionBinaryT(AcquisitionBase):
    """
    T value acquisition function for active classification with binary classes

    :param model: GPyOpt class of model
    :param space: GPyOpt class of domain
    :param optimizer: optimizer of the acquisition. Should be a GPyOpt optimizer
    :param cost_withGradients: function
    :param jitter: positive value to make the acquisition more explorative.

    .. Note:: allows to compute the Improvement per unit of cost

    """

    analytical_gradient_prediction = True

    def __init__(self, model, space, optimizer=None, cost_withGradients=None, jitter=0.01):
        self.optimizer = optimizer
        super(AcquisitionBinaryT, self).__init__(model, space, optimizer, cost_withGradients=cost_withGradients)
        self.jitter = jitter
        
    @staticmethod
    def fromConfig(model, space, optimizer, cost_withGradients, config):
        return AcquisitionBinaryT(model, space, optimizer, cost_withGradients, jitter=config['jitter'])

    # def _compute_acq(self, x):
    #     """
    #     Computes the Expected Improvement per unit of cost
    #     """
    #     m, s = self.model.predict(x)
    #     fmin = self.model.get_fmin()
    #     phi, Phi, _ = get_quantiles(self.jitter, fmin, m, s)    
    #     f_acqu = (fmin - m + self.jitter) * Phi + s * phi
    #     return f_acqu

    def _compute_acq(self, x):
        """
        Computes the Expected Improvement per unit of cost, always negative for this acq.
        """
        m, s = self.model.predict(x)
        f_acqu = - m / s
        return f_acqu

    # def _compute_acq_withGradients(self, x):
    #     """
    #     Computes the Expected Improvement and its derivative (has a very easy derivative!)
    #     """
    #     fmin = self.model.get_fmin()
    #     m, s, dmdx, dsdx = self.model.predict_withGradients(x)
    #     phi, Phi, _ = get_quantiles(self.jitter, fmin, m, s)    
    #     f_acqu = (fmin - m + self.jitter) * Phi + s * phi        
    #     df_acqu = dsdx * phi - Phi * dmdx
    #     return f_acqu, df_acqu

    def _compute_acq_withGradients(self, x):
        """
        Computes the Expected Improvement and its derivative (has a very easy derivative!)
        """
        fmin = self.model.get_fmin()
        m, s, dmdx, dsdx = self.model.predict_withGradients(x)
        f_acqu = - m / s
        df_acqu = - dmdx / s + m * dsdx / s / s 
        return f_acqu, df_acqu

