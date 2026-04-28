# Creates a 3D volumetric render of the cubes, downsampled slightly for performance
X, Y, Z = np.mgrid[0:BOX_PARAM//2, 0:BOX_PARAM//2, 0:BOX_PARAM//2]
X, Y, Z = X.flatten(), Y.flatten(), Z.flatten()

fig = go.Figure()
reduced_Z_PARAM_RANGE = Z_PARAM_RANGE[::5] # Downsample redshift steps for the 3D slider

for z in reduced_Z_PARAM_RANGE:
    values = dTb_array[z]
    downsampled_values = values[::2,::2,::2] # Downsample spatial resolution
    fig.add_trace(go.Volume(
        x=X, y=Y, z=Z,
        value=downsampled_values.flatten(),
        isomin=dTb_min, isomax=dTb_max,
        opacity=0.2, surface_count=5,
        colorscale=mincut_colorscale("Rainbow", dTb_min, dTb_max, dTb_min),
        colorbar=dict(title=dict(text="Brightness Temperature δT_b [mK]", side="right"), x=0.95),
    ))

fig.data[0].visible = True

sliders = [dict(
    active=len(reduced_Z_PARAM_RANGE)-1,
    pad={"t": 50},
    steps=[dict(
        method="update",
        args=[
            {"visible": [_z == z for _z in reduced_Z_PARAM_RANGE]},
            {"title": dict(text=f"Redshift z = {z}", y=0.96, x=0.5, xanchor="center", yanchor="middle")}
        ],
        label=f"z={z}",
    ) for z in reduced_Z_PARAM_RANGE]
)]

vals = Z[::5]
texts = vals*2
fig.update_layout(
    scene=dict(
        zaxis=dict(ticktext=texts, tickvals=vals, title=dict(text="z [Mpc]")),
        xaxis=dict(ticktext=texts, tickvals=vals, title=dict(text="x [Mpc]")),
        yaxis=dict(ticktext=texts, tickvals=vals, title=dict(text="y [Mpc]"))
    ),
    width=700, height=700, sliders=sliders
)

fig.write_html("plots/volume_brightness_temperature_redshift_slider.html")