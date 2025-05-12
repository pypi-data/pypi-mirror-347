# fashiondata00

`fashiondata00` is a lightweight Python package that provides a single versatile function `all()`  
for Excel-style conditional aggregation in pandas, supporting AND / OR logic.

---

## 📦 Installation

```bash
pip install fashiondata00
```

---

## 🧠 Function: `all()`

```python
all(df, target_col=None, agg='sum', logic='and', **conditions)
```

### Parameters:

- `df`: pandas DataFrame
- `target_col`: column to aggregate (optional if using `count`)
- `agg`: aggregation type - `'sum'`, `'mean'`, `'count'`, `'min'`, `'max'`
- `logic`: `'and'` (default) or `'or'` for combining conditions
- `**conditions`: keyword arguments specifying conditions  
  (e.g., `Gender='F', City='Seoul'`)

---

## ✅ Examples

```python
from fashiondata00 import all
import pandas as pd

df = pd.DataFrame({
    'Gender': ['F', 'M', 'F', 'F'],
    'City': ['Seoul', 'Busan', 'Seoul', 'Busan'],
    'Score': [90, 70, 85, 95]
})

# AND condition: Female AND lives in Seoul → sum of scores
all(df, target_col='Score', agg='sum', logic='and', Gender='F', City='Seoul')
# Output: 175

# OR condition: Female OR lives in Seoul → average score
all(df, target_col='Score', agg='mean', logic='or', Gender='F', City='Seoul')
```

---

## 👤 Author

Made by [Kwon Ki Yong]
