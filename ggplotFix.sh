#!/bin/sh

pip uninstall ggplot
pip install git+git://github.com/yhat/ggpy.git@9d00182343eccca6486beabd256e8c89fb0c59e8 --no-cache


sed -e "s/fill_levels = self.data[[fillcol_raw, fillcol]].sort(fillcol_raw)[fillcol].unique()\
/fill_levels = self.data[[fillcol_raw, fillcol]].sort_values(by=fillcol_raw)[fillcol].unique()" /usr/local/lib/python3.5/dist-packages/ggplot/ggplot.py
