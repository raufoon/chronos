# Averages slices of the 3D lightcone to render it as a manageable 3D volume
avgrange = 10
coneoutput_len = len(dTb_cone) // 10
downsampled_dTbcone = np.zeros((coneoutput_len, BOX_PARAM, BOX_PARAM))

for i in range(coneoutput_len):
    start = i * avgrange
    end = start + avgrange if start + avgrange < len(dTb_cone) else len(dTb_cone)
    downsampled_dTbcone[i,:,:] = np.mean(dTb_cone[start:end,:,:], axis=0)

X, Y, Z = np.mgrid[0:coneoutput_len, 0:BOX_PARAM, 0:BOX_PARAM]

fig = go.Figure()
fig.add_trace(go.Volume(
    x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
    value=downsampled_dTbcone.flatten(),
    isomin=dTb_cone_min, isomax=dTb_cone_max,
    opacity=0.2, surface_count=5,
    colorscale="Rainbow",
    colorbar=dict(title=dict(text="Brightness Temperature δT_b [mK]", side="right"), x=0.95),
))

tickvals = list(range(0, len(z_cone_range), len(z_cone_range)//10))
ticktext = [f"{z:.4f}" for z in z_cone_range[tickvals]]
tickvals = [t//10 for t in tickvals]

fig.update_layout(
    title=dict(text=f"Light Cone", y=0.91, x=0.5, xanchor="center", yanchor="middle"),
    width=600, height=600,
    scene=dict(
        xaxis=dict(ticktext=ticktext, tickvals=tickvals, title=dict(text="Redshift z")),
        yaxis=dict(title=dict(text="x")),
        zaxis=dict(title=dict(text="y"))
    )
)

fig.write_html("plots/volume_light_cone.html")