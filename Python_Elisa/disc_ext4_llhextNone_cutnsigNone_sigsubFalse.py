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

mp_cpus = 5
ana_dir = utils.ensure_dir ('/data/user/drysewyk/csky_cache/ana_new')
repo = selections.mrichman_repo
ana7 = analysis.Analysis (repo, selections.PSDataSpecs.ps_7yr, dir=ana_dir)

def get_llh (a, src, cut_n_sigma, sigsub):
    # space PDF - use default background space PDF and signal acceptance parameterization
    space_model = pdf.PointSourceSpacePDFRatioModel ( a, src, a.bg_space_param, a.acc_param, cut_n_sigma=cut_n_sigma, sigsub=sigsub )
    # energy PDF - use default parameterization
    energy_model = a.energy_pdf_ratio_model
    # put it together
    pdf_ratio_model = pdf.MultiPDFRatioModel (space_model, energy_model)
    N = len (a.data)
    llh_model = llh.LLHModel (pdf_ratio_model, N, cut_n_sigma=cut_n_sigma, sigsub=sigsub)
    return llh_model

def get_injs (a, llh_model, src, llh_src, flux, cut_n_sigma, inj):
    # note which event features we need
    keep = llh_model.pdf_ratio_model.keep
    # optimization: dec band cut
    selector = cy.inj.DecBandSelector (llh_src, cut_n_sigma=cut_n_sigma)
    # truth: unscrambled data, for unblinding
    truth = cy.inj.DataInjector (a, selector (a.data), keep, randomizers=[])
    # bg: scrambled data
    randomizers = [cy.inj.RARandomizer ()]#, cy.inj.DecRandomizer()]#, cy.inj.PoleRandomizer (np.radians (30))]
    bg = cy.inj.DataInjector (a, selector (a.data), keep, randomizers=randomizers)
    # sig: signal injection
    sig = cy.inj.PointSourceInjector (a, src, flux, keep) if inj else None
    return truth, bg, sig

def get_tr (src, ana=ana7, ext=np.radians(0), llh_ext=None, flux=hyp.PowerLawFlux (2), inj=True, use_energy=True, cut_n_sigma=None, sigsub=False, _fit_null=\
True, mp_cpus=mp_cpus):
    llh_ext = ext if llh_ext is None else llh_ext
    llh_src = cy.utils.Sources(ra=src.ra, dec=src.dec, extension=llh_ext)

    if cut_n_sigma is None:
        cut_n_sigma = 5 if llh_ext < np.radians(3) else 3

    # get_llh needs the src list
    llh_kw = dict (src=llh_src, cut_n_sigma=cut_n_sigma, sigsub=sigsub)
    # get_injs needs the src list and signal spectrum
    inj_kw = dict (src=src, llh_src=llh_src, flux=flux, cut_n_sigma=cut_n_sigma, inj=inj)
    # trial.get_trial_runner loops over sub analyses and gives a single TrialRunner
    return trial.get_trial_runner (
        ana, get_llh, get_injs, llh_kw=llh_kw, inj_kw=inj_kw, mp_cpus=mp_cpus)

def get_sens(ana, ra, sindec, ext=np.radians(0), llh_ext=None, cut_n_sigma=None, sigsub=False, gamma=2, batch_size=500):
    src = cy.utils.Sources(ra=0, dec=np.arcsin(sindec),extension=ext)
    flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src=src, ana=ana, ext=ext, llh_ext=llh_ext, flux=flux, cut_n_sigma=cut_n_sigma, sigsub=sigsub)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(1000))
    sens = tr.find_n_sig(bg.median(),0.9,batch_size=batch_size,max_batch_size=1000,tol=0.03, coverage=2)
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

def get_disc(ana, ra, sindec, ext=np.radians(0), llh_ext=None, cut_n_sigma=None, sigsub=False, gamma=2, batch_size=500):
    src = cy.utils.Sources(ra=0, dec=np.arcsin(sindec),extension=ext)
    flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src=src, ana=ana, ext=ext, llh_ext=llh_ext, flux=flux, cut_n_sigma=cut_n_sigma, sigsub=sigsub)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(1000))
    sens = tr.find_n_sig(bg.isf_nsigma(5,fit=True),0.5,batch_size=batch_size,max_batch_size=1000,tol=0.03, coverage=2)
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

# llh_ext=None for extended source analysis on an extended source
# llh_ext=0 for point source analysis on an extended source

sindec_array = np.linspace(-0.98,0.98,50)
disc_4 = [get_disc(ana7,ra=0,sindec=d,ext=np.radians(4),llh_ext=None, cut_n_sigma=None, gamma=2, sigsub=False) for d in sindec_array]
np.save('/data/user/drysewyk/llh_sandbox/NumPyArrays/DiscoveryPotential/disc_4ext_llhextNone_cutnsigNone_gamma2_sigsubFalse_50bins.npy',disc_4)


