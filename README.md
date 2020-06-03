# Automated_skew_reduce
Function which reduces skew of pandas data frame automatically.
Having looked at Kaggle workbooks, and observed people's somewhat arbitrary application of transforms for reducing skew. I throught it would be easily automated. I am open to comments on the statistical pitfalls of this blind approach (in fact any strong insights are welcome), or edits etc.

See walkthrough https://cormaccollins.github.io/Automated_skew_reduce/automated_skew_reduce.html

Example import/usage:

```python
from scipy import stats
import numpy as np
import pandas as pd
from skew_reduce import minimize_skew_with_transform


train = pd.read_csv("train.csv")
skew1 = train.skew()
df, diff_list = minimize_skew_with_transform(train.copy(), np, pd, stats, SKEW_CUT_OFF=[-1, 1])
skew2 = df.skew()

print('Diff in skew post minimization:')
print(np.mean(skew1))
print(np.mean(skew2))

```

Note the runtime error as I didn't do anything about NaN values,
Output:
```
RuntimeWarning: invalid value encountered in less_equal
  if any(x <= 0):
Log transformed: LotFrontage
Log transformed: LotArea
Sqrt transformed: MasVnrArea
Sqrt transformed: BsmtFinSF1
Sqrt transformed: BsmtFinSF2
Sqrt transformed: TotalBsmtSF
Boxcox transformed: 1stFlrSF
Sqrt transformed: LowQualFinSF
Log transformed: GrLivArea
Sqrt transformed: BsmtHalfBath
Sqrt transformed: KitchenAbvGr
Sqrt transformed: WoodDeckSF
Sqrt transformed: OpenPorchSF
Sqrt transformed: EnclosedPorch
Sqrt transformed: 3SsnPorch
Sqrt transformed: ScreenPorch
Sqrt transformed: PoolArea
Sqrt transformed: MiscVal
Boxcox transformed: SalePrice
Skew minimization complete
Diff in skew post minimization:
2.966802901764881
2.5287513660787697
```



