import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder


class AutoClean:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)
        print(self.df)
        print(f"✅ Data loaded successfully!")

    def handle_missing_values(self):
        df = self.df.copy()
        
        missing_value_percent = (df.isnull().sum() / len(df) * 100).reset_index()
        missing_value_percent.columns = ["column", "missing_percent"]
        print("Missing Values (%):")
        print(missing_value_percent)
        to_drop = missing_value_percent[missing_value_percent["missing_percent"] > 50]["column"].tolist()
        df.drop(columns=to_drop, inplace=True)

        num_cols = df.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = df.select_dtypes(include="object").columns
        if len(num_cols) > 0:
            df[num_cols] = SimpleImputer(strategy="mean").fit_transform(df[num_cols])
        if len(cat_cols) > 0:
            df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])
        
        print("-"*40)
        print(f"Dropped columns: {to_drop}")
        print("-"*40)
        print(df.isnull().sum())
        print("✅ Missing value handling successful.")
        self.df = df
        return self

    def encode(self, encoding_type="label", ordinal_mapping=None, max_unique=10):
        df = self.df.copy()
        cat_cols = df.select_dtypes(include="object").columns

        if encoding_type == "label":
            for col in cat_cols:
                df[col] = LabelEncoder().fit_transform(df[col].astype(str))
            print("✅ Label encoding applied.")

        elif encoding_type == "onehot":
            df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
            print("✅ One-hot encoding applied.")

        elif encoding_type == "ordinal":
            if ordinal_mapping is None:
                ordinal_mapping = {
                    col: sorted(df[col].dropna().unique())
                    for col in cat_cols if df[col].nunique() <= max_unique
                }
                print("Auto ordinal mapping:")
                for col, order in ordinal_mapping.items():
                    print(f"   {col}: {order}")

            oe = OrdinalEncoder(categories=[ordinal_mapping[col] for col in ordinal_mapping])
            df[list(ordinal_mapping.keys())] = oe.fit_transform(df[list(ordinal_mapping.keys())].astype(str))
            print("✅ Ordinal encoding applied.")

        else:
            raise ValueError("❌ encoding_type must be 'label', 'onehot', or 'ordinal'")

        self.df = df
        return self

    def get_df(self):
        return self.df.copy()
