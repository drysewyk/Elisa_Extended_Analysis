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

mp_cpus = 5

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

def get_sens(ana,ra,sindec,ext,gamma,batch_size=500):
    src = cy.utils.Sources(ra=0, dec=np.arcsin(sindec),extension=np.radians(ext))
    #flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src, ana)#, flux=flux)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(500))
    sens = tr.find_n_sig(bg.median(),0.9,batch_size=batch_size,max_batch_size=1000,tol=0.03) 
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

def get_sens_sigsub(ana,ra,sindec,ext,gamma,batch_size=500):
    src = cy.utils.Sources(ra=0, dec=np.arcsin(sindec),extension=np.radians(ext))
    #flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src, ana, sigsub=True)#, flux=flux)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(500))
    sens = tr.find_n_sig(bg.median(),0.9,batch_size=batch_size,max_batch_size=1000,tol=0.03) 
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

def get_discovery(ana,ra,sindec,ext,gamma,batch_size=500):
    src = utils.Sources(ra=0, dec=np.arcsin(sindec),extension=np.radians(ext))
    #flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src, ana)#, flux=flux)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(500))
    sens = tr.find_n_sig(bg.isf_nsigma(5,fit=True),0.5,batch_size=batch_size,max_batch_size=1000,tol=0.03) 
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

def get_discovery_sigsub(ana,ra,sindec,ext,gamma,batch_size=500):
    src = utils.Sources(ra=0, dec=np.arcsin(sindec),extension=np.radians(ext))
    #flux = hyp.PowerLawFlux(gamma)
    tr = get_tr(src, ana, sigsub=True)#, flux=flux)
    bg = cy.dists.Chi2TSD(tr.get_many_fits(500))
    sens = tr.find_n_sig(bg.isf_nsigma(5,fit=True),0.5,batch_size=batch_size,max_batch_size=1000,tol=0.03) 
    sens['flux'] = tr.to_E2dNdE(sens['n_sig'], E0=100, unit=1e3)
    return sens['flux']

dec_array = np.linspace(-0.98,0.98,30)
disc_0 = [get_discovery(ana7,ra=0,sindec=d,ext=0,gamma=2) for d in dec_array]
np.save('/data/user/drysewyk/llh_sandbox/NumPyArrays/DiscoveryPotential/disc_0_30bins.npy',disc_0)
