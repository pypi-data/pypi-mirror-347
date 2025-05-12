#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from .auc_ci_delong import AUC_CI_Delong
from .classification_ci_wilson import Classification_CI_Wilson
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, f1_score
from sklearn.utils import resample


def bootstrap_ci(true, pred, fx, n_iterations=1000, alpha=0.95):
    """
    <Parameters>
    true (list, array): true values
    pred (list, array): predicted values
    fx (function): scoring function
    n_iterations (int): number of iterations for bootstrapping
    alpha (float)

    <Returns>
    [estimate, ci]
    """

    n_samples = len(true)
    stats = []

    for _ in range(n_iterations):
        true_sampled, pred_sampled = resample(true, pred, n_samples=n_samples)
        stat = fx(true_sampled, pred_sampled)
        stats.append(stat)

    stats = np.array(stats)
    p_lower = ((1.0 - alpha) / 2.0) * 100
    lower = np.percentile(stats, p_lower, axis=0)
    mean = np.mean(stats, axis=0)
    p_upper = (1 - ((1.0 - alpha) / 2.0)) * 100
    upper = np.percentile(stats, p_upper, axis=0)

    return [mean, np.array([lower, upper])]

def _sen(true, pred):
    conf = confusion_matrix(true, pred)
    return conf[1,1] / (sum(conf[1]) + 1e-8)

def _spe(true, pred):
    conf = confusion_matrix(true, pred)
    return conf[0,0] / (sum(conf[0]) + 1e-8)

def _ppv(true, pred):
    conf = confusion_matrix(true, pred)
    return conf[1,1] / (sum(conf[:,1]) + 1e-8)

def _npv(true, pred):
    conf = confusion_matrix(true, pred)
    return conf[0,0] / (sum(conf[:,0]) + 1e-8)

def classification_metrics(true, pred, method='wilson', alpha=0.95, 
                           n_iterations=1000, show=False):
    """
    <Parameters>
    true (list, array): true values
    pred (list, array): predicted values
    method (str): 'wilson' or 'bootstrap' -> method to obtain CI
    n_iterations (int): number of iterations for bootstrapping
    show (bool): print results to 3 decimals
    alpha (float)

    <Returns>
    metrics (dict): keys -> sen, spe, ppv, npv, f1
    """

    if method == 'wilson':
        conf = confusion_matrix(true, pred)
        TP, FP, FN, TN = conf[1,1], conf[0,1], conf[1,0], conf[0,0]
        metrics = Classification_CI_Wilson(TP, FP, FN, TN, alpha=alpha)
    elif method == 'bootstrap':
        metrics = {}
        metrics['sen'] = bootstrap_ci(true, pred, _sen, n_iterations=n_iterations, alpha=alpha)
        metrics['spe'] = bootstrap_ci(true, pred, _spe, n_iterations=n_iterations, alpha=alpha)
        metrics['ppv'] = bootstrap_ci(true, pred, _ppv, n_iterations=n_iterations, alpha=alpha)
        metrics['npv'] = bootstrap_ci(true, pred, _npv, n_iterations=n_iterations, alpha=alpha)
    else:
        raise "method must be 'wilson' or 'bootstrap'"

    metrics['f1'] = bootstrap_ci(true, pred, f1_score, n_iterations=n_iterations, alpha=alpha)

    if show:
        print("Sensitivity: %.3f (%.3f-%.3f)" %(metrics['sen'][0], metrics['sen'][1][0], metrics['sen'][1][1]))
        print("Specificity: %.3f (%.3f-%.3f)" %(metrics['spe'][0], metrics['spe'][1][0], metrics['spe'][1][1]))
        print("PPV: %.3f (%.3f-%.3f)" %(metrics['ppv'][0], metrics['ppv'][1][0], metrics['ppv'][1][1]))
        print("NPV: %.3f (%.3f-%.3f)" %(metrics['npv'][0], metrics['npv'][1][0], metrics['npv'][1][1]))
        print("F1 score: %.3f (%.3f-%.3f)" %(metrics['f1'][0], metrics['f1'][1][0], metrics['f1'][1][1]))

    return metrics

def youden_metrics(true, prob, method='wilson', alpha=0.95, 
                n_iterations=1000, show=False):
    true, prob = np.array(true), np.array(prob)
    fpr, tpr, thresholds = roc_curve(true, prob)
    youden = thresholds[np.argmax(tpr-fpr)]
    pred = (prob >= youden) * 1

    metrics = classification_metrics(true, pred, method='wilson', alpha=alpha, 
                           n_iterations=n_iterations, show=show)

    return metrics, youden

def auc_score(true, prob, method='delong', alpha=0.95, 
              n_iterations=1000, show=False):
    """
    <Parameters>
    true (list, array): true values
    prob (list, array): probabilities
    method (str): 'delong' or 'bootstrap' -> method to obtain CI
    n_iterations (int): number of iterations for bootstrapping
    show (bool): print results to 3 decimals
    alpha (float)

    <Returns>
    [auc estimate, auc ci]
    """

    if method == 'delong':
        metric = AUC_CI_Delong(true, prob, alpha=alpha)
    elif method == 'bootstrap':
        metric = bootstrap_ci(true, prob, roc_auc_score, n_iterations=n_iterations, alpha=alpha)
    else:
        raise "method must be 'delong' or 'bootstrap'"

    if show:
        print("AUC: %.3f (%.3f-%.3f)" %(metric[0], metric[1][0], metric[1][1]))

    return metric


class binary_outcome_analysis():
    """
    <Methods>
    binary_outcome_analysis.auc(): show AUC values
    binary_outcome_analysis.roc_auc(styles): show ROC curve and AUC values
    binary_outcome_analysis.classification(**cutoffs): show classification results
    """

    def __init__(self, true, **probs):
        """
        <Parameters>
        true (list, array): true values
        **probs (dict): dictionary with model name as keys and probabilities as values

        <Example>
        probs = {'XGBoost': prob0, 'Random Forest': prob1, 'Logistic Regression': prob2}
        result = binary_outcome_analysis(true, **probs)
        """

        self.true = np.array(true)
        self.probs = probs
        pass

    def auc(self):
        print("================ AUC results ================")

        for name, value in self.probs.items():
            prob = np.array(value)

            print("< %s >" %name)
            auc_score(self.true, prob, show=True)

        print("=============================================\n")

    def roc_auc(self, **styles):
        """
        <Parameters>
        styles (dict): model name as key and matplotlib kwargs as values

        <Example>
        styles = {'XGBoost': {'color': 'C0', 'linestyle': '-'},
                  'Random Forest': {'color': 'C1', 'linestyle': '-.'}, 
                  'Logistic Regression': {'color': 'C2', 'linestyle': '--'}}
        """

        plt.figure(figsize=(3.5,3.5))
        plt.rcParams['font.family'] ='Times New Roman'

        for name, value in self.probs.items():
            prob = np.array(value)
            fpr, tpr, thresholds = roc_curve(self.true, prob)

            if name in styles.keys():
                plt.plot(fpr, tpr, label=name, **styles[name])
            else:
                plt.plot(fpr, tpr, label=name, color='black')

        plt.plot([0,1], [0,1], color='black', linestyle=':')
        plt.xticks(np.arange(0,1.2,0.2))
        plt.yticks(np.arange(0,1.2,0.2))
        plt.xlabel('1-specificity')
        plt.ylabel('Sensitivity')
        plt.legend(loc='lower right')
        plt.show()

        self.auc()

    def classification(self, **cutoffs):
        """
        <Parameters>
        cutoffs (dict): model name as key and cutoff thresholds as values
                        values can be one of the following: 
                        1) float(0~1): this threshold will be used
                        2) 'sen50' with number indicating the target sensitivity
                        3) 'spe90' with number indicating the target specificity
                        4) 'youden': Youden's index will be used

        <Example>
        cutoffs = {'XGBoost': 0.5, 'Random Forest': 'sen90', 'Logistic Regression': 'spe80'}
        """

        print("================ Classification results ================")

        for name, value in self.probs.items():
            print("< %s >" %name)
            prob = np.array(value)
            fpr, tpr, thresholds = roc_curve(self.true, prob)

            if name in cutoffs.keys():
                if type(cutoffs[name]) in [float, int]:
                    threshold = cutoffs[name]
                elif cutoffs[name][:3] == 'sen':
                    cutoff = int(cutoffs[name][3:]) / 100
                    threshold = thresholds[np.argmin(np.abs(tpr - cutoff))]
                elif cutoffs[name][:3] == 'spe':
                    cutoff = int(cutoffs[name][3:]) / 100
                    threshold = thresholds[np.argmin(np.abs((1 - fpr) - cutoff))]
                elif cutoffs[name] == 'youden':
                    threshold = thresholds[np.argmax(tpr-fpr)]
                else:
                    raise ValueError
            else:
                threshold = thresholds[np.argmax(tpr-fpr)]

            pred = (prob >= threshold) * 1
            classification_metrics(self.true, pred, method='wilson', n_iterations=1000, show=True)
            print()

        print("========================================================\n")


def overview_df(df):
    """
    Take a dataframe and print an overview of the dataframe
       For each column: 
       - Identify the Data Types - Numpy
       - Count the unique values
       - Count missing values
       - Count for each variable 
       - Count of zero values

    <Parameters>
    df (dataframe): dataframe to analyze

    <Returns>
    overview dataframe
    """
    if isinstance(df, pd.DataFrame):
        data_dd = pd.DataFrame(df.dtypes, columns=['Numpy Dtype'])
        data_dd['Nunique'] = df.nunique()
        data_dd['MissingValues'] = df.isnull().sum()
        data_dd['Count'] = df.count()
        data_dd['ZeroValues'] = (df==0).sum()
        return data_dd
    else:
        print("Not a pandas dataframe")

