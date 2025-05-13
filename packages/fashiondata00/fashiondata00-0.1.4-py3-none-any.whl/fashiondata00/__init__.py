
import pandas as pd

def all(df, target_col=None, agg='sum', logic='and', **conditions):
    if logic == 'and':
        cond = pd.Series([True] * len(df))
        for col, val in conditions.items():
            cond &= df[col] == val
    elif logic == 'or':
        cond = pd.Series([False] * len(df))
        for col, val in conditions.items():
            cond |= df[col] == val
    else:
        raise ValueError("logic must be 'and' or 'or'")

    filtered = df[cond]

    if target_col is None:
        return len(filtered)

    values = filtered[target_col]

    if agg == 'sum':
        return values.sum()
    elif agg == 'mean':
        return values.mean()
    elif agg == 'count':
        return values.count()
    elif agg == 'min':
        return values.min()
    elif agg == 'max':
        return values.max()
    elif agg == 'groupcount':
        return values.value_counts().to_dict()
    else:
        raise ValueError(f"Unsupported aggregation: {agg}")

__all__ = ['all']