import pandas as pd
import numpy as np

def rmse(y_true, y_pred):
    """Compute RMSE
    
    Computes the root mean-squared error between the observed and predicted values.
    
    y_true: a numpy array of observed values.
    y_pred: a numpy array of predicted values.
    
    Returns:
    A float value. A value closer to 0 is better.
    """
    out = np.sqrt(np.mean((y_true - y_pred)**2))
    return out

def mae(y_true, y_pred):
    """Compute MAE
    
    Computes the mean absolute error between observed and predicted values.

    y_true: a numpy array of observed values.
    y_pred: a numpy array of predicted values.
    
    Returns:
    A float value. A value closer to 0 is better.    
    """
    out = np.mean(np.abs(y_true - y_pred))
    return out

def smape(y_true, y_pred):
    """Compute sMAPE
    
    Computes the symmetric percentage error between observed and predicted values.

    y_true: a numpy array of observed values.
    y_pred: a numpy array of predicted values.
    
    Returns:
    A float value between -2 and 2. A value closer to 0 is better.
    """
    numer = np.abs(y_true - y_pred)
    denom = y_true + y_pred
    out = np.mean(2*numer/denom)
    return out

def meanf(y_train, h):
    """Compute the forecast using the mean.
    
    Computes and returns the mean as the forecast for h periods ahead.
    
    y_train: Should be a pandas series object.
    h      : This should be an integer value.
    """
    train_mean = y_train.mean()
    h_range = pd.date_range(y_train.index[-1], periods=h+1, 
                            freq=y_train.index.freq)[1:]
    return pd.Series(data=train_mean, index = h_range)

def naive(y_train, h):
    """Compute the forecast using the naive method.
    
    Returns the most recent observation as the forecast for h periods ahead.
    
    y_train: Should be a pandas series object.
    h      : This should be an integer value.
    """
    h_range = pd.date_range(y_train.index[-1], periods=h+1, 
                            freq=y_train.index.freq)[1:]
    return pd.Series(data=y_train.values[-1], index = h_range)

def snaive(y_train, h, nobs_season):
    """Compute the forecast using the seasonal naive method.
    
    Returns the most recent observation as the forecast for h periods ahead.
    
    y_train    : Should be a pandas series object.
    h          : This should be an integer value.
    nobs_season: The number of observations per season. For instance, 
                 quarterly data should have a value of 4 here.       
    """
    recent_yvals = y_train[-nobs_season:].values
    fcast_yvals = np.tile(recent_yvals, int(np.ceil(1.0*h/nobs_season)))
    h_range = pd.date_range(y_train.index[-1], periods=h+1, 
                            freq=y_train.index.freq)[1:]   
    return pd.Series(data=fcast_yvals[:h], index=h_range)