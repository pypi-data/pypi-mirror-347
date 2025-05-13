#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function, division
from math import sqrt
import numpy as np
from scipy.special import ndtri

def _proportion_confidence_interval(r, n, z):
    """Compute confidence interval for a proportion.

    Follows notation described on pages 46--47 of [1]. 

    References
    ----------
    [1] R. G. Newcombe and D. G. Altman, Proportions and their differences, in Statisics
    with Confidence: Confidence intervals and statisctical guidelines, 2nd Ed., D. G. Altman, 
    D. Machin, T. N. Bryant and M. J. Gardner (Eds.), pp. 45-57, BMJ Books, 2000. 
    """

    A = 2*r + z**2
    B = z*sqrt(z**2 + 4*r*(1 - r/n))
    C = 2*(n + z**2)
    return ((A-B)/C, (A+B)/C)

def Classification_CI_Wilson(TP, FP, FN, TN, alpha=0.95):
    """Compute confidence intervals for sensitivity and specificity using Wilson's method. 

    This method does not rely on a normal approximation and results in accurate 
    confidence intervals even for small sample sizes.

    Parameters
    ----------
    TP : int
        Number of true positives
    FP : int 
        Number of false positives
    FN : int
        Number of false negatives
    TN : int
        Number of true negatives
    alpha : float, optional
        Desired confidence. Defaults to 0.95, which yields a 95% confidence interval. 

    Returns
    -------
    sensitivity_point_estimate : float
        Numerical estimate of the test sensitivity
    specificity_point_estimate : float
        Numerical estimate of the test specificity
    sensitivity_confidence_interval : Tuple (float, float)
        Lower and upper bounds on the alpha confidence interval for sensitivity
    specificity_confidence_interval
        Lower and upper bounds on the alpha confidence interval for specificity 

    References
    ----------
    [1] R. G. Newcombe and D. G. Altman, Proportions and their differences, in Statisics
    with Confidence: Confidence intervals and statisctical guidelines, 2nd Ed., D. G. Altman, 
    D. Machin, T. N. Bryant and M. J. Gardner (Eds.), pp. 45-57, BMJ Books, 2000. 
    [2] E. B. Wilson, Probable inference, the law of succession, and statistical inference,
    J Am Stat Assoc 22:209-12, 1927. 
    """

    z = -ndtri((1.0-alpha)/2)

    # Compute sensitivity using method described in [1]
    sensitivity_point_estimate = TP/(TP + FN)
    sensitivity_confidence_interval = _proportion_confidence_interval(TP, TP + FN, z)

    # Compute specificity using method described in [1]
    specificity_point_estimate = TN/(TN + FP)
    specificity_confidence_interval = _proportion_confidence_interval(TN, TN + FP, z)

    ppv_point_estimate = TP/(TP + FP)
    ppv_confidence_interval = _proportion_confidence_interval(TP, TP + FP, z)

    npv_point_estimate = TN/(TN + FN)
    npv_confidence_interval = _proportion_confidence_interval(TN, TN + FN, z)

    output = {'sen': [sensitivity_point_estimate, np.array(sensitivity_confidence_interval)], 
              'spe': [specificity_point_estimate, np.array(specificity_confidence_interval)],
              'ppv': [ppv_point_estimate, np.array(ppv_confidence_interval)],
              'npv': [npv_point_estimate, np.array(npv_confidence_interval)]}

    return output


