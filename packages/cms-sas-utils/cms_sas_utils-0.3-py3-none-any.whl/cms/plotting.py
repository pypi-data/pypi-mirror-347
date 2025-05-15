from ijazz.categorize import categorize
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import cms_fstyle as cms
import numpy as np
import pandas as pd
from typing import Union, List, Dict, Tuple

  

def create_fig(n_subfig: int=1) -> tuple[Figure, Figure]:
    """Create a figure with subfigures if requested

    Args:
        n_subfig (int, optional): number of sub-figures (either 1 or 2). Defaults to 1.

    Returns:
        tuple[Figure, Figure]: tuple of figures or subfigures when creating sub-figures
    """
    fig = plt.figure(figsize=(7 * n_subfig, 7), layout='constrained') 
    fig1 = fig
    fig2 = None
    if n_subfig > 1:
        fig1, fig2 = fig.subfigures(1, 2)
    return fig1, fig2


def plot_mll_data_per_cat(dt: List[pd.DataFrame], mc: List[pd.DataFrame], cut0:str=None,
                          mll_name1:str="mee", mll_name2: str=None, pt_name1:str=None, pt_name2:str=None, 
                          var_name:str=None, var_cats:str=None, var_latex:str=None, var_unit:str='',
                          var_prefixes:List[str]=None, var_suffixes:List[str]=['1','2'], 
                          mc_w_name:str=None, both_leptons=False, lead_electron=False, is_comparison=False,**kwargs) -> Tuple[List[Figure], Tuple[List[float], List[float]]]:
    """Make data/MC plot comparison of the di-lepton mass potentially in different categories based on the variable var_name.
    It can compare 2 different masses side by side (before and after sas correction for instance).

    Args:
        dt (pd.DataFrame): dataframe containing the data with the mass variable and 
        mc (pd.DataFrame): _description_
        cut0 (str, optional): cut to apply on the dataframes. Defaults to None.
        mll_name1 (str, optional): name of the di-lepton mass variable. Defaults to "mee".
        mll_name2 (str, optional): name of the second di-lepton mass variable to compare side by side. Defaults to None.
        pt_name1 (str, optional): name of the first pt variable. Defaults to None.
        pt_name2 (str, optional): name of the second pt variable, use to replace pt_name1 in cut and categories. Defaults to None.
        var_name (str or List[str], optional): name of the variable to categorize on (1 plot per category). Defaults to None.
        var_cats (List or List(List), optional): bining for the categorization. Defaults to None.
        var_latex (str List[str], optional): latex string to display the categorisation var. Defaults to None.
        var_unit (str, optional): unit of the categorisation var. Defaults to ''.
        var_prefixes (List[str], optional): prefixes to add to the categorization var. Use ['lead_','sublead_'] if working with HDNA files. Defaults to None.
        var_suffixes (List[str], optional): suffixes to add to the categorization var. Defaults to ['1','2'].
        mc_w_name (str, optional): name of weight column in the mc dataframe. Defaults to None.
        both_leptons(bool, optional): both lepton in category (diag.) or at least one lepton (incl.). Defaults to False.
        lead_electron (bool, optional): only the leading electron in category (like Run2 mass AN). Defaults to False.
        is_comparison (bool, optional): if True, overlaid the different data or mc inputs else use the additionnal mc inputs as systematics (HDNA files). Defaults to False.
    """

    if isinstance(mc, pd.DataFrame):
        mc = {'MC':{'df':mc, 'weight': mc_w_name}}

    if isinstance(dt, pd.DataFrame):
        dt = {'Data':{'df':dt, 'weight': None}}

    if cut0 is None:
        cut0 = f"{mll_name1} > 40"  

    if mll_name2 is not None:
        if cut0 is None or cut0 == f"{mll_name1} > 40":
            cut02 = f"{mll_name2} > 40"
        else:
            cut02 = cut0
            if mll_name1 in cut0:
                cut02 = cut02.replace(mll_name1, mll_name2)
            if pt_name1 and pt_name2 and (pt_name1 in cut02):
                cut02 = cut02.replace(pt_name1, pt_name2)
            
    chi21 = []
    chi22 = []
    show_bkg = kwargs.get('show_bkg', False)
    n_subfig = 1 if mll_name2 is None else 2

    def prepare_data_for_plotting(mc, dt, cut0, mll_name1, mc_w_name=None, show_bkg=False, is_comparison=False):
            """Prepare data and MC for plotting by applying cuts and extracting relevant columns."""
            idx_mc = [mci['df'].eval(cut0) for mci in mc.values()] if mc else None
            idx_dt = [dti['df'].eval(cut0) for dti in dt.values()] if dt else None

            if mc:
                if mc_w_name is not None:
                    mc_w = [mci['df'].loc[idx_mci, mc_w_name] for mci, idx_mci in zip(mc.values(), idx_mc)]
                else:
                    mc_w = [mci['df'].loc[idx_mci, mci['weight']] if mci['weight'] is not None else None for mci, idx_mci in zip(mc.values(), idx_mc)]
            else:
                mc_w = None

            mcs = [mci['df'].loc[idx_mci, mll_name1] for mci, idx_mci in zip(mc.values(), idx_mc)] if mc else None
            mc_names = list(mc.keys()) if mc else None

            dts = [dti['df'].loc[idx_dti, mll_name1] for dti, idx_dti in zip(dt.values(), idx_dt)] if dt else None
            dt_names = list(dt.keys()) if dt else None

            if show_bkg:
                mc_type = mc[mc_names[0]]['df'].loc[idx_mc[0], "bkg_type"]
            else:
                mc_type = None

            # Add systematics from S&S
            if mc and not is_comparison:
                if f'{mll_name1}_scale_up' in mc[mc_names[0]]['df'].columns:
                    print("Add syst with scale_up")
                    mcs.append(mc[mc_names[0]]['df'].loc[idx_mc[0], f'{mll_name1}_scale_up'])
                    mc_w += [mc_w[0]]
                if f'{mll_name1}_smear_up' in mc[mc_names[0]]['df'].columns:
                    print("Add syst with smear_up")
                    mcs.append(mc[mc_names[0]]['df'].loc[idx_mc[0], f'{mll_name1}_smear_up'])
                    mc_w += [mc_w[0]]

            return idx_mc, idx_dt, mc_w, mcs, mc_names, dts, dt_names, mc_type
    
    if var_name is None:
        idx_mc, idx_dt, mc_w, mcs, mc_names, dts, dt_names, mc_type = prepare_data_for_plotting(mc, dt, cut0, mll_name1, mc_w_name=mc_w_name, show_bkg=show_bkg, is_comparison=is_comparison)
        fig1, fig2 = create_fig(n_subfig=n_subfig)
        y_range, chi2, ndof, mll_bins_out, hists = plot_data_mc_with_ratio(dts, mcs, dt_names=dt_names, mc_names=mc_names, mc_type=mc_type, mc_w=mc_w, fig=fig1, 
                                                                            is_comparison=is_comparison, **kwargs)
        chi21.append(chi2)
        if mll_name2 is not None:
            idx_mc, idx_dt, mc_w, mcs, mc_names, dts, dt_names, mc_type = prepare_data_for_plotting(mc, dt, cut02, mll_name2, mc_w_name=mc_w_name, show_bkg=show_bkg, is_comparison=is_comparison)

            kwargs['mll_bins'] = mll_bins_out
            kwargs['y_range'] = y_range
            _, chi2, ndof, _, hists2 = plot_data_mc_with_ratio(dts, mcs, dt_names=dt_names, mc_names=mc_names, mc_type=mc_type, mc_w=mc_w, fig=fig2, 
                                                               is_comparison=is_comparison, **kwargs)
            chi22.append(chi2)
        if lead_electron:                            
            return [plt.gcf()], (chi21, chi22), [], []
        else:
            return [plt.gcf()], (chi21, chi22), (mll_bins_out, hists)

    else:
        if not isinstance(var_name, list):
            var_name = [var_name]
            var_cats = [var_cats]
            var_latex = [var_latex]
            var_unit = [var_unit]

        plot_categories = {f'{vname}': vcats for vname, vcats in zip(var_name, var_cats)}
        print(plot_categories)
        
        if dt:
            cat_dt = [pd.Index(categorize(dti['df'], category_dict=plot_categories, cut=cut0, var_suffixes=var_suffixes, var_prefixes=var_prefixes).flatten()) for dti in dt.values()]
            cat_dt0 = cat_dt[0]
        if mc:
            cat_mc = [pd.Index(categorize(mci['df'], category_dict=plot_categories, cut=cut0, var_suffixes=var_suffixes, var_prefixes=var_prefixes).flatten()) for mci in mc.values()]
            cat_mc0 = cat_mc[0]
        if dt and mc:
            cat_plot = cat_dt0.intersection(cat_mc0)
        elif dt:
            cat_plot = cat_dt0
        elif mc:
            cat_plot = cat_mc0

        if mll_name2:
            if pt_name1 in plot_categories:
                # -- we want to keep the same order for keys
                keys = list(plot_categories.keys())
                values = list(plot_categories.values())
                index = keys.index(pt_name1)
                keys[index] = pt_name2
                plot_categories = dict(zip(keys, values))

            if dt:
                cat_dt = [pd.Index(categorize(dti['df'], category_dict=plot_categories, cut=cut02, prefix='cat2_', var_suffixes=var_suffixes, var_prefixes=var_prefixes).flatten()) for dti in dt.values()]
                cat_dt0 = cat_dt[0]
            if mc:
                cat_mc = [pd.Index(categorize(mci['df'], category_dict=plot_categories, cut=cut02, prefix='cat2_', var_suffixes=var_suffixes, var_prefixes=var_prefixes).flatten()) for mci in mc.values()]
                cat_mc0 = cat_mc[0]


        n_cat_bins = [len(bin)-1 for bin in var_cats]
        categories = np.arange(np.prod(n_cat_bins)).reshape(*n_cat_bins)

        if var_latex is None:
            var_latex = var_name
        figs = []
        cat_legends = []
        mll_bins_list = []
        hist_ijazz_list = []
        hist_egm_list = []
        for icat, cat in enumerate(cat_plot):
            cut = cut0 + f" and (cat1 == {cat} or cat2 == {cat})"
            if mll_name2:
                cut2 = cut02 + f" and (cat2_1 == {cat} or cat2_2 == {cat})"
            if both_leptons:
                cut = cut0 + f" and (cat1 == {cat} and cat2 == {cat})"
                if mll_name2:
                    cut2 = cut02 + f" and (cat2_1 == {cat} and cat2_2 == {cat})"
            elif lead_electron:
                cut = cut0 + f" and (cat1 == {cat})"
                if mll_name2:
                    cut2 = cut02 + f" and (cat2_1 == {cat})"
            fig1, fig2 = create_fig(n_subfig=n_subfig)

            
            cat_title = ''
            
            icats = np.unravel_index(icat, n_cat_bins) # get icat for each categories
            if var_unit == '':
                var_unit = [''] * len(var_name)

            if lead_electron:
                for icat, vcats, vlatex, vunit in zip(icats, var_cats, var_latex, var_unit):
                    cat_title += f"${vcats[icat]:.3g} \leq${vlatex}$< {vcats[icat+1]:.3g}$ {vunit}\n"
                cat_legends.append(cat_title[:-2])
                cat_title = ''
            else:
                for icat, vcats, vlatex, vunit in zip(icats, var_cats, var_latex, var_unit):
                    cat_title += f"${vcats[icat]:.3g} \leq${vlatex}$< {vcats[icat+1]:.3g}$ {vunit}\n"
                cat_title = cat_title[:-2]

            idx_mc, idx_dt, mc_w, mcs, mc_names, dts, dt_names, mc_type = prepare_data_for_plotting(mc, dt, cut, mll_name1, mc_w_name=mc_w_name, show_bkg=show_bkg, is_comparison=is_comparison)

            y_range, chi2, ndof, mll_bins_out, hists = plot_data_mc_with_ratio(dts, mcs, dt_names=dt_names, mc_names=mc_names, mc_type=mc_type, mc_w=mc_w, fig=fig1, 
                                                                            is_comparison=is_comparison, title=cat_title, **kwargs)
            chi21.append(chi2/ndof)
            mll_bins_list.append(mll_bins_out)
            hist_ijazz_list.append(hists)
            if mll_name2 is not None:
                print(mll_name2,',', cut02)
                
                idx_mc, idx_dt, mc_w, mcs, mc_names, dts, dt_names, mc_type = prepare_data_for_plotting(mc, dt, cut2, mll_name2, mc_w_name=mc_w_name, show_bkg=show_bkg, is_comparison=is_comparison)

                kwargs2 = kwargs.copy()
                kwargs2['mll_bins'] = mll_bins_out
                kwargs2['y_range'] = y_range
                _, chi2, ndof, _, hists = plot_data_mc_with_ratio(dts, mcs, dt_names=dt_names, mc_names=mc_names, mc_type=mc_type, mc_w=mc_w, fig=fig2, 
                                                                            is_comparison=is_comparison, title=cat_title, **kwargs2)
                chi22.append(chi2/ndof)
                hist_egm_list.append(hists)
            figs.append(plt.gcf())
        if lead_electron:
            return figs, (chi21, chi22), cat_legends, (mll_bins_list, hist_ijazz_list, hist_egm_list)
        else:
            return figs, (chi21, chi22), []


def plot_data_mc_with_ratio(dt: List[np.ndarray], mc: List[np.ndarray], dt_names: List[str]=None, mc_names: List[str]=None,
                            mc_type: np.ndarray=None, mc_w:np.ndarray=None, fig:Figure=None,
                            mll_bins: Union[list, np.ndarray]=None, mll_latex: str='$m_{\ell\ell}$  (GeV)', mll_unit:str='GeV',
                            y_range:tuple[float, float]=None, y_scale:str='linear', yr_range = (0.8, 1.2), 
                            show_bkg:bool=False, show_median:bool=False, title: str=None, is_comparison=False, normalize=True) -> Tuple[Tuple[float, float], float, float]:
    """Make a plot with top panel: mll data vs MC, bottom panel, data/MC
    NB: the MC is normalised to data.

    Args:
        dt (np.ndarray): mll list for data
        mc (np.ndarray): mll list for mc
        dt_names (List[str], optional): list of data names. Defaults to None.
        mc_names (List[str], optional): list of mc names. Defaults to None.
        mc_type (np.ndarray, optional): array with mc types for background e.g. 0,1,2 etc. Defaults to None.
        mc_w (np.ndarray, optional): list of mc weights. Defaults to None.
        fig (plt.Figure, optional): figure or subfigure to plot on. Defaults to None.
        y_range (tuple, optional): y range top panel . Defaults to None.
        yr_range (tuple, optional): y range bottom pabel. Defaults to (0.8, 1.2).
        y_scale (str, optional): The axis scale type to apply ("linear", "log", "function",...). Defaults to "linear".
        show_bkg (bool, optional): show backgrounds in different colors using mc_type. Defaults to False.
        show_median (bool, optional): show median mass on the plot instead of number of events. Defaults to False.
        mll_bins (Union[list, np.ndarray], optional): bining. Defaults to None.
        mll_latex (str, optional): latex string for the x axis. Defaults to '$m_{\ell\ell}$  (GeV)'.
        mll_unit (str, optional): unit for the x axis. Defaults to 'GeV'.
        title (str, optional): title to put on top on. Defaults to None.
        is_comparison (bool, optional): if True, overlaid the different data or mc inputs else use the additionnal mc inputs as systematics (HDNA files). Defaults to False.
        normalize (bool, optional): if True, normalise the MC to data. Defaults to True.

    Returns: 
        Tuple[Tuple[float, float], float, float]: return a tuple with the ((y_range0, y_range_1), chi2, ndof)
    """

    if fig is None:
        fig = plt.figure(figsize=(7,7))
    fig.subplots_adjust(hspace=0, wspace=0)
    ax = fig.subplots(2, 1, sharex=True, height_ratios=(4, 1))

    bin_width = None
    if mll_bins is None:
        mll_bins = np.linspace(80, 100, 81)
    elif isinstance(mll_bins[-1], float):
        pass # already a bin array
    elif mll_bins[-1] in ['adaptative','a', 'adapt']:
        win_z_dt = (mll_bins[0], mll_bins[1])
        if (dt and len(dt[0])) or (mc and len(mc[0])):
            if dt:
                dt_win = dt[0][(dt[0] > win_z_dt[0]) & (dt[0] < win_z_dt[1])]
            else:
                dt_win = mc[0][(mc[0] > win_z_dt[0]) & (mc[0] < win_z_dt[1])]

            if mc:
                mc_win = mc[0][(mc[0] > win_z_dt[0]) & (mc[0] < win_z_dt[1])]
            else:
                mc_win = dt_win
        
            # -- using Freedman–Diaconis rule to determine bin width
            irq = np.subtract(*np.percentile(dt_win, [75, 25]))
            bin_width = max(2 * irq / np.power(len(mc_win),1/3), 0.25)
            n_bins = max(3,int(np.floor((win_z_dt[1]-win_z_dt[0])/bin_width)+1))
            bin_width = (win_z_dt[1]-win_z_dt[0])/(n_bins-1)
            mll_bins = np.linspace(*win_z_dt, n_bins)
        
        else:
            n_bins = 11
            bin_width = (win_z_dt[1]-win_z_dt[0])/(n_bins-1)
            mll_bins = np.linspace(*win_z_dt, n_bins)
    else:
        mll_bins = np.linspace(*mll_bins)

    if bin_width is None:
        bin_width = mll_bins[1] - mll_bins[0]

    x = mll_bins
    x_min = mll_bins[0]
    x_max = mll_bins[-1]
    range_x = (x_min, x_max)
    n_bins = len(mll_bins) - 1

    hmc = []
    hmc_counts = []
    if mc:
        for mci, mc_wi in zip(mc, mc_w):
            hmc.append(np.histogram(mci, bins=n_bins, range=range_x, weights=mc_wi)[0])
            hmc_counts.append(np.histogram(mci, bins=n_bins, range=range_x)[0])
            # hsyst = [np.histogram(my_mc, bins=n_bins, range=range_x, weights=mc_wi)[0] for my_mc in mc[1:]]
        hmc0 = hmc[0]
    else:
        hmc0 = np.zeros(n_bins)
    hdt = []
    if dt:
        for dti in dt:
            hdt.append(np.histogram(dti, bins=n_bins, range=range_x)[0])
        hdt0 = hdt[0]
    else:
        hdt0 = np.zeros(n_bins)

    if normalize:    
        if dt and mc:
            mc_norm = [hdt0.sum()/hmci.sum() for hmci in hmc]
            dt_norm = [hdt0.sum()/hdti.sum() for hdti in hdt]
            hmc_normed = [hmci * hdt0.sum()/hmci.sum() for hmci in hmc]
            hdt_normed = [hdti * hdt0.sum()/hdti.sum() for hdti in hdt]

        elif dt:
            dt_norm = [hdt0.sum()/hdti.sum() for hdti in hdt]
            hdt_normed = [hdti * hdt0.sum()/hdti.sum() for hdti in hdt]
            mc_norm = []
            hmc = []
            hmc_normed = []
            
        elif mc:
            mc_norm = [hmc0.sum()/hmci.sum() for hmci in hmc]
            hmc_normed = [hmci * hmc0.sum()/hmci.sum() for hmci in hmc]
            dt_norm = []
            hdt = []
            hdt_normed = []
    else:
        mc_norm = [1.0] * len(hmc)
        hmc_normed = hmc
        hdt_normed = hdt
        dt_norm = [1.0] * len(hdt)

    if mc:
        hmc_count = hmc_counts[0]
        hmc_out = hmc0
        hmc_err = [np.sqrt(np.histogram(mci, bins=n_bins, range=range_x, weights=mc_wi**2)[0]) * mc_normi  if mc_wi is not None else np.sqrt(hmci)*mc_normi for mci, mc_wi, mc_normi, hmci in zip(mc, mc_w, mc_norm, hmc)]
        # print(hmc_err[0]/hmc[0])
    else :
        hmc_err = []
        hmc_count = []
        hmc_out = []

    
        
    syst_labels = ['scale_up','smear_up']
    colors = ['r','g']
    plt.sca(ax[0])

    def weighted_median(values, weights, mll_bins):
        # Apply the same mask to both values and weights
        mask = (values > mll_bins[0]) & (values < mll_bins[-1])
        filtered_values = values[mask]
        filtered_weights = weights[mask]
        i = np.argsort(filtered_values)
        sorted_values = filtered_values.iloc[i]
        sorted_weights = filtered_weights.iloc[i]
        c = np.cumsum(sorted_weights)
        median_idx = np.searchsorted(c, 0.5 * c.iloc[-1])
        return sorted_values.iloc[median_idx]

    if show_median:
        mc_median = weighted_median(mc[0], mc_w[0], mll_bins)
        if isinstance(dt, list):
            dt = dt[0]
        dt_median = dt[(dt > mll_bins[0]) & (dt < mll_bins[-1])].median()

    # color cycle for MC and data
    import matplotlib.cm   
    colors = matplotlib.cm.tab10(range(20))
    colors_dt = np.vstack((
    [0.0, 0.0, 0.0, 1.0],                     # Black (RGBA)
    matplotlib.cm.Set1(np.linspace(0, 1, 9)) # 9 colors from Set1
))
    
    if not is_comparison:
        hsyst = [hmci * mc_norm[0] for hmci in hmc[1:]]
        # hsyst = [hmci * mc_normi for hmci, mc_normi in zip(hmc[1:], mc_norm[1:])]
        hmc_normed = hmc_normed[0:1]
        hmc_err = hmc_err[0:1]
        mc_norm = mc_norm[0:1]

    if not show_bkg:
        for i, hmci in enumerate(hmc_normed):
            if show_median:
                cms.draw(x, hmci, yerr=hmc_err, option="H", legend=f"MC: {mc_median:.3f}", color=colors[i])
            else:
                legend = f"{mc_names[i]}" if is_comparison else f"{mc_names[i]}: {hmc_count.sum():.3e}".replace('e+0','e')
                cms.draw(x, hmci, option="H", legend=legend, color=colors[i])

    for i, (hdti, norm) in enumerate(zip(hdt_normed, dt_norm)):
        if show_median:
            cms.draw(x, hdti, yerr=np.sqrt(hdti), option='E', color=colors_dt[i], legend=f"Data: {dt_median:.3f}")
        else:
            legend = f"{dt_names[i]}" if is_comparison else f"{dt_names[i]}: {hdt[i].sum():.3e}".replace('e+0','e')
            cms.draw(x, hdti, yerr=np.sqrt(hdti), option='E', color=colors_dt[i], legend=legend)

    # -- show different bkgs
    if show_bkg:
        bkg_names = ['DYtoEE', 'DY TauTau', 'TT', 'VV', 'Wjets', 'QCD']
        bkg_colors = ['C0', 'C1', 'C2', 'C3', 'C4']
        bkg_types = np.sort(np.unique(mc_type))[::-1]
        bottom = np.zeros_like(hmc[0])
        for bkg_type in bkg_types:
            idx = mc_type == bkg_type
            hmc_bkg, _ = np.histogram(mc[0][idx], bins=n_bins, range=range_x, weights=mc_w[0][idx])
            hmc_bkg = hmc_bkg.astype(np.float64)
            hmc_bkg *= mc_norm
            xx = 0.5*(x[1:]+x[:-1])
            plt.sca(ax[0])
            plt.bar(xx, hmc_bkg, width=bin_width, bottom=bottom, alpha=0.5, label=bkg_names[bkg_type], color=bkg_colors[bkg_type])
            bottom += hmc_bkg

    # -- ratio plot
    plt.sca(ax[1])
    if not is_comparison:
        yerr2 = hmc_err[0]**2
        for i,hs in enumerate(hsyst):
            yerr2 += (hs-hmc_normed[0])**2
        syst_err = np.sqrt(yerr2)
        # -- show each systematics
        # cms.draw(x, hs/hmc, option="E",legend=syst_labels[i], color=colors[i])
    for i, (hmci, hmc_erri, norm) in enumerate(zip(hmc, hmc_err, mc_norm)):
        if not is_comparison:
            cms.draw(x, hmci/hmci, yerr=syst_err/(hmci*norm), option="E1", color="gray")

        ratio = hdt0/norm/hmci if len(hdt) == 1 and len(hmc) > 1 and is_comparison else hmci/hmc0*norm/mc_norm[0]
        cms.draw(x, ratio, yerr=hmc_erri/(hmci*norm), option="E1", color=colors[i])
    for i, (hdti, norm) in enumerate(zip(hdt, dt_norm)):
        num = hmc0*mc_norm[0] if len(hmc) == 1 or not is_comparison else hdt0
        cms.draw(x, hdti*norm/num, yerr=np.sqrt(hdti)/np.abs(num)*norm, option="E", color=colors_dt[i])
    # cms.draw(x, hdt/hmc, yerr=np.sqrt(hdt)/np.abs(hmc), option="E", color='k')
            

    # -- chi2 computation for binomial distribution
    # -- add MC normalisation to account for proper MC stat. power with weights
    # -- formula from https://online.stat.psu.edu/stat415/book/export/html/833
    if not is_comparison and dt is not None:
        yij = np.array([hdt[0], hmc_normed[0] * hmc_normed[0].sum() / (hmc_err[0]**2).sum()])
        yi = yij.sum(axis=1)
        yj = yij.sum(axis=0)
        n_tot = yi.sum()
        yi_yj_o_n = yi.reshape(-1, 1) * yj / n_tot
        mask = np.where(yi_yj_o_n !=0)
        if len(mask[0]) > 1:
            chi2 = ((yij[mask] - yi_yj_o_n[mask])**2 / yi_yj_o_n[mask]).sum() 
        else: 
            chi2 = 0
        ndof = int(len(mask[0])/2) - 1
    else:
        chi2 = 0
        ndof = 1

   
    if y_range is None:
        y_range = list(ax[0].get_ylim())
        y_range[0] = 0
        if show_bkg:
            y_range[1] *= 10
        else:
            y_range[1] *= 1.4

    if show_median:
        cms.polish_axis(ax=ax[0], y_range=y_range, y_title=f'Events/{bin_width:.2f} {mll_unit}', leg_title=f'$\chi^2/n_f$ = {chi2:.1f}/{ndof}\nMedian mass (GeV):', 
                        leg_loc='upper right', leg_title_fontsize='large', leg_fontsize='medium')
    else:
        leg_title = None if is_comparison else f'$\chi^2/n_f$ = {chi2:.1f}/{ndof}'
        cms.polish_axis(ax=ax[0], y_range=y_range, y_title=f'Events/{bin_width:.2f} {mll_unit}', leg_loc='upper right', leg_title=leg_title)
    
    cms.polish_axis(ax=ax[1], x_title=mll_latex, y_range=yr_range, y_title='data/MC')
    ax[0].set_title(title)
    ax[0].set_yscale(y_scale)
    if y_scale == "linear":
        ax[0].ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    else:
        y_range = list(ax[0].get_ylim())
        # y_range[0] = min(hdt.min(), hmc.min())/100
        y_range[0] = 2
        y_range[1] *= 100
        ax[0].set_ylim(y_range)

    
    return y_range, chi2, ndof, mll_bins, (hdt,hmc_count,hmc_out)
