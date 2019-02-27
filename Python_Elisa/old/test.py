from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from csky.ipyconfig import *
from csky import bk, analysis, coord, dists, hyp, inj, llh, pdf, selections, trial, utils
import csky as cy
import histlite as hl
import healpy as hp
import numpy as np


#from icecube import astro

mp_cpus = 1

ana_dir = utils.ensure_dir ('/data/user/drysewyk/csky_cache/ana_new')
repo = selections.mrichman_repo
ana7 = analysis.Analysis (repo, selections.PSDataSpecs.ps_7yr, dir=ana_dir)

def get_llh (a, src, sigsub):
    # space PDF - use default background space PDF and signal acceptance parameterization
    space_model = pdf.PointSourceSpacePDFRatioModel ( a, src, a.bg_space_param, a.acc_param, sigsub=sigsub )
    # energy PDF - use default parameterization
    energy_model = a.energy_pdf_ratio_model
    # put it together
    pdf_ratio_model = pdf.MultiPDFRatioModel (space_model, energy_model)
    N = len (a.data)
    llh_model = llh.LLHModel (pdf_ratio_model, N, sigsub=sigsub)
    return llh_model

def get_injs (a, llh_model, src, flux, cut_n_sigma, inj):
    # note which event features we need
    keep = llh_model.pdf_ratio_model.keep
    # optimization: dec band cut
    selector = cy.inj.DecBandSelector (src, cut_n_sigma=cut_n_sigma)
    # truth: unscrambled data, for unblinding
    truth = cy.inj.DataInjector (a, selector (a.data), keep, randomizers=[])
    # bg: scrambled data
    randomizers = [cy.inj.RARandomizer ()]#, cy.inj.DecRandomizer()]#, cy.inj.PoleRandomizer (np.radians (30))]
    bg = cy.inj.DataInjector (a, selector (a.data), keep, randomizers=randomizers)
    # sig: signal injection
    sig = cy.inj.PointSourceInjector (a, src, flux, keep) if inj else None
    return truth, bg, sig

def get_tr (src, ana=ana7, flux=hyp.PowerLawFlux (2), inj=True, use_energy=True, cut_n_sigma=5, sigsub=False, _fit_null=True, mp_cpus=mp_cpus):
    # get_llh needs the src list
    llh_kw = dict (src=src, sigsub=sigsub)
    # get_injs needs the src list and signal spectrum
    inj_kw = dict (src=src, flux=flux, cut_n_sigma=cut_n_sigma, inj=inj)
    # trial.get_trial_runner loops over sub analyses and gives a single TrialRunner
    return trial.get_trial_runner (
        ana, get_llh, get_injs, llh_kw=llh_kw, inj_kw=inj_kw, mp_cpus=mp_cpus)


def get_getters (ana=ana7, extension=0, cut_n_sigma=3, sigsub=False):
    def get_tr_skymap (src=None, cut_n_sigma=3, _fit_null=True, inj=True):
        if src is None:
            src = utils.Sources (ra=0, dec=0, extension=extension)
        src['extension'] = extension * np.ones_like (src.dec)
        return get_tr (src, ana=ana, cut_n_sigma=cut_n_sigma, sigsub=sigsub, _fit_null=_fit_null, inj=inj)
    def get_selector (dec):
        return inj.DecBandSelector (utils.Sources (dec=dec, extension=extension))
    return get_tr_skymap, get_selector

def plot_result (v, clabel, title='', vmin=None, vmax=None, cmap='viridis', projection='aitoff'):
    if vmin is None:
        vmin = 0
    if vmax is None:
        vmax = np.ceil (v.max())
    fig, ax = plt.subplots (figsize=(8,6), subplot_kw=dict (projection=projection))
    sp = csp.SkyPlotter (pc_kw=dict (cmap=cmap, vmin=vmin, vmax=vmax))
    v = hp.ud_grade (v, 256)
    mesh, cb = sp.plot_map (ax, v, n_ticks=2, titleticks=bool (title))
    sp.plot_gp (ax, color='.5', lw=.5, alpha=.25)
    ax.grid (alpha=.5, ls='-')
    cb.set_label (clabel)
    ax.set_title (title)
    plt.tight_layout()
    return fig, ax 

src_1 = cy.utils.Sources (ra=0, dec=0, extension=np.radians (1))
src_2 = cy.utils.Sources (ra=0, dec=0, extension=np.radians (2))
src_3 = cy.utils.Sources (ra=0, dec=0, extension=np.radians (3))
src_4 = cy.utils.Sources (ra=0, dec=0, extension=np.radians (4))
src_5 = cy.utils.Sources (ra=0, dec=0, extension=np.radians (5))

tr_1 = get_tr (src_1, ana7)
tr_2 = get_tr (src_2, ana7)
tr_3 = get_tr (src_3, ana7)
tr_4 = get_tr (src_4, ana7)
tr_5 = get_tr (src_5, ana7)


bg_1 = cy.dists.Chi2TSD (tr_1.get_many_fits (50000))
np.save('/data/user/drysewyk/llh_sandbox/Background/bg_1_50000fits_test.npy',bg_1)
bg_2 = cy.dists.Chi2TSD (tr_2.get_many_fits (50000))
np.save('/data/user/drysewyk/llh_sandbox/Background/bg_2_50000fits_test.npy',bg_2)
bg_3 = cy.dists.Chi2TSD (tr_3.get_many_fits (50000))
np.save('/data/user/drysewyk/llh_sandbox/Background/bg_3_50000fits_test.npy',bg_3)
bg_4 = cy.dists.Chi2TSD (tr_4.get_many_fits (50000))
np.save('/data/user/drysewyk/llh_sandbox/Background/bg_4_50000fits_test.npy',bg_4)
bg_5 = cy.dists.Chi2TSD (tr_5.get_many_fits (50000))
np.save('/data/user/drysewyk/llh_sandbox/Background/bg_5_50000fits_test.npy',bg_5)
