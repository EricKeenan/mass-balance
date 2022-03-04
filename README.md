# mass-balance
### Local Antarctic Mass Balance Constrained by Repeat Altimetry and Ensemble-Based Firn Modeling
##### Worflow is currently as folows:
1. Run `SNOWPACK` and `n` "training sites". These sites are used for training the 91 day change in firn air content (FAC) model. Current implementation found in `mass-balance/100_sites`. 
2. Gather training data from `SNOWPACK` input and output: `mass-balance/notebooks/multi-site-build-training-set.ipynb`
3. Train and save machine learning-based 91 day change in FAC model: `mass-balance/notebooks/FAC-emulator.ipynb`
4. Understand the relative importance of the different model features: `mass-balance/notebooks/explainability.ipynb`
5. Reduce MERRA-2 data to daily means so that feature collection runs faster: `mass-balance/notebooks/M2-daily-means.ipynb`
6. Gather data needed to run inference: `mass-balance/notebooks/gather-inference-inputs.ipynb`
7. Perform inference: `mass-balance/notebooks/inference.ipynb`
8. Get coordinates needed for steps 6-7 (sorry... this is out of order) and visualize ICESat-2 change in surface height against modeled 91 day change in FAC: `mass-balance/notebooks/get-IC2-coords.ipynb`
