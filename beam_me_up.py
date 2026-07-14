import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# Profile catalogue
# Units:
# A_mm2      cross-sectional area in mm²
# I_mm4      second moment of area in mm^4
# W_mm3      section modulus in mm^3
# E          Young's modulus in Pa
# density    kg/m³
# cost_per_kg EUR/kg
# ============================================================

PROFILE_CATALOGUE = {
    # ------------------------------------------------------------
    # Rectangular timber profiles, C24
    # Strong-axis bending; the larger dimension is assumed as section height h
    # Values refer to bending about the strong axis y-y:
    # E = 11 GPa, density = 420 kg/m³
    # A in mm², Iy in mm⁴, Wel,y in mm³
    # ------------------------------------------------------------
    "C24 timber 60 x 120 mm": {
        "A_mm2": 7200.0,
        "I_mm4": 8.640e6,
        "W_mm3": 144.0e3,
        "E": 11.0e9,
        "density": 420.0,
        "cost_per_kg": 0.80,
    },
    "C24 timber 80 x 160 mm": {
        "A_mm2": 12800.0,
        "I_mm4": 27.307e6,
        "W_mm3": 341.333e3,
        "E": 11.0e9,
        "density": 420.0,
        "cost_per_kg": 0.80,
    },
    "C24 timber 80 x 200 mm": {
        "A_mm2": 16000.0,
        "I_mm4": 53.333e6,
        "W_mm3": 533.333e3,
        "E": 11.0e9,
        "density": 420.0,
        "cost_per_kg": 0.80,
    },
    "C24 timber 120 x 240 mm": {
        "A_mm2": 28800.0,
        "I_mm4": 138.240e6,
        "W_mm3": 1152.0e3,
        "E": 11.0e9,
        "density": 420.0,
        "cost_per_kg": 0.80,
    },
    # ------------------------------------------------------------
    # IPE profiles
    # Values refer to bending about the strong axis y-y:
    # A in mm², Iy in mm⁴, Wel,y in mm³
    # ------------------------------------------------------------
    "IPE 100": {
        "A_mm2": 1032.0,
        "I_mm4": 1.710e6,
        "W_mm3": 34.20e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "IPE 160": {
        "A_mm2": 2009.0,
        "I_mm4": 8.693e6,
        "W_mm3": 108.7e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "IPE 200": {
        "A_mm2": 2848.0,
        "I_mm4": 19.43e6,
        "W_mm3": 194.3e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "IPE 240": {
        "A_mm2": 3912.0,
        "I_mm4": 38.92e6,
        "W_mm3": 324.3e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "IPE 300": {
        "A_mm2": 5381.0,
        "I_mm4": 83.56e6,
        "W_mm3": 557.1e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    # ------------------------------------------------------------
    # HEA profiles
    # Older German designation: IPBl
    # ------------------------------------------------------------
    "HEA 100 / IPBl 100": {
        "A_mm2": 2124.0,
        "I_mm4": 3.492e6,
        "W_mm3": 72.76e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEA 160 / IPBl 160": {
        "A_mm2": 3877.0,
        "I_mm4": 16.73e6,
        "W_mm3": 220.1e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEA 200 / IPBl 200": {
        "A_mm2": 5383.0,
        "I_mm4": 36.92e6,
        "W_mm3": 388.6e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEA 240 / IPBl 240": {
        "A_mm2": 7684.0,
        "I_mm4": 77.63e6,
        "W_mm3": 675.1e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEA 300 / IPBl 300": {
        "A_mm2": 11250.0,
        "I_mm4": 182.60e6,
        "W_mm3": 1260.0e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    # ------------------------------------------------------------
    # HEB profiles
    # Older German designation: IPB
    # ------------------------------------------------------------
    "HEB 100 / IPB 100": {
        "A_mm2": 2604.0,
        "I_mm4": 4.495e6,
        "W_mm3": 89.91e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEB 160 / IPB 160": {
        "A_mm2": 5425.0,
        "I_mm4": 24.92e6,
        "W_mm3": 311.5e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEB 200 / IPB 200": {
        "A_mm2": 7808.0,
        "I_mm4": 56.96e6,
        "W_mm3": 569.6e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEB 240 / IPB 240": {
        "A_mm2": 10600.0,
        "I_mm4": 112.60e6,
        "W_mm3": 938.3e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "HEB 300 / IPB 300": {
        "A_mm2": 14910.0,
        "I_mm4": 251.70e6,
        "W_mm3": 1678.0e3,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    # ------------------------------------------------------------
    # Circular hollow sections (CHS)
    # D x t: outside diameter x wall thickness
    # A in mm², I in mm⁴, W in mm³
    # ------------------------------------------------------------
    "CHS 76.1 x 4 mm": {
        "A_mm2": 906.0,
        "I_mm4": 590_555.0,
        "W_mm3": 15_520.5,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "CHS 88.9 x 4 mm": {
        "A_mm2": 1_066.9,
        "I_mm4": 963_398.4,
        "W_mm3": 21_673.8,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "CHS 101.6 x 4 mm": {
        "A_mm2": 1_226.5,
        "I_mm4": 1_462_844.6,
        "W_mm3": 28_796.2,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "CHS 114.3 x 5 mm": {
        "A_mm2": 1_716.9,
        "I_mm4": 2_569_202.0,
        "W_mm3": 44_955.4,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "CHS 139.7 x 6 mm": {
        "A_mm2": 2_520.2,
        "I_mm4": 5_642_598.0,
        "W_mm3": 80_781.6,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
    "CHS 168.3 x 6 mm": {
        "A_mm2": 3_059.3,
        "I_mm4": 10_086_949.1,
        "W_mm3": 119_868.7,
        "E": 210e9,
        "density": 7850.0,
        "cost_per_kg": 1.50,
    },
}


# ============================================================
# Helper functions
# ============================================================

def to_bool(value):
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ["true", "1", "yes", "y", "x"]


def to_float(value, default=0.0):
    if pd.isna(value) or value == "":
        return default
    return float(value)


def clean_string(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def characteristic_length(nodes_df):
    x = nodes_df["x"].astype(float).to_numpy()
    y = nodes_df["y"].astype(float).to_numpy()
    dx = max(x.max() - x.min(), 1.0)
    dy = max(y.max() - y.min(), 1.0)
    return max(dx, dy, 1.0)


# ============================================================
# Element formulation
# ============================================================

def transformation_matrix(c, s):
    """
    Transformation from global to local element degrees of freedom.

    local = T @ global
    """
    return np.array([
        [ c,  s, 0.0, 0.0, 0.0, 0.0],
        [-s,  c, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0,  c,  s, 0.0],
        [0.0, 0.0, 0.0, -s,  c, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ])


def local_frame_stiffness(E, A, I, L):
    EA = E * A
    EI = E * I

    return np.array([
        [ EA / L,              0.0,             0.0, -EA / L,              0.0,             0.0],
        [    0.0,  12 * EI / L**3,  6 * EI / L**2,     0.0, -12 * EI / L**3,  6 * EI / L**2],
        [    0.0,   6 * EI / L**2,      4 * EI / L,     0.0,  -6 * EI / L**2,      2 * EI / L],
        [-EA / L,              0.0,             0.0,  EA / L,              0.0,             0.0],
        [    0.0, -12 * EI / L**3, -6 * EI / L**2,     0.0,  12 * EI / L**3, -6 * EI / L**2],
        [    0.0,   6 * EI / L**2,      2 * EI / L,     0.0,  -6 * EI / L**2,      4 * EI / L],
    ], dtype=float)


def equivalent_uniform_load_local(qx, qy, L):
    """
    Consistent nodal load vector for constant distributed loads in local axes.

    qx: load in local x direction [N/m]
    qy: load in local y direction [N/m]

    Positive qy acts in positive local y direction.
    For a horizontal beam with local y upward, a downward load is qy < 0.
    """
    return np.array([
        qx * L / 2.0,
        qy * L / 2.0,
        qy * L**2 / 12.0,
        qx * L / 2.0,
        qy * L / 2.0,
       -qy * L**2 / 12.0,
    ], dtype=float)


def apply_moment_releases(k_full, f_full, release_i=False, release_j=False):
    """
    Moment releases are implemented by static condensation of the
    corresponding local rotational element DOFs.

    Released local DOFs:
    - theta_i: index 2
    - theta_j: index 5
    """
    released = []
    if release_i:
        released.append(2)
    if release_j:
        released.append(5)

    if len(released) == 0:
        return k_full.copy(), f_full.copy(), released

    retained = [i for i in range(6) if i not in released]

    K_rr = k_full[np.ix_(retained, retained)]
    K_rq = k_full[np.ix_(retained, released)]
    K_qr = k_full[np.ix_(released, retained)]
    K_qq = k_full[np.ix_(released, released)]

    f_r = f_full[retained]
    f_q = f_full[released]

    K_qq_inv = np.linalg.inv(K_qq)

    K_cond_rr = K_rr - K_rq @ K_qq_inv @ K_qr
    f_cond_r = f_r - K_rq @ K_qq_inv @ f_q

    k_cond = np.zeros((6, 6), dtype=float)
    f_cond = np.zeros(6, dtype=float)

    for a, ia in enumerate(retained):
        f_cond[ia] = f_cond_r[a]
        for b, ib in enumerate(retained):
            k_cond[ia, ib] = K_cond_rr[a, b]

    return k_cond, f_cond, released


def recover_local_displacements_with_releases(u_local_nodal, k_full, f_full, released):
    """
    Reconstructs the internal released element rotations from the condition
    that the released end moments are zero.
    """
    u_local = u_local_nodal.copy()

    if len(released) == 0:
        return u_local

    retained = [i for i in range(6) if i not in released]

    K_qr = k_full[np.ix_(released, retained)]
    K_qq = k_full[np.ix_(released, released)]
    f_q = f_full[released]

    u_r = u_local[retained]
    u_q = np.linalg.solve(K_qq, f_q - K_qr @ u_r)

    for a, ia in enumerate(released):
        u_local[ia] = u_q[a]

    return u_local


# ============================================================
# Hinges
# ============================================================

def preprocess_internal_hinges(nodes_df, members_df, hinges_df):
    """
    Internal hinges are modeled by splitting the corresponding member and
    applying moment releases at the generated hinge node.

    A hinge at xi = 0.5 divides member M1 into:
    M1_1 and M1_2

    Moment release:
    - end j of M1_1
    - end i of M1_2
    """
    nodes_out = nodes_df.copy()
    members_out = []

    node_ids = set(nodes_out["node"].astype(str))
    node_lookup = {
        str(row["node"]): (float(row["x"]), float(row["y"]))
        for _, row in nodes_out.iterrows()
    }

    hinges_by_member = {}

    if hinges_df is not None and len(hinges_df) > 0:
        for _, row in hinges_df.iterrows():
            member_id = clean_string(row.get("member", ""))
            if member_id == "":
                continue

            xi = to_float(row.get("xi", np.nan), default=np.nan)
            if not np.isfinite(xi):
                continue
            if xi <= 0.0 or xi >= 1.0:
                continue

            hinge_node = clean_string(row.get("hinge_node", ""))
            if hinge_node == "":
                hinge_node = f"{member_id}_H{len(hinges_by_member.get(member_id, [])) + 1}"

            hinges_by_member.setdefault(member_id, []).append({
                "xi": xi,
                "hinge_node": hinge_node,
            })

    for _, member in members_df.iterrows():
        member_id = clean_string(member["member"])
        node_i = clean_string(member["node_i"])
        node_j = clean_string(member["node_j"])

        if member_id == "" or node_i == "" or node_j == "":
            continue

        release_i_original = to_bool(member.get("release_i", False))
        release_j_original = to_bool(member.get("release_j", False))

        if member_id not in hinges_by_member:
            row = member.copy()
            row["source_member"] = member_id
            row["release_i"] = release_i_original
            row["release_j"] = release_j_original
            members_out.append(row)
            continue

        if node_i not in node_lookup or node_j not in node_lookup:
            raise ValueError(f"Member {member_id}: unknown node.")

        xi_coord, yi_coord = node_lookup[node_i]
        xj_coord, yj_coord = node_lookup[node_j]

        hinge_list = sorted(hinges_by_member[member_id], key=lambda h: h["xi"])

        split_nodes = [(0.0, node_i)]

        for h in hinge_list:
            xi = h["xi"]
            hinge_node = h["hinge_node"]

            xh = xi_coord + xi * (xj_coord - xi_coord)
            yh = yi_coord + xi * (yj_coord - yi_coord)

            if hinge_node not in node_ids:
                nodes_out.loc[len(nodes_out)] = {
                    "node": hinge_node,
                    "x": xh,
                    "y": yh,
                }
                node_ids.add(hinge_node)
                node_lookup[hinge_node] = (xh, yh)

            split_nodes.append((xi, hinge_node))

        split_nodes.append((1.0, node_j))

        for k in range(len(split_nodes) - 1):
            start_is_hinge = k > 0
            end_is_hinge = k < len(split_nodes) - 2

            new_member = member.copy()
            new_member["member"] = f"{member_id}_{k + 1}"
            new_member["source_member"] = member_id
            new_member["node_i"] = split_nodes[k][1]
            new_member["node_j"] = split_nodes[k + 1][1]
            new_member["release_i"] = release_i_original if k == 0 else True
            new_member["release_j"] = release_j_original if k == len(split_nodes) - 2 else True

            if start_is_hinge:
                new_member["release_i"] = True
            if end_is_hinge:
                new_member["release_j"] = True

            members_out.append(new_member)

    members_out_df = pd.DataFrame(members_out)

    return nodes_out.reset_index(drop=True), members_out_df.reset_index(drop=True)


# ============================================================
# Solver
# ============================================================

def solve_frame(nodes_df, members_df, supports_df, nodal_loads_df, distributed_loads_df, hinges_df):
    nodes_df = nodes_df.copy()
    members_df = members_df.copy()
    supports_df = supports_df.copy()
    nodal_loads_df = nodal_loads_df.copy()
    distributed_loads_df = distributed_loads_df.copy()
    hinges_df = hinges_df.copy()

    # Clean relevant rows
    nodes_df = nodes_df.dropna(how="all")
    members_df = members_df.dropna(how="all")
    supports_df = supports_df.dropna(how="all")
    nodal_loads_df = nodal_loads_df.dropna(how="all")
    distributed_loads_df = distributed_loads_df.dropna(how="all")
    hinges_df = hinges_df.dropna(how="all")

    nodes_df["node"] = nodes_df["node"].astype(str)
    nodes_df["x"] = nodes_df["x"].astype(float)
    nodes_df["y"] = nodes_df["y"].astype(float)

    # Create hinge nodes and split members
    nodes_df, members_df = preprocess_internal_hinges(nodes_df, members_df, hinges_df)

    node_ids = list(nodes_df["node"].astype(str))
    node_to_index = {node: i for i, node in enumerate(node_ids)}
    coords = nodes_df[["x", "y"]].to_numpy(dtype=float)

    n_nodes = len(nodes_df)
    n_dof = 3 * n_nodes

    K = np.zeros((n_dof, n_dof), dtype=float)
    F = np.zeros(n_dof, dtype=float)

    # Distributed loads are assigned to the original source member
    member_loads = {}
    for _, row in distributed_loads_df.iterrows():
        member = clean_string(row.get("member", ""))
        if member == "":
            continue
        qx = to_float(row.get("qx_local", 0.0))
        qy = to_float(row.get("qy_local", 0.0))

        if member not in member_loads:
            member_loads[member] = [0.0, 0.0]

        member_loads[member][0] += qx
        member_loads[member][1] += qy

    elements = []

    # Assemble elements
    for _, member in members_df.iterrows():
        member_id = clean_string(member["member"])
        source_member = clean_string(member.get("source_member", member_id))
        node_i = clean_string(member["node_i"])
        node_j = clean_string(member["node_j"])
        profile_name = clean_string(member["profile"])

        if node_i not in node_to_index or node_j not in node_to_index:
            raise ValueError(f"Member {member_id}: unknown node.")

        if profile_name not in PROFILE_CATALOGUE:
            raise ValueError(f"Member {member_id}: unknown profile '{profile_name}'.")

        i = node_to_index[node_i]
        j = node_to_index[node_j]

        xi, yi = coords[i]
        xj, yj = coords[j]

        dx = xj - xi
        dy = yj - yi
        L = float(np.sqrt(dx**2 + dy**2))

        if L <= 0.0:
            raise ValueError(f"Member {member_id}: length is zero.")

        c = dx / L
        s = dy / L

        profile = PROFILE_CATALOGUE[profile_name]

        A = profile["A_mm2"] * 1e-6
        I = profile["I_mm4"] * 1e-12
        E = profile["E"]

        qx, qy = member_loads.get(source_member, [0.0, 0.0])

        k_full_local = local_frame_stiffness(E, A, I, L)
        f_full_local = equivalent_uniform_load_local(qx, qy, L)

        release_i = to_bool(member.get("release_i", False))
        release_j = to_bool(member.get("release_j", False))

        k_cond_local, f_cond_local, released = apply_moment_releases(
            k_full_local,
            f_full_local,
            release_i=release_i,
            release_j=release_j,
        )

        T = transformation_matrix(c, s)

        k_global = T.T @ k_cond_local @ T
        f_global = T.T @ f_cond_local

        dofs = np.array([
            3 * i,
            3 * i + 1,
            3 * i + 2,
            3 * j,
            3 * j + 1,
            3 * j + 2,
        ])

        for a in range(6):
            F[dofs[a]] += f_global[a]
            for b in range(6):
                K[dofs[a], dofs[b]] += k_global[a, b]

        elements.append({
            "member": member_id,
            "source_member": source_member,
            "node_i": node_i,
            "node_j": node_j,
            "profile": profile_name,
            "i": i,
            "j": j,
            "dofs": dofs,
            "L": L,
            "c": c,
            "s": s,
            "T": T,
            "k_full_local": k_full_local,
            "f_full_local": f_full_local,
            "released": released,
            "release_i": release_i,
            "release_j": release_j,
            "qx": qx,
            "qy": qy,
            "A_m2": A,
            "I_m4": I,
            "A_mm2": profile["A_mm2"],
            "I_mm4": profile["I_mm4"],
            "W_mm3": profile["W_mm3"],
            "E": E,
            "density": profile["density"],
            "cost_per_kg": profile["cost_per_kg"],
        })

    # Nodal loads
    for _, row in nodal_loads_df.iterrows():
        node = clean_string(row.get("node", ""))
        if node == "":
            continue

        if node not in node_to_index:
            raise ValueError(f"Nodal load: unknown node '{node}'.")

        i = node_to_index[node]

        F[3 * i] += to_float(row.get("Fx", 0.0))
        F[3 * i + 1] += to_float(row.get("Fy", 0.0))
        F[3 * i + 2] += to_float(row.get("Mz", 0.0))

    # Supports
    fixed_dofs = []

    for _, row in supports_df.iterrows():
        node = clean_string(row.get("node", ""))
        if node == "":
            continue

        if node not in node_to_index:
            raise ValueError(f"Support: unknown node '{node}'.")

        i = node_to_index[node]

        if to_bool(row.get("fix_x", False)):
            fixed_dofs.append(3 * i)
        if to_bool(row.get("fix_y", False)):
            fixed_dofs.append(3 * i + 1)
        if to_bool(row.get("fix_rot", False)):
            fixed_dofs.append(3 * i + 2)

    fixed_dofs = sorted(set(fixed_dofs))

    # Automatically constrain inactive zero-stiffness DOFs.
    # This is especially relevant for pure hinge rotations.
    inactive_dofs = []
    row_norms = np.linalg.norm(K, axis=1) + np.linalg.norm(K, axis=0)
    reference_norm = max(float(np.max(row_norms)), 1.0)
    tol = 1e-10 * reference_norm

    for dof in range(n_dof):
        if row_norms[dof] < tol:
            if abs(F[dof]) > 1e-9:
                node = node_ids[dof // 3]
                dof_name = ["ux", "uy", "rot"][dof % 3]
                raise ValueError(
                    f"Inactive DOF with external load detected: node {node}, DOF {dof_name}."
                )
            fixed_dofs.append(dof)
            inactive_dofs.append(dof)

    fixed_dofs = sorted(set(fixed_dofs))
    free_dofs = [dof for dof in range(n_dof) if dof not in fixed_dofs]

    if len(free_dofs) == 0:
        raise ValueError("No free degrees of freedom available.")

    K_ff = K[np.ix_(free_dofs, free_dofs)]
    F_f = F[free_dofs]

    rank = np.linalg.matrix_rank(K_ff)

    if rank < K_ff.shape[0]:
        raise ValueError(
            "The reduced stiffness matrix is singular. "
            "The structure may be unstable, insufficiently supported, "
            "or contain a mechanism."
        )

    u = np.zeros(n_dof, dtype=float)
    u[free_dofs] = np.linalg.solve(K_ff, F_f)

    reactions = K @ u - F

    element_results = []
    diagram_data = []

    for element in elements:
        dofs = element["dofs"]
        u_global_e = u[dofs]
        u_local_nodal = element["T"] @ u_global_e

        u_local = recover_local_displacements_with_releases(
            u_local_nodal,
            element["k_full_local"],
            element["f_full_local"],
            element["released"],
        )

        p_local = element["k_full_local"] @ u_local - element["f_full_local"]

        for released_dof in element["released"]:
            p_local[released_dof] = 0.0

        L = element["L"]
        qx = element["qx"]
        qy = element["qy"]

        x = np.linspace(0.0, L, 101)

        N_i = p_local[0]
        V_i = p_local[1]
        M_i = p_local[2]

        # Sign convention:
        # N > 0: tension
        # Q and M follow the local element convention.
        # For a simply supported horizontal beam with downward qy < 0:
        # M is positive in the sagging region.
        N = -N_i - qx * x
        Q = V_i + qy * x
        M = -M_i + V_i * x + 0.5 * qy * x**2

        A_mm2 = element["A_mm2"]
        W_mm3 = element["W_mm3"]

        sigma_axial = N / A_mm2
        sigma_bending = M * 1000.0 / W_mm3

        sigma_top = sigma_axial + sigma_bending
        sigma_bottom = sigma_axial - sigma_bending

        max_normal_stress = max(
            float(np.max(np.abs(sigma_top))),
            float(np.max(np.abs(sigma_bottom))),
        )

        max_nominal_shear = float(np.max(np.abs(Q))) / A_mm2

        mass = element["A_m2"] * L * element["density"]
        cost = mass * element["cost_per_kg"]

        element_results.append({
            "member": element["member"],
            "source_member": element["source_member"],
            "node_i": element["node_i"],
            "node_j": element["node_j"],
            "profile": element["profile"],
            "length_m": L,
            "release_i": element["release_i"],
            "release_j": element["release_j"],
            "N_start_N": N[0],
            "N_end_N": N[-1],
            "Q_start_N": Q[0],
            "Q_end_N": Q[-1],
            "M_start_Nm": M[0],
            "M_end_Nm": M[-1],
            "max_abs_N_N": float(np.max(np.abs(N))),
            "max_abs_Q_N": float(np.max(np.abs(Q))),
            "max_abs_M_Nm": float(np.max(np.abs(M))),
            "max_normal_stress_MPa": max_normal_stress,
            "max_nominal_shear_MPa": max_nominal_shear,
            "mass_kg": mass,
            "cost_EUR": cost,
        })

        diagram_data.append({
            "member": element["member"],
            "node_i": element["node_i"],
            "node_j": element["node_j"],
            "L": L,
            "c": element["c"],
            "s": element["s"],
            "x": x,
            "N": N,
            "Q": Q,
            "M": M,
        })

    displacement_rows = []

    for node in node_ids:
        i = node_to_index[node]
        displacement_rows.append({
            "node": node,
            "ux_mm": u[3 * i] * 1000.0,
            "uy_mm": u[3 * i + 1] * 1000.0,
            "rot_rad": u[3 * i + 2],
            "rot_deg": np.degrees(u[3 * i + 2]),
        })

    reaction_rows = []

    for node in node_ids:
        i = node_to_index[node]
        reaction_rows.append({
            "node": node,
            "Rx_N": reactions[3 * i],
            "Ry_N": reactions[3 * i + 1],
            "Mz_Nm": reactions[3 * i + 2],
        })

    return {
        "nodes": nodes_df,
        "members": members_df,
        "elements": elements,
        "displacements": pd.DataFrame(displacement_rows),
        "reactions": pd.DataFrame(reaction_rows),
        "element_results": pd.DataFrame(element_results),
        "diagram_data": diagram_data,
        "K": K,
        "F": F,
        "u": u,
        "inactive_dofs": inactive_dofs,
    }


# ============================================================
# Plotting
# ============================================================

def compute_deformed_shape_data(results, deformation_scale=1.0, n_points=80):
    """
    Computes the deformed centerline of each beam/frame element.

    The axial displacement is interpolated linearly.
    The transverse displacement is interpolated using cubic Hermite shape functions.
    """

    nodes_df = results["nodes"]
    u_global = results["u"]

    node_xy = {
        str(row["node"]): np.array([float(row["x"]), float(row["y"])])
        for _, row in nodes_df.iterrows()
    }

    deformed_data = []

    for element in results["elements"]:
        ni = element["node_i"]
        nj = element["node_j"]

        pi = node_xy[ni]
        pj = node_xy[nj]

        L = element["L"]
        c = element["c"]
        s = element["s"]

        tangent = np.array([c, s])
        normal = np.array([-s, c])

        dofs = element["dofs"]
        u_global_e = u_global[dofs]

        # Local nodal displacement vector:
        # [u_i, v_i, theta_i, u_j, v_j, theta_j]
        u_local_nodal = element["T"] @ u_global_e

        # Include internally released rotations, if present
        u_local = recover_local_displacements_with_releases(
            u_local_nodal,
            element["k_full_local"],
            element["f_full_local"],
            element["released"],
        )

        u_i = u_local[0]
        v_i = u_local[1]
        th_i = u_local[2]

        u_j = u_local[3]
        v_j = u_local[4]
        th_j = u_local[5]

        x = np.linspace(0.0, L, n_points)
        r = x / L

        # Linear axial interpolation
        u_axial = (1.0 - r) * u_i + r * u_j

        # Cubic Hermite interpolation for transverse displacement
        H1 = 1.0 - 3.0 * r**2 + 2.0 * r**3
        H2 = L * (r - 2.0 * r**2 + r**3)
        H3 = 3.0 * r**2 - 2.0 * r**3
        H4 = L * (-r**2 + r**3)

        v_trans = H1 * v_i + H2 * th_i + H3 * v_j + H4 * th_j

        undeformed_points = pi[None, :] + x[:, None] * tangent[None, :]

        deformed_points = (
            undeformed_points
            + deformation_scale * u_axial[:, None] * tangent[None, :]
            + deformation_scale * v_trans[:, None] * normal[None, :]
        )

        deformed_data.append({
            "member": element["member"],
            "node_i": ni,
            "node_j": nj,
            "x": x,
            "u_axial": u_axial,
            "v_trans": v_trans,
            "undeformed_points": undeformed_points,
            "deformed_points": deformed_points,
        })

    return deformed_data

def plot_structure(nodes_df, members_df, title="Structure"):
    fig = go.Figure()

    node_xy = {
        str(row["node"]): (float(row["x"]), float(row["y"]))
        for _, row in nodes_df.iterrows()
    }

    for _, member in members_df.iterrows():
        ni = clean_string(member["node_i"])
        nj = clean_string(member["node_j"])

        if ni not in node_xy or nj not in node_xy:
            continue

        xi, yi = node_xy[ni]
        xj, yj = node_xy[nj]

        fig.add_trace(go.Scatter(
            x=[xi, xj],
            y=[yi, yj],
            mode="lines",
            line=dict(width=4),
            showlegend=False,
            hovertext=f"{member['member']}: {ni} – {nj}",
            name=str(member["member"]),
        ))

        if to_bool(member.get("release_i", False)):
            fig.add_trace(go.Scatter(
                x=[xi],
                y=[yi],
                mode="markers",
                marker=dict(size=12, symbol="circle-open"),
                showlegend=False,
                hovertext=f"Moment release at {member['member']} / node {ni}",
                name="Moment release",
            ))

        if to_bool(member.get("release_j", False)):
            fig.add_trace(go.Scatter(
                x=[xj],
                y=[yj],
                mode="markers",
                marker=dict(size=12, symbol="circle-open"),
                showlegend=False,
                hovertext=f"Moment release at {member['member']} / node {nj}",
                name="Moment release",
            ))

    fig.add_trace(go.Scatter(
        x=[node_xy[n][0] for n in node_xy],
        y=[node_xy[n][1] for n in node_xy],
        mode="markers+text",
        text=list(node_xy.keys()),
        textposition="top center",
        marker=dict(size=9),
        name="Nodes",
        showlegend=False,
    ))

    fig.update_layout(
        title=title,
        xaxis_title="x [m]",
        yaxis_title="y [m]",
        yaxis_scaleanchor="x",
        height=600,
    )

    return fig

def format_section_value(quantity, value):
    """
    Formats section-force values for compact labels in the plot.
    Internal values are assumed to be:
    N, Q in N
    M in N m
    """

    if quantity in ["N", "Q"]:
        return f"{value / 1000.0:.3f} kN"

    if quantity == "M":
        return f"{value / 1000.0:.3f} kN m"

    return f"{value:.3f}"

def plot_section_diagram(results, quantity="M", scale_factor=0.25, show_extrema=True):
    nodes_df = results["nodes"]
    members_df = results["members"]
    diagram_data = results["diagram_data"]

    fig = plot_structure(
        nodes_df,
        members_df,
        title=f"{quantity}-diagram directly on the structure"
    )

    # The structural system itself should not show coordinate hover data
    # in the section-force plot.
    for trace in fig.data:
        trace.hoverinfo = "skip"
        trace.hovertemplate = None

    node_xy = {
        str(row["node"]): np.array([float(row["x"]), float(row["y"])])
        for _, row in nodes_df.iterrows()
    }

    max_abs_value = 0.0

    for data in diagram_data:
        values = np.asarray(data[quantity], dtype=float)
        max_abs_value = max(max_abs_value, float(np.max(np.abs(values))))

    char_len = characteristic_length(nodes_df)

    if max_abs_value <= 0.0:
        diagram_scale = 0.0
    else:
        # This scale affects only the graphical height of the diagram.
        diagram_scale = scale_factor * char_len / max_abs_value

    unit = {"N": "N", "Q": "N", "M": "N m"}[quantity]

    # Store plotted points and original values for extrema annotation.
    extrema_candidates = []

    for data in diagram_data:
        ni = data["node_i"]
        nj = data["node_j"]

        pi = node_xy[ni]
        pj = node_xy[nj]

        x_local = np.asarray(data["x"], dtype=float)
        L = float(data["L"])

        values = np.asarray(data[quantity], dtype=float)

        tangent_points = pi[None, :] + (x_local / L)[:, None] * (pj - pi)[None, :]
        normal = np.array([-data["s"], data["c"]])

        # Scaled values are used only for drawing.
        diagram_points = tangent_points + (diagram_scale * values)[:, None] * normal[None, :]

        hover_text = [
            (
                f"member: {data['member']}<br>"
                f"local coordinate x: {x_val:.3f} m<br>"
                f"{quantity}: {value:.3f} {unit}"
            )
            for x_val, value in zip(x_local, values)
        ]

        fig.add_trace(go.Scatter(
            x=diagram_points[:, 0],
            y=diagram_points[:, 1],
            mode="lines",
            line=dict(width=3),
            showlegend=False,
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            name=f"{quantity} {data['member']}",
        ))

        # Connector lines between the undeformed structure and the scaled diagram.
        connector_indices = np.linspace(0, len(x_local) - 1, 7, dtype=int)

        for idx in connector_indices:
            fig.add_trace(go.Scatter(
                x=[tangent_points[idx, 0], diagram_points[idx, 0]],
                y=[tangent_points[idx, 1], diagram_points[idx, 1]],
                mode="lines",
                line=dict(width=1, dash="dot"),
                showlegend=False,
                hoverinfo="skip",
            ))

        # Collect extrema candidates from the plotted sampling points.
        if len(values) > 0:
            idx_max = int(np.argmax(values))
            idx_min = int(np.argmin(values))

            extrema_candidates.append({
                "kind": "max",
                "member": data["member"],
                "x_local": x_local[idx_max],
                "value": values[idx_max],
                "point": diagram_points[idx_max],
            })

            extrema_candidates.append({
                "kind": "min",
                "member": data["member"],
                "x_local": x_local[idx_min],
                "value": values[idx_min],
                "point": diagram_points[idx_min],
            })

    # Annotate global maximum and minimum of the selected section force.
    if show_extrema and len(extrema_candidates) > 0 and max_abs_value > 0.0:
        global_max = max(extrema_candidates, key=lambda item: item["value"])
        global_min = min(extrema_candidates, key=lambda item: item["value"])

        extrema_to_plot = [global_max]

        # Avoid duplicate label if maximum and minimum are numerically identical.
        if not np.isclose(global_max["value"], global_min["value"]):
            extrema_to_plot.append(global_min)

        for item in extrema_to_plot:
            label_symbol = "max" if item["kind"] == "max" else "min"

            label = (
                f"{quantity}_{label_symbol} = "
                f"{format_section_value(quantity, item['value'])}"
            )

            hover = (
                f"{quantity}_{label_symbol}<br>"
                f"member: {item['member']}<br>"
                f"local coordinate x: {item['x_local']:.3f} m<br>"
                f"value: {format_section_value(quantity, item['value'])}"
            )

            text_position = "top center" if item["kind"] == "max" else "bottom center"

            fig.add_trace(go.Scatter(
                x=[item["point"][0]],
                y=[item["point"][1]],
                mode="markers+text",
                marker=dict(size=10, symbol="circle-open"),
                text=[label],
                textposition=text_position,
                hovertext=[hover],
                hovertemplate="%{hovertext}<extra></extra>",
                showlegend=False,
                name=label,
            ))

    fig.update_layout(
        title=(
            f"{quantity}-diagram directly on the structure "
            f"(graphical scale factor: {scale_factor:.2f})"
        ),
        xaxis_title="",
        yaxis_title="",
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        ticks="",
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        ticks="",
        scaleanchor="x",
        scaleratio=1,
    )

    return fig

def plot_deformed_shape(results, deformation_scale=1.0):
    """
    Plots undeformed and deformed structure.
    The deformation_scale affects only the graphical representation.
    """

    nodes_df = results["nodes"]
    members_df = results["members"]

    fig = plot_structure(
        nodes_df,
        members_df,
        title="Deformed shape"
    )

    # Make the undeformed structure visually secondary
    for trace in fig.data:
        if hasattr(trace, "line") and trace.line is not None:
            trace.line.width = 2
            trace.opacity = 0.45
        trace.hoverinfo = "skip"
        trace.hovertemplate = None

    deformed_data = compute_deformed_shape_data(
        results,
        deformation_scale=deformation_scale,
        n_points=100,
    )

    for data in deformed_data:
        pts = data["deformed_points"]

        hover_text = [
            (
                f"member: {data['member']}<br>"
                f"local coordinate x: {x_val:.3f} m<br>"
                f"axial displacement u: {u_val * 1000.0:.6f} mm<br>"
                f"transverse displacement v: {v_val * 1000.0:.6f} mm"
            )
            for x_val, u_val, v_val in zip(
                data["x"],
                data["u_axial"],
                data["v_trans"],
            )
        ]

        fig.add_trace(go.Scatter(
            x=pts[:, 0],
            y=pts[:, 1],
            mode="lines",
            line=dict(width=4),
            showlegend=False,
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            name=f"Deformed {data['member']}",
        ))

    fig.update_layout(
        title=(
            f"Deformed shape "
            f"(graphical scale factor: {deformation_scale:.1f})"
        ),
        xaxis_title="",
        yaxis_title="",
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        ticks="",
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        ticks="",
        scaleanchor="x",
        scaleratio=1,
    )

    return fig
    
def show_header_image(filename, caption=None):
    image_path = Path(__file__).parent / "assets" / filename

    if image_path.exists():
        st.image(
            image_path,
            caption=caption,
            width="stretch",
        )
    else:
        st.info(f"Header image not found: {image_path}")

# ============================================================
# Streamlit app
# ============================================================

st.set_page_config(page_title="Beam Me Up", layout="wide")

show_header_image("beam_me_up_header.png")

st.title("Beam Me Up")

st.caption(
    "An interactive beam analysis tool for teaching and learning structural mechanics"
)

with st.expander("How to use the interface", expanded=False):
    st.markdown(
        """
        This app analyzes planar beam and frame structures using Euler-Bernoulli beam elements.
        Each node has three degrees of freedom: horizontal displacement `ux`, vertical displacement `uy`,
        and rotation `rot`.

        The predefined entries form a small example beam. They are only intended as a guide and can
        be overwritten. You can rename nodes and members directly in the tables by replacing labels
        such as `A`, `B`, or `B1`.

        **Nodes**  
        Enter the node labels and their Cartesian coordinates `x` and `y`.
        
        A new node is required whenever a point has mechanical relevance in the model. This is the case in particular when:
        - a member starts or ends at that point,
        - a support is located at that point,
        - a nodal force or nodal moment is applied at that point,
        - the geometry changes direction, for example at a kink or corner of a frame,
        - several members are connected at that point,

        **Members**  
        Define each beam or frame member by specifying its start node `node_i`, its end node `node_j`,
        and a profile. The options `release_i` and `release_j` create moment releases at the
        corresponding member ends. 'True' means, the specific member cannot transfer moments at ist end
        i and/or j.

        **Supports**  
        Use `fix_x`, `fix_y`, and `fix_rot` to restrain horizontal displacement, vertical displacement,
        and rotation. A full clamped support is obtained by activating all three options.

        **Nodal loads**  
        Enter external nodal loads as `Fx`, `Fy`, and `Mz`.

        **Distributed loads**  
        Enter constant distributed loads in the local member coordinate system. For a horizontal member
        from left to right, local `y` points upward. Therefore, a downward vertical load is usually
        entered as a negative `qy_local`.

        **Internal hinges**  
        Internal hinges can be positioned along a member by entering the member name and the relative
        coordinate `xi`, where `xi = 0` is the start node and `xi = 1` is the end node. The app splits
        the member internally and applies moment releases at the generated hinge node.

        **Adding entries**  
        Click the `+` symbol in the bottom row of each table to add new nodes, members, supports,
        loads, or internal hinges.

        **Calculation**  
        Click **Calculate frame** to compute displacements, reactions, section-force diagrams,
        stresses, mass, and estimated costs.
        """
    )

with st.expander("Model assumptions and limitations", expanded=False):
    st.markdown(
        """
        The current version uses a linear-elastic Euler-Bernoulli beam formulation.
        It assumes small displacements, straight members, constant cross-sections per member,
        and constant distributed loads in local element directions.

        The app currently does not include shear deformation, geometrical nonlinearity, plasticity,
        buckling checks, nonlinear supports, moving loads, or code-compliant structural design checks.

        Sign convention: `N > 0` denotes tension. The plotted `Q` and `M` diagrams follow the local
        element convention. For a simply supported horizontal beam with downward `qy_local < 0`,
        the sagging bending moment appears positive.
        """
    )

with st.expander("License, attribution, and disclaimer", expanded=False):
    st.markdown(
        """
        **Copyright**  
        © 2026 Thorsten Bartel.

        **AI-assisted development**  
        The concept, user interface structure, and parts of the Python/Streamlit implementation were
        developed with assistance from OpenAI ChatGPT, GPT-5.5 Thinking, June 2026.

        **Third-party software**  
        This app is implemented in Python using Streamlit, NumPy, pandas, and Plotly. These packages
        are distributed under their respective open-source licenses.

        **Disclaimer**  
        This app is intended for teaching and demonstration purposes only. It does not replace
        professional engineering verification, safety assessment, or code-compliant structural design.
        """
    )


# ------------------------------------------------------------
# Default example
# ------------------------------------------------------------

default_nodes = pd.DataFrame({
    "node": ["A", "B"],
    "x": [0.0, 6.0],
    "y": [0.0, 0.0],
})

default_members = pd.DataFrame({
    "member": ["B1"],
    "node_i": ["A"],
    "node_j": ["B"],
    "profile": ["Generic steel medium"],
    "release_i": [False],
    "release_j": [False],
})

default_supports = pd.DataFrame({
    "node": ["A", "B"],
    "fix_x": [True, False],
    "fix_y": [True, True],
    "fix_rot": [False, False],
})

default_nodal_loads = pd.DataFrame({
    "node": ["B"],
    "Fx": [0.0],
    "Fy": [0.0],
    "Mz": [0.0],
})

default_distributed_loads = pd.DataFrame({
    "member": ["B1"],
    "qx_local": [0.0],
    "qy_local": [-1000.0],
})

default_hinges = pd.DataFrame({
    "member": [""],
    "xi": [0.5],
    "hinge_node": ["H1"],
})


left, right = st.columns([1, 1])

with left:
    st.subheader("Input data")

    st.write("### Nodes")
    nodes_df = st.data_editor(
        default_nodes,
        num_rows="dynamic",
        width="stretch",
    )

    st.write("### Members")
    members_df = st.data_editor(
        default_members,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "profile": st.column_config.SelectboxColumn(
                "profile",
                options=list(PROFILE_CATALOGUE.keys()),
            )
        },
    )

    st.write("### Supports")
    supports_df = st.data_editor(
        default_supports,
        num_rows="dynamic",
        width="stretch",
    )

    st.write("### Nodal loads")
    nodal_loads_df = st.data_editor(
        default_nodal_loads,
        num_rows="dynamic",
        width="stretch",
    )

    st.write("### Distributed member loads")
    distributed_loads_df = st.data_editor(
        default_distributed_loads,
        num_rows="dynamic",
        width="stretch",
    )

    st.write("### Internal hinges")
    hinges_df = st.data_editor(
        default_hinges,
        num_rows="dynamic",
        width="stretch",
    )

with right:
    st.subheader("Profile catalogue")

    profile_table = pd.DataFrame(PROFILE_CATALOGUE).T.reset_index()
    profile_table = profile_table.rename(columns={"index": "profile"})
    st.dataframe(profile_table, width="stretch")

    st.subheader("Structure preview")
    try:
        preview_nodes, preview_members = preprocess_internal_hinges(
            nodes_df.copy(),
            members_df.copy(),
            hinges_df.copy(),
        )
        st.plotly_chart(
            plot_structure(preview_nodes, preview_members, title="Structure preview"),
            width="stretch",
        )
    except Exception as e:
        st.warning(f"Preview could not be generated: {e}")


# ------------------------------------------------------------
# Calculation and persistent state
# ------------------------------------------------------------

if "frame_results" not in st.session_state:
    st.session_state.frame_results = None

if "frame_error" not in st.session_state:
    st.session_state.frame_error = None


if st.button("Calculate frame", type="primary"):
    try:
        st.session_state.frame_results = solve_frame(
            nodes_df,
            members_df,
            supports_df,
            nodal_loads_df,
            distributed_loads_df,
            hinges_df,
        )
        st.session_state.frame_error = None

    except Exception as e:
        st.session_state.frame_results = None
        st.session_state.frame_error = str(e)


if st.session_state.frame_error is not None:
    st.error(st.session_state.frame_error)


if st.session_state.frame_results is not None:
    results = st.session_state.frame_results

    st.success("Calculation completed.")

    if len(results["inactive_dofs"]) > 0:
        st.info(
            "Some inactive zero-stiffness degrees of freedom were automatically constrained. "
            "This can occur at pure hinge rotations."
        )

    st.subheader("Section-force diagrams")

    st.subheader("Deformed shape")

    deformation_scale = st.slider(
        "Graphical deformation scale factor",
        min_value=1.0,
        max_value=1000.0,
        value=100.0,
        step=10.0,
        key="deformation_scale",
    )

    st.plotly_chart(
        plot_deformed_shape(
            results,
            deformation_scale=deformation_scale,
        ),
        width="stretch",
    )

    diagram_scale = st.slider(
        "Diagram scale factor",
        min_value=0.05,
        max_value=1.00,
        value=0.25,
        step=0.05,
        key="diagram_scale",
    )

    tab_n, tab_q, tab_m = st.tabs(["N diagram", "Q diagram", "M diagram"])

    with tab_n:
        st.plotly_chart(
            plot_section_diagram(results, quantity="N", scale_factor=diagram_scale),
            width="stretch",
        )

    with tab_q:
        st.plotly_chart(
            plot_section_diagram(results, quantity="Q", scale_factor=diagram_scale),
            width="stretch",
        )

    with tab_m:
        st.plotly_chart(
            plot_section_diagram(results, quantity="M", scale_factor=diagram_scale),
            width="stretch",
        )

    st.subheader("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Support reactions")
        reactions = results["reactions"].copy()
        reactions["Rx_N"] = reactions["Rx_N"].round(3)
        reactions["Ry_N"] = reactions["Ry_N"].round(3)
        reactions["Mz_Nm"] = reactions["Mz_Nm"].round(3)
        st.dataframe(reactions, width="stretch")

    with col2:
        st.write("### Nodal displacements")
        displacements = results["displacements"].copy()
        displacements["ux_mm"] = displacements["ux_mm"].round(6)
        displacements["uy_mm"] = displacements["uy_mm"].round(6)
        displacements["rot_rad"] = displacements["rot_rad"].round(8)
        displacements["rot_deg"] = displacements["rot_deg"].round(6)
        st.dataframe(displacements, width="stretch")

    st.write("### Member results")

    element_results = results["element_results"].copy()

    for col in [
        "length_m",
        "N_start_N",
        "N_end_N",
        "Q_start_N",
        "Q_end_N",
        "M_start_Nm",
        "M_end_Nm",
        "max_abs_N_N",
        "max_abs_Q_N",
        "max_abs_M_Nm",
        "max_normal_stress_MPa",
        "max_nominal_shear_MPa",
        "mass_kg",
        "cost_EUR",
    ]:
        element_results[col] = element_results[col].round(3)

    st.dataframe(element_results, width="stretch")

    total_mass = results["element_results"]["mass_kg"].sum()
    total_cost = results["element_results"]["cost_EUR"].sum()

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Total material mass", f"{total_mass:.3f} kg")

    with col4:
        st.metric("Estimated material cost", f"{total_cost:.2f} €")