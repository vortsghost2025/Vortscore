import numpy as np
from typing import Dict

DIM = 10_000
SEED = 42
_rng = np.random.default_rng(SEED)

# Bipolar base vectors (-1/1) to match hdc_engine.bind and VitalisKernel
BASE_MFCC = _rng.choice([-1, 1], size=(13, DIM)).astype(np.int8)
BASE_PROSODY = {
    "pitch":       _rng.choice([-1, 1], size=DIM).astype(np.int8),
    "energy":      _rng.choice([-1, 1], size=DIM).astype(np.int8),
    "tempo":       _rng.choice([-1, 1], size=DIM).astype(np.int8),
    "pause_ratio": _rng.choice([-1, 1], size=DIM).astype(np.int8),
}

PROSODY_SCALE = {
    "pitch": 300.0,
    "energy": 0.5,
    "tempo": 200.0,
    "pause_ratio": 1.0,
}


def _bipolar_binarize(val: float) -> np.ndarray:
    """Map a scalar [0,1] to a bipolar hypervector."""
    bits = (_rng.random(DIM) < val).astype(np.int8)
    bits[bits == 0] = -1
    return bits


def _permute(vec: np.ndarray, shift: int) -> np.ndarray:
    """Cyclic shift — encodes temporal position."""
    return np.roll(vec, shift % DIM)


def _bind(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Bipolar binding: element-wise multiply (-1/1 * -1/1 = -1/1)."""
    return (a * b).astype(np.int8)


def _bundle(vecs: list) -> np.ndarray:
    """
    Bipolar bundling: sum then binarize via sign.
    Ties broken toward +1.
    """
    stacked = np.stack(vecs, axis=0).astype(np.int32)
    result = np.sign(stacked.sum(axis=0)).astype(np.int8)
    result[result == 0] = 1
    return result


def encode(
    mfcc: np.ndarray,
    prosody: Dict[str, float],
    chunk_size: int = 5,
) -> np.ndarray:
    """
    Convert one utterance (MFCC matrix + prosody dict) into a single
    bipolar 10k-dim hypervector that preserves temporal order.

    Temporal encoding equation:
        S = V_1 * rho(V_2) * rho^2(V_3) ... rho^n(V_n)
    where rho is cyclic shift and * is bipolar binding.
    """
    n_frames = mfcc.shape[1]

    # ------------------------------------------------------------------
    # 1. Frame-level bipolar vectors
    #    Each frame: 13 MFCC coefficients bound with their base vectors
    # ------------------------------------------------------------------
    frame_hvs = []
    for t in range(n_frames):
        frame_components = []
        for i in range(13):
            coeff_val = float(mfcc[i, t])
            # Threshold against coefficient median → bipolar
            bit = np.int8(1) if coeff_val > 0 else np.int8(-1)
            coeff_vec = np.full(DIM, bit, dtype=np.int8)
            frame_components.append(_bind(coeff_vec, BASE_MFCC[i]))
        frame_hvs.append(_bundle(frame_components))

    # ------------------------------------------------------------------
    # 2. Forward temporal binding (preserves order)
    #    S_fwd = frame_0 * rho(frame_1) * rho^2(frame_2) ...
    # ------------------------------------------------------------------
    forward_hv = frame_hvs[0].copy() if frame_hvs else np.ones(DIM, dtype=np.int8)
    for t in range(1, len(frame_hvs)):
        forward_hv = _bind(forward_hv, _permute(frame_hvs[t], shift=t))

    # ------------------------------------------------------------------
    # 3. Backward temporal binding (reverse rhythm)
    # ------------------------------------------------------------------
    backward_hv = frame_hvs[-1].copy() if frame_hvs else np.ones(DIM, dtype=np.int8)
    for t in range(len(frame_hvs) - 2, -1, -1):
        backward_hv = _bind(backward_hv, _permute(frame_hvs[t], shift=-(t + 1)))

    # ------------------------------------------------------------------
    # 4. Chunk-level binding (mid-scale temporal structure)
    # ------------------------------------------------------------------
    n_chunks = max(1, n_frames // chunk_size)
    chunk_hvs = []
    for c in range(n_chunks):
        start = c * chunk_size
        end = min(start + chunk_size, n_frames)
        chunk_bundle = _bundle(frame_hvs[start:end])
        chunk_hvs.append(_permute(chunk_bundle, shift=c))
    chunk_hv = _bundle(chunk_hvs) if chunk_hvs else np.ones(DIM, dtype=np.int8)

    # ------------------------------------------------------------------
    # 5. Prosody binding (tone, energy, rhythm, silence)
    #    Each prosody feature bound with its base vector and
    #    permuted by frame count (ties prosody to utterance length)
    # ------------------------------------------------------------------
    prosody_hvs = []
    for key, val in prosody.items():
        norm = min(val / PROSODY_SCALE.get(key, 1.0), 1.0)
        pv = _bind(_bipolar_binarize(norm), BASE_PROSODY[key])
        pv = _permute(pv, shift=n_frames)
        prosody_hvs.append(pv)

    # ------------------------------------------------------------------
    # 6. Final composition: bundle all levels
    #    forward captures sequence, backward captures rhythm,
    #    chunks capture phrase structure, prosody captures tone
    # ------------------------------------------------------------------
    all_components = [forward_hv, backward_hv, chunk_hv] + prosody_hvs
    return _bundle(all_components)
