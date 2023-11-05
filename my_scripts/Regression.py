from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from my_scripts.Data_loader import Data_loader

class Regression(Data_loader):
    def __init__(self, raw_dir, output_dir, nyc_shapefile_dir, data, if_st=True):
        Data_loader.__init__(self, raw_dir, output_dir, nyc_shapefile_dir)
        # noinspection PyCompatibility
        super().__init__(raw_dir, output_dir, nyc_shapefile_dir)
        self.data = data
        self.if_st = if_st


