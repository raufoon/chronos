# Calculates the global mean of the entire box at each redshift
def frequency(z): return 1420.40575 / (1 + z)

frequencies = [frequency(z) for z in Z_PARAM_RANGE]
global_means = [np.mean(dTb_array[z]) for z in Z_PARAM_RANGE]

fig = go.Figure(data=go.Scatter(x=frequencies, y=global_means, mode='lines+markers'))

fig.update_layout(
    title="Global Frequency Spectrum",
    xaxis_title="Frequency [MHz]",
    yaxis_title=r"Global δT_b [mK] [mK]",
    width=700, height=500
)

fig.write_html("plots/global_frequency_spectrum.html")