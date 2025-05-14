"""
Convenience functions that are inefficient, but are maybe a bit easier to work with?
"""

from .. import Iterators as itut
from .. import Numputils as nput

import itertools
from collections import namedtuple
import numpy as np

from .CoordinateSystems import *

__all__ = [
    "cartesian_to_zmatrix",
    "zmatrix_to_cartesian",
    "canonicalize_internal",
    "enumerate_zmatrices",
    "extract_zmatrix_internals",
    "parse_zmatrix_string",
    "validate_zmatrix",
    "chain_zmatrix",
    "attached_zmatrix_fragment",
    "functionalized_zmatrix",
    "reindex_zmatrix"
]

def cartesian_to_zmatrix(coords, ordering=None, use_rad = True):
    """
    Converts Cartesians to Z-Matrix coords and returns the underlying arrays

    :param coords: input Cartesians
    :type coords: np.ndarray
    :param ordering: the Z-matrix ordering as a list of lists
    :type ordering:
    :return: Z-matrix coords
    :rtype: Iterable[np.ndarray | list]
    """

    zms = CoordinateSet(coords, system=CartesianCoordinates3D).convert(ZMatrixCoordinates, ordering=ordering, use_rad=use_rad)
    crds = namedtuple("zms", ["coords", "ordering"])
    return crds(np.asarray(zms), zms.converter_options['ordering'])

def zmatrix_to_cartesian(coords, ordering=None, origins=None, axes=None, use_rad=True):
    """
    Converts Z-maztrix coords to Cartesians

    :param coords:
    :type coords: np.ndarray
    :param ordering:
    :type ordering:
    :param origins:
    :type origins:
    :param axes:
    :type axes:
    :param use_rad:
    :type use_rad:
    :return:
    :rtype:
    """
    carts = CoordinateSet(coords, ZMatrixCoordinates).convert(CartesianCoordinates3D,
                                                            ordering=ordering, origins=origins, axes=axes, use_rad=use_rad)
    return np.asarray(carts)


def canonicalize_internal(coord):
    dupes = len(np.unique(coord)) < len(coord)
    if dupes: return None
    if len(coord) == 2:
        i, j = coord
        if i > j:
            coord = (j, i)
    elif len(coord) == 3:
        i, j, k = coord
        if i > k:
            coord = (k, j, i)
    elif len(coord) == 4:
        i, j, k, l = coord
        if i > l:
            coord = (l, k, j, i)
    elif coord[0] > coord[-1]:
        coord = tuple(reversed(coord))
    return coord

def _zmatrix_iterate(coords, natoms=None,
                     include_origins=False,
                     canonicalize=True,
                     deduplicate=True,
                     allow_completions=False
                     ):
    # TODO: this fixes an atom ordering, to change that up we'd need to permute the initial coords...
    if canonicalize:
        coords = [tuple(reversed(canonicalize_internal(s))) for s in coords]

    if deduplicate:
        dupes = set()
        _ = []
        for c in coords:
            if c in dupes: continue
            _.append(c)
            dupes.add(c)
        coords = _

    if include_origins:
        if (1, 0) not in coords:
            coords = [(1, 0)] + coords
        if (2, 1) not in coords and (2, 0) not in coords:
            if (2, 1, 0) in coords:
                coords = [(2, 1)] + coords
            else:
                coords = [(2, 0)] + coords
        if (2, 0) in coords and (2, 0, 1) not in coords: # can this happen?
            coords.append((2,1,0))

    if natoms is None:
        all_atoms = {i for s in coords for i in s}
        natoms = len(all_atoms)

    dihedrals = [k for k in coords if len(k) == 4]
    all_dihedrals = [
        (i, j, k, l)
        for (i, j, k, l) in dihedrals
        if i > j and i > k and i > l
    ]

    # need to iterate over all N-2 choices of dihedrals (in principle)...
    # should first reduce over consistent sets
    if not allow_completions:
        dihedrals = [
            (i,j,k,l) for i,j,k,l in dihedrals
            if (i,j) in coords and (i,j,k) in coords
            # if (
            #         any(x in coords or tuple(reversed(x)) in coords for x in [(i,j), (l,k)])
            #         and any(x in coords or tuple(reversed(x)) in coords for x in [(i,j,k), (l,k,j)])
            # )
        ]

    embedding = [
        x for x in [(2, 0, 1), (2, 1, 0)]
        if x in coords
    ]

    # we also will want to sample from dihedrals that provide individual atoms
    atom_diheds = [[] for _ in range(natoms)]
    for n,(i,j,k,l) in enumerate(dihedrals):
        atom_diheds[i].append((i,j,k,l))

    # completions = []
    # if allow_completions:
    #     for d in all_dihedrals:
    #         if d in dihedrals: continue
    #         completions.extend([d[:2], d[:3]])
    #
    #     c_set = set()
    #     for d in dihedrals:
    #         c_set.add(d[:2])
    #         c_set.add(d[:3])
    #     coord_pairs = [
    #         (c[:2],c[:3])
    #         for
    #     ]
    #     for d in all_dihedrals:
    #         if d in dihedrals: continue
    #         completions.extend([d[:2], d[:3]])

    for dihed_choice in itertools.product(embedding, *atom_diheds[3:]):
        emb, dis = dihed_choice[0], dihed_choice[1:]
        yield (
            (0, -1, -1, -1),
            (1, 0, -1, -1),
            emb + (-1,)
        ) + dis

def enumerate_zmatrices(coords, natoms=None,
                        allow_permutation=True,
                        include_origins=False,
                        canonicalize=True,
                        deduplicate=True,
                        preorder_atoms=True,
                        allow_completions=False
                        ):
    if canonicalize:
        coords = [tuple(reversed(canonicalize_internal(s))) for s in coords]

    if deduplicate:
        dupes = set()
        _ = []
        for c in coords:
            if c in dupes: continue
            _.append(c)
            dupes.add(c)
        coords = _

    if natoms is None:
        all_atoms = {i for s in coords for i in s}
        natoms = len(all_atoms)

    if preorder_atoms:
        counts = itut.counts(itertools.chain(*coords))
        max_order = list(sorted(range(natoms), key=lambda k:-counts[k]))
    else:
        max_order = np.arange(natoms)

    for atoms in (
            itertools.permutations(max_order)
                if allow_permutation else
            [max_order]
    ):
        atom_perm = np.argsort(atoms)
        perm_coords = [
            tuple(reversed(canonicalize_internal([atom_perm[c] for c in crd])))
            for crd in coords
        ]
        for zm in _zmatrix_iterate(perm_coords,
                                   natoms=natoms,
                                   include_origins=include_origins,
                                   canonicalize=False,
                                   deduplicate=False,
                                   allow_completions=allow_completions
                                   ):
            yield [
                [atoms[c] if c >= 0 else c for c in z]
                for z in zm
            ]

def extract_zmatrix_internals(zmat):
    specs = []
    for row in zmat:
        if row[1] < 0: continue
        specs.append(tuple(row[:2]))
        if row[2] < 0: continue
        specs.append(tuple(row[:3]))
        if row[3] < 0: continue
        specs.append(tuple(row[:4]))
    return specs

def parse_zmatrix_string(zmat):
    from ..Data import AtomData, UnitsData
    # we have to reparse the Gaussian Z-matrix...

    possible_atoms = {d["Symbol"][:2] for d in AtomData.data.values()}

    atoms = []
    ordering = []
    coords = []
    vars = {}

    zmat, vars_block = zmat.split("\n\n", 1)
    bits = zmat.split()

    coord = []
    ord = []
    complete = False
    last_complete = -1
    for i, b in enumerate(bits):
        d = (i - last_complete) - 1
        m = d % 2
        if d == 0:
            atoms.append(b)
        elif m == 1:
            b = int(b)
            if b > 0: b = b - 1
            ord.append(b)
        elif m == 0:
            coord.append(b)

        if i == len(bits) - 1 or bits[i + 1][-1] in possible_atoms:
            last_complete = i
            ord = ord + [-1] * (4 - len(ord))
            coord = coord + [0] * (3 - len(coord))
            ordering.append(ord)
            coords.append(coord)
            ord = []
            coord = []

    split_pairs = [vb.strip().split() for vb in vars_block.split("\n")]
    split_pairs = [s for s in split_pairs if len(s) > 0]

    vars = {k: float(v) for k, v in split_pairs}
    coords = [
        [vars.get(x, x) for x in c]
        for c in coords
    ]

    ordering = [
        [i] + o
        for i, o in enumerate(ordering)
    ]
    # convert book angles into sensible dihedrals...
    # actually...I think I don't need to do anything for this?
    ordering = np.array(ordering)[:, :4]

    coords = np.array(coords)
    coords[:, 0] *= UnitsData.convert("Angstroms", "BohrRadius")
    coords[:, 1] = np.deg2rad(coords[:, 1])
    coords[:, 2] = np.deg2rad(coords[:, 2])

    return (atoms, ordering, coords)

def validate_zmatrix(ordering):
    proxy_order = [o[0] for o in ordering]
    if any(p < 0 for p in proxy_order):
        return False
    order_sorting = np.argsort(proxy_order)
    if len(ordering) > 1:
        ...

        # if ordering[0] < ordering

    return True

def chain_zmatrix(n):
    return [
        list(range(i, i-4, -1))
        for i in range(n)
    ]

def attached_zmatrix_fragment(n, fragment, attachment_points):
    return [
        [attachment_points[-r-1] if r < 0 else n+r for r in row]
        for row in fragment
    ]

def functionalized_zmatrix(
        base_zm,
        attachments:dict,
        single_atoms:list[int]=None # individual components, embedding doesn't matter
):
    if nput.is_numeric(base_zm):
        zm = chain_zmatrix(base_zm)
    else:
        zm = [
            list(x) for x in base_zm
        ]
    for attachment_points, fragment in attachments.items():
        if nput.is_numeric(fragment):
            fragment = chain_zmatrix(fragment)
        zm = zm + attached_zmatrix_fragment(
            len(zm),
            fragment,
            attachment_points
        )
    if single_atoms is not None:
        for atom in single_atoms:
            zm = zm + attached_zmatrix_fragment(
                len(zm),
                [[0, -1, -2, -3]],
                [
                    (atom - i) if i < 0 else i
                    for i in range(atom, atom - 4, -1)
                ]
            )
    return zm

def reindex_zmatrix(zm, perm):
    return [
        [perm[r] if r >= 0 else r for r in row]
        for row in zm
    ]
