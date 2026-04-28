# Uses tools21cm to calculate the 1D power spectrum (Fourier Transform variance)
fig = go.Figure()
num_z = len(Z_PARAM_RANGE)
colors = px.colors.sample_colorscale("Turbo", [i/(num_z - 1) for i in range(num_z)])

# Calculate and plot the raw Power Spectrum for each redshift box
for i, Z_PARAM in enumerate(Z_PARAM_RANGE):
    # This is the statistical "simulation" generating the power spectrum data
    ps_raw, ks_raw = t2c.power_spectrum_1d(dTb_array[Z_PARAM], kbins=15, box_dims=BOX_PARAM)
    
    fig.add_trace(go.Scatter(
        x=ks_raw,
        y=ps_raw * ks_raw**3 / 2 / np.pi**2, # Converts to dimensionless power spectrum Delta^2(k)
        mode='lines',
        line=dict(color=colors[i]),
        name=f'z={Z_PARAM} (Raw)'
    ))

fig.update_layout(
    title='Spherically averaged power spectrum',
    xaxis_title='k (Mpc<sup>-1</sup>)',
    yaxis_title='P(k) k<sup>3</sup>/(2π<sup>2</sup>)',
    xaxis_type='log', yaxis_type='log',
    width=700, height=500,
    showlegend=False
)

fig.write_html("plots/spherically_averaged_power_spectrum.html")

