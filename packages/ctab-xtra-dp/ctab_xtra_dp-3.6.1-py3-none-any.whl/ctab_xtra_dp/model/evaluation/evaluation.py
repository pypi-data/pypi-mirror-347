import numpy as np
import pandas as pd 
from sklearn import metrics
from sklearn import model_selection
from sklearn.preprocessing import MinMaxScaler,StandardScaler, LabelEncoder

from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn import svm,tree
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor ,HistGradientBoostingClassifier, HistGradientBoostingRegressor
from dython.nominal import associations
from scipy.stats import wasserstein_distance
from scipy.spatial import distance
import warnings
from .gower_mix import gower_distance
from collections import defaultdict

from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor


warnings.filterwarnings("ignore")





def get_summary_metrics(real_train,
                        real_test,
                        fake,
                        categorical=[],
                        mixed={},
                        mnar=True,
                        mixed_type=False,
                        problem="classification",
                        privacy_data_percent=0.15
                        ):

    simmlarity = stat_sim(real_train,fake,categorical,mixed,mnar)
    models_to_run = get_models_to_run(problem_type=problem,mixed_type=mixed_type)
    utility = get_utility_metrics(real_train,real_test,[fake],categorical=categorical, mixed=mixed,scaler="MinMax",problem=problem, models=models_to_run)
    privacy = privacy_metrics(real_train,fake,metric='gower',data_percent=privacy_data_percent)
    return utility, simmlarity, privacy


def supervised_model_training(x_train, y_train, x_test, 
                              y_test, model_name,problem_type):
  
  model = get_supervised_model(model_name,problem_type)
  
  model.fit(x_train, y_train)
  pred = model.predict(x_test)

  if problem_type == "classification":
    acc = metrics.accuracy_score(y_test,pred)
    if len(np.unique(y_train))>2: # We have mulitclass classification
      predict = model.predict_proba(x_test)        
      auc = metrics.roc_auc_score(y_test, predict,average="weighted",multi_class="ovr")
      f1_score = metrics.precision_recall_fscore_support(y_test, pred,average="weighted")[2]

    else: # We have binary classification
      predict = model.predict_proba(x_test)[:,1]    
      auc = metrics.roc_auc_score(y_test, predict)
      f1_score = metrics.precision_recall_fscore_support(y_test,pred)[2].mean()
    return [acc, auc, f1_score] 
  
  if problem_type == "regression":
    mse = metrics.mean_absolute_percentage_error(y_test,pred)
    evs = metrics.explained_variance_score(y_test, pred)
    r2_score = metrics.r2_score(y_test,pred)
    return [mse, evs, r2_score]

  raise ValueError(f"Unknown problem type: {problem_type}. Supported types are 'classification' and 'regression'.")




def get_supervised_model(model_name,problem_type,random_state=42):
  if problem_type == "classification":
    if model_name == 'lr': return LogisticRegression(random_state=random_state,max_iter=500)
    if model_name == 'svm': return svm.SVC(random_state=random_state,probability=True)

    if model_name == 'dt': return tree.DecisionTreeClassifier(random_state=random_state)
    if model_name == 'rf': return RandomForestClassifier(random_state=random_state)
    if model_name == 'mlp': return MLPClassifier(random_state=random_state,max_iter=100)
    if model_name == 'xgb': return XGBClassifier(random_state=random_state, use_label_encoder=False, eval_metric='logloss')
    if model_name == 'lgbm': return LGBMClassifier(random_state=random_state,verbose=-1)
    if model_name == 'cat': return CatBoostClassifier(random_state=random_state, verbose=0)
    raise ValueError(f"Unknown model name: {model_name} for classification")
  
  if problem_type == "regression":
    if model_name == 'lin': return LinearRegression()
    if model_name == 'ridge': return Ridge(random_state=random_state)
    if model_name == 'lasso': return Lasso(random_state=random_state)
    if model_name == 'B_ridge': return BayesianRidge()
  
    if model_name == 'dt': return tree.DecisionTreeRegressor(random_state=random_state)
    if model_name == 'rf': return RandomForestRegressor(random_state=random_state)
    if model_name == 'hgb': return HistGradientBoostingRegressor(random_state=random_state)
    if model_name == 'xgb': return XGBRegressor(random_state=random_state)
    if model_name == 'lgbm': return LGBMRegressor(random_state=random_state,verbose=-1)
    if model_name == 'cat': return CatBoostRegressor(random_state=random_state, verbose=0)
    raise ValueError(f"Unknown model name: {model_name} for regression")

  raise ValueError(f"Unknown problem type: {problem_type}. Supported types are 'classification' and 'regression'.")


def get_models_to_run(problem_type,mixed_type=False):
  if problem_type == "classification":
    if mixed_type:
      return ["rf","xgb","lgbm","cat"] # Can old use tree based models for mixed data types, sumpement with catboost 
    else:
      return ["lr","svm","rf","xgb","lgbm"] # The default models, add a simpler model for a varied set of models
  if problem_type == "regression":
    if mixed_type:
      return ["rf","xgb","lgbm","cat"] # Can old use tree based models for mixed data types, sumpement with catboost 
    else:
      return ["lin","lasso","rf","xgb","lgbm"] # The default models, add a simpler model for a varied set of models

  raise ValueError(f"Unknown problem type: {problem_type}. Supported types are 'classification' and 'regression'.")


def split_data(df, test_ratio=.20, target=None,problem="classification",random_state=42):
  if problem == "classification":
    if target is None: raise ValueError("Target column must be specified for classification")
    train, test = model_selection.train_test_split(df, test_size=test_ratio, stratify=df[target], random_state=random_state)
  else:
    train, test = model_selection.train_test_split(df, test_size=test_ratio, random_state=random_state)
  return train, test


def get_utility_metrics(real_train,
                        real_test,
                        fakes,
                        categorical=[],
                        mixed={},
                        target=None,
                        scaler="MinMax",
                        problem="classification", 
                        models=["lr","dt","rf","mlp"]):


    real_train = real_train.copy()
    real_test = real_test.copy()
    categorical = categorical.copy()

    if target is None:
      target = real_train.columns[-1]
    
    real_train, additional_categorical_cols, _=_process_mixed_columns(real_train, mixed, continuous_placeholder=np.nan)

    real_test, _, _=_process_mixed_columns(real_test, mixed, continuous_placeholder=np.nan)

    categorical.extend(additional_categorical_cols)

    # Encode categorical columns in the real dataset
    for col in categorical:
        # Combine both columns into one Series
        combined = pd.concat([real_train[col], real_test[col]], axis=0)

        # Fit encoder on the combined set
        le = LabelEncoder()
        le.fit(combined)

        # Transform separately
        real_train[col] = le.transform(real_train[col])
        real_test[col] = le.transform(real_test[col])
      
      
    data_dim = real_train.shape[1]

    data_real_X_train = real_train.drop(target, axis=1).to_numpy()
    data_real_y_train = real_train[target].to_numpy()

    data_real_X_test = real_test.drop(target, axis=1).to_numpy()
    data_real_y_test = real_test[target].to_numpy()
    
    # Apply scaling
    if scaler=="MinMax":
        scaler_real = MinMaxScaler()
    else:
        scaler_real = StandardScaler()
    

    
    scaler_real.fit(data_real_X_train)
    X_train_real_scaled = scaler_real.transform(data_real_X_train)
    X_test_real_scaled = scaler_real.transform(data_real_X_test)



    if problem == "classification":
      metrics_list = ["Accuracy", "AUC", "F1-Score"]
    else:
      metrics_list = ["MAPE", "Explained Variance", "R2 Score"]


    all_real_results = []
    for model in models:
      real_results = supervised_model_training(X_train_real_scaled,data_real_y_train,X_test_real_scaled,data_real_y_test,model,problem)
      all_real_results.append(real_results)
      
    all_fake_results_avg = []
    
    for fake in fakes:
      fake = fake.copy()

      fake, _, _=_process_mixed_columns(fake, mixed, continuous_placeholder=np.nan)

      # Encode categorical columns in the fake dataset
      for col in categorical:
        label_encoder = LabelEncoder()
        fake[col] = label_encoder.fit_transform(fake[col])

      data_fake = fake.to_numpy()

      data_fake_y = fake.loc[:, target].to_numpy()
      data_fake_X = fake.drop(target,axis=1).to_numpy()
     
    


      # Apply scaling
      if scaler=="MinMax":
        scaler_fake = MinMaxScaler()
      else:
        scaler_fake = StandardScaler()
      
      scaler_fake.fit(data_fake_X)
      
      X_train_fake_scaled = scaler_fake.transform(data_fake_X)
      
      all_fake_results = []
      for model in models:
        fake_results = supervised_model_training(X_train_fake_scaled,data_fake_y,X_test_real_scaled,data_real_y_test,model,problem)
        all_fake_results.append(fake_results)

      all_fake_results_avg.append(all_fake_results)
    

    

    
    real_results_df = pd.DataFrame(all_real_results, columns=metrics_list, index=models)

    fake_results_dfs = []

    for fake_results in all_fake_results_avg:
      fake_df = pd.DataFrame(fake_results, columns=metrics_list, index=models)
      fake_results_dfs.append(fake_df)

  # Return real and list of fake DataFrames
    return real_results_df, fake_results_dfs




def stat_sim(real,fake,categorical=[],mixed={},mnar=True):
    

    nan_placeholder = "__MISSING__"
    continuous_placeholder='__CONTINUOUS__'


    real = real.copy()
    fake = fake.copy()
    categorical = categorical.copy()

   
    mixed = defaultdict(list, mixed)

    columns_with_nan = []
    if mnar: # If Missing not at random, we replace NaN values with a placeholder,effectively treating them as a separate category
      
      nan_counts_real = real.isna().sum()
      nan_counts_fake = fake.isna().sum()
      columns_with_nan_real = nan_counts_real[nan_counts_real > 0].index.tolist()
      columns_with_nan_fake = nan_counts_fake[nan_counts_fake > 0].index.tolist()

      columns_with_nan = list(set(columns_with_nan_real + columns_with_nan_fake))

      for column in columns_with_nan:
        if continuous_placeholder not in mixed[column]: mixed[column].append(nan_placeholder)

      real = real.fillna(nan_placeholder)
      fake = fake.fillna(nan_placeholder)

    real_processed, additional_categorical_cols, additional_continuous_cols = _process_mixed_columns(real, mixed, continuous_placeholder=continuous_placeholder)
    fake_processed, _, _ = _process_mixed_columns(fake, mixed, continuous_placeholder=continuous_placeholder)
    categorical.extend(additional_categorical_cols)


    diff_corr_forbenious, diff_corr_mae = alternative_correlation(real_processed, fake_processed, columns_to_remove=additional_continuous_cols) 
    summary, column_stats = column_similarity(real_processed, fake_processed, categorical)

    return summary, column_stats, {"forbenious": diff_corr_forbenious, "mae": diff_corr_mae}



def column_similarity(real, fake, categorical=[]):


    real = real.copy()
    fake = fake.copy()



    for col in categorical:

      combined = pd.concat([real[col], fake[col]], axis=0)

      le = LabelEncoder()
      le.fit(combined)

      real[col] = le.transform(real[col])
      fake[col] = le.transform(fake[col])


    column_stats = []

    previous_hybrid_feature_continous_weight = 0
    weights = []
    for column in real.columns:
        
        if column in categorical:
            
            real_pdf=(real[column].value_counts()/real[column].value_counts().sum())
            fake_pdf=(fake[column].value_counts()/fake[column].value_counts().sum())
            categories = (fake[column].value_counts()/fake[column].value_counts().sum()).keys().tolist()
            sorted_categories = sorted(categories)
            
            real_pdf_values = [] 
            fake_pdf_values = []

            for i in sorted_categories:
                #if i not in real_pdd: raise ValueError(f"Category {i} present in fake but not in real data")
                if i not in real_pdf: real_pdf[i] = 0 #TODO: might not be like this
                if i not in fake_pdf: fake_pdf[i] = 0
                real_pdf_values.append(real_pdf[i])
                fake_pdf_values.append(fake_pdf[i])
            
                
            js_distance = (distance.jensenshannon(real_pdf_values,fake_pdf_values, 2.0))

            
            weight = 1 - previous_hybrid_feature_continous_weight if previous_hybrid_feature_continous_weight else 1 # If we have hybrid column we save the weight for next itteration
            previous_hybrid_feature_continous_weight = 0 # reset for next iteration
            statistics = [column, "JSD",js_distance, weight]
    
            weights.append(weight)
    
        else:
            scaler = MinMaxScaler()
            scaler.fit(real[column].values.reshape(-1,1))
            l1 = scaler.transform(real[column].values.reshape(-1,1)).flatten()
            l2 = scaler.transform(fake[column].values.reshape(-1,1)).flatten()
            #TODO: this might drop stuff it should not
            weight = 1 - np.isnan(l1).sum()/len(l1)
            previous_hybrid_feature_continous_weight = 0 if weight == 1 else weight # If we have hybrid column we save the weight for next itteration
            l1 = l1[~np.isnan(l1)]
            l2 = l2[~np.isnan(l2)]
            w_distance = (wasserstein_distance(l1,l2))
            statistics = [column, "WD", w_distance, weight]
            weights.append(weight)
        column_stats.append(statistics)

    column_stats = pd.DataFrame(column_stats, columns=["Column", "Metric", "Distance", "Weight"])

    summary = column_stats.groupby('Metric').agg({
        'Distance': [
            ('Weighted_Avg', lambda x: np.average(x, weights=column_stats.loc[x.index, 'Weight'])),
            ('Mean', 'mean'),
            ('Std', 'std')
        ]
    })
    summary.columns = summary.columns.get_level_values(1)
    summary = summary.reset_index()
    return summary, column_stats

def alternative_correlation(real, fake, columns_to_remove=[]):
    """
    Calculate the correlation between real and fake datasets
    
    Args:
        real (pd.DataFrame): Real dataset
        fake (pd.DataFrame): Fake dataset
        columns_to_remove (list): List of columns to remove from the datasets
    
    Returns:
        float: Correlation distance
    """
    # Remove specified columns
    real = real.drop(columns=columns_to_remove, errors='ignore')
    fake = fake.drop(columns=columns_to_remove, errors='ignore')

    # Calculate correlation matrices
    real_corr = associations(real, compute_only=True)["corr"]
    fake_corr = associations(fake, compute_only=True)["corr"]

    
    # Using forbenious
    diff_corr_forbenious = np.linalg.norm(real_corr - fake_corr, ord='fro')

    # Caclulate using mean absolute error
    diff_matrix = np.abs(real_corr - fake_corr)
    columnwise_avg_diff = diff_matrix.mean(axis=0)
    diff_corr_mae = columnwise_avg_diff.mean()
  
    return diff_corr_forbenious, diff_corr_mae
    
    

def _process_mixed_columns(df, mixed, continuous_placeholder='__CONTINUOUS__'):
    """
    Process mixed columns by extracting categorical values
    
    Args:
        df (pd.DataFrame): Input DataFrame
        mixed (dict): Dictionary of mixed columns with their categories
        continuous_placeholder (str): Placeholder to indicate continuous value in categorical part of mixed columns
    
    Returns:
        tuple: (processed_df, additional_categorical_cols)
    """
    # Create a copy of the DataFrame
    df_copy = df.copy()
    additional_categorical_cols = []
    additional_continuous_cols = []
    
    for col, categories in mixed.items():
        # Create a new categorical column
        new_cont_col_name = f"{col}_continuous"
        new_cat_col_name = f"{col}_categorical"
        
        continuous_series = df_copy[col].apply(
            lambda x: x if x not in categories else np.nan
        )
        df_copy[new_cont_col_name] = continuous_series
        additional_continuous_cols.append(new_cont_col_name)

        # Create a series for categorical values
        categorical_series = df_copy[col].apply(
            lambda x: x if x in categories else continuous_placeholder
        )
        
        # Add the new categorical column
        df_copy[new_cat_col_name] = categorical_series
        additional_categorical_cols.append(new_cat_col_name)


        # Drop the original column
        df_copy.drop(columns=[col], inplace=True)
    
    return df_copy, additional_categorical_cols, additional_continuous_cols





def privacy_metrics(real, 
                    fake, 
                    metric = 'gower', 
                    data_percent=0.15,
                    verbose=False):
    """
    Calculate privacy metrics between real and fake datasets.
    
    Parameters:
    real (DataFrame): Real dataset
    fake (DataFrame): Synthetic dataset
    data_percent (int): Percentage of data to sample for analysis
    
    Returns:
    dict: Dictionary containing detailed privacy metrics
    """
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn import metrics
    import pandas as pd
    
    # Create a metrics dictionary to store all results
    privacy_summary = []
    
    # Sample the data
    real_refined = real.sample(n=int(len(real)*data_percent), random_state=42).to_numpy()
    fake_refined = fake.sample(n=int(len(fake)*data_percent), random_state=42).to_numpy()
    
    if verbose:
      print("==== Privacy Metrics Analysis ====")
      print(f"Using {data_percent}% of data for analysis")
      
      
      print(f"Real data sample size: {len(real_refined)}")
      print(f"Fake data sample size: {len(fake_refined)}")
      

      print("\nCalculating pairwise distances...")
    
    # Compute distance matrix from real-fake, real-real, and fake-fake
    dist_rf, dist_rr, dist_ff = _calculate_pariwise_distances(real_refined, fake_refined, metric=metric)

    # Remove the diagonal to ignore self-distances
    dist_rr = dist_rr[~np.eye(dist_rr.shape[0],dtype=bool)].reshape(dist_rr.shape[0],-1)
    dist_ff = dist_ff[~np.eye(dist_ff.shape[0],dtype=bool)].reshape(dist_ff.shape[0],-1) 

    
    
    # Find smallest two distances for each metric
    smallest_two_indexes_rf = [dist_rf[i].argsort()[:2] for i in range(len(dist_rf))]
    smallest_two_rf = [dist_rf[i][smallest_two_indexes_rf[i]] for i in range(len(dist_rf))]       
    smallest_two_indexes_rr = [dist_rr[i].argsort()[:2] for i in range(len(dist_rr))]
    smallest_two_rr = [dist_rr[i][smallest_two_indexes_rr[i]] for i in range(len(dist_rr))]
    smallest_two_indexes_ff = [dist_ff[i].argsort()[:2] for i in range(len(dist_ff))]
    smallest_two_ff = [dist_ff[i][smallest_two_indexes_ff[i]] for i in range(len(dist_ff))]
    
    # Cacluaate nearest neighbor distance ratios
    nndr_ratio_rr = np.array([i[0]/i[1] for i in smallest_two_rr])
    nndr_ratio_ff = np.array([i[0]/i[1] for i in smallest_two_ff])
    nndr_ratio_rf = np.array([i[0]/i[1] for i in smallest_two_rf])

    # Calculate distance to closest record
    dcr_rf = np.array([i[0] for i in smallest_two_rf])
    dcr_rr = np.array([i[0] for i in smallest_two_rr])
    dcr_ff = np.array([i[0] for i in smallest_two_ff])
    
    # We report the lowerst 5th percentile of the metrics
    nndr_fifth_perc_rr = np.percentile(nndr_ratio_rr, 5)
    nndr_fifth_perc_ff = np.percentile(nndr_ratio_ff, 5)
    nndr_fifth_perc_rf = np.percentile(nndr_ratio_rf, 5)
    
    fifth_perc_rf = np.percentile(dcr_rf, 5)
    fifth_perc_rr = np.percentile(dcr_rr, 5)
    fifth_perc_ff = np.percentile(dcr_ff, 5)
    
    

    privacy_percentiles = pd.DataFrame({
    'rr': [nndr_fifth_perc_rr, fifth_perc_rr],
    'ff': [nndr_fifth_perc_ff, fifth_perc_ff],
    'rf': [nndr_fifth_perc_rf, fifth_perc_rf]
    }, index=['nndr_5th', 'dcr_5th'])

    privacy_summary.append(privacy_percentiles)
    
    if verbose:
      print("\n== Nearest Neighbor Ratio Metrics (5th percentile) ==")
      print(f"Real-to-Real NN Ratio (5th): {nndr_fifth_perc_rr:.4f}")
      print(f"Fake-to-Fake NN Ratio (5th): {nndr_fifth_perc_ff:.4f}")
      print(f"Real-to-Fake NN Ratio (5th): {nndr_fifth_perc_rf:.4f}")
    
      print("\n== Minimum Distance Metrics (5th percentile) ==")
      print(f"Real-to-Real Min Distance (5th): {fifth_perc_rr:.4f}")
      print(f"Fake-to-Fake Min Distance (5th): {fifth_perc_ff:.4f}")
      print(f"Real-to-Fake Min Distance (5th): {fifth_perc_rf:.4f}")


    nnaa = compute_nnaa(dist_rf,dist_rr,dist_ff)
    privacy_summary.append(nnaa)

    if verbose:
      print("\n== Nearest Neighbor Adversarial Accuracy (NNAA) ==")
      print(f"NNAA: {nnaa:.4f}")
        
    
    
    if verbose:
      print("\n==== Summary Interpretation ====")
      if fifth_perc_rf > (fifth_perc_rr + fifth_perc_ff)/2:
          print("✓ Good distance between real and synthetic records")
      else:
          print("⚠ Synthetic records may be too similar to real data")
          
      if nndr_fifth_perc_rf > (nndr_fifth_perc_rr + nndr_fifth_perc_ff)/2:
          print("✓ Good neighbor distance ratios")
      else:
          print("⚠ Neighbor distance ratios indicate possible privacy concerns")
      
    
    return privacy_summary


# Compute the Nearest Neighbor Adversarial Accuaracy (NNAA) between real and fake data
def compute_nnaa(dist_rf, # Distance matrix between real and fake data
                 dist_rr, # Distance matrix between real and real data
                 dist_ff): # Distance matrix between fake and fake data

    real_data_size = dist_rf.shape[0] # Number of real data points
    fake_data_size = dist_rf.shape[1] # Number of fake data points

    dist_fr = dist_rf.T # Transpose to get distance matrix between fake and real data

    dist_rf_min = np.min(dist_rf, axis=1) # Minimum distance from real to fake
    dist_fr_min = np.min(dist_fr, axis=1) # Minimum distance from fake to real
    dist_rr_min = np.min(dist_rr, axis=1) # Minimum distance from real to real
    dist_ff_min = np.min(dist_ff, axis=1) # Minimum distance from fake to fake

    real_data_closest = (dist_rr_min < dist_rf_min).astype(int) # The closest point to real data is reals data
    fake_data_closest = (dist_ff_min < dist_fr_min).astype(int) # The closest point to fake data is fakes data

    nnaa = (real_data_closest.mean() + fake_data_closest.mean()) / 2 # Take the mean of both and average them

    return nnaa



def _calculate_pariwise_distances(real, fake, metric='gower'):
    dist_rf = 0 # Pairwise distance between real and fake
    dist_rr = 0 # Pairwise distance in real data
    dist_ff = 0 # Pairwise distance between fake and fake
    if metric == 'gower':
      dist_rf = gower_distance(real,fake)
      dist_rr = gower_distance(real,real)
      dist_ff = gower_distance(fake,fake)
      return dist_rf, dist_rr, dist_ff


    if metric == 'euclidean':
      scalerR = StandardScaler()
      scalerF = StandardScaler()
      scalerR.fit(real)
      scalerF.fit(fake)
      df_real_scaled = scalerR.transform(real)
      df_fake_scaled = scalerF.transform(fake)

      dist_rf = metrics.pairwise_distances(df_real_scaled, Y=df_fake_scaled, metric='minkowski', n_jobs=-1)
      dist_rr = metrics.pairwise_distances(df_real_scaled, Y=None, metric='minkowski', n_jobs=-1)
      dist_ff = metrics.pairwise_distances(df_fake_scaled, Y=None, metric='minkowski', n_jobs=-1)

      return dist_rf, dist_rr, dist_ff
    

    raise ValueError(f"Unknown metric: {metric}. Supported metrics are 'gower' and 'euclidean'.")




import matplotlib.pyplot as plt


def compare_dataframes(
    df: pd.DataFrame,
    syn: pd.DataFrame,
    nominal_values: dict,
    categorical_columns: list = None,
    columns: list = None
):
    # 100 % ChatGPTs work
    """
    Compare each column in df and syn using:
    - Histogram if the column has continuous data
    - Bar chart if the column has categorical data

    Mixed columns are plotted alone; one-type columns (cat or cont only) are plotted two per row.

    Parameters:
    - df: Original DataFrame
    - syn: Synthetic DataFrame (same columns)
    - nominal_values: dict mapping column names to categorical entries (can include np.nan)
    - categorical_columns: list of columns to treat as fully categorical (optional)
    - columns: optional list of column names to include in the plot
    """
    categorical_columns = categorical_columns or []
    columns_to_plot = columns if columns is not None else df.columns
    one_part_buffer = []

    def plot_one_part_pair(pair):
        plt.figure(figsize=(14, 5))
        for i, (col, cat_vals, cont_vals, is_cat) in enumerate(pair):
            plt.subplot(1, 2, i + 1)
            if is_cat:
                all_categories = set(cat_vals[0].unique()).union(set(cat_vals[1].unique()))
                orig_counts = cat_vals[0].value_counts().reindex(all_categories, fill_value=0)
                syn_counts = cat_vals[1].value_counts().reindex(all_categories, fill_value=0)
                width = 0.35
                x = np.arange(len(all_categories))
                plt.bar(x - width/2, orig_counts.values, width=width, label='Original', edgecolor='black')
                plt.bar(x + width/2, syn_counts.values, width=width, label='Synthetic', edgecolor='black')
                plt.xticks(ticks=x, labels=all_categories, rotation=45)
                plt.title(f'{col} (Categorical)')
                plt.xlabel('Category')
                plt.ylabel('Count')
                plt.legend()
            else:
                bins = np.histogram_bin_edges(np.concatenate([cont_vals[0], cont_vals[1]]), bins=50)
                plt.hist(cont_vals[0], bins=bins, alpha=0.6, label='Original', edgecolor='black')
                plt.hist(cont_vals[1], bins=bins, alpha=0.6, label='Synthetic', edgecolor='black')
                plt.title(f'{col} (Continuous)')
                plt.xlabel('Value')
                plt.ylabel('Frequency')
                plt.legend()
        plt.tight_layout()
        plt.show()

    for col in columns_to_plot:
        original = df[col]
        synthetic = syn[col]

        if col in categorical_columns:
            cat_orig = original.fillna('NaN').astype(str)
            cat_syn = synthetic.fillna('NaN').astype(str)
            cont_orig = cont_syn = pd.Series(dtype=float)
        else:
            mixed_values = nominal_values.get(col, [])

            def split_series(series, mixed_values):
                is_categorical = series.apply(
                    lambda x: any((pd.isna(val) and pd.isna(x)) or (str(x) == str(val)) for val in mixed_values)
                )
                categorical = series[is_categorical].fillna('NaN')
                continuous = pd.to_numeric(series[~is_categorical], errors='coerce').dropna().astype(float)
                return categorical, continuous

            cat_orig, cont_orig = split_series(original, mixed_values)
            cat_syn, cont_syn = split_series(synthetic, mixed_values)

        has_cont = not cont_orig.empty or not cont_syn.empty
        has_cat = not cat_orig.empty or not cat_syn.empty

        # Case 1: Mixed → full-row layout
        if has_cat and has_cont:
            plt.figure(figsize=(14, 6))
            plt.subplot(1, 2, 1)
            bins = np.histogram_bin_edges(np.concatenate([cont_orig, cont_syn]), bins=50)
            plt.hist(cont_orig, bins=bins, alpha=0.6, label='Original', edgecolor='black')
            plt.hist(cont_syn, bins=bins, alpha=0.6, label='Synthetic', edgecolor='black')
            plt.title(f'Histogram (Continuous): {col}')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.legend()

            plt.subplot(1, 2, 2)
            all_categories = set(cat_orig.unique()).union(set(cat_syn.unique()))
            orig_counts = cat_orig.value_counts().reindex(all_categories, fill_value=0)
            syn_counts = cat_syn.value_counts().reindex(all_categories, fill_value=0)
            width = 0.35
            x = np.arange(len(all_categories))
            plt.bar(x - width/2, orig_counts.values, width=width, label='Original', edgecolor='black')
            plt.bar(x + width/2, syn_counts.values, width=width, label='Synthetic', edgecolor='black')
            plt.xticks(ticks=x, labels=all_categories, rotation=45)
            plt.title(f'Bar Chart (Categorical): {col}')
            plt.xlabel('Category')
            plt.ylabel('Count')
            plt.legend()
            plt.tight_layout()
            plt.show()

        # Case 2: Only categorical or continuous → buffer it for side-by-side plotting
        elif has_cat:
            one_part_buffer.append((col, (cat_orig, cat_syn), None, True))
        elif has_cont:
            one_part_buffer.append((col, None, (cont_orig, cont_syn), False))

        # Plot in pairs if buffer has two items
        if len(one_part_buffer) == 2:
            plot_one_part_pair(one_part_buffer)
            one_part_buffer = []

    # Final leftover plot if only one item in buffer
    if len(one_part_buffer) == 1:
        plot_one_part_pair([one_part_buffer[0]])
