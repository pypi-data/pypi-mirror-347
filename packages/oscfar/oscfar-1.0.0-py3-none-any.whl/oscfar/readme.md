# `oscfar`

OSCFAR (Order Statistic Constant False Alarm Rate) is a radar signal processing technique used for target detection. It adaptively estimates the noise or clutter power in the vicinity of a potential target and sets a detection threshold accordingly, maintaining a constant false alarm rate regardless of the background noise characteristics.

## Getting Started

To get started with the OSCFAR implementation, you'll need to set up your environment. We recommend using Conda for managing dependencies.

### **1. Create a Conda Environment:**

```bash
conda create -n myenv python=3.9  # Or your preferred Python version above 3.9
conda activate myenv
```

### **2. Install OSCFAR Package:**

```bash
pip install oscfar
```

You may need to manually install some packages like `fitburst`. For `fitburst` follow installation instructions on [GitHub](https://github.com/CHIMEFRB/fitburst).

# **Documentation:**

## Table of Contents

- 🅼 [oscfar](#oscfar)
- 🅼 [oscfar\.cfar](#oscfar-cfar)
- 🅼 [oscfar\.filters](#oscfar-filters)
- 🅼 [oscfar\.gaussian_fit](#oscfar-gaussian_fit)
- 🅼 [oscfar\.setup](#oscfar-setup)
- 🅼 [oscfar\.utils](#oscfar-utils)

<a name="oscfar"></a>

## 🅼 oscfar

- **Functions:**
  - 🅵 [do_os_cfar](#oscfar-do_os_cfar)

### Functions

<a name="oscfar-do_os_cfar"></a>

### 🅵 oscfar\.do_os_cfar

```python
def do_os_cfar(data: np.array, guard_cells, train_cells, rank_k, threshold_factor, averaging, min_dist, min_snr, baseline):
```

<a name="oscfar-cfar"></a>

## 🅼 oscfar\.cfar

- **Functions:**
  - 🅵 [os_cfar_1d](#oscfar-cfar-os_cfar_1d)
  - 🅵 [variable_window_cfar](#oscfar-cfar-variable_window_cfar)
  - 🅵 [variable_window_os_cfar_indices](#oscfar-cfar-variable_window_os_cfar_indices)

### Functions

<a name="oscfar-cfar-os_cfar_1d"></a>

### 🅵 oscfar\.cfar\.os_cfar_1d

```python
def os_cfar_1d(data, guard_cells, train_cells, rank_k, threshold_factor):
```

Performs 1D Ordered Statistic Constant False Alarm Rate \(OS-CFAR\) detection\.

**Parameters:**

- **data** (`np.ndarray`): 1D array of input data \(must be in linear power,
  not dB\)\.
- **guard_cells** (`int`): Number of guard cells on EACH side of the CUT\.
- **train_cells** (`int`): Number of training cells on EACH side of the CUT\.
- **rank_k** (`int`): The rank \(1-based index\) of the sorted training cell
  values to use for noise estimation \(1 \<= rank_k \<= N\)\.
  N = 2 \* train_cells is the total number of training cells\.
  A common choice is around 0\.75 \* N\.
- **threshold_factor** (`float`): The scaling factor \(alpha\) to multiply the
  noise estimate by to get the threshold\.

**Returns:**

- `tuple`: A tuple containing:
- detected_peaks_indices \(np\.ndarray\): Indices where peaks were detected\.
- threshold \(np\.ndarray\): The calculated threshold for each cell\.
  \(Same size as input data, padded with NaNs
  at edges where CFAR wasn't computed\)\.
  <a name="oscfar-cfar-variable_window_cfar"></a>

### 🅵 oscfar\.cfar\.variable_window_cfar

```python
def variable_window_cfar(data, guard_cells, min_window, max_window, homogeneity_threshold):
```

A basic implementation of a Variable Window CFAR detector using a split-window approach\.

**Parameters:**

- **data** (`np.ndarray`): The input signal data \(1D\)\.
- **guard_cells** (`int`): The number of guard cells on each side of the CUT\.
- **min_window** (`int`): The minimum number of reference cells on each side\.
- **max_window** (`int`): The maximum number of reference cells on each side\.
- **homogeneity_threshold** (`float`): A threshold to determine if the reference
  windows are considered homogeneous\.

**Returns:**

- `np.ndarray`: A boolean array indicating detections \(True\) and non-detections \(False\)\.
  <a name="oscfar-cfar-variable_window_os_cfar_indices"></a>

### 🅵 oscfar\.cfar\.variable_window_os_cfar_indices

```python
def variable_window_os_cfar_indices(data, guard_cells, min_window, max_window, k_rank, homogeneity_threshold, threshold_factor):
```

A basic implementation of a Variable Window OS-CFAR detector returning detection indices\.

**Parameters:**

- **data** (`np.ndarray`): The input signal data \(1D\)\.
- **guard_cells** (`int`): The number of guard cells on each side of the CUT\.
- **min_window** (`int`): The minimum number of reference cells on each side\.
- **max_window** (`int`): The maximum number of reference cells on each side\.
- **k_rank** (`int`): The rank of the order statistic to use for noise estimation\.
- **homogeneity_threshold** (`float`): A threshold to determine if the reference
  windows are considered homogeneous\.
- **threshold_factor** (`float`): Factor multiplied by the noise estimate for the threshold\.

**Returns:**

- `np.ndarray`: An array of indices where detections occurred\.
  <a name="oscfar-filters"></a>

## 🅼 oscfar\.filters

- **Functions:**
  - 🅵 [remove_baseline_peaks](#oscfar-filters-remove_baseline_peaks)
  - 🅵 [median_filter](#oscfar-filters-median_filter)
  - 🅵 [lowpass_filter](#oscfar-filters-lowpass_filter)
  - 🅵 [highpass_filter](#oscfar-filters-highpass_filter)
  - 🅵 [group_close_peaks](#oscfar-filters-group_close_peaks)
  - 🅵 [find_representative_peaks](#oscfar-filters-find_representative_peaks)
  - 🅵 [verify_peaks_snr](#oscfar-filters-verify_peaks_snr)
  - 🅵 [enforce_min_distance](#oscfar-filters-enforce_min_distance)
  - 🅵 [filter_peaks_by_extent_1d](#oscfar-filters-filter_peaks_by_extent_1d)
  - 🅵 [moving_average_filter](#oscfar-filters-moving_average_filter)

### Functions

<a name="oscfar-filters-remove_baseline_peaks"></a>

### 🅵 oscfar\.filters\.remove_baseline_peaks

```python
def remove_baseline_peaks(data, detection_indices, noise_estimates, secondary_threshold_factor = 2.0):
```

Removes detected peaks that are too close to the baseline using a

secondary amplitude threshold\.

**Parameters:**

- **data** (`np.ndarray`): The original signal data\.
- **detection_indices** (`np.ndarray`): Indices of peaks detected by OS-CFAR\.
- **noise_estimates** (`np.ndarray`): Array of noise estimates corresponding to each detection\.
- **secondary_threshold_factor** (`float`): Factor multiplied by the noise estimate
  to set the secondary threshold\.

**Returns:**

- `np.ndarray`: Indices of the filtered detections\.
  <a name="oscfar-filters-median_filter"></a>

### 🅵 oscfar\.filters\.median_filter

```python
def median_filter(data, kernel_size):
```

Applies a median filter\.
<a name="oscfar-filters-lowpass_filter"></a>

### 🅵 oscfar\.filters\.lowpass_filter

```python
def lowpass_filter(data, cutoff_freq, sampling_rate, order = 5):
```

Applies a low-pass Butterworth filter\.
<a name="oscfar-filters-highpass_filter"></a>

### 🅵 oscfar\.filters\.highpass_filter

```python
def highpass_filter(data, cutoff_freq, sampling_rate, order = 5):
```

Applies a high-pass Butterworth filter to the 1D data\.

This uses a zero-phase filter \('filtfilt'\) to avoid introducing
phase shifts in the filtered signal\.

**Parameters:**

- **data** (`np.ndarray`): 1D array of input data \(e\.g\., time series\)\.
- **cutoff_freq** (`float`): The desired cutoff frequency in Hz\. Frequencies
  below this value will be attenuated\.
- **sampling_rate** (`float`): The sampling rate of the input data in Hz\.
  This is crucial for digital filter design\.
- **order** (`int`): The order of the Butterworth filter\. Higher
  orders provide a steeper rolloff but can be
  less stable\. Defaults to 5\.

**Returns:**

- `np.ndarray`: The high-pass filtered data array, same shape as input\.

**Raises:**

- **ValueError**: If input data is not a 1D numpy array, or if
  cutoff_freq or sampling_rate are invalid\.
  <a name="oscfar-filters-group_close_peaks"></a>

### 🅵 oscfar\.filters\.group_close_peaks

```python
def group_close_peaks(peak_indices, min_distance):
```

Groups peak indices that are close to each other\.

Iterates through sorted peak indices and groups any peaks that are
separated by less than or equal to 'min_distance' samples\.

**Parameters:**

- **peak_indices** (`list or np.ndarray`): A list or array of peak indices,
  assumed to be sorted or will be sorted\.
- **min_distance** (`int`): The maximum distance \(in samples\) between two
  consecutive peaks for them to be considered
  part of the same group\.

**Returns:**

- `list[list[int]]`: A list where each element is a list representing a
  group of close peak indices\. Returns an empty list
  if no peaks are provided\.
  <a name="oscfar-filters-find_representative_peaks"></a>

### 🅵 oscfar\.filters\.find_representative_peaks

```python
def find_representative_peaks(data, peak_indices, min_distance):
```

Groups close peaks and returns the index of the maximum peak from each group\.

First, groups peaks that are within 'min_distance' of each other using
group_close_peaks\. Then, for each group, identifies the index
corresponding to the highest value in the 'data' array\.

**Parameters:**

- **data** (`np.ndarray`): The 1D data array \(e\.g\., time series\) where
  peak values are found\. Used to determine the max peak\.
- **peak_indices** (`list or np.ndarray`): A list or array of peak indices
  to be grouped and processed\.
- **min_distance** (`int`): The maximum distance \(in samples\) between two
  consecutive peaks for them to be considered
  part of the same group\.

**Returns:**

- `list[int]`: A list containing the index of the maximum peak from
  each identified group\. Returns an empty list if no
  peaks are provided\.
  <a name="oscfar-filters-verify_peaks_snr"></a>

### 🅵 oscfar\.filters\.verify_peaks_snr

```python
def verify_peaks_snr(data, peak_indices, noise_window_factor = 3, min_snr = 3.0):
```

Verifies peaks based on their local Signal-to-Noise Ratio \(SNR\)\.

Calculates SNR for each peak relative to the noise estimated in
adjacent windows\.

**Parameters:**

- **data** (`np.ndarray`): The 1D data array \(e\.g\., time series\) where
  peaks were detected\.
- **peak_indices** (`list or np.ndarray`): Indices of the detected peaks\.
- **noise_window_factor** (`int`): Determines the size and offset
  of the noise estimation windows
  relative to a conceptual 'peak width'\.
  A simple proxy for peak width \(e\.g\., 5 samples\)
  is used internally\. The noise windows will
  be roughly this size and offset by
  this amount from the peak center\.
  Defaults to 3\.
- **min_snr** (`float`): The minimum acceptable local SNR for a
  peak to be considered verified\. Defaults to 3\.0\.

**Returns:**

- `list`: A list of indices corresponding to the verified peaks\.

**Raises:**

- **ValueError**: If input data is not a 1D numpy array\.
  <a name="oscfar-filters-enforce_min_distance"></a>

### 🅵 oscfar\.filters\.enforce_min_distance

```python
def enforce_min_distance(raw_peak_indices, data_values, min_distance):
```

Refines CFAR detections to enforce a minimum distance between peaks\.

**Parameters:**

- **raw_peak_indices**: List of indices where CFAR detected a peak\.
- **data_values**: The original data array \(or SNR array\) used for sorting\.
- **min_distance**: The minimum allowed separation between final peaks \(in indices\)\.

**Returns:**

- List of indices of the final, refined peaks\.
  <a name="oscfar-filters-filter_peaks_by_extent_1d"></a>

### 🅵 oscfar\.filters\.filter_peaks_by_extent_1d

```python
def filter_peaks_by_extent_1d(peak_indices, min_extent, max_extent):
```

Filters a list of 1D peak indices, removing peaks that belong to

consecutive groups larger than max_extent\.

**Parameters:**

- **peak_indices** (`list or np.ndarray`): A list or array of integer indices
  where peaks were detected by CFAR\.
  Assumed to be along a single dimension\.
- **max_extent** (`int`): The maximum allowed number of consecutive indices
  for a valid peak group\. Groups larger than this
  are considered extended clutter/scattering and removed\.

**Returns:**

- `list`: A list of filtered peak indices, keeping only those belonging
  to groups with extent \<= max_extent\.
  <a name="oscfar-filters-moving_average_filter"></a>

### 🅵 oscfar\.filters\.moving_average_filter

```python
def moving_average_filter(data, window_size):
```

Applies a simple moving average filter to the 1D data\.

Each point in the output is the average of the 'window_size' neighboring
points in the input data \(including the point itself\)\. Uses 'same' mode
for convolution, meaning the output array has the same size as the input,
but edge effects might be present where the window doesn't fully overlap\.

**Parameters:**

- **data** (`np.ndarray`): 1D array of input data\.
- **window_size** (`int`): The number of points to include in the averaging
  window\. Should be an odd number for a centered average,
  but works with even numbers too\. Must be positive\.

**Returns:**

- `np.ndarray`: The smoothed data array, same shape as input\.

**Raises:**

- **ValueError**: If input data is not a 1D numpy array or if window_size
  is not a positive integer\.
  <a name="oscfar-gaussian_fit"></a>

## 🅼 oscfar\.gaussian_fit

- **Functions:**
  - 🅵 [sum_of_gaussians](#oscfar-gaussian_fit-sum_of_gaussians)
  - 🅵 [sum_of_scattered_gaussians](#oscfar-gaussian_fit-sum_of_scattered_gaussians)
  - 🅵 [find_best_multi_gaussian_fit](#oscfar-gaussian_fit-find_best_multi_gaussian_fit)
  - 🅵 [find_best_multi_gaussian_fit_combinatorial](#oscfar-gaussian_fit-find_best_multi_gaussian_fit_combinatorial)

### Functions

<a name="oscfar-gaussian_fit-sum_of_gaussians"></a>

### 🅵 oscfar\.gaussian_fit\.sum_of_gaussians

```python
def sum_of_gaussians(x, *params):
```

Calculates the sum of multiple Gaussian functions\.

The parameters for the Gaussians are provided in a flat list:
\[amp1, mean1, stddev1, amp2, mean2, stddev2, \.\.\., ampN, meanN, stddevN\]

## Parameters:

x : array_like
The independent variable where the Gaussians are calculated\.
\*params : float
A variable number of arguments representing the parameters for the Gaussians\.
The total number of parameters must be a multiple of 3\. - amp: Amplitude of the Gaussian\. - mean: Mean \(center\) of the Gaussian\. - stddev: Standard deviation \(width\) of the Gaussian\. Stddev should be positive\.

## Returns:

y : array_like
The sum of the Gaussian functions evaluated at x\.

## Raises:

ValueError:
If the number of parameters in \`params\` is not a multiple of 3\.
<a name="oscfar-gaussian_fit-sum_of_scattered_gaussians"></a>

### 🅵 oscfar\.gaussian_fit\.sum_of_scattered_gaussians

```python
def sum_of_scattered_gaussians(x, *params):
```

Calculates the sum of multiple scattered Gaussian functions \(Exponentially Modified Gaussian\)\.

Each scattered Gaussian is defined by the convolution of a Gaussian with a
one-sided exponential decay\. This implementation uses a numerically stable
formulation involving erfcx\(x\) = exp\(x^2\)erfc\(x\):
EMG\(t\) = \(amp / \(2 \* tau\)\) \* erfcx\(B\) \* exp\(-0\.5 \* \(\(t - mean\) / sigma\)^2\)
where B = \(1/sqrt\(2\)\) \* \(sigma/tau - \(t - mean\)/sigma\)

If the scattering timescale 'tau' is very close to zero \(below a small
threshold\), the component defaults to a standard Gaussian function to ensure
stability and represent the unscattered limit\.

The parameters for the scattered Gaussians are provided in a flat list:
\[amp1, mean1, sigma1, tau1, amp2, mean2, sigma2, tau2, \.\.\., ampN, meanN, sigmaN, tauN\]

## Parameters:

x : array_like
The independent variable where the functions are calculated\.
\*params : float
A variable number of arguments representing the parameters\.
The total number of parameters must be a multiple of 4\. - amp: Amplitude of the component\. - mean: Mean \(center\) of the Gaussian part before convolution \(t0\)\. - sigma: Standard deviation \(width\) of the Gaussian part\.
Must be positive \(e\.g\., enforced by fitter bounds\)\. - tau: Scattering timescale \(decay constant of the exponential\)\.
Must be non-negative \(e\.g\., enforced by fitter bounds\)\.

## Returns:

y : array_like
The sum of the scattered Gaussian functions evaluated at x\.

## Raises:

ValueError:
If the number of parameters in \`params\` is not a multiple of 4\.
<a name="oscfar-gaussian_fit-find_best_multi_gaussian_fit"></a>

### 🅵 oscfar\.gaussian_fit\.find_best_multi_gaussian_fit

```python
def find_best_multi_gaussian_fit(x_data, y_data, initial_flat_params, max_n_gaussians = None, y_err = None):
```

Performs a grid search to find the best multi-Gaussian fit by trying

different numbers of Gaussian components\.

The function iterates from 1 to \`max_n_gaussians\` \(or the number of
peaks in \`initial_flat_params\`\), fitting the data with that many
Gaussian components\. Initial guesses for the fits are derived from the
\`initial_flat_params\` by selecting the components with the largest
amplitudes\.

The best fit is selected based on the Bayesian Information Criterion \(BIC\)\.

## Parameters:

x_data : array_like
The independent variable where the data is measured\.
y_data : array_like
The dependent data\.
initial_flat_params : list or array_like
A flat list of initial parameters for Gaussian components, ordered as
\[amp1, mean1, sigma1, amp2, mean2, sigma2, \.\.\.\]\.
max_n_gaussians : int, optional
The maximum number of Gaussian components to try\. If None, it defaults
to the number of components present in \`initial_flat_params\`\.
y_err : array_like, optional
Error on y_data\. If provided, it's used in \`curve_fit\` for weighted
least squares\.

## Returns:

dict
A dictionary containing: - 'best_fit': A dict with 'n_components', 'popt', 'pcov', 'bic', 'rss'
for the model with the lowest BIC\. - 'all_fits': A list of dicts, each containing 'n_components', 'popt',
'pcov', 'bic', 'rss' for every number of components tried\.

## Raises:

ValueError:
If \`initial_flat_params\` is empty or not a multiple of 3\.
If \`x_data\` or \`y_data\` are empty or have mismatched lengths\.
<a name="oscfar-gaussian_fit-find_best_multi_gaussian_fit_combinatorial"></a>

### 🅵 oscfar\.gaussian_fit\.find_best_multi_gaussian_fit_combinatorial

```python
def find_best_multi_gaussian_fit_combinatorial(x_data, y_data, initial_flat_params, max_n_gaussians = None, y_err = None, max_initial_components_for_pool = None, model_to_test = 'gaussian', default_initial_tau = 0.0001, max_tau_bound_factor = 1.0, use_multiprocessing = True, num_processes = None):
```

Performs a grid search to find the best multi-component fit by trying

different numbers of components, different combinations of initial peak
guesses, and optionally different model types \(Gaussian or Scattered Gaussian\)\.

This version supports multiprocessing to speed up the fitting process\.

## Parameters:

\(Same as the single-process version, plus the following:\)
use_multiprocessing : bool, optional
Whether to use multiprocessing\. Defaults to True\.
num_processes : int, optional
The number of processes to use\. If None, uses the number of CPU cores\.

## Returns:

\(Same as the single-process version\)

## Raises:

\(Same as the single-process version\)
<a name="oscfar-setup"></a>

## 🅼 oscfar\.setup

<a name="oscfar-utils"></a>

## 🅼 oscfar\.utils

- **Classes:**
  - 🅲 [NpzReader](#oscfar-utils-NpzReader)
  - 🅲 [NpzWriter](#oscfar-utils-NpzWriter)
  - 🅲 [Peaks](#oscfar-utils-Peaks)
  - 🅲 [WaterFallAxes](#oscfar-utils-WaterFallAxes)
  - 🅲 [WaterFallGrid](#oscfar-utils-WaterFallGrid)

### Classes

<a name="oscfar-utils-NpzReader"></a>

### 🅲 oscfar\.utils\.NpzReader

```python
class NpzReader(DataReader):
```

**Functions:**

<a name="oscfar-utils-NpzReader-__init__"></a>

#### 🅵 oscfar\.utils\.NpzReader\.\_\_init\_\_

```python
def __init__(self, fname, factor):
```

<a name="oscfar-utils-NpzReader-__repr__"></a>

#### 🅵 oscfar\.utils\.NpzReader\.\_\_repr\_\_

```python
def __repr__(self):
```

<a name="oscfar-utils-NpzReader-__str__"></a>

#### 🅵 oscfar\.utils\.NpzReader\.\_\_str\_\_

```python
def __str__(self):
```

<a name="oscfar-utils-NpzWriter"></a>

### 🅲 oscfar\.utils\.NpzWriter

```python
class NpzWriter:
```

**Functions:**

<a name="oscfar-utils-NpzWriter-__init__"></a>

#### 🅵 oscfar\.utils\.NpzWriter\.\_\_init\_\_

```python
def __init__(self, original_data: NpzReader):
```

<a name="oscfar-utils-NpzWriter-update_burst_parameters"></a>

#### 🅵 oscfar\.utils\.NpzWriter\.update_burst_parameters

```python
def update_burst_parameters(self, **kwargs):
```

<a name="oscfar-utils-NpzWriter-save"></a>

#### 🅵 oscfar\.utils\.NpzWriter\.save

```python
def save(self, new_filepath: str):
```

<a name="oscfar-utils-Peaks"></a>

### 🅲 oscfar\.utils\.Peaks

```python
class Peaks:
```

**Functions:**

<a name="oscfar-utils-Peaks-__init__"></a>

#### 🅵 oscfar\.utils\.Peaks\.\_\_init\_\_

```python
def __init__(self, oscfar_result):
```

<a name="oscfar-utils-WaterFallAxes"></a>

### 🅲 oscfar\.utils\.WaterFallAxes

```python
class WaterFallAxes:
```

**Functions:**

<a name="oscfar-utils-WaterFallAxes-__init__"></a>

#### 🅵 oscfar\.utils\.WaterFallAxes\.\_\_init\_\_

```python
def __init__(self, data: DataReader, width: float, height: float, bottom: float, left: float = None, hratio: float = 1, vratio: float = 1, show_ts = True, show_spec = True, labels_on = [True, True], title = '', readjust_title = 0):
```

<a name="oscfar-utils-WaterFallAxes-plot"></a>

#### 🅵 oscfar\.utils\.WaterFallAxes\.plot

```python
def plot(self):
```

<a name="oscfar-utils-WaterFallAxes-plot_time_peaks"></a>

#### 🅵 oscfar\.utils\.WaterFallAxes\.plot_time_peaks

```python
def plot_time_peaks(self, peaks: Peaks, color, show_thres = False):
```

<a name="oscfar-utils-WaterFallGrid"></a>

### 🅲 oscfar\.utils\.WaterFallGrid

```python
class WaterFallGrid:
```

**Functions:**

<a name="oscfar-utils-WaterFallGrid-__init__"></a>

#### 🅵 oscfar\.utils\.WaterFallGrid\.\_\_init\_\_

```python
def __init__(self, nrows: int, ncols: int, vspacing = 0.1, hspacing = 0.1):
```

<a name="oscfar-utils-WaterFallGrid-plot"></a>

#### 🅵 oscfar\.utils\.WaterFallGrid\.plot

```python
def plot(self, data: list, peaks: list, titles: list, color, labels = [True, False], adjust_t = 0, show_thres = False):
```

<a name="oscfar-utils-WaterFallGrid-add_info"></a>

#### 🅵 oscfar\.utils\.WaterFallGrid\.add_info

```python
def add_info(self, info: pd.DataFrame):
```
