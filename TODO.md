# TODO List

Legend:
```
- [X] Task       = done
- [X] ~~Task~~   = won't fix / not needed anymore
```

## High priority:
- [X] Run fit with --fity0=non-obs on HoaxModel;
- [X] Run fit with --fity0=all on HoaxModel;
- [X] Run fit with --fity0=none on HoaxModel;
- [X] Compare results of fity0 alternatives and decide what is best option;
- [X] Investigate odeint instabilities on SegHoaxModel, DoubleSIR, SEIZ (fit synth data);
- [X] Run fit for all models (fity0 = all);
- [X] Compare MAPE/SMAPE/LOG ACC RATIO/RMSE for model selection;
- [X] Do not set S to zero in fity0 = none;
- [X] Re-run `test_fitting.py` on HoaxModel;
- [X] Run fit for all models (fity0 = non-obs);
- [X] Recompute errors;
- [X] Remove cumsum() call from curves.py;
- [X] Truncate trailing zeroes from data in curves.py;
- [X] Fix issues with `_resample` (see FIXME in `curves.py`);
- [X] Fix issue with `_align` and (see FIXME in `curves.py`);
- [X] Refresh data;
- [X] In SegHoaxModel, change inity0 to use gamma parameter instead of 0.5;
- [X] Run fit with --fity0=non-obs;
- [X] Run fit with --fity0=all;
- [X] Run fit with --fity0=none;
- [ ] Plot fit results: same model different fity0;
- [ ] Plot fit results: different models same fity0 (for non-obs, all, none);
- [X] ~~Re-run testing plots for SegHoaxModel for slides;~~
- [ ] Inspect fit results for possible integration errors; 
- [X] Extract fitted parameters;
- [X] Update presentation slides (new plots, fitted parameters);

## Normal priority: 
- [ ] Write script to sweep parameter space for systematic testing fit reconstruction;
- [X] Write k-means + PCA script for model-based clustering;
- [ ] Forecast y(t) (for t=12h,24h,48h,168h) with variable-size training set;
- [X] ~~Repeat fit on the full dataset;~~

## Low priority:
- [X] ~~Add option to cumulate observations and model before fitting with `least_squares`;~~
- [ ] Repeat fit on number of tweets instead of number of users;
- [ ] Fix issue with `ODEModel.summary` (see FIXME in `models/base.py`)
- [ ] Fix issue with root logger (see FIXME in `fit.py`);
- [X] Fix issue with `utils.logaccratio`
- [ ] Fix issue with missing data folder for package (see FIXME in `fit.py`).
- [ ] Move ode-fitting code under replication;
- [ ] Write Snakefile(s) for replication;
- [ ] Create minimal environment for replication;
- [X] ~~Test `scipy.integrate.solve_ivp` as replacement for `odeint`;~~
- [X] ~~Implement more models from literature (see in `models.__init__.py`);~~
- [ ] Write test cases for models.base.Variable, models.base.ODEModel;
- [ ] Write test cases for odeint based on `test_fitting.py` (fit synthetic data);
- [ ] Make test case based on `odecomp.py` (compare odeint with prob updating);
- [X] ~~Implement Jacobian using SymPy to speed up least squares fitting;~~
- [ ] Refactor `models.base.ODEModel` based on [scikit-learn API](https://scikit-learn.org/stable/developers/develop.html);
