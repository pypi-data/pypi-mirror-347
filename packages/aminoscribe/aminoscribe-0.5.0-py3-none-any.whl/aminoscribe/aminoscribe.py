import pandas as pd
import numpy as np
import pickle
import scipy.signal as scipy_signal
from scipy.interpolate import interp1d
import importlib
import aminoscribe.generate_template as generate_template
from pathlib import Path

FREQ = 3012

_step_sizes_df = None
_step_durations_df = None
_amplitude_noise_df = None
_human_proteome_dict = None

def load_data(data_dir=None):
    global _step_sizes_df, _step_durations_df, _amplitude_noise_df, _human_proteome_dict

    if data_dir is None:
        data_dir = importlib.resources.files("aminoscribe").joinpath("data")
    else:
        data_dir = data_dir if isinstance(data_dir, Path) else Path(data_dir)

    _step_sizes_df = pd.read_csv(data_dir.joinpath("step_sizes_in_aa.csv"))
    _step_durations_df = pd.read_csv(data_dir.joinpath("step_durations.csv"))
    _amplitude_noise_df = pd.read_csv(data_dir.joinpath("amplitude_noise.csv"))

    with open(data_dir.joinpath("sequences.pickle"), "rb") as f:
        _human_proteome_dict = pickle.load(f)
            

def verify_data_loaded():
    if (_step_sizes_df is None or
        _step_durations_df is None or
        _amplitude_noise_df is None or
        _human_proteome_dict is None):
        load_data()


def add_timewarp(template, rng=None):
    verify_data_loaded()
    rng = rng or np.random.default_rng()
    
    # Choose an array of step sizes from the (weighted) options
    step_sizes = rng.choice(
        _step_sizes_df['step_size'],
        size=len(template),
        p=_step_sizes_df['count'] / _step_sizes_df['count'].sum()
    )
    
    # Choose step durations from the (weighted) options
    durations = rng.choice(
        _step_durations_df['duration_in_datapoints'],
        size=len(template),
        p=_step_durations_df['count'] / _step_durations_df['count'].sum()
    )

    # Use the step size and duration options that we picked out to build the timewarped squiggle
    i = -1
    timewarped_squiggle = []
    for step_size, step_duration in zip(step_sizes, durations):
        i += int(step_size)
        if i >= len(template):
            break

        # Add this step to the timewarped_squiggle
        step = [template[i]] * step_duration
        timewarped_squiggle.extend(step)

    return np.array(timewarped_squiggle)


def add_noise(timewarped_template, rng=None):
    verify_data_loaded()
    rng = rng or np.random.default_rng()
    # Noise values are binned, we use the middle value of each bin
    bin_size = _amplitude_noise_df['bin_end'][0] - _amplitude_noise_df['bin_start'][0]
    noise_values = _amplitude_noise_df['bin_start'] + bin_size / 2
    noise = rng.choice(
        noise_values,
        size=len(timewarped_template),
        p=_amplitude_noise_df['count'] / _amplitude_noise_df['count'].sum()
    )
    
    return timewarped_template + noise


def timewarp_and_noise(template, rng=None):
    verify_data_loaded()
    return add_noise(add_timewarp(template, rng), rng)


def get_protein_seq(protein_id):
    verify_data_loaded()
    # Use UniProt Accession Number as a safe id (without weird characters for filenames)
    protein_id = protein_id.split("|")[1] if "|" in protein_id else protein_id
    if protein_id not in _human_proteome_dict:
        raise ValueError(f"Unable to recognize protein id '{protein_id}'")
    return _human_proteome_dict[protein_id]

def normalize_squiggle(normalization_signal, signal):
    mean = np.mean(normalization_signal)
    std = np.std(normalization_signal)
    normalized_signal = (signal - mean) / std
    return normalized_signal, (mean, std)

def generate_squiggle(sequence: str = None,
                      protein_id: str = None,
                      base_template=None,
                      seed=None,
                      template_only: bool = False,
                      platonian: bool = False,
                      cterm: str = "",
                      nterm: str = "",
                      filter_noise: bool = False,
                      bessel_N: int = 8,
                      bessel_Wn: float = 100/(0.5 * 3012),  # A 100Hz cutoff
                      normalize: bool = False,
                      downsample: bool = False,
                      downsample_factor: float = 10,
                      return_metadata: bool = False):
    """
    Generates a simulated squiggle signal from an amino acid sequence.

    This function converts an amino acid sequence into a simulated nanopore squiggle. 
    It can optionally apply noise filtering, min-max normalization, and downsampling. 
    The sequence can be provided directly or retrieved using a protein ID.
    
    If no sequence is provided, it will attempt to retrieve the sequence using `protein_id`. 
    If neither is provided, the `base_template` is used.

    Args:
        sequence (str, optional): Amino acid sequence. Required if neither `protein_id` nor `base_template` is provided.
        protein_id (str, optional): Protein ID to fetch the sequence. Ignored if `sequence` is provided.
        base_template (optional): Base template (signal) on which to apply time and amplitude domain noise. Ignored if `sequence` or `protein_id` is provided.
        seed (int, optional): Random seed for reproducibility of the generated squiggle.
        template_only (bool, optional): If True, returns an idealized template for this sequence's nanopore squiggle. There is one datapoint for every reading window (20 amino acids) in the sequence.
        platonian (bool, optional): If True, uses a platonian template instead of one with varying amino acid contributions (more realistic).
        cterm (str, optional): Additional sequence to append to the C-terminal end. Default is an empty string.
        nterm (str, optional): Additional sequence to prepend to the N-terminal end. Default is an empty string.
        filter_noise (bool, optional): If True, applies a low-pass Bessel filter to reduce noise.
        bessel_N (int, optional): Order of the Bessel filter. Defaults to 8.
        bessel_Wn (float, optional): Normalized cutoff frequency for the Bessel filter. Defaults to 100Hz at 3012Hz sampling rate.
        normalize (bool, optional): If True, applies z-score normalization, using the cterm portion to extract std and mean.
        downsample (bool, optional): If True, applies linear downsampling to the squiggle signal.
        downsample_factor (float, optional): Factor by which the signal length is reduced. Defaults to 10.

    Returns:
        list: Processed squiggle signal as a list of float values.

    Raises:
        ValueError: If both `sequence` and `protein_id` are missing and no `base_template` is provided.

    Example:
        >>> signal = generate_squiggle(sequence="MKTLLDLGYTMKTLLLTLVVTMKTLLDLGYTMKTLLLTLVVLLTLVVVTIVCLDLGYTLGYT", normalize=True, downsample=True, downsample_factor=5)
        >>> print(signal[:5])  # First few values of the processed signal
    """
    verify_data_loaded()
    rng = np.random.default_rng(seed)
    if sequence:
        template = generate_template.template_from_sequence(nterm+sequence+cterm, platonian, rng=rng)
    elif protein_id:
        sequence = get_protein_seq(protein_id)
        template = generate_template.template_from_sequence(nterm+sequence+cterm, platonian, rng=rng)
    elif base_template is not None:
        template = base_template
    else:
        raise ValueError(
            "Either 'sequence', 'protein_id', or 'base_template' must be provided.")

    # At this stage we have 'template' to use for the remaining options
    if template_only:
        if normalize:
            if len(cterm)==0: return template # must have cterm to normalize
            cutoff = len(cterm) - 19
            normalization_signal = template[:cutoff]
            if return_metadata:
                return normalize_squiggle(normalization_signal, template)
            else:
                squiggle, _ = normalize_squiggle(normalization_signal, template)
                return squiggle
        return template
    
    # At this stage we will add timewarping and noise
    # If we normalize using the cterm we need to keep track of where in
    # the timewarped squiggle the cterm portion ends. To do this we 
    # timewarp each portion seperately (timewarping is iid)
    cutoff = len(cterm) - 19
    cterm_portion = timewarp_and_noise(template[:cutoff], rng)
    remaining_portion = timewarp_and_noise(template[cutoff:], rng)
    squiggle = np.concatenate((cterm_portion, remaining_portion))
    b, a = scipy_signal.bessel(bessel_N, bessel_Wn, btype='low')
    
    if filter_noise:
        squiggle = scipy_signal.filtfilt(b, a, squiggle)
    
    if downsample:
        x_original = np.linspace(0, len(squiggle), len(squiggle))
        x_new = np.linspace(0, len(squiggle), int(
            len(squiggle)/downsample_factor))
        f_linear = interp1d(x_original, squiggle, kind='linear')
        squiggle = f_linear(x_new)
    
    if normalize:
        # Use the cterm_portion as the normalization signal
        # Filter out high frequency noise then extract mean and std
        normalization_signal = scipy_signal.filtfilt(b, a, cterm_portion)
        if return_metadata:
            return normalize_squiggle(normalization_signal, squiggle)
        else:
            squiggle, _ = normalize_squiggle(normalization_signal, squiggle)
            return squiggle
    return squiggle
