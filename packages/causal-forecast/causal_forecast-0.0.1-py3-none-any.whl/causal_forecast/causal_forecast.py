import warnings
import time
import json

# Streamlit
import streamlit as st

# Core Python Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Sklearn
from sklearn.preprocessing import StandardScaler, PowerTransformer, QuantileTransformer
from sklearn.linear_model import LinearRegression, LassoCV, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split

# Statsmodels & SciPy
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats

# Regressors
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor

# TabNet
from pytorch_tabnet.tab_model import TabNetRegressor
import torch

# AutoML
from flaml import AutoML

# SHAP for interpretability
import shap

# Optional: Deep Learning with Keras
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.optimizers import Adam
    keras_available = True
except ImportError:
    keras_available = False

# Suppress warnings
warnings.filterwarnings("ignore")



def calculate_vif(X, threshold=10):
    """
    Remove features with VIF higher than threshold iteratively.
    """
    while True:
        vif_df = pd.DataFrame()
        vif_df["Variable"] = X.columns
        vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        
        max_vif = vif_df["VIF"].max()
        if max_vif > threshold:
            drop_feature = vif_df.sort_values("VIF", ascending=False).iloc[0]["Variable"]
            X = X.drop(columns=[drop_feature])
        else:
            break

    return X

def apply_boxcox(y):
    """
    Apply Box-Cox (or log) transformation to y to fix normality/heteroscedasticity.
    Shift y if any values are zero or negative.
    """
    y_shift = 0
    if (y <= 0).any():
        y_shift = abs(y.min()) + 1
        y = y + y_shift

    try:
        y_transformed, lmbda = stats.boxcox(y)
    except:
        y_transformed = np.log(y)
        lmbda = None

    return y_transformed, lmbda, y_shift

def fix_ols_assumptions(X, y, vif_threshold=10.0):
    """
    Fix all key OLS assumptions:
    - Multicollinearity (via VIF)
    - Non-normality and heteroscedasticity of residuals (Box-Cox and Yeo-Johnson)
    """
    # 1. Fix multicollinearity
    X_reduced = calculate_vif(X.copy(), threshold=vif_threshold)

    # 2. Power-transform X to address linearity + scale (Yeo-Johnson works with all values)
    pt = PowerTransformer(method='yeo-johnson', standardize=True)
    X_transformed = pd.DataFrame(pt.fit_transform(X_reduced), columns=X_reduced.columns, index=X.index)

    # 3. Transform y (Box-Cox requires positive)
    y_transformed, lmbda, y_shift = apply_boxcox(y)

    return X_transformed, y_transformed, lmbda, y_shift

def inverse_boxcox(y_transformed, lmbda, y_shift):
    """
    Inverse Box-Cox transformation to get predictions back to original scale.
    """
    if lmbda is None:
        y_original = np.exp(y_transformed)
    else:
        y_original = (y_transformed * lmbda + 1) ** (1 / lmbda)

    return y_original - y_shift

def interpret_shap(row):
    val = row['SHAP_Mean']
    if val > 0.01:
        return "Higher → Higher Target"
    elif val < -0.01:
        return "Higher → Lower Target"
    else:
        return "Little Impact"


def get_model_outputs(X_train, y_train, X_test, models_to_run=None):
    results = {}


    def ols_model(X, y, X_eval):
        X_const = sm.add_constant(X)
        model = sm.OLS(y, X_const).fit()
        X_eval_const = sm.add_constant(X_eval)
        y_pred = model.predict(X_eval_const)
        p_values = model.pvalues[1:]  # exclude intercept
        significant_vars = list(p_values[p_values < 0.05].index)
        coeffs = model.params
        equation = " + ".join([f"{coeffs[i]:.4f}*{i}" for i in coeffs.index if i != 'const'])
        equation = f"{coeffs['const']:.4f} + {equation}" if 'const' in coeffs else equation
        return y_pred, significant_vars, equation

    def lasso_model(X, y, X_eval):
        model = LassoCV(cv=5).fit(X, y)
        y_pred = model.predict(X_eval)
        coefs = pd.Series(model.coef_, index=X.columns)
        significant_vars = list(coefs[coefs != 0].index)
        equation = " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
        if model.intercept_ != 0:
            equation = f"{model.intercept_:.4f} + {equation}"
        return y_pred, significant_vars, equation

    def elastic_net_model(X, y, X_eval):
        model = ElasticNetCV(cv=5).fit(X, y)
        y_pred = model.predict(X_eval)
        coefs = pd.Series(model.coef_, index=X.columns)
        significant_vars = list(coefs[coefs != 0].index)
        equation = " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
        if model.intercept_ != 0:
            equation = f"{model.intercept_:.4f} + {equation}"
        return y_pred, significant_vars, equation

    def xgb_model(X, y, X_eval):
        model = XGBRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def rf_model(X, y, X_eval):
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        # model = RandomForestRegressor(max_features=0.5328335419963713, max_leaf_nodes=12,n_estimators=7, n_jobs=-1, random_state=12032022)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def dt_model(X, y, X_eval):
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def svr_model(X, y, X_eval):
        model = SVR()
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def mlp_model(X, y, X_eval):
        model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def keras_dnn_model(X, y, X_eval):
        if not keras_available:
            return None, None, None
        model = Sequential()
        model.add(Dense(64, input_dim=X.shape[1], activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        model.fit(X, y, epochs=100, verbose=0)
        y_pred = model.predict(X_eval).flatten()
        return y_pred, None, None

    def lightgbm_model(X_train, y_train, X_test):
        model = LGBMRegressor()
        model.fit(X_train, y_train)
        return model.predict(X_test), None, None

    def catboost_model(X_train, y_train, X_test):
        model = CatBoostRegressor(verbose=0)
        model.fit(X_train, y_train)

        # Extracting Significant Features
        feature_importance = model.get_feature_importance()
        columns = X_train.columns
        sig_vars = sorted(zip(columns, feature_importance), key=lambda x: x[1], reverse=True)


        # Extracting Dependency on target variable
        explainer = shap.TreeExplainer(model)
        shap_array = explainer.shap_values(X_train)
        
        # Mean absolute and directional SHAP values
        mean_abs_shap = np.abs(shap_array).mean(axis=0)
        mean_shap = shap_array.mean(axis=0)
        
        # Combine into a DataFrame
        shap_df = pd.DataFrame({
            'Feature': X_train.columns,
            'SHAP_Mean_Abs': mean_abs_shap,
            'SHAP_Mean': mean_shap
        })
        
        # Sort and interpret
        shap_df = shap_df.sort_values(by='SHAP_Mean_Abs', ascending=False)
        shap_df['Interpretation'] = shap_df.apply(interpret_shap, axis=1)
        shap_df = shap_df[shap_df['SHAP_Mean_Abs'] != 0]
        
        # ✅ Convert to dictionary
        interpretation_dict = dict(zip(shap_df['Feature'], shap_df['Interpretation']))


         
        return model.predict(X_test), sig_vars, interpretation_dict

    def tabnet_model(X_train, y_train, X_test):
        qt = QuantileTransformer(output_distribution='normal')
        X_train_scaled = qt.fit_transform(X_train)
        X_test_scaled = qt.transform(X_test)
        y_train_array = y_train.values.reshape(-1, 1)

        model = TabNetRegressor()
        model.fit(X_train_scaled, y_train_array, max_epochs=200, patience=20, batch_size=256, virtual_batch_size=128)
        y_pred = model.predict(X_test_scaled).flatten()
        return y_pred, None, None

    def flaml_model(X_train, y_train, X_test):
        automl = AutoML()
        automl.fit(X_train=X_train, y_train=y_train, task="regression", time_budget=5)
        return automl.predict(X_test), None, None

    def stacking_model(X_train, y_train, X_test):
        base_models = [
            ('rf', RandomForestRegressor(n_estimators=50, random_state=42)),
            ('lasso', LassoCV(cv=5))
        ]
        final_estimator = LinearRegression()
        model = StackingRegressor(estimators=base_models, final_estimator=final_estimator)
        model.fit(X_train, y_train)
        return model.predict(X_test), None, None




    
    model_dict = {
        "OLS": ols_model,
        "Lasso": lasso_model,
        "ElasticNet": elastic_net_model,
        "XGBoost": xgb_model,
        "RandomForest": rf_model,
        "DecisionTree": dt_model,
        "SVR": svr_model,
        "MLPRegressor": mlp_model,
        "LightGBM": lightgbm_model,
        "CatBoost": catboost_model,
        "TabNet": tabnet_model,
        "Stacking": stacking_model,
        "FLAML": flaml_model
    }

    if keras_available:
        model_dict['KerasDNN'] = keras_dnn_model

    # Filter if user passed model list
    if models_to_run:
        model_dict = {k: v for k, v in model_dict.items() if k in models_to_run}

    for name, model_fn in model_dict.items():
        try:
            y_pred, significant_vars, equation = model_fn(X_train, y_train, X_test)
            results[name] = {
                'y_pred': y_pred,
                'significant_vars': significant_vars,
                'equation': equation
            }
        except Exception as e:
            results[name] = {
                'y_pred': None,
                'significant_vars': None,
                'equation': None,
                'error': str(e)
            }

    return results


def get_testing_data(result_df, n):
    try:
        result_df['yearmonth'] = pd.to_datetime(result_df['yearmonth'], format='%Y%m')
        
        # Define your grouping columns
        grouping_cols = ['banner', 'category', 'brand', 'segment']
        
        # Sort the data
        df = result_df.sort_values(grouping_cols + ['yearmonth'])
        
        # Filter last "n" rows per group
        df = (
            df.groupby(grouping_cols, group_keys=False)
              .apply(lambda group: group.tail(n))
              .reset_index(drop=True)
        )
    except:
        return result_df
    return df

def drop_zero_rows_and_get_active_columns(subset, columns):

    cols_to_check = pd.Index(columns).difference(['no_of_working_days'])
    subset = subset[~(subset[cols_to_check] == 0).all(axis=1)]
    
    non_zero_cols = []
    for col in columns:
        if (subset[col] == 0).all():
            subset.drop(columns=col, inplace=True)
        else:
            non_zero_cols.append(col)
    return subset, non_zero_cols
# 
def full_output_ols(df, featured_cols, target, group_cols,simulate_change, selected_causal, change_percent, models_needed=None, config=None):
    count = 0
    df.fillna(0, inplace=True)
    df.sort_values(by=group_cols + ['yearmonth'], inplace=True)

    df_out = pd.DataFrame()
    total_cases = df[group_cols].drop_duplicates().shape[0]
    for keys, group_idx in df.groupby(group_cols).groups.items():
        count += 1
        task_completed = int(count * 100/total_cases) 
        # print(f"\rTask in Progress: {task_completed} %", end='', flush=True)
        
        group = df.loc[group_idx]
        group, features = drop_zero_rows_and_get_active_columns(group, featured_cols)
        group.fillna(0, inplace=True)

        if len(group) < len(features) + 2:
            continue

        X = group[features].copy().reset_index(drop=True)
        y = group[target].copy().reset_index(drop=True)

        # Apply scaling only if config says so
        if config and config.get("scale_features", False):
            scaler = StandardScaler()
            X = pd.DataFrame(scaler.fit_transform(X), columns=features)

        # Fix OLS assumptions if specified
        if config and config.get("fix_ols_violations", False):
            X, y_transformed, lmbda, y_shift = fix_ols_assumptions(X, y)
        else:
            y_transformed = y.copy()
            lmbda = None
            y_shift = 0

        n = len(X)
        if config['training_data_percent']:
            train_size = int(config['training_data_percent'] * n)
        else:
            train_size = n
        if n >= 12:
            X_train = X.iloc[:train_size]
            X_test = X.iloc[n - 12:]
            y_transformed = pd.Series(y_transformed, index=y.index)
            y_train = y_transformed.iloc[:train_size]
            y_test = y_transformed.iloc[n - 12:]

            x_changed = X.copy(deep=True)
            # if simulate_change:

            #     if len(selected_causal) > 0:
            #         for feature in selected_causal:
            #             if feature in x_changed.columns:
            #                 x_changed[feature] *= (1 + change_percent / 100)

            if simulate_change:
                if len(selected_causal) > 0:
                    for feature in selected_causal:
                        if feature in x_changed.columns:
                            percent_change = config["change_percent"].get(feature, 0)
                            x_changed[feature] *= (1 + percent_change / 100)

            results = get_model_outputs(X_train, y_train, x_changed, models_to_run=models_needed)

            for model, output in results.items():

                sig_vars_list = output['significant_vars']

                if model == 'CatBoost':
                    first_elements_sig_vars = [data[0] for data in sig_vars_list] if sig_vars_list else None
                else:
                    first_elements_sig_vars = output['significant_vars']
                st.markdown(f"**Significant Factors:** {first_elements_sig_vars}")

                y_pred_var = str(model) + '_y_pred'
                y_pred_transformed = output['y_pred']
                y_pred_sig_vars = str(model) + '_significant_vars'
                y_pred_equation = str(model) + '_equation'
                # print(y_pred_transformed)

                if y_pred_transformed is not None:
                    if config and config.get("fix_ols_violations", False):
                        y_pred = inverse_boxcox(y_pred_transformed, lmbda, y_shift)
                    else:
                        y_pred = y_pred_transformed

                    y_pred = np.where(np.isfinite(y_pred), y_pred, np.nan)
                else:
                    y_pred = 0

                group[y_pred_var] = y_pred
                group[y_pred_sig_vars] = [output['significant_vars']] * len(group)
                group[y_pred_equation] = [output['equation']] * len(group)
                
                

        # print(count, keys)
        
        df_out = pd.concat([df_out, group])
        # if count == 1:
        #     return df_out
    # print()
    
    return df_out

# def load_data(config,simulate_change, selected_causal = None, change_percent = 0):
#     original_data = pd.read_csv(config["data_path"])
#     # Add lag features
#     for lag in range(1, 4):
#         original_data[f'promo_effect_after_{lag}_month'] = original_data.groupby(config["grouping_columns"])['promo_in_month'].shift(lag)
    
#     df_sim = original_data.copy()

#     if simulate_change:
        
#         # If multiple causal features selected, apply change to all
#         if len(selected_causal) > 0:
#             for feature in selected_causal:
#                 df_sim[feature] *= (1 + change_percent / 100)

#     return df_sim


def main_function(config, simulate_change, selected_causal = None, change_percent = {}):
    # Load and prepare data
    original_data = pd.read_csv(config["data_path"])

    original_data = original_data[config["required_columns"]].copy()
    
    if config['filter_granularity']:
        filter_granularity = config['filter_granularity']
    
    
        original_data = original_data[
                                    (original_data['banner'] == filter_granularity[0]) &
                                    (original_data['category'] == filter_granularity[1]) &
                                    (original_data['brand'] == filter_granularity[2]) &
                                    (original_data['segment'] == filter_granularity[3]) 
                                    ]
    
    
    original_data["yearmonth"] = original_data["yearmonth"].astype(str)
    
    original_data['Error_reg'] = original_data["outlier_corrected_data"] - original_data["Insample Forecast"]
    original_data['month_no'] = original_data["yearmonth"].apply(lambda x: int(str(x)[4:]))
    
    original_data['monthly_seasonality'] = config['monthly_seasonality']
    original_data['monthly_seasonality'] = original_data.apply(lambda row: 1 if row['month_no'] == row['monthly_seasonality'] else 0, axis=1)
    
    original_data['quarter_no'] = ((original_data['month_no'] - 1) // 3) + 1
    original_data['quarterly_seasonality'] = config['quarterly_seasonality']
    original_data['quarterly_seasonality'] = original_data.apply(lambda row: 1 if row['quarter_no'] == row['quarterly_seasonality'] else 0, axis=1)
    
    
    # Add lag features
    for lag in range(1, 4):
        original_data[f'promo_effect_after_{lag}_month'] = original_data.groupby(config["grouping_columns"])['promo_in_month'].shift(lag)
    
    
    # Run modeling
    models = config["models"]
    causal_features = config["causal_features"]
    grouping = config["grouping_columns"]
    target = config["target_column"]
    
    
    result_df = full_output_ols(original_data, causal_features, target, grouping, simulate_change, selected_causal, change_percent, models_needed=models, config=config)
    result_df.fillna(0, inplace=True)
    # st.dataframe(result_df)
    # print(result_df)
    result_df['MAPE_TS'] = np.where(
        result_df['outlier_corrected_data'] == 0, 0,
        abs((result_df['Insample Forecast'] - result_df['outlier_corrected_data']) / result_df['outlier_corrected_data'])
    ) * 100
    
    # Filter test data
    testing_date = config["test_start_date"]
    if len(str(testing_date)) <= 2:
        testing_date = int(testing_date)
        df1 = get_testing_data(result_df, testing_date)
    else:
        df1 = result_df[result_df["yearmonth"] >= config["test_start_date"]]
        
    # Evaluation loop
    evaluation_results = []
    # print("Total Cases : ",  df1[['banner', 'category', 'brand', 'segment']].drop_duplicates().shape[0])
    for model in models:
        final_forecast_var = f"{model}_final_forecast"
        y_pred_var = f"{model}_y_pred"
        mape_var = f"{model}_MAPE_causal"
    
        if config['target_column'] == "Error_reg":
    
            df1[final_forecast_var] = df1[y_pred_var] + df1["Insample Forecast"]
        else:
            df1[final_forecast_var] = df1[y_pred_var]
            
        df1[mape_var] = np.where(
            df1["outlier_corrected_data"] == 0, 0,
            abs((df1[final_forecast_var] - df1["outlier_corrected_data"]) / df1["outlier_corrected_data"])
        ) * 100
    
        group_mape = df1[[*grouping, mape_var, "MAPE_TS"]].groupby(grouping).mean().reset_index()
    
        better_than_ts = group_mape[group_mape[mape_var] < group_mape["MAPE_TS"]].shape[0]
        group_mape["difference"] = (group_mape["MAPE_TS"] - group_mape[mape_var]) 
        greater_than_5pct = group_mape[group_mape["difference"] > 5].shape[0]
    
        evaluation_results.append({
            "Model": model,
            "Better_than_TS_count": better_than_ts,
            "Greater_than_5pct_count": greater_than_5pct
        })
    
    summary_df = pd.DataFrame(evaluation_results)
    st.dataframe(group_mape)

    # print(group_mape)
    draw_graph(df1,final_forecast_var, config,simulate_change, selected_causal, change_percent)

    return df1


def draw_graph(df1,final_forecast_var, config, simulate_change, selected_causal = None, change_percent = 0):
    # Load and prepare data
    original_data = pd.read_csv(config["data_path"])
    original_data = original_data[config["required_columns"]].copy()
    
    if config['filter_granularity']:
        filter_granularity = config['filter_granularity']
    
    
        original_data = original_data[
                                    (original_data['banner'] == filter_granularity[0]) &
                                    (original_data['category'] == filter_granularity[1]) &
                                    (original_data['brand'] == filter_granularity[2]) &
                                    (original_data['segment'] == filter_granularity[3]) 
                                    ]
    
    original_data["yearmonth"] = original_data["yearmonth"].astype(str)
    
    original_data['Error_reg'] = original_data["outlier_corrected_data"] - original_data["Insample Forecast"]
    original_data = original_data[original_data["yearmonth"] < config["test_start_date"]]
    original_data.drop('Insample Forecast', axis = 1, inplace = True)
    
    df = pd.concat([original_data,df1])
    
    filtered_df = df.copy()
    scaler = StandardScaler()
    unique_combinations = filtered_df[['banner', 'category', 'brand', 'segment']].drop_duplicates() 
    for _, row in unique_combinations.iterrows():
        banner, category, brand, segment = row['banner'], row['category'], row['brand'], row['segment']
    
        subset = filtered_df[
                (filtered_df['banner'] == banner) &
                (filtered_df['category'] == category) &
                (filtered_df['brand'] == brand) &
                (filtered_df['segment'] == segment)
            ]
    
        subset = subset.sort_values('yearmonth')
    
        plt.figure(figsize=(10, 4))
        
        subset[['media_in_month','outlier_corrected_data',final_forecast_var, 'Insample Forecast']] = scaler.fit_transform(subset[['media_in_month','outlier_corrected_data',final_forecast_var,'Insample Forecast']])
    
        
        plt.plot(subset['yearmonth'], subset['outlier_corrected_data'], marker='o', linestyle='-', label='Outlier Corrected Sales', )
        plt.plot(subset['yearmonth'], subset['Insample Forecast'], marker='.', linestyle='-', label='Insample Forecast', color = 'red')
        plt.plot(subset['yearmonth'], subset[final_forecast_var], marker='*', linestyle='--', label='Forecast', color = 'orange')

        # plt.plot(subset['yearmonth'], subset['promo_lag1'], marker='.', linestyle='--', label='Promo Lag')
        
        
        plt.title(f'{banner} | {category} | {brand} | {segment}')
        plt.xlabel('Year-Month')
        plt.ylabel('Sales (tons)')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.legend()  # <- this adds the labels
        plt.tight_layout()
        plt.show()
        st.pyplot(plt.gcf())
    



# Load existing config or return empty if no config exists
def load_config(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

# Save updated config to the JSON file
def save_config(config,CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def generating_key(values):
    return ",".join(values)


def main():
    CONFIG_PATH = "config.json"  # This is where we'll save the config

    # Create the Streamlit app UI
    st.title("📊 Dynamic Model Configurator")

    # Load existing configuration
    config = load_config(CONFIG_PATH)

    # Inputs to update the config
    config["data_path"] = st.text_input("Data Path", config.get("data_path", "generating_final_data.csv"))

    config["target_column"] = st.selectbox("Target Column", [
        "Error_reg", "outlier_corrected_data"
    ], index=0 if config.get("target_column", "Error_reg") == "Error_reg" else 1)


    config["models"] = [st.selectbox(
        "Select Model",
        [
            "OLS", "Lasso", "ElasticNet", "XGBoost", "RandomForest",
            "DecisionTree", "SVR", "MLPRegressor", "CatBoost", "Stacking"
        ],
        index=(
            [
                "OLS", "Lasso", "ElasticNet", "XGBoost", "RandomForest",
                "DecisionTree", "SVR", "MLPRegressor", "CatBoost", "Stacking"
            ].index(config.get("models", ["CatBoost"])[0])
            if config.get("models") else 8  # Default to "CatBoost"
        )
    )]

    config["scale_features"] = st.checkbox("Scale Features", value=config.get("scale_features", True))
    config["fix_ols_violations"] = st.checkbox("Fix OLS Violations", value=config.get("fix_ols_violations", True))

    config["training_data_percent"] = st.slider("Training Data %", 0.1, 0.95, config.get("training_data_percent", 0.8), step=0.05)

    config["test_start_date"] = st.text_input("Test Start Date (yyyymm)", config.get("test_start_date", "202311"))


    valid_seasonality = list(range(13))
    default_value = config.get("monthly_seasonality", 8)

    # Ensure default_value is valid
    if default_value not in valid_seasonality:
        default_value = 0  # Fallback to 8 if invalid

    config["monthly_seasonality"] = st.selectbox(
        "Monthly Seasonality",
        valid_seasonality,
        index=valid_seasonality.index(default_value)
    )

    valid_quarterly_seasonality = list(range(5))
    default_value = config.get("quarterly_seasonality", 2)

    # Ensure default_value is valid
    if default_value not in valid_quarterly_seasonality:
        default_value = 0  # Fallback to 8 if invalid

    config["quarterly_seasonality"] = st.selectbox(
        "Quarterly Seasonality",
        valid_quarterly_seasonality,
        index=valid_quarterly_seasonality.index(default_value)
    )


    causal_features = config.get("causal_features", [])

    st.subheader("🔧 Simulate Impact of Causal Factors")

    # simulate_change = 0
    # # User input: select causal features and change percentage
    # selected_causal = st.multiselect("Select Causal Factors to Simulate", causal_features)
    # change_percent = st.slider("Change Percentage (%)", -50, 50, 10)

    # # Save into config or session state
    # config["simulated_causal_factors"] = selected_causal
    # config["change_percent"] = change_percent

    # # Optional: show selected inputs
    # st.markdown(f"**Change Applied:** {change_percent}%")
    # simulate_change = 1

    simulate_change = 0

    # User input: select causal features to simulate
    selected_causal = st.multiselect("Select Causal Factors to Simulate", causal_features)

    # Initialize a dictionary to hold individual change percentages
    change_percent_dict = {}

    if selected_causal:
        st.markdown("### Adjust Change Percentage for Each Selected Causal")
        cols = st.columns(len(selected_causal))  # Create one column per feature
        
        for i, causal in enumerate(selected_causal):
            with cols[i]:
                change_percent_dict[causal] = st.slider(
                    f"{causal}", -50, 50, 0, key=f"slider_{causal}"
                )

    # Save into config or session state
    config["simulated_causal_factors"] = selected_causal
    config["change_percent"] = change_percent_dict

    # Optional: show selected inputs
    if change_percent_dict:
        st.markdown("**Change Applied:**")
        for factor, percent in change_percent_dict.items():
            st.markdown(f"- `{factor}`: **{percent}%**")

    simulate_change = 1 if change_percent_dict else 0



    # Load and preprocess data
    original_data = pd.read_csv(config["data_path"])

    original_data['key'] = original_data[["banner", "category", "brand", "segment"]].apply(generating_key, axis=1)
    valid_filter_granularity = list(original_data['key'].unique())

    # Get default as a string
    default_value_list = config.get("filter_granularity", ["AEON", "ORAL", "CLOSEUP", "TOOTHPASTE"])
    default_value_str = ",".join(default_value_list)

    # Ensure default is in the valid list
    if default_value_str not in valid_filter_granularity:
        default_value_str = "AEON,ORAL,CLOSEUP,TOOTHPASTE"

    # Dropdown selection (returns string)
    selected_key = st.selectbox(
        "Filter Granularity",
        valid_filter_granularity,
        index=valid_filter_granularity.index(default_value_str)
    )

    # Convert selected string back to list and save to config
    config["filter_granularity"] = selected_key.split(",")




    # Button to run the model with updated config
    if st.button("Run Model"):
        save_config(config, CONFIG_PATH)  # Save the updated config
        st.success("✅ Config saved. Running model...")
        with st.spinner("Processing..."):
            if simulate_change:
                main_function(config, simulate_change, selected_causal, change_percent_dict)  # This will run your model with the updated config
            else:
                main_function(config, simulate_change)
        st.success("✅ Done!")

main()