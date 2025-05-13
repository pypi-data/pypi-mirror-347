import abc
from neurostats_API.utils import StatsProcessor, YoY_Calculator
import pandas as pd

class BaseTransformer(abc.ABC):
    """
    Transformer用途: 轉換資料為fetcher可使用的格式
    """
    def __init__(self, ticker, company_name, zone):
        self.ticker = ticker
        self.company_name = company_name

        self.zone = zone
        self.return_keys = []


    @abc.abstractmethod
    def process_transform(self):
        pass

    @classmethod
    def flatten_dict(cls, value_dict, target_keys):
        indexes = value_dict.keys()
        new_dict = {}


        for key in indexes:
            new_dict.update(
                {
                    f"{key}_{sub_key}": value_dict[key].get(sub_key, None) 
                    for sub_key in target_keys
                }
            )
        return new_dict
    
    @staticmethod
    def _process_unit(data_df, postfix):

        lambda_map = {
            "_value":  lambda x: StatsProcessor.cal_non_percentage(x, postfix="千元"),
            "_percentage": lambda x : StatsProcessor.cal_non_percentage(x, to_str=True, postfix="%"),
            '_growth': lambda x : StatsProcessor.cal_non_percentage(x, to_str=True, postfix="%"),
            "_YoY_1": StatsProcessor.cal_percentage,
            "_YoY_3": StatsProcessor.cal_percentage,
            "_YoY_5": StatsProcessor.cal_percentage,
            "_YoY_10": StatsProcessor.cal_percentage
        }

        process_fn = lambda_map.get(postfix)
        postfix_cols = data_df.columns.str.endswith(postfix)
        postfix_cols = data_df.loc[:, postfix_cols].columns

        if (postfix == "_value"):
            postfix_cols = [col for col in postfix_cols if not ("eps" in col or "每股盈餘" in col)]
        
        if (postfix == '_growth'):
            data_df[postfix_cols] =data_df[postfix_cols].map(
               lambda x: x * 100.0 if isinstance(x, float) else x
            )

        data_df[postfix_cols] = (
            data_df[postfix_cols].map(
               process_fn
            )
        )

        return data_df

    def _apply_process_unit_pipeline(self, data_df, postfix_list = ["_value", "percentage"]):
        for postfix in postfix_list:
            data_df = self._process_unit(data_df, postfix)
        return data_df

    @staticmethod
    def _slice_target_season(stats_df, target_season):
        target_season_columns = stats_df.columns.str.endswith(f"Q{target_season}")
        stats_df = stats_df.loc[:, target_season_columns]

        return stats_df
    
    def _get_empty_structure(self):
        return_dict = {
            "warning": "No data fetched",
            "ticker": self.ticker,
            "company_name": self.company_name
        }

        return_dict.update(
            {
                key: pd.DataFrame(columns= pd.Index([], name = 'date')) for key in self.return_keys
            }
        )
        return return_dict
    
    def _process_value(self, value):
        if isinstance(value, str) and "%" in value:
            value = value.replace("%", "")
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _calculate_growth(self, this_value, last_value, delta):
        try:
            return YoY_Calculator.cal_growth(
                this_value, last_value, delta
            ) * 100
        except Exception:
            return None
    
