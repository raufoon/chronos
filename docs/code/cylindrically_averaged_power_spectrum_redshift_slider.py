# Calculates the 2D power spectrum separated into transverse (k_perp) and line-of-sight (k_parallel) modes
N = dTb_array[Z_PARAM_RANGE[0]].shape[0]
L = BOX_PARAM
custom_kbins = np.linspace(2 * np.pi / L, np.pi * N / L, N // 2)

ps_results = []
all_values = []

# Calculate the 2D Power Spectrum for each redshift box
for z in Z_PARAM_RANGE:
    # This is the statistical "simulation" generating the cylindrical data
    ps, ksperp, kspar = t2c.power_spectrum_2d(
        dTb_array[z], kbins=[custom_kbins, custom_kbins], box_dims=BOX_PARAM
    )
    ps_results.append((ps, ksperp, kspar, z))
    all_values.extend(ps[ps > 0].flatten())

global_vmin = np.nanmin(all_values)
global_vmax = np.nanmax(all_values)

fig = go.Figure()

# Plot the 2D heatmap for each calculated redshift
for i, (ps, ksperp, kspar, z) in enumerate(ps_results):
    ps_safe = np.copy(ps.T)
    ps_safe[ps_safe <= 0] = np.nan
    log_ps = np.log10(ps_safe)

    fig.add_trace(go.Heatmap(
        x=ksperp, y=kspar, z=log_ps,
        colorscale='Rainbow',
        zmin=np.log10(global_vmin), zmax=np.log10(global_vmax),
        showscale=False, visible=(i == 0)
    ))

steps = []
for i, z in enumerate(Z_PARAM_RANGE):
    visibility = [False] * len(Z_PARAM_RANGE)
    visibility[i] = True
    steps.append(dict(
        method="update",
        args=[{"visible": visibility}, {"title": f'Cylindrically Averaged 2D Power Spectrum (z={z})'}],
        label=f"z={z}"
    ))

sliders = [dict(active=0, pad={"t": 50}, steps=steps)]

fig.update_layout(
    title=dict(text=f'Cylindrically Averaged 2D Power Spectrum (z={Z_PARAM_RANGE[0]})', x=0.5, xanchor="center"),
    xaxis=dict(title='k_perp [Mpc<sup>-1</sup>]', type='log'),
    yaxis=dict(title='k_parallel [Mpc<sup>-1</sup>]', type='log'),
    width=750, height=650, sliders=sliders
)

fig.write_html("plots/cylindrically_averaged_power_spectrum_redshift_slider.html")