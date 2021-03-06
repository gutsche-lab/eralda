import numpy as np
import einops
from .cyclic import derive_rotation_matrices as derive_cyclic_rotation_matrices


def derive_rotation_matrices(order: int) -> np.ndarray:
    """Calculate a set of rotation matrices for a dihedral symmetry.

    Axis of rotation is the Z axis.
    Reflection occurs in the XY plane.

    Cyclic matrices are defined by
    Rz = [[cos(t), -sin(t),    0],
          [sin(t),  cos(t),    0],
          [     0,       0,    1]]

    Reflections of the above in the XY plane are given by
    Rz = [[cos(t),  sin(t),    0],
          [sin(t), -cos(t),    0],
          [     0,       0,   -1]]

    Parameters
    ----------
    order : int
        symmetry order

    Returns
    -------
    rotation_matrices: (2 * order, 3, 3) np.ndarray
        matrices defining dihedral symmetries with rotation around the Z axis
        and reflection in the XY plane
    """
    cyclic_matrices = derive_cyclic_rotation_matrices(order)
    rotation_matrices = einops.repeat(
        np.eye(3),
        'i j -> 2 new_axis i j',
        new_axis=order
    )
    rotation_matrices[..., :, :] = cyclic_matrices
    rotation_matrices[1, :, :, 1:] *= -1

    rotation_matrices = einops.rearrange(
        rotation_matrices,
        'd n i j -> (d n) i j'
    )
    return rotation_matrices