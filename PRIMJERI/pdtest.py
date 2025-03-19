import numpy as np
import pandas as pd
s = 'aab'
ds = pd.Series(list(s))
dsu = ds.unique().astype(list)
su = "".join(dsu)

dsh = pd.pivot_table(pd.DataFrame(s,columns='v'),values='v',aggfunc='sum')
print(dsh)