
"""A module to help perform analyses on various observatioanl studies.

This module was implemented following studies of M249, Book 1.

Dependencies:
    - **scipy**
    - **statsmodels**
    - **pandas**
    - **numpy**
"""


from __future__ import annotations as _annotations
import math as _math
from scipy import stats as _st
from statsmodels.stats import contingency_tables as _tables
import pandas as _pd
import numpy as _np


def riskratio(obs: _np.ndarray, alpha: float = 0.05) -> _pd.DataFrame:
    """Return the point and (1-alpha)% confidence interval estimates for
    the relative risk.

    Args:
        alpha: Significance level for the confidence interval.

    Returns:
        Point and (1-alpha)% confidence interval estimates for\
        the relative risk.
    """
    z: float = _st.norm().ppf(1-alpha/2)
    a = obs[0, 1]
    n1: int = _np.sum(obs[0])
    df = _pd.DataFrame(index=["riskratio", "stderr", "lower", "upper"])
    # add the reference category results
    df["Exposed1 (-)"] = [1.0, 0.0, "NA", "NA"]
    # gather results from array
    for i in range(1, obs.shape[0]):
        # get exposure results
        c = obs[i, 1]
        n2: int = _np.sum(obs[i])
        # calculate the risk ratio
        rr: float = (c/n2) / (a/n1)
        stderr: float = _math.sqrt((1/a - 1/n1) +  (1/c - 1/n2))
        ci: tuple[float, float] = (
            rr * _math.exp(-z * stderr), rr * _math.exp(z * stderr)
        )
        # append to df
        df[f"Exposed{i+1} (+)"] = [rr, stderr, ci[0], ci[1]]
    return df.T


def oddsratio(obs: _np.ndarray, alpha: float = 0.05) -> _pd.DataFrame:
    """Return the point and (1-alpha)% confidence interval estimates for
    the odds ratio.

    Args:
        alpha: Significance level for the confidence interval.

    Returns:
        Point and (1-alpha)% confidence interval estimates for\
        the odds ratio.
    """
    # gather results
    z: float = _st.norm().ppf(1-alpha/2)
    a: float = obs[0, 0]
    b: float = obs[0, 1]
    df = _pd.DataFrame(index=["oddsratio", "stderr", "lower", "upper"])
    # add the reference category results
    df["Exposed1 (-)"] = [1.0, 0.0, "NA", "NA"]
    # gather results from array
    for i in range(1, obs.shape[0]):
        # get exposure results
        c: float = obs[i, 0]
        d: float = obs[i, 1]
        # calculate the odds ratio
        or_: float = (a * d) / (b * c)
        stderr: float = _math.sqrt(1/a +  1/b + 1/c +  1/d)
        ci: tuple[float, float] =(
            or_ * _math.exp(-z * stderr), or_ * _math.exp(z * stderr)
        )
        # append to df
        df[f"Exposed{i+1} (+)"] = [or_, stderr, ci[0], ci[1]]
    return df.T 


def expectedfreq(obs: _np.ndarray) -> _np.ndarray:
    """Return the expected frequencies from a contingency table under
    the hypothesis of no association.

    Returns:
        Expected frequencies.
    """
    return _st.contingency.expected_freq(obs)


def chisqcontribs(obs: _np.ndarray) -> _np.ndarray:
    """Return the chi-squared contributions for each observation used in a
    chi-squared test of no association.

    Returns:
        chi-squared contributions.
    """
    exp = expectedfreq(obs)
    contribs = _np.divide(_np.square(obs-exp), exp)
    return contribs


def chisqtest( obs: _np.ndarray) -> _pd.DataFrame:
    """Return the results of a chi-squared test of no association.

    Returns:
        Results of a chi-squared test of no association.
    """
    res = _st.chi2_contingency(obs, correction=False)
    df = _pd.DataFrame(index=["chisq", "pval", "df"])
    df["result"] = [res[0], res[1], res[2]]
    return df.T


def aggregate(obs) -> _np.ndarray:
    """Return an aggregated array.
    """
    agg: _np.ndarray = _np.empty((2, 2))
    for table in obs:
        agg += table
    return agg


def adjusted_oddsratio(obs: _np.ndarray, alpha: float = 0.05) -> _pd.DataFrame:
    """Return the point and (1-alpha)% confidence interval estimates for
    the adjusted odds ratio.

    It uses the Mantel-Haenszel odds ratio.

    Args:
        alpha: Significance level for the confidence interval.

    Returns:
        Point and (1-alpha)% confidence interval estimates for\
        the adjusted odds ratio.
    """
    strattable = _tables.StratifiedTable(obs.tolist())
    est = strattable.oddsratio_pooled
    stderr = strattable.logodds_pooled_se
    ci = strattable.oddsratio_pooled_confint(alpha)
    """
    elif isinstance(table, OneToOneMatched):
        est = table.table[0][1] /table.table[1][0]
        se = (1/table.table[0][1] + 1/table.table[1][0]) ** 0.5
        zscore = _st.norm.ppf(1-alpha/2)
        ci = (est * _exp(-zscore * se), est * _exp(zscore * se))
    else:
        "Not defined for table type."
    """
    df = _pd.DataFrame(index=["oddsratio", "stderr", "lower", "upper"])
    df["result"] = [est, stderr, ci[0], ci[1]]
    return df.T


def crude_oddsratio(obs: _np.ndarray, alpha: float = 0.05) -> _pd.DataFrame:
    """Return the point and (1-alpha)% confidence interval estimates for
    the crude odds ratio.

    Args:
        alpha: Significance level for the confidence interval.

    Returns:
        Point and (1-alpha)% confidence interval estimates for\
        the crude odds ratio.
    """
    return oddsratio(aggregate(obs), alpha)


def test_equalodds(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the results test of the null hypothesis that the odds
    ratio is the same in all _k_ strata.

    This is the Tarone test.

    Args:
        adjust: If true, use the Tarone adjustment to achieve the chi^2\
            asymptotic distribution. 

    Returns:
        test statistic and the p-value.
    """
    strattable = _tables.StratifiedTable(obs.tolist())
    res = strattable.test_equal_odds(True)
    df = _pd.DataFrame(index=["chisq", "pval"])
    df["result"] = [res.statistic, res.pvalue]
    return df.T


def test_nullodds(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the results of a test of the null hypothesis of no
    association between the exposure and the disease, adjusted for the
    stratifying variable.

    Uses the Mantel-Haenszel test.

    Returns:
        test statistic and the p-value.
    """
    strattable = _tables.StratifiedTable(obs.tolist())
    res = strattable.test_null_odds(False)
    df = _pd.DataFrame(index=["chisq", "pval"])
    df["result"] = [res.statistic, res.pvalue]
    return df.T


def matched_oddsratio(obs: _np.ndarray, alpha: float = 0.05) -> _pd.DataFrame:
    """Return the point and (1-alpha)% confidence interval estimates for
    the odds ratio in a 1-1 matched case-control study.

    Args:
        alpha: Significance level for the confidence interval.

    Returns:
        Point and (1-alpha)% confidence interval estimates for\
        the odds ratio.
    """
    or_ = obs[1, 0] / obs[0, 1]
    stderr = _math.sqrt(1/obs[1, 0] + 1/obs[0, 1])
    z = _st.norm.ppf(1-alpha/2)
    ci = (or_ * _math.exp(-z * stderr), or_ * _math.exp(z * stderr))
    df = _pd.DataFrame(index=["oddsratio", "stderr", "lcb", "ucb"])
    df["result"] = [or_, stderr, ci[0], ci[1]]
    return df.T


def mcnemar(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the results of a test of the null hypothesis of no
    association in a 1-1 matched case-control study.

    This is the McNemar test.

    Returns:
        test statistic and the p-value.
    """
    f = obs[1, 0]
    g = obs[0, 1]
    num = (abs(f-g) - 1) ** 2
    den = f + g
    chisq = num / den
    pval = _st.chi2(df=1).sf(chisq)
    df = _pd.DataFrame(index=["chisq", "pval"])
    df["result"] = [chisq, pval]
    return df.T


def weighted_means(
    obs: _np.ndarray,
    u:  _np.ndarray,
    v:  _np.ndarray
) -> tuple[float, float]:
    """Return the weighted row and column means of an Rx2 contingency table.

    Args:
        obs: Rx2 contingency table representing representing a\
            dose-response analysis.   
        n: sample size
        u: row integer scores
        v: column integer scores

    Returns:
        weighted row mean, weighted col mean
    """
    ubar, vbar = 0, 0
    for i in range(obs.shape[0]):
        for j in range(obs.shape[1]):
            ubar += ((u[i] * obs[i, j]) / obs.sum())
            vbar += ((v[j] * obs[i, j]) / obs.sum())
    return ubar, vbar


def weighted_pearsonr(
    obs: _np.ndarray,
    scores: list[list[int]] = None
) -> float:
    """Return the weight Pearson correlation coefficient.

    Reference: https://online.stat.psu.edu/stat504/book/export/html/710

    Args:
        obs: Rx2 contingency table representing representing dose-response\
            analysis.   
        scores: Integer scores for the rows and columns. If None is pass,\
            then arbitrary integer scores are assigned.

    Returns:
        Weighted Pearson correlation coefficient.
    """
    # scores
    if scores is None:
        u, v = _np.arange(1, obs.shape[0] + 1), _np.arange(1, 3)
    else:
        u, v = scores[0], scores[1]
    # sample size and integer scores for row and columns
    ubar, vbar = weighted_means(obs, obs.sum(), u, v)
    print(ubar, vbar)
    num, den1, den2 = 0, 0, 0
    for i in range(obs.shape[0]):
        for j in range(obs.shape[1]):
            num += (u[i] * ubar) * (v[j] * vbar) * obs[i, j]
            den1 += ((u[i] * ubar)**2 * obs[i, j])
            den2 += ((v[j] * vbar)**2 * obs[i, j])
    return num / _math.sqrt(den1 * den2)    


def odds(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the odds of disease for each exposure dose in a dose-response\
    analysis.

    Args:
        obs: Rx2 contingency table representing representing dose-response\
            analysis. 

    Returns:
        Odds of disease given exposure-dose.
    """
    return _np.divide(obs[:, 1], obs[:, 0])


def doseexposure_odds(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the odds and log-odds of disease for each exposure dose\
        in a dose-response analysis.

    Args:
        obs: Rx2 contingency table representing representing dose-response\
            analysis. 

    Returns:
        Dataframe showing odds, log-odds of each exposure-dose
    """

    od = odds(obs)
    log_od = _np.log(od)
    df = _pd.DataFrame(index=["odds", "log-odds"])
    for i in range(obs.shape[0]):
        df[f"Exposed{i+1}"] = [od[i], log_od[i]]
    return df.T 


def midranks(obs: _np.ndarray) -> _np.ndarray:
    """Return the midrank scores for an array.

    Ref: https://online.stat.psu.edu/stat504/lesson/4/4.1/4.1.2
    """
    ranks = _np.empty(shape=(obs.shape[0]))
    rowsums = obs.sum(1)
    rowcounter = 0
    for i in range(len(rowsums)):
        ranks[i] += (rowcounter + ((1 + rowsums[i]) / 2))
        rowcounter += rowsums[i]
    return ranks


def cov(obs: _np.ndarray, scores: _np.ndarray) -> float:
    """Return the covariance of an RxC array.

    Args:
        obs: [description]

    Returns:
        Covariance of rows and columns.
    """
    u, v = scores[0], scores[1]
    ubar, vbar = weighted_means(obs, u, v)
    cov = 0
    for i in range(len(u)):
        for j in range(len(v)):
            cov += (u[i] - ubar) * (v[j] - vbar) * obs[i, j]
    return cov


def stddev(obs: _np.ndarray, scores: _np.ndarray) -> float:
    """Return the standard deviation of the rows.

    Args:
        obs: [description]

    Returns:
        Covariance of rows and columns.
    """
    u, v = scores[0], scores[1]
    ubar, vbar = weighted_means(obs, u, v)
    varx, vary = 0, 0
    for i in range(len(u)):
        for j in range(len(v)):
            varx += (u[i] - ubar)**2 * obs[i, j]
            vary += (v[j] - vbar)**2 * obs[i, j]
    return _math.sqrt(varx), _math.sqrt(vary)


def corrcoeff(obs: _np.ndarray, scores: _np.ndarray) -> float:
    """Return Pearson's correlation coefficients for an array.

    Args:
        obs: [description]

    Returns:
        Pearson's correlation coefficient, r
    """
    return cov(obs, scores) / (stddev(obs, scores)[0] * stddev(obs, scores)[1])


def chisq_lineartrend(obs: _np.ndarray) -> _pd.DataFrame:
    """Return the test statistic and p-value for a chi-squared test
    of no linear trend.

    Reference: https://online.stat.psu.edu/stat504/book/export/html/710

    Args:
        obs: Rx2 contingency table representing representing dose-response\
            analysis.

    Returns:
        chi-square, p-value as a DataFrame.
    """
    # select the ranks => row score then col score
    scores = midranks(obs), [0, 1]
    # gather results
    r = corrcoeff(obs, scores)
    chisq = (obs.sum() - 1) * (r ** 2)
    pval = _st.chi2(df=1).sf(chisq)
    # results to dataframe
    df = _pd.DataFrame(index=["chisq", "pval"])
    df["result"] = [chisq, pval]
    return df.T
