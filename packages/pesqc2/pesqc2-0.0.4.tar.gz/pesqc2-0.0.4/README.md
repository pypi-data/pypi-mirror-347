# pesqc2

[![DOI](https://zenodo.org/badge/939487338.svg)](https://doi.org/10.5281/zenodo.14938543)

This project forks from [ludlows/PESQ](https://github.com/ludlows/PESQ/), updating the PESQ implementation to include its latest correction addressed in [P.862 Corrigendum 2 (03/18)](https://www.itu.int/rec/T-REC-P.862-201803-W!Cor2/en).

The correction addresses the under-prediction of subjective scores (by 0.8 MOS on average) by correcting the level of the loudness model.


This code is designed for numpy array specially.

# Requirements

    C compiler
    numpy
    cython


# Install with pip

```bash
# PyPi Repository
$ pip install pesqc2

# The Latest Version
$ pip install https://github.com/audiolabs/pesq/archive/master.zip
```

# Usage for narrowband and wideband Modes

Please note that the sampling rate (frequency) should be 16000 or 8000 (Hz). 

A sample rate of 8000 Hz is supported only in narrowband mode.

The code supports error-handling behaviors.

```python
def pesq(fs, ref, deg, mode='wb', on_error=PesqError.RAISE_EXCEPTION):
    """
    Args:
        ref: numpy 1D array, reference audio signal 
        deg: numpy 1D array, degraded audio signal
        fs:  integer, sampling rate
        mode: 'wb' (wide-band) or 'nb' (narrow-band)
        on_error: error-handling behavior, it could be PesqError.RETURN_VALUES or PesqError.RAISE_EXCEPTION by default
    Returns:
        pesq_score: float, P.862.2 Prediction (MOS-LQO) including Corrigendum 2
    """
```
Once you select `PesqError.RETURN_VALUES`, the `pesq` function will return -1 when an error occurs.

Once you select `PesqError.RAISE_EXCEPTION`, the `pesq` function will raise an exception when an error occurs.

It now supports the following errors: `InvalidSampleRateError`, `OutOfMemoryError`,`BufferTooShortError`,`NoUtterancesError`,`PesqError`(other unknown errors).

```python
from scipy.io import wavfile
from pesqc2 import pesq

rate, ref = wavfile.read("./audio/speech.wav")
rate, deg = wavfile.read("./audio/speech_bab_0dB.wav")

print(pesq(rate, ref, deg, 'wb'))
print(pesq(rate, ref, deg, 'nb'))
```

# Usage for `multiprocessing` feature

```python
def pesq_batch(fs, ref, deg, mode='wb', n_processor=None, on_error=PesqError.RAISE_EXCEPTION):
    """
   Running `pesq` using multiple processors
    Args:
        on_error:
        ref: numpy 1D (n_sample,) or 2D array (n_file, n_sample), reference audio signal
        deg: numpy 1D (n_sample,) or 2D array (n_file, n_sample), degraded audio signal
        fs:  integer, sampling rate
        mode: 'wb' (wide-band) or 'nb' (narrow-band)
        n_processor: cpu_count() (default) or number of processors (chosen by the user) or 0 (without multiprocessing)
        on_error: PesqError.RAISE_EXCEPTION (default) or PesqError.RETURN_VALUES
    Returns:
        pesq_score: list of pesq scores, P.862.2 Prediction (MOS-LQO)
    """
```
This function uses `multiprocessing` features to boost time efficiency.

When the `ref` is an 1-D numpy array and `deg` is a 2-D numpy array, the result of `pesq_batch` is identical to the value of `[pesq(fs, ref, deg[i,:],**kwargs) for i in range(deg.shape[0])]`.

When the `ref` is a 2-D numpy array and `deg` is a 2-D numpy array, the result of `pesq_batch` is identical to the value of `[pesq(fs, ref[i,:], deg[i,:],**kwargs) for i in range(deg.shape[0])]`.


# Correctness

The correctness is verified by running samples in the audio folder.

PESQ computed by this code in wideband mode is    1.5128041505813599 
(instead of 1.0832337141036987 which you would obtain without Corrigendum 2)

PESQ computed by this code in narrowband mode is  1.6072081327438354 
(no differences with or without Corrigendum 2)

# Note

Sampling rate (fs|rate) - No default. You must select either 8000Hz or 16000Hz.
 
Note that narrowband (nb) mode is only available when the sampling rate is 8000Hz.

The original C source code is modified.