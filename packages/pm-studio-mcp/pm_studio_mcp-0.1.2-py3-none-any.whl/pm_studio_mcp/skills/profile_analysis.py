import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import json
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Add a JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int_, np.intc, np.intp, np.int8,
                           np.int16, np.int32, np.int64, np.uint8, np.uint16,
                           np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, np.bool)):
            return bool(obj)
        elif isinstance(obj, np.void):
            return None
        elif isinstance(obj, np.datetime64):
            return str(obj)
        elif isinstance(obj, np.timedelta64):
            return str(obj)
        elif isinstance(obj, np.complex_):
            return obj.real
        return super(NumpyEncoder, self).default(obj)

class ProfileAnalyzer:
    """MCP Tool: User Profile Clustering Analysis Tool for discovering user groups and automatically generating user profiles"""
    
    @staticmethod
    def analyze_user_profiles(file_path: str, working_dir: str, 
                             max_clusters: int = 10, 
                             id_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform cluster analysis on user data to generate user profiles
        
        Args:
            file_path (str): User data file path (Excel or CSV)
            working_dir (str): Working directory for saving result files
            max_clusters (int): Maximum number of clusters
            id_column (Optional[str]): User ID column name, if available
            
        Returns:
            Dict[str, Any]: Dictionary containing analysis results
        """
        try:
            print(f"Starting user profile cluster analysis...")
            
            # Create results directory
            results_dir = os.path.join(working_dir, "profile_analysis_results")
            os.makedirs(results_dir, exist_ok=True)
            
            # Load and explore data
            df = ProfileAnalyzer._load_data(file_path)
            
            # Data preprocessing
            X, df_clean, numeric_features, categorical_features = ProfileAnalyzer._preprocess_data(df)
            
            # Determine optimal number of clusters
            optimal_k, image_paths = ProfileAnalyzer._determine_optimal_k(
                X, max_clusters, results_dir)
            
            # Perform clustering
            df_with_clusters, clusters_image_path = ProfileAnalyzer._perform_clustering(
                X, optimal_k, df_clean, results_dir)
            
            # Save complete data with cluster labels as CSV file
            clustered_data_path = os.path.join(results_dir, "data_with_clusters.csv")
            df_with_clusters.to_csv(clustered_data_path, index=False)
            print(f"Complete data with cluster labels saved to: {clustered_data_path}")
            
            # Analyze clustering results
            cluster_profiles, profile_csv_path = ProfileAnalyzer._analyze_clusters(
                df_with_clusters, numeric_features, categorical_features, results_dir)
            
            # Create results summary
            summary = {
                "status": "success",
                "message": f"User profile cluster analysis completed, discovered {optimal_k} user groups",
                "cluster_count": optimal_k,
                "data_points": len(df_clean),
                "cluster_profiles": cluster_profiles,
                "result_files": {
                    "profiles_csv": profile_csv_path,
                    "clustered_data_csv": clustered_data_path,  # Add path to data with cluster labels
                    "optimal_k_plot": image_paths["optimal_k_plot"],
                    "clusters_plot": clusters_image_path
                },
                "df_with_clusters": df_with_clusters  # Add dataframe with cluster labels
            }
            
            # Save the result summary
            summary_path = os.path.join(results_dir, "analysis_summary.json")
            
            # Create a serializable summary (remove DataFrame)
            json_summary = summary.copy()
            json_summary.pop("df_with_clusters", None)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(json_summary, f, ensure_ascii=False, indent=2)
            
            print(f"User profile cluster analysis completed! Results saved in: {results_dir}")
            return summary
            
        except Exception as e:
            error_message = f"User profile analysis error: {str(e)}"
            print(error_message)
            return {
                "status": "error",
                "message": error_message
            }
    
    @staticmethod
    def _load_data(file_path: str) -> pd.DataFrame:
        """Load data file"""
        print(f"Reading file: {file_path}")
        
        try:
            # Try to determine format based on file extension
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
                print("Successfully read Excel file")
            elif ext.lower() == '.csv':
                # Try different encodings and separators
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file_path, encoding='gbk')
                    except:
                        df = pd.read_csv(file_path, encoding='latin1')
                print("Successfully read CSV file")
            else:
                raise ValueError(f"Unsupported file format: {ext}")
                
            # Basic data description
            print(f"Data shape: {df.shape}")
            print(f"Contains {df.shape[0]} rows and {df.shape[1]} columns")
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    @staticmethod
    def _preprocess_data(df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame, List[str], List[str]]:
        """Preprocess data"""
        print("\nData preprocessing...")
        
        # Handle missing values
        # Remove columns and rows with too many missing values
        threshold_cols = len(df) * 0.5  # Delete columns with more than 50% missing values
        threshold_rows = len(df.columns) * 0.5  # Delete rows with more than 50% missing values
        
        df_clean = df.dropna(thresh=threshold_rows, axis=0)  # Remove rows with too many missing values
        df_clean = df_clean.dropna(thresh=threshold_cols, axis=1)  # Remove columns with too many missing values
        
        print(f"Clean data shape: {df_clean.shape}")
        
        # Identify numeric and categorical features
        numeric_features = df_clean.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"Numeric features: {len(numeric_features)}")
        print(f"Categorical features: {len(categorical_features)}")
        
        try:
            # Create preprocessing pipeline
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features),
                    ('cat', categorical_transformer, categorical_features)
                ])
            
            # Apply preprocessing
            X = preprocessor.fit_transform(df_clean)
            print(f"Preprocessed feature matrix shape: {X.shape}")
            
        except Exception as e:
            print(f"Complex preprocessing error: {str(e)}")
            print("Attempting simplified preprocessing...")
            
            # Alternative simplified processing: use only numeric features
            if not numeric_features:
                raise Exception("No numeric features available in the data, cannot perform clustering analysis")
                
            X = df_clean[numeric_features].fillna(df_clean[numeric_features].median())
            X = StandardScaler().fit_transform(X)
            print(f"Simplified preprocessed feature matrix shape: {X.shape}")
            
            # Empty categorical features list if no categories after simplification 
            if categorical_features and len(X.shape) < 2:
                categorical_features = []
        
        return X, df_clean, numeric_features, categorical_features
    
    @staticmethod
    def _determine_optimal_k(X: np.ndarray, max_k: int, results_dir: str) -> Tuple[int, Dict[str, str]]:
        """Determine optimal number of clusters"""
        print("\nDetermining optimal number of clusters...")
        
        # Ensure reasonable maximum cluster count
        n_samples = X.shape[0]
        max_k = min(max_k, n_samples // 5, 20)  # Not more than 1/5 of samples and not more than 20
        max_k = max(max_k, 2)  # At least 2
        
        # Calculate SSE (Sum of Squared Errors) for different k values
        sse = []
        silhouette_scores = []
        k_values = range(2, max_k + 1)
        
        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            sse.append(kmeans.inertia_)
            
            # Calculate silhouette score (only if enough samples)
            if n_samples > k * 10:  # Ensure enough samples per cluster
                try:
                    silhouette_scores.append(silhouette_score(X, kmeans.labels_))
                except Exception:
                    silhouette_scores.append(0)
        
        # Use elbow method to determine optimal k
        if len(sse) > 2:
            diffs = np.diff(sse)
            diffs_r = diffs / sse[:-1]  # Relative change rate
            
            # Find elbow point
            elbow_found = False
            for i in range(len(diffs_r) - 1):
                if diffs_r[i] > 0.1 and diffs_r[i+1] < 0.05:
                    elbow_k = k_values[i+1]
                    elbow_found = True
                    break
            
            if not elbow_found:
                # Use second derivative
                diffs_of_diffs = np.diff(diffs)
                k_idx = np.argmin(diffs_of_diffs)
                elbow_k = k_values[k_idx + 1]
        else:
            # Use default if too few clusters
            elbow_k = 3
        
        # Use silhouette score to determine optimal k
        silhouette_k = k_values[np.argmax(silhouette_scores)] if silhouette_scores else elbow_k
        
        # Return combined optimal k
        optimal_k = round((elbow_k + silhouette_k) / 2)
        
        # Visualization
        plt.figure(figsize=(12, 5))
        
        # SSE curve
        plt.subplot(1, 2, 1)
        plt.plot(k_values, sse, 'bo-')
        plt.plot(elbow_k, sse[elbow_k-2], 'ro', markersize=10)
        plt.title(f'Elbow Method (Best K = {elbow_k})')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('SSE')
        plt.grid(True)
        
        # Silhouette score curve
        if silhouette_scores:
            plt.subplot(1, 2, 2)
            plt.plot(k_values, silhouette_scores, 'bo-')
            plt.plot(silhouette_k, silhouette_scores[silhouette_k-2], 'ro', markersize=10)
            plt.title(f'Silhouette Score (Best K = {silhouette_k})')
            plt.xlabel('Number of Clusters (k)')
            plt.ylabel('Silhouette Score')
            plt.grid(True)
        
        plt.tight_layout()
        
        # Save plot
        optimal_k_plot = os.path.join(results_dir, "optimal_k_plot.png")
        plt.savefig(optimal_k_plot)
        plt.close()
        
        print(f"Optimal number of clusters: {optimal_k}")
        
        return optimal_k, {"optimal_k_plot": optimal_k_plot}
    
    @staticmethod
    def _perform_clustering(X: np.ndarray, optimal_k: int, df_clean: pd.DataFrame, 
                          results_dir: str) -> Tuple[pd.DataFrame, str]:
        """Perform clustering and visualization"""
        print(f"\nPerforming K-means clustering (k = {optimal_k})...")
        
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X)
        
        # Add cluster labels to original data
        df_clean = df_clean.copy()
        df_clean['cluster'] = cluster_labels
        
        # Use PCA for visualization
        clusters_image_path = os.path.join(results_dir, "clusters_pca_plot.png")
        
        if X.shape[1] > 2:
            # Use PCA for dimensionality reduction
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X)
            
            # Visualize clustering results
            plt.figure(figsize=(10, 8))
            
            # Define colors for different clusters
            colors = plt.cm.tab10(np.linspace(0, 1, optimal_k))
            
            for cluster in range(optimal_k):
                plt.scatter(
                    X_pca[cluster_labels == cluster, 0],
                    X_pca[cluster_labels == cluster, 1],
                    s=50, color=colors[cluster],
                    label=f'Cluster {cluster}',
                    alpha=0.7
                )
            
            plt.title('User Profile Clustering Results (PCA Visualization)')
            plt.xlabel('Principal Component 1')
            plt.ylabel('Principal Component 2')
            plt.legend()
            plt.grid(True)
            
            # Save plot
            plt.savefig(clusters_image_path)
            plt.close()
        else:
            # Direct plotting for 2D or lower dimensions
            plt.figure(figsize=(10, 8))
            
            if X.shape[1] == 2:
                for cluster in range(optimal_k):
                    plt.scatter(
                        X[cluster_labels == cluster, 0],
                        X[cluster_labels == cluster, 1],
                        label=f'Cluster {cluster}',
                        alpha=0.7
                    )
            else:
                # 1D data
                for cluster in range(optimal_k):
                    plt.scatter(
                        X[cluster_labels == cluster],
                        np.zeros(np.sum(cluster_labels == cluster)),
                        label=f'Cluster {cluster}',
                        alpha=0.7
                    )
                    
            plt.title('User Profile Clustering Results')
            plt.legend()
            plt.grid(True)
            
            # Save image
            plt.savefig(clusters_image_path)
            plt.close()
        
        return df_clean, clusters_image_path
    
    @staticmethod
    def _analyze_clusters(df_with_clusters: pd.DataFrame, 
                         numeric_features: List[str], 
                         categorical_features: List[str],
                         results_dir: str) -> Tuple[List[Dict[str, Any]], str]:
        """Analyze clustering results and generate user profiles"""
        print("\nAnalyzing clustering results...")
        
        # Get cluster labels and counts
        clusters = df_with_clusters['cluster'].unique()
        cluster_sizes = df_with_clusters['cluster'].value_counts().to_dict()
        
        print(f"Total of {len(clusters)} clusters")
        for cluster, size in cluster_sizes.items():
            print(f"Cluster {cluster}: {size} users ({size/len(df_with_clusters):.1%})")
        
        # Analyze features for each cluster
        cluster_profiles = []
        
        for cluster in sorted(clusters):
            cluster_df = df_with_clusters[df_with_clusters['cluster'] == cluster]
            profile = {
                'ClusterID': int(cluster), 
                'UserCount': int(len(cluster_df)), 
                'Percentage': f"{len(cluster_df)/len(df_with_clusters):.1%}"
            }
            
            # Average of numeric features
            for feature in numeric_features:
                if feature in cluster_df.columns:  # Ensure feature exists
                    profile[feature] = float(cluster_df[feature].mean())
            
            # Most common value for categorical features
            for feature in categorical_features:
                if feature in cluster_df.columns:  # Ensure feature exists
                    top_value = cluster_df[feature].mode()[0] if not cluster_df[feature].mode().empty else "Unknown"
                    profile[f"{feature}_MostCommon"] = str(top_value)
                    profile[f"{feature}_Percentage"] = f"{cluster_df[feature].value_counts().get(top_value, 0)/len(cluster_df):.1%}"
            
            cluster_profiles.append(profile)
        
        # Generate label/name for each cluster
        for profile in cluster_profiles:
            # Generate label based on key features
            label_parts = []
            
            # Try to extract age group information
            age_features = [f for f in numeric_features if 'age' in f.lower()]
            if age_features and age_features[0] in profile:
                age = profile[age_features[0]]
                if age < 25:
                    label_parts.append("Young Users")
                elif age < 40:
                    label_parts.append("Middle-aged Users")
                else:
                    label_parts.append("Mature Users")
            
            # Try to extract gender information
            gender_features = [f for f in categorical_features if 'gender' in f.lower() or 'sex' in f.lower()]
            if gender_features and f"{gender_features[0]}_MostCommon" in profile:
                gender = profile[f"{gender_features[0]}_MostCommon"]
                if isinstance(gender, str):
                    gender_lower = gender.lower()
                    if 'female' in gender_lower or 'f' == gender_lower:
                        label_parts.append("Female")
                    elif 'male' in gender_lower or 'm' == gender_lower:
                        label_parts.append("Male")
            
            # Try to extract occupation information
            occupation_features = [f for f in categorical_features 
                                   if 'occupation' in f.lower() or 'job' in f.lower() 
                                   or 'profession' in f.lower()]
            if occupation_features and f"{occupation_features[0]}_MostCommon" in profile:
                occupation = profile[f"{occupation_features[0]}_MostCommon"]
                if isinstance(occupation, str) and occupation != "Unknown":
                    label_parts.append(f"{occupation}")
            
            # Combine label parts
            if label_parts:
                profile['ClusterLabel'] = " ".join(label_parts)
            else:
                profile['ClusterLabel'] = f"User Group {profile['ClusterID']}"
        
        # Print detailed cluster features
        print("\n=== User Profile Clustering Analysis Results ===")
        
        for profile in cluster_profiles:
            print(f"\nCluster {profile['ClusterID']}: {profile['ClusterLabel']}")
            print(f"  User Count: {profile['UserCount']} ({profile['Percentage']})")
            
            # Print key numeric features
            print("  Key Numeric Features:")
            for feature in numeric_features[:5]:  # Select first 5 numeric features
                if feature in profile:
                    print(f"    - {feature}: {profile[feature]:.2f}")
            
            # Print key categorical features
            print("  Key Categorical Features:")
            for feature in categorical_features[:5]:  # Select first 5 categorical features
                mode_key = f"{feature}_MostCommon"
                pct_key = f"{feature}_Percentage"
                if mode_key in profile and pct_key in profile:
                    print(f"    - {feature}: {profile[mode_key]} ({profile[pct_key]})")
        
        # Output to CSV file for further analysis
        profile_csv_path = os.path.join(results_dir, "user_cluster_profiles.csv")
        pd.DataFrame(cluster_profiles).to_csv(profile_csv_path, index=False)
        print(f"Clustering analysis results saved to: {profile_csv_path}")
        
        return cluster_profiles, profile_csv_path

    @staticmethod
    def analyze_complete_cluster_profiles(input_file: str, working_dir: str, cluster_file: str = None, show_all_features: bool = False) -> Dict[str, Any]:
        """
        Analyze complete cluster user profiles, showing all feature distributions for each cluster
        
        Args:
            input_file: Original data file path (with cluster column)
            working_dir: Working directory for saving result files
            cluster_file: Optional, path to clustering results CSV file
            show_all_features: Whether to display all feature details in terminal
            
        Returns:
            Dict[str, Any]: Dictionary containing analysis results
        """
        print(f"Analyzing complete feature information for clusters...")
        
        try:
            # Read original data (with cluster labels)
            try:
                # Determine reading method based on file extension
                _, ext = os.path.splitext(input_file)
                if ext.lower() in ['.xlsx', '.xls']:
                    df = pd.read_excel(input_file)
                elif ext.lower() == '.csv':
                    df = pd.read_csv(input_file)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
                    
                print(f"Successfully read data file: {input_file}")
                print(f"Data shape: {df.shape}")
                
                # Ensure there is a cluster column
                if 'cluster' not in df.columns:
                    raise ValueError("No cluster column in the data, please run clustering analysis first")
                    
            except Exception as e:
                error_message = f"Error reading file: {str(e)}"
                print(error_message)
                return {
                    "status": "error",
                    "message": error_message
                }
            
            # Read cluster results file (optional) 
            cluster_profiles = None
            if cluster_file and os.path.exists(cluster_file):
                try:
                    cluster_profiles = pd.read_csv(cluster_file)
                    print(f"Successfully read cluster results file: {cluster_file}")
                except Exception as e:
                    print(f"Error reading cluster results file: {str(e)}")
            
            # Get cluster labels and counts
            clusters = df['cluster'].unique()
            # Ensure clusters are not empty
            if len(clusters) == 0:
                raise ValueError("No valid cluster labels in the data")
            
            cluster_sizes = df['cluster'].value_counts().to_dict()
            
            print(f"\nTotal of {len(clusters)} clusters")
            for cluster, size in cluster_sizes.items():
                print(f"Cluster {cluster}: {size} users ({size/len(df):.1%})")
            
            # Create results directory
            results_dir = os.path.join(working_dir, "cluster_complete_profiles")
            os.makedirs(results_dir, exist_ok=True)
            
            # Identify numeric and categorical features
            numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Remove cluster column (if in numeric features)
            if 'cluster' in numeric_features:
                numeric_features.remove('cluster')
            
            # Remove cluster column (if in categorical features)  
            if 'cluster' in categorical_features:
                categorical_features.remove('cluster')
            
            print(f"\nNumeric features: {len(numeric_features)}")
            print(f"Categorical features: {len(categorical_features)}")
            
            # Create HTML report and feature structure
            html_parts = []
            html_parts.append(f"""
            <html>
            <head>
                <title>Detailed Cluster Profile Analysis</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2, h3 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    .cluster-section {{ margin-bottom: 40px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
                    .feature-chart {{ width: 100%; max-width: 800px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>Detailed Cluster Profile Analysis</h1>
                <p>Total of {len(clusters)} clusters, total data points: {len(df)}</p>
            """)
            
            # Create Markdown content
            md_parts = []
            md_parts.append(f"# Detailed Cluster Profile Analysis\n\n")
            md_parts.append(f"Total of **{len(clusters)}** clusters, total data points: **{len(df)}**\n\n")
            # Save feature information for all clusters for output
            all_cluster_features = []
            
            # Limit output volume to avoid excessive console output
            print(f"\nStarting analysis of {len(clusters)} clusters, please wait...")
            
            # Analyze each cluster in detail
            for cluster in sorted(clusters):
                cluster_df = df[df['cluster'] == cluster]
                
                # Check if this cluster has any data
                if len(cluster_df) == 0:
                    print(f"Warning: Cluster {cluster} has no data, skipping")
                    continue
                    
                cluster_size = len(cluster_df)
                cluster_pct = cluster_size/len(df)
                
                # Get cluster label (if there's a cluster result file)
                cluster_label = f"User Group {cluster}"
                if cluster_profiles is not None:
                    try:
                        label_row = cluster_profiles[cluster_profiles['ClusterID'] == cluster]
                        if not label_row.empty and 'ClusterLabel' in label_row.columns:
                            cluster_label = label_row['ClusterLabel'].values[0]
                    except Exception as e:
                        print(f"Error getting cluster label: {str(e)}")
                
                # Create feature information dictionary for current cluster
                cluster_features = {
                    "ClusterID": cluster,
                    "ClusterLabel": cluster_label,
                    "UserCount": cluster_size,
                    "Percentage": f"{cluster_pct:.1%}",
                    "CategoricalFeatures": {},
                    "NumericFeatures": {}
                }
                
                if show_all_features:
                    print(f"\nProcessing Cluster {cluster}: {cluster_label} ({cluster_size} users, {cluster_pct:.1%})")
                
                html_parts.append(f"""
                <div class="cluster-section">
                    <h2>Cluster {cluster}: {cluster_label}</h2>
                    <p>User count: {cluster_size} ({cluster_pct:.1%})</p>
                """)
                
                # Markdown: Add cluster title
                md_parts.append(f"## Cluster {cluster}: {cluster_label}\n\n")
                md_parts.append(f"User count: **{cluster_size}** ({cluster_pct:.1%})\n\n")
                
                # === Analyze categorical features ===
                html_parts.append("<h3>Categorical Feature Distribution</h3>")
                
                # Markdown: Add categorical feature title
                md_parts.append(f"### Categorical Feature Distribution\n\n")
                
                # Create table header
                html_parts.append("""
                <table>
                    <tr>
                        <th>Feature</th>
                        <th>Most Common Value</th>
                        <th>Percentage</th>
                        <th>Value Distribution</th>
                    </tr>
                """)
                
                # Markdown table header
                md_parts.append("| Feature | Most Common Value | Percentage | Value Distribution |\n")
                md_parts.append("|---------|------------------|------------|--------------------|\n")
                
                # Reduce output volume, especially when show_all_features=false
                if show_all_features:
                    print("  Processing categorical features...")
                
                for feature in categorical_features:
                    if feature in cluster_df.columns:
                        try:
                            # Calculate feature distribution in this cluster
                            value_counts = cluster_df[feature].value_counts()
                            value_pcts = cluster_df[feature].value_counts(normalize=True)
                            
                            # Check if there are values
                            if value_counts.empty:
                                # Skip this feature if no values
                                continue
                                
                            # Most common value
                            top_value = value_counts.index[0] if not value_counts.empty else "Unknown"
                            top_pct = value_pcts.iloc[0] if not value_pcts.empty else 0
                            
                            # Show only top 5 values
                            top_values = []
                            for i, (val, pct) in enumerate(zip(value_counts.index[:5], value_pcts.iloc[:5])):
                                if pd.notna(val) and val != "":
                                    top_values.append(f"{val} ({pct:.1%})")
                            
                            value_dist = ", ".join(top_values)
                            
                            # Print only if show_all_features is true and is important feature
                            if show_all_features and feature in ['Operating System', 'Browser', 'Main Usage Scenario', 'Gender', 'Occupation', 'Education Level']:
                                print(f"    - {feature}: {top_value} ({top_pct:.1%})")
                            
                            # Save to feature information dictionary
                            cluster_features["CategoricalFeatures"][feature] = {
                                "MostCommonValue": top_value,
                                "Percentage": f"{top_pct:.1%}",
                                "Distribution": value_dist
                            }
                            
                            html_parts.append(f"""
                            <tr>
                                <td>{feature}</td>
                                <td>{top_value}</td>
                                <td>{top_pct:.1%}</td>
                                <td>{value_dist}</td>
                            </tr>
                            """)
                            
                            # Markdown: Add table row
                            # Handle fields that may contain | character to avoid breaking Markdown table
                            safe_feature = str(feature).replace('|', '&#124;')
                            safe_top_value = str(top_value).replace('|', '&#124;')
                            safe_value_dist = str(value_dist).replace('|', '&#124;')
                            
                            md_parts.append(f"| {safe_feature} | {safe_top_value} | {top_pct:.1%} | {safe_value_dist} |\n")
                            
                            # Generate distribution plot
                            try:
                                plt.figure(figsize=(10, 6))
                                
                                # Keep only top 10 categories, group others as "Others"
                                if len(value_counts) > 10:
                                    top_n = value_counts.iloc[:10]
                                    others_sum = value_counts.iloc[10:].sum()
                                    if others_sum > 0:
                                        top_n = pd.concat([top_n, pd.Series({'Others': others_sum})])
                                    value_counts_plot = top_n
                                else:
                                    value_counts_plot = value_counts
                                
                                # Plot
                                if not value_counts_plot.empty:
                                    ax = value_counts_plot.plot(kind='bar')
                                    plt.title(f'Cluster {cluster} - {feature} Distribution')
                                    plt.ylabel('Frequency')
                                    plt.xlabel(feature)
                                    plt.xticks(rotation=45, ha='right')
                                    plt.tight_layout()
                                    
                                    # Save image
                                    fig_filename = f"{results_dir}/cluster_{cluster}_{feature}_dist.png"
                                    plt.savefig(fig_filename)
                                    
                                    # Markdown add image reference
                                    img_path = os.path.basename(fig_filename)
                                    md_parts.append(f"\n![Cluster {cluster} - {feature} Distribution]({img_path})\n\n")
                                    
                                    plt.close()
                            except Exception as e:
                                if show_all_features:
                                    print(f"    Error generating distribution plot ({feature}): {str(e)}")
                                plt.close()
                        except Exception as e:
                            if show_all_features:
                                print(f"    Error processing categorical feature ({feature}): {str(e)}")
                
                html_parts.append("</table>")
                md_parts.append("\n")
                
                # === Analyze numeric features ===
                if numeric_features:
                    html_parts.append("<h3>Numeric Feature Statistics</h3>")
                    
                    # Markdown: Add numeric feature title
                    md_parts.append(f"### Numeric Feature Statistics\n\n")
                    
                    # Create table header
                    html_parts.append("""
                    <table>
                        <tr>
                            <th>Feature</th>
                            <th>Mean</th>
                            <th>Median</th>
                            <th>Std Dev</th>
                            <th>Min</th>
                            <th>Max</th>
                        </tr>
                    """)
                    
                    # Markdown table header
                    md_parts.append("| Feature | Mean | Median | Std Dev | Min | Max |\n")
                    md_parts.append("|---------|------|--------|---------|-----|-----|\n")
                    
                    if show_all_features:
                        print("  Processing numeric features...")
                    
                    for feature in numeric_features:
                        if feature in cluster_df.columns:
                            try:
                                # Exclude empty values
                                feat_data = cluster_df[feature].dropna()
                                
                                if not feat_data.empty:
                                    # Basic statistics
                                    feat_mean = feat_data.mean()
                                    feat_median = feat_data.median()
                                    feat_std = feat_data.std()
                                    feat_min = feat_data.min()
                                    feat_max = feat_data.max()
                                    
                                    # Print only if show_all_features is true and is important feature
                                    if show_all_features and feature in ['Age', 'Monthly Income', 'Daily Internet Usage']:
                                        print(f"    - {feature}: Mean={feat_mean:.2f}, Median={feat_median:.2f}")
                                    
                                    # Save to feature information dictionary
                                    cluster_features["NumericFeatures"][feature] = {
                                        "Mean": f"{feat_mean:.2f}",
                                        "Median": f"{feat_median:.2f}",
                                        "StdDev": f"{feat_std:.2f}",
                                        "Min": f"{feat_min:.2f}",
                                        "Max": f"{feat_max:.2f}"
                                    }
                                    
                                    html_parts.append(f"""
                                    <tr>
                                        <td>{feature}</td>
                                        <td>{feat_mean:.2f}</td>
                                        <td>{feat_median:.2f}</td>
                                        <td>{feat_std:.2f}</td>
                                        <td>{feat_min:.2f}</td>
                                        <td>{feat_max:.2f}</td>
                                    </tr>
                                    """)
                                    
                                    # Markdown: Add table row
                                    safe_feature = str(feature).replace('|', '&#124;')
                                    md_parts.append(f"| {safe_feature} | {feat_mean:.2f} | {feat_median:.2f} | {feat_std:.2f} | {feat_min:.2f} | {feat_max:.2f} |\n")
                                    
                                    # Generate distribution plot
                                    try:
                                        plt.figure(figsize=(10, 6))
                                        
                                        # Histogram
                                        sns.histplot(feat_data, kde=True)
                                        plt.title(f'Cluster {cluster} - {feature} Distribution')
                                        plt.xlabel(feature)
                                        plt.ylabel('Frequency')
                                        plt.tight_layout()
                                        
                                        # Save image
                                        fig_filename = f"{results_dir}/cluster_{cluster}_{feature}_dist.png"
                                        plt.savefig(fig_filename)
                                        
                                        # Markdown add image reference
                                        img_path = os.path.basename(fig_filename)
                                        md_parts.append(f"\n![Cluster {cluster} - {feature} Distribution]({img_path})\n\n")
                                        
                                        plt.close()
                                    except Exception as e:
                                        if show_all_features:
                                            print(f"    Error generating numeric distribution plot ({feature}): {str(e)}")
                                        plt.close()
                            except Exception as e:
                                if show_all_features:
                                    print(f"    Error processing numeric feature ({feature}): {str(e)}")
                    
                    html_parts.append("</table>")
                    md_parts.append("\n")
                
                html_parts.append("</div>")
                md_parts.append("\n---\n\n")  # Add separator line
                
                # Add current cluster info to overall list
                all_cluster_features.append(cluster_features)
                
                # Clear plot objects from memory to avoid memory leak
                plt.close('all')
            
            # Check if there are valid cluster results
            if not all_cluster_features:
                raise ValueError("No valid cluster results found")
            
            # Add overall summary information to the end of the Markdown file
            md_parts.append("\n## Cluster Summary\n\n")
            md_parts.append("| Cluster ID | Cluster Label | User Count | Percentage |\n")
            md_parts.append("|------------|--------------|------------|------------|\n")
            
            for cf in all_cluster_features:
                md_parts.append(f"| {cf['ClusterID']} | {cf['ClusterLabel']} | {cf['UserCount']} | {cf['Percentage']} |\n")
            
            # Complete HTML
            html_parts.append("</body></html>")
            
            # Save HTML report
            html_report = "".join(html_parts)
            html_report_path = os.path.join(results_dir, "cluster_complete_profiles.html")
            with open(html_report_path, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            # Save Markdown report
            md_content = "".join(md_parts)
            md_report_path = os.path.join(results_dir, "cluster_complete_profiles.md")
            with open(md_report_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            # Save all cluster features to JSON file
            json_output_file = os.path.join(results_dir, "all_cluster_features.json")
            with open(json_output_file, 'w') as f:
                json.dump(all_cluster_features, f, cls=NumpyEncoder, indent=4)
            
            print(f"\nAnalysis complete! HTML report, Markdown report, and JSON data have been saved")
            
            # Create results summary
            summary = {
                "status": "success",
                "message": f"Complete cluster feature analysis finished, analyzed {len(clusters)} clusters",
                "cluster_count": len(clusters),
                "data_points": len(df),
                "result_files": {
                    "html_report": html_report_path,
                    "markdown_report": md_report_path,
                    "json_data": json_output_file
                }
            }
            
            # Force close all plots to ensure resource cleanup
            plt.close('all')
            # Force cleanup of potentially unreferenced objects in memory
            import gc
            gc.collect()
            
            return summary
            
        except Exception as e:
            # Ensure all plot objects are closed even on error
            plt.close('all')
            
            error_message = f"Cluster analysis error: {str(e)}"
            print(error_message)
            import traceback
            traceback.print_exc()  # Print full stack trace for debugging
            
            # Force cleanup of potentially unreferenced objects in memory
            import gc
            gc.collect()
            
            return {
                "status": "error",
                "message": error_message
            }


# Entry point when running as standalone script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python profile_analysis.py <data_file_path> [max_clusters]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    max_clusters = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Create working directory
    working_dir = os.getcwd()
    
    # Execute analysis
    results = ProfileAnalyzer.analyze_user_profiles(file_path, working_dir, max_clusters)
    
    # Print results summary
    if results["status"] == "success":
        print(f"\nAnalysis complete: {results['message']}")
        print(f"Result files saved in: {working_dir}/profile_analysis_results/")
    else:
        print(f"\nAnalysis failed: {results['message']}") 