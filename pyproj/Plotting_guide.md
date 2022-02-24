# Matplotlib guide

Note: DUMP ALL RELEVANT CODE SNIPPETS AT THE END OF THIS FILE, ORGANIZE THEM LATER

## References

[Pyplot guide](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)
[Markers styles](https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers)
[Figure doc](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html)
[]()
[]()

## Scatterplot

```python
import matplotlib as mplt
from matplotlib import pyplot as plt
import seaborn

# Basic scatterplot
plt.scatter(x, y)
```

-------------------------------------------------------------------------------
## Code snippets dump
```python

# create twin axis and color it differently
ax_twin = ax[1].twinx()
ax_twin.tick_params(axis='y', colors='darkgreen')



```


