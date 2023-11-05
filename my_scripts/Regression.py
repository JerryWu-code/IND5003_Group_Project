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
        
    def GB_regression(self, feature_columns, target_column):
        """
        Performs a full regression analysis including data preparation, model training,
        evaluation, and plotting feature importances.

        Parameters:
        - feature_columns: list of column names to be used as features.
        - target_column: column name of the target variable.

        Returns:
        - None
        """
        # Data preparation
        self.data['PU_time'] = pd.to_datetime(self.data['PU_time'], errors='coerce')
        self.data['pickup_hour'] = self.data['PU_time'].dt.hour
        X = self.data[feature_columns]
        y = self.data[target_column]

        # Splitting and scaling
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        median_passenger_count = X_train['passenger_count'].median()
        X_train['passenger_count'].fillna(median_passenger_count, inplace=True)
        X_test['passenger_count'].fillna(median_passenger_count, inplace=True)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Model training and evaluation
        model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=0
        )
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        # Calculate performance metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        # Prepare performance metrics DataFrame
        performance_metrics = pd.DataFrame({
            'Metric': ['RMSE', 'R^2', 'MAE'],
            'Value': [rmse, r2, mae]
        })

        # Display the performance metrics table
        if self.if_st:
            st.dataframe(performance_metrics)
        else:
            display(performance_metrics.style.hide(axis='index').set_caption("Performance Metrics"))
        
        # Get and plot feature importances
        feature_importances = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importances)
        plt.title('Feature Importance')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()

        return model 
        
    def xgboost_regression(self, feature_columns, target_column):
        """
        Performs XGBoost regression analysis including data preparation, model training,
        evaluation, and plotting feature importances.

        Parameters:
        - feature_columns: list of column names to be used as features.
        - target_column: column name of the target variable.

        Returns:
        - The trained XGBoost regressor model.
        """
        # Data preparation
        self.data['PU_time'] = pd.to_datetime(self.data['PU_time'], errors='coerce')
        self.data['pickup_hour'] = self.data['PU_time'].dt.hour
        X = self.data[feature_columns]
        y = self.data[target_column]

        # Splitting and scaling
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        median_passenger_count = X_train['passenger_count'].median()
        X_train['passenger_count'].fillna(median_passenger_count, inplace=True)
        X_test['passenger_count'].fillna(median_passenger_count, inplace=True)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Defining and fitting the XGBoost regressor
        xgboost_regressor = XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=0
        )
        xgboost_regressor.fit(X_train_scaled, y_train)

        # Predicting and evaluating
        y_pred_xgboost = xgboost_regressor.predict(X_test_scaled)
        xgboost_mse = mean_squared_error(y_test, y_pred_xgboost)
        xgboost_rmse = np.sqrt(xgboost_mse)
        xgboost_r2 = r2_score(y_test, y_pred_xgboost)
        mae = mean_absolute_error(y_test, y_pred_xgboost)

        # Performance metrics
        xgboost_performance_metrics = pd.DataFrame({
            'Metric': ['RMSE', 'R^2', 'MAE'],
            'Value': [xgboost_rmse, xgboost_r2, mae]
        })
        if self.if_st:
            st.dataframe(xgboost_performance_metrics)
        else:
            display(xgboost_performance_metrics.style.hide(axis='index').set_caption("Performance Metrics"))
        
        # Feature importances
        feature_importances = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': xgboost_regressor.feature_importances_
        }).sort_values('Importance', ascending=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importances)
        plt.title('Feature Importance')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()
        return xgboost_regressor
        
    def decision_tree_regression(self, feature_columns, target_column):
        """
        Performs Decision Tree regression analysis including data preparation, model training,
        evaluation, and plotting feature importances.

        Parameters:
        - feature_columns: list of column names to be used as features.
        - target_column: column name of the target variable.

        Returns:
        - The trained Decision Tree regressor model.
        """
        # Data preparation
        self.data['PU_time'] = pd.to_datetime(self.data['PU_time'], errors='coerce')
        self.data['pickup_hour'] = self.data['PU_time'].dt.hour
        X = self.data[feature_columns]
        y = self.data[target_column]

        # Splitting and scaling
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        median_passenger_count = X_train['passenger_count'].median()
        X_train['passenger_count'].fillna(median_passenger_count, inplace=True)
        X_test['passenger_count'].fillna(median_passenger_count, inplace=True)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Defining and fitting the Decision Tree regressor
        decision_tree = DecisionTreeRegressor(random_state=0)
        decision_tree.fit(X_train_scaled, y_train)

        # Predicting and evaluating
        y_pred_decision_tree = decision_tree.predict(X_test_scaled)
        dt_rmse = np.sqrt(mean_squared_error(y_test, y_pred_decision_tree))
        dt_r2 = r2_score(y_test, y_pred_decision_tree)
        mae = mean_absolute_error(y_test, y_pred_decision_tree)

        # Performance metrics
        dt_performance_metrics = pd.DataFrame({
            'Metric': ['RMSE', 'R^2', 'MAE'],
            'Value': [dt_rmse, dt_r2, mae]
        })
        if self.if_st:
            st.dataframe(dt_performance_metrics)
        else:
            display(dt_performance_metrics.style.hide(axis='index').set_caption("Performance Metrics"))
            
        # Feature importances
        feature_importances = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': decision_tree.feature_importances_
        }).sort_values('Importance', ascending=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importances)
        plt.title('Feature Importance')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        if self.if_st:
            st.pyplot(fig)
        else:
            plt.show()
            
        return decision_tree


