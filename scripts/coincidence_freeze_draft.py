#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
coincidence_freeze_draft.py -- Axis 1 methodology paper, M1 support.

Generates the DRAFT frozen-observable list (machine-readable mirror of
canonical/papers/counting_coincidences/freeze/OBSERVABLES_FREEZE.md).

v1 (2026-06-12): values verified against PRIMARY sources by four research
agents with per-value citations (CODATA 2022 / PDG 2025 / NuFIT 6.1 / Planck
2018); see OBSERVABLES_FREEZE.md section 2 for the citation table. Derived
ratios are computed HERE from the verified primary inputs with first-order
error propagation (uncorrelated; asymmetric errors symmetrized to the larger
side, PLAN.md D11). Status 'agent-verified' means: read on a fetched primary
source by an agent; human spot-check still pending before deposit (PLAN.md
TODO).

This is DATA ASSEMBLY, not expression search (PLAN.md discipline rule 1).

Output: freeze/observables_freeze_draft.json
"""

import json
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   'freeze',
                   'observables_freeze_draft.json')


def ratio(num, num_err, den, den_err):
    """x/y with first-order uncorrelated propagation."""
    r = num / den
    return r, abs(r) * math.hypot(num_err / num, den_err / den)


# ----------------------------------------------------------------------
# Verified primary inputs (agent pass 2026-06-12, citations in
# OBSERVABLES_FREEZE.md). Units as stated; asymmetric errors already
# symmetrized to the larger side (D11).
# ----------------------------------------------------------------------
P = {
    # CODATA 2022 / PDG 2025 physical constants
    'alpha_inv_0':   (137.035999177, 0.000000021, 'CODATA 2022'),
    'alpha_s_MZ':    (0.1180, 0.0009, 'PDG 2025 Table 1.1'),
    'sin2hat_MZ':    (0.23122, 0.00006, 'PDG 2025 Table 1.1 (MS-bar)'),
    # PDG 2025 boson masses (GeV) + derived v (GeV)
    'm_W':           (80.3692, 0.0133, 'PDG 2025 Summary Tables (CDF-2022 excluded)'),
    'm_Z':           (91.1880, 0.0020, 'PDG 2025 Summary Tables'),
    'm_H':           (125.20, 0.11, 'PDG 2025 Summary Tables (S=1.4)'),
    'v_EW':          (246.21965, 0.00006, 'derived from CODATA 2022 G_F'),
    # PDG 2025 lepton masses (MeV)
    'm_e':           (0.51099895000, 0.00000000015, 'PDG 2025 Lepton Summary'),
    'm_mu':          (105.6583755, 0.0000023, 'PDG 2025 Lepton Summary'),
    'm_tau':         (1776.93, 0.09, 'PDG 2025 Lepton Summary'),
    # PDG 2025 Quark Masses review, lattice averages, MS-bar (D13 surface)
    'mu_over_md':    (0.473, 0.017, 'PDG 2025 QM review Eq. 60.9'),
    'ms_over_mud':   (27.30, 0.08, 'PDG 2025 QM review Eq. 60.6'),
    'm_s_2GeV':      (92.74, 0.54, 'PDG 2025 QM review Eq. 60.5 (MeV)'),
    'm_c_mc':        (1275.0, 9.0, 'PDG 2025 QM review Eq. 60.23 (MeV)'),
    'm_b_mb':        (4196.0, 12.0, 'PDG 2025 QM review Eq. 60.24 (MeV)'),
    'm_t_msbar':     (162500.0, 2100.0, 'PDG 2025 Quark Summary, x-sec (MeV; D14)'),
    # PDG 2025 CKM review global fit Eq. 12.26 (main fit, not UTfit variant)
    'lambda_W':      (0.22501, 0.00068, 'PDG 2025 CKM review Eq. 12.26'),
    'A_W':           (0.826, 0.016, 'PDG 2025 CKM review Eq. 12.26'),
    'rho_bar':       (0.1591, 0.0094, 'PDG 2025 CKM review Eq. 12.26'),
    'eta_bar':       (0.3523, 0.0073, 'PDG 2025 CKM review Eq. 12.26'),
    # NuFIT 6.1, NO, IC23 WITHOUT SK-atm (D6), v61.tbl-parameters
    'sin2_t12':      (0.3088, 0.0067, 'NuFIT 6.1 NO w/o SK-atm'),
    'sin2_t23':      (0.470, 0.017, 'NuFIT 6.1 NO w/o SK-atm'),
    'sin2_t13':      (0.02249, 0.00057, 'NuFIT 6.1 NO w/o SK-atm'),
    'delta_CP':      (207.0, 23.0, 'NuFIT 6.1 NO w/o SK-atm (degrees)'),
    'dm2_21':        (7.537e-5, 0.10e-5, 'NuFIT 6.1 NO w/o SK-atm (eV^2)'),
    'dm2_3l':        (2.521e-3, 0.026e-3, 'NuFIT 6.1 NO w/o SK-atm (eV^2)'),
    # Planck 2018 VI Table 2, TT,TE,EE+lowE+lensing
    'Ob_h2':         (0.02237, 0.00015, 'Planck VI Table 2'),
    'Oc_h2':         (0.1200, 0.0012, 'Planck VI Table 2'),
    'O_L':           (0.6847, 0.0073, 'Planck VI Table 2'),
    'O_m':           (0.3153, 0.0073, 'Planck VI Table 2'),
    'n_s':           (0.9649, 0.0042, 'Planck VI Table 2'),
    'sigma_8':       (0.8111, 0.0060, 'Planck VI Table 2'),
    'Y_p':           (0.245, 0.003, 'PDG BBN review Eq. 24.3 (observational, D15)'),
    'eta_10':        (6.12, 0.04, 'PDG BBN review sec. 24.4 (from Planck Ob_h2)'),
    'Onu_h2':        (0.00064, 0.0, 'Planck baseline Sum m_nu = 0.06 eV'),
}


def E(name, category, convention, value, error, source, status, note=''):
    return {'name': name, 'category': category, 'convention': convention,
            'value': value, 'error': error, 'source': source,
            'status': status, 'verify_primary': status != 'agent-verified',
            'note': note}


def prim(name, category, convention, key, note=''):
    v, e, src = P[key]
    return E(name, category, convention, v, e, src, 'agent-verified', note)


def der(name, category, convention, numk, denk, note=''):
    nv, ne, ns = P[numk]
    dv, de, ds = P[denk]
    v, e = ratio(nv, ne, dv, de)
    return E(name, category, convention, round(v, 10), round(e, 10),
             f'{ns} / {ds}', 'agent-verified',
             (note + ' ' if note else '') + 'derived ratio, first-order propagation')


entries = [
    # Cat A. Gauge couplings (reference points per D12)
    prim('alpha_inv_0', 'A_gauge', 'q^2 = 0 (Thomson limit), CODATA 2022',
         'alpha_inv_0', 'D12: zero-momentum value, convention-free'),
    prim('alpha_s_MZ', 'A_gauge', 'MS-bar at M_Z', 'alpha_s_MZ'),
    prim('sin2_theta_W_MSbar', 'A_gauge', 'MS-bar at M_Z (sin^2 theta-hat)',
         'sin2hat_MZ', 'D12: resolves v0 flag (NOT the eff. leptonic 0.23155)'),
    # Cat B. Charged lepton mass ratios
    der('m_mu_over_m_e', 'B_lepton_ratios', 'pole masses', 'm_mu', 'm_e'),
    der('m_tau_over_m_mu', 'B_lepton_ratios', 'pole masses', 'm_tau', 'm_mu'),
    # Cat C. Quark mass ratios (D7 MS-bar; D13 lattice-average surface)
    prim('m_u_over_m_d', 'C_quark_ratios', 'MS-bar 2 GeV, direct lattice ratio',
         'mu_over_md'),
    prim('m_s_over_m_ud', 'C_quark_ratios', 'MS-bar 2 GeV, m_ud = (m_u+m_d)/2',
         'ms_over_mud', 'replaces v0 m_s/m_d: PDG quotes only a 17-22 band for it'),
    der('m_c_over_m_s', 'C_quark_ratios', 'm_c(m_c) / m_s(2 GeV), mixed ref points',
        'm_c_mc', 'm_s_2GeV', 'resolves v0 conflict (11.7 was scale-mismatched);'),
    der('m_b_over_m_c', 'C_quark_ratios', 'm_b(m_b) / m_c(m_c)', 'm_b_mb', 'm_c_mc'),
    der('m_t_over_m_b', 'C_quark_ratios', 'm_t(x-sec, MS-bar-type) / m_b(m_b), D14',
        'm_t_msbar', 'm_b_mb'),
    # Cat D. CKM (PDG global fit, main prescription)
    prim('lambda_Wolfenstein', 'D_CKM', 'PDG Wolfenstein, global fit', 'lambda_W'),
    prim('A_Wolfenstein', 'D_CKM', 'PDG Wolfenstein, global fit', 'A_W',
         'main fit 0.826(16); v0 carried the UTfit variant 0.839(11)'),
    prim('rho_bar', 'D_CKM', 'PDG Wolfenstein, global fit', 'rho_bar'),
    prim('eta_bar', 'D_CKM', 'PDG Wolfenstein, global fit', 'eta_bar'),
    # Cat E. PMNS + neutrino mass ratio (D6: NO, w/o SK-atm)
    prim('sin2_theta12_PMNS', 'E_PMNS', 'NuFIT 6.1 NO w/o SK-atm', 'sin2_t12'),
    prim('sin2_theta23_PMNS', 'E_PMNS', 'NuFIT 6.1 NO w/o SK-atm', 'sin2_t23'),
    prim('sin2_theta13_PMNS', 'E_PMNS', 'NuFIT 6.1 NO w/o SK-atm', 'sin2_t13',
         'DISCREPANCY vs internal obs.json (0.02224): spot-check, may touch FoP S-docs'),
    prim('delta_CP_degrees', 'E_PMNS', 'degrees, NuFIT 6.1 NO w/o SK-atm', 'delta_CP'),
    der('dm2_21_over_abs_dm2_3l', 'E_PMNS', 'NuFIT 6.1 NO convention dm2_3l = dm2_31',
        'dm2_21', 'dm2_3l'),
    # Cat F. Boson mass ratios (D-decision: m_H/v over lambda_H)
    der('m_W_over_m_Z', 'F_boson_ratios', 'pole', 'm_W', 'm_Z'),
    der('m_H_over_m_Z', 'F_boson_ratios', 'pole', 'm_H', 'm_Z'),
    der('m_H_over_v', 'F_boson_ratios', 'pole / vev(G_F)', 'm_H', 'v_EW',
        'chosen over lambda_H (no factor-2 convention ambiguity);'),
    # Cat G. Cosmology (Planck VI Table 2 column TT,TE,EE+lowE+lensing)
    E('Omega_b_over_Omega_m', 'G_cosmology', 'flat LCDM, with nu correction',
      *ratio(P['Ob_h2'][0], P['Ob_h2'][1],
             P['Ob_h2'][0] + P['Oc_h2'][0] + P['Onu_h2'][0],
             math.hypot(P['Ob_h2'][1], P['Oc_h2'][1])),
      'Planck VI Table 2 (Ob_h2, Oc_h2, Onu_h2)', 'agent-verified',
      'derived; Omega_m h^2 = Ob + Oc + Onu contributions'),
    der('Omega_m_over_Omega_Lambda', 'G_cosmology', 'flat LCDM', 'O_m', 'O_L',
        'uncorrelated propagation is conservative vs flatness anticorrelation;'),
    prim('n_s', 'G_cosmology', 'Planck 2018 baseline', 'n_s'),
    prim('sigma_8', 'G_cosmology', 'Planck 2018 baseline', 'sigma_8',
         'DISCREPANCY vs internal obs.json (0.807): spot-check'),
    prim('Y_p', 'G_cosmology', 'observational (PDG BBN Eq. 24.3), per D15', 'Y_p'),
    prim('eta_10', 'G_cosmology', 'eta_B x 10^10, from Planck Ob_h2 via PDG 274 conv.',
         'eta_10', 'independent of admitted Omega ratios (absolute baryon density)'),
]

# round derived values for readability (errors to 2 sig figs equivalent)
for e in entries:
    if e['value'] is not None and isinstance(e['value'], float):
        e['value'] = float(f"{e['value']:.8g}")
        e['error'] = float(f"{e['error']:.3g}")

doc = {
    'meta': {
        'status': 'DRAFT v1 -- agent-verified, human spot-check pending, NOT deposited',
        'paper': 'counting_coincidences (Axis 1 methodology paper)',
        'criteria': 'OBSERVABLES_FREEZE.md sections 1 and 3',
        'conventions': 'PLAN.md decisions D6, D7, D11, D12, D13, D14, D15',
        'discipline': 'no expression search against these values before DOI deposit',
        'verification': 'four research agents, primary sources fetched, 2026-06-12',
        'generator': 'scripts/coincidence_freeze_draft.py',
        'n_entries': len(entries),
        'n_agent_verified': sum(1 for e in entries if e['status'] == 'agent-verified'),
    },
    'primary_inputs': {k: {'value': v, 'error': err, 'source': s}
                       for k, (v, err, s) in P.items()},
    'entries': entries,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)

m = doc['meta']
print(f"wrote {os.path.relpath(OUT)}")
print(f"entries: {m['n_entries']} | agent-verified: {m['n_agent_verified']}")
for e in entries:
    val = f"{e['value']:.6g}" if e['value'] is not None else '-'
    err = f"{e['error']:.3g}" if e['error'] is not None else '-'
    disc = ' <-- DISCREPANCY' if 'DISCREPANCY' in e.get('note', '') else ''
    print(f"  {e['category']:<16} {e['name']:<26} {val:<12} +/- {err}{disc}")
