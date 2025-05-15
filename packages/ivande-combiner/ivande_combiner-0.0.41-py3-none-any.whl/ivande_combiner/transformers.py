import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, RobustScaler, StandardScaler

from .utils import check_fill, check_key_tuple_empty_intersection, check_transform


class CalendarExtractor(BaseEstimator, TransformerMixin):
    """
    extract number data from date column and them to the pandas dataframe

    :param calendar_level: from 0 to 7,
        0 - no data
        1 - only year,
        2 - year and month,
        3 - year, month, day,
        4 - year, month, day, dayofweek,
        5 - year, month, day, dayofweek, dayofyear,
        6 - year, month, day, dayofweek, dayofyear, weekofyear
        7 - year, month, day, dayofweek, dayofyear, weekofyear, hour
    """
    def __init__(self, calendar_level: int = None):
        self.date_cols = None
        self.calendar_level = calendar_level

    def fit(self, X, y=None):
        check_fill(X)
        self.date_cols = [col for col in X.columns if pd.api.types.is_datetime64_any_dtype(X[col])]
        return self

    @staticmethod
    def _generate_feature(X, col, feature):
        if feature == "year":
            s = X[col].dt.year
            s.name = col + "_" + "year"
        elif feature == "month":
            s = X[col].dt.month
            s.name = col + "_" + "month"
        elif feature == "day":
            s = X[col].dt.day
            s.name = col + "_" + "day"
        elif feature == "dayofweek":
            s = X[col].dt.dayofweek
            s.name = col + "_" + "dayofweek"
        elif feature == "dayofyear":
            s = X[col].dt.dayofyear
            s.name = col + "_" + "dayofyear"
        elif feature == "weekofyear":
            s = X[col].dt.isocalendar().week
            s.name = col + "_" + "weekofyear"
        elif feature == "hour":
            s = X[col].dt.hour
            s.name = col + "_" + "hour"
        else:
            raise ValueError(f"unknown parameter {feature} in what_to_generate")

        return s

    def transform(self, X):
        check_transform(X, fitted_item=self.date_cols, transformer_name=self.__class__.__name__)

        X_ = X.copy()
        cols_to_add = []

        what_to_generate = ["year", "month", "day", "dayofweek", "dayofyear", "weekofyear", "hour"]
        if self.calendar_level is not None:
            what_to_generate = what_to_generate[: self.calendar_level]

        for dc in self.date_cols:
            cols_to_add.extend([self._generate_feature(X_, dc, feature) for feature in what_to_generate])

        X_.drop(self.date_cols, axis=1, inplace=True)
        X_ = pd.concat([X_, *cols_to_add], axis=1)

        return X_


class NoInfoColsRemover(BaseEstimator, TransformerMixin):
    """
    remove columns with the same values along all rows

    :param cols_to_except: list of columns that should not be removed
    :param verbose: True if you want to see the list of removed columns
    """
    def __init__(self, cols_to_except: list[str] = None, verbose=False):
        self._cols_to_remove = None
        self.cols_to_except = cols_to_except if cols_to_except is not None else []
        self.verbose = verbose

    def fit(self, X, y=None):
        check_fill(X)
        self._cols_to_remove = []

        for col in X.columns:
            if X[col].nunique() <= 1 and col not in self.cols_to_except:
                self._cols_to_remove.append(col)

        if self.verbose and self._cols_to_remove:
            print(f"columns {self._cols_to_remove} have no info and will be removed")

        return self

    def transform(self, X):
        check_transform(X, fitted_item=self._cols_to_remove, transformer_name=self.__class__.__name__)
        X_ = X.drop(self._cols_to_remove, axis=1)
        return X_


class OutlierRemover(BaseEstimator, TransformerMixin):
    """
    remove outliers from the columns

    :param cols_to_transform: list of column names from which to remove outliers
    :param method:
    "iqr" - remove outliers by interquartile range
    "std" - remove outliers by standard deviation
    "quantile" - remove outliers by quantile 0.01 and 0.99
    "skip" - do not remove outliers
    """
    def __init__(self, cols_to_transform: list[str], method: str = "iqr"):
        if cols_to_transform is None:
            raise ValueError("cols_to_transform parameter is should be filled")
        self.cols_to_transform = cols_to_transform
        self.method = method
        self._col_thresholds = None

    def fit(self, X, y=None):
        check_fill(X)
        self.cols_to_transform = [col for col in self.cols_to_transform if col in X.columns]
        self._col_thresholds = {}

        for col in self.cols_to_transform:
            if self.method == "iqr":
                q1 = X[col].quantile(.25)
                q3 = X[col].quantile(.75)
                iqr = q3 - q1
                left_bound = q1 - 1.5 * iqr
                right_bound = q3 + 1.5 * iqr
            elif self.method == "std":
                mean = X[col].mean()
                std = X[col].std()
                left_bound = mean - 3 * std
                right_bound = mean + 3 * std
            elif self.method == "quantile":
                left_bound = X[col].quantile(.01)
                right_bound = X[col].quantile(.99)
            elif self.method == "skip":
                left_bound = X[col].min()
                right_bound = X[col].max()
            else:
                raise ValueError(f"unknown method {self.method} for outlier remover")

            s = X[col][(X[col] >= left_bound) & (X[col] <= right_bound)]
            self._col_thresholds[col] = (s.min(), s.max())

        return self

    def transform(self, X):
        check_transform(X, fitted_item=self._col_thresholds, transformer_name=self.__class__.__name__)
        X_ = X.copy()

        for col in self.cols_to_transform:
            X_[col] = X_[col].clip(*self._col_thresholds[col])

        return X_


class WithAnotherColumnImputer(BaseEstimator, TransformerMixin):
    """
    impute missing values in one column with values from another column

    :param cols_to_impute: dictionary with column names as keys and column names to impute from as values
    """
    def __init__(self, cols_to_impute: dict[str, str] = None):
        if cols_to_impute is None:
            raise ValueError("cols_to_impute parameter is should be filled")
        self.cols_to_impute = cols_to_impute

    def fit(self, X, y=None):
        check_fill(X)
        self.cols_to_impute = {col: self.cols_to_impute[col] for col in self.cols_to_impute if col in X.columns}
        return self

    def transform(self, X):
        check_transform(X, fitted_item=self.cols_to_impute, transformer_name=self.__class__.__name__)
        X_ = X.copy()

        for col in self.cols_to_impute:
            X_[col] = X_[col].fillna(X_[self.cols_to_impute[col]])

        return X_


class CatCaster(BaseEstimator, TransformerMixin):
    """
    cast columns to category type

    :param cols_to_cast: list of columns to cast to category type
    """
    def __init__(self, cols_to_cast: list[str]):
        self.cols_to_cast = cols_to_cast

    def fit(self, X, y=None):
        check_fill(X)
        self.cols_to_cast = [col for col in self.cols_to_cast if col in X.columns]
        return self

    def transform(self, X) -> pd.DataFrame:
        check_transform(X, is_check_fill=False)
        X_ = X.copy()
        X_[self.cols_to_cast] = X[self.cols_to_cast].astype("category")
        return X_


class ColsOrder(BaseEstimator, TransformerMixin):
    """
    order columns in the same order as in the cols_order list

    :param cols_order: list of columns in the order you want them to be
    """
    def __init__(self, cols_order: list[str]):
        self.cols_order = cols_order
        self._cols_order = None

    def fit(self, X, y=None):
        check_fill(X)
        self._cols_order = [col for col in self.cols_order if col in X.columns]
        self._cols_order += [col for col in X.columns if col not in self._cols_order]
        return self

    def transform(self, X):
        check_transform(X, fitted_item=self._cols_order, transformer_name=self.__class__.__name__)
        X_ = X[self._cols_order]
        return X_


class ScalerPicker(BaseEstimator, TransformerMixin):
    """
    scale columns with a scaler of your choice

    :param cols_to_scale: list of columns to scale
    :param scaler_type:
        "standard" - StandardScaler
        "minmax" - MinMaxScaler
    """
    def __init__(self, cols_to_scale: list[str] = None, scaler_type: str = "standard"):
        self.cols_to_scale = cols_to_scale
        self.scaler_type = scaler_type
        self._scaler = None

    def _get_scaler_class(self):
        if self.scaler_type == "standard":
            return StandardScaler
        elif self.scaler_type == "minmax":
            return MinMaxScaler
        elif self.scaler_type == "robust":
            return RobustScaler
        elif self.scaler_type == "power":
            return PowerTransformer
        elif self.scaler_type == "skip":
            return None
        else:
            raise ValueError(f"unknown scaler type {self.scaler_type} should be standard or minmax")

    def fit(self, X, y=None):
        check_fill(X)

        if self.cols_to_scale is None:
            self.cols_to_scale = list(X.columns)
        else:
            self.cols_to_scale = [col for col in self.cols_to_scale if col in X.columns]

        scaler = self._get_scaler_class()
        if scaler:
            self._scaler = scaler().set_output(transform="pandas").fit(X[self.cols_to_scale])
        else:
            self._scaler = "skip"
        return self

    def transform(self, X):
        check_transform(X, fitted_item=self._scaler, transformer_name=self.__class__.__name__)
        X_ = X.copy()

        if self._scaler == "skip":
            return X_

        X_[self.cols_to_scale] = self._scaler.transform(X_[self.cols_to_scale])
        X_[self.cols_to_scale] = X_[self.cols_to_scale].astype(float)

        return X_


class SimpleImputerPicker(BaseEstimator, TransformerMixin):
    """
    impute missing values with a SimpleImputer

    :param strategy: strategy for SimpleImputer.
        Possible values: "constant", "mean", "median", "most_frequent", "max", "skip"
    :param cols_to_impute: dictionary with tuple column names as keys and fill values as values
        (only for strategy="constant")
    """
    def __init__(self, strategy: str = "mean", cols_to_impute: dict[tuple[str, ...], int] | list[str] = None):
        if cols_to_impute is not None and isinstance(cols_to_impute, dict):
            check_key_tuple_empty_intersection(cols_to_impute)
        self.cols_to_impute = cols_to_impute
        self.strategy = strategy
        self._imputer = None

    def _cast_to_float(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.cols_to_impute is None:
            cols = X.columns
        elif isinstance(self.cols_to_impute, dict):
            cols = [col for cols in self.cols_to_impute for col in cols if col in X.columns]
        elif isinstance(self.cols_to_impute, list):
            cols = [col for col in self.cols_to_impute if col in X.columns]
        else:
            raise ValueError("cols_to_impute should be dict or list or None")

        X[cols] = X[cols].astype(float)

        return X

    def fit(self, X, y=None):
        check_fill(X)
        if X.isnull().all().any():
            nan_cols = X.columns[X.isnull().all()].tolist()
            raise ValueError(f"columns with all nans {nan_cols}")

        if self.cols_to_impute is None:
            self.cols_to_impute = list(X.columns)

        if self.strategy == "constant":
            self._imputer = {}
            for cols, fill_value in self.cols_to_impute.items():
                cols_to_impute = [col for col in cols if col in X.columns]
                if len(cols_to_impute) != 0:
                    self._imputer[tuple(cols_to_impute)] = (
                        SimpleImputer(strategy="constant", fill_value=fill_value, keep_empty_features=True)
                        .set_output(transform="pandas")
                        .fit(X[cols_to_impute])
                    )
        elif self.strategy in ("mean", "median", "most_frequent"):
            self.cols_to_impute = [col for col in self.cols_to_impute if col in X.columns]
            self._imputer = (
                SimpleImputer(strategy=self.strategy, keep_empty_features=True)
                .set_output(transform="pandas")
                .fit(X[self.cols_to_impute])
            )
        elif self.strategy == "max":
            cols_to_impute = [col for col in self.cols_to_impute if col in X.columns]
            self._imputer = {}

            for col in cols_to_impute:
                self._imputer[col] = (
                    SimpleImputer(strategy="constant", fill_value=X[col].max(), keep_empty_features=True)
                    .set_output(transform="pandas")
                    .fit(X[[col]])
                )

        elif self.strategy == "skip":
            self._imputer = "skip"

        else:
            raise ValueError(f"unknown strategy {self.strategy} should be constant, mean, median or most_frequent")

        return self

    def transform(self, X):
        check_transform(X, fitted_item=self._imputer, transformer_name=self.__class__.__name__)
        X_ = X.copy()

        if self.strategy == "constant":
            for cols, imputer in self._imputer.items():
                cols = list(cols)
                X_[cols] = imputer.transform(X_[cols])
        elif self.strategy == "max":
            for col, imputer in self._imputer.items():
                X_[col] = imputer.transform(X_[[col]])
        elif self.strategy == "skip":
            pass
        else:
            X_[self.cols_to_impute] = self._imputer.transform(X_[self.cols_to_impute])

        X_ = self._cast_to_float(X_)

        return X_


class GroupForwardFillTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, group_cols, order_col, value_cols=None, drop: bool = True):
        self.group_cols = group_cols
        self.order_col = order_col
        self.value_cols = value_cols
        self.drop = drop
        self.memorized_values = None
        self.memorized_dates = None

    def fit(self, X, y=None):
        check_fill(X)
        X = X.copy()

        if self.value_cols is None:
            self.value_cols = [col for col in X.columns if col not in self.group_cols + [self.order_col]]

        self.memorized_values = {}
        self.memorized_dates = {}

        for col in self.value_cols:
            self.memorized_values[col] = {}
            self.memorized_dates[col] = {}

            for key, group in X.groupby(self.group_cols):
                last_valid_index = group[col].last_valid_index()
                if last_valid_index is not None:
                    self.memorized_values[col][key] = group.loc[last_valid_index, col]
                    self.memorized_dates[col][key] = group.loc[last_valid_index, self.order_col]

        return self

    def transform(self, X):
        check_transform(X, fitted_item=self.memorized_values, transformer_name=self.__class__.__name__)
        X = X.copy()

        def apply_ffill(group):
            key = tuple(group.name) if hasattr(group, "name") else tuple(group[self.group_cols].iloc[0])

            for col in self.value_cols:
                if key in self.memorized_values[col]:
                    last_value = self.memorized_values[col][key]
                    last_date = self.memorized_dates[col][key]

                    group[col] = group[col].ffill()
                    group.loc[group[self.order_col] > last_date, col] = group[col].fillna(last_value)

            return group

        X = X.groupby(by=self.group_cols, as_index=False)[X.columns].apply(apply_ffill).reset_index(drop=True)

        return X.drop(columns=self.group_cols + [self.order_col]) if self.drop else X
