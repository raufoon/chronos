BOX_PARAM, BOX_LEN = 50, 50
z_cone_full_range = np.round(t2c.lightcone.redshifts_at_equal_comoving_distance(5,35,BOX_PARAM,BOX_LEN),4)

z_min, z_max = 7, 10
z_cone_range = np.array([z for z in z_cone_full_range if z_min <= z <= z_max])

# Assemble the lightcone array by taking sequential slices from different redshift boxes
dTb_cone = np.empty((len(z_cone_range), BOX_PARAM, BOX_PARAM))
for i, Z_PARAM in enumerate(z_cone_range):
    box = get_brightness_temp_box(
        box=BOX_PARAM, box_len=BOX_LEN, redshift=Z_PARAM,
        hubble=0.69, matter=0.31, baryon=0.02
    )
    # Take a 2D slice from the box and append it to the cone's depth axis
    dTb_cone[i, :, :] = box[i % BOX_PARAM] 

dTb_cone_max, dTb_cone_min = np.nanmax(dTb_cone), np.nanmin(dTb_cone)

# Plots a 2D slice of the 3D lightcone (y-axis = space, x-axis = time/redshift)
fig = go.Figure()

fig.add_trace(go.Heatmap(
    z=dTb_cone[:,:,0].T, # Take the 0th spatial slice across all redshifts
    hoverinfo="z",
    zmax=dTb_cone_max, zmin=dTb_cone_min,
    colorscale="Turbo"
))

tickvals = list(range(0, len(z_cone_range), len(z_cone_range)//10))
ticktext = [f"{z:.4f}" for z in z_cone_range[tickvals]]

fig.update_layout(
    title=dict(text=f"Light Cone", y=0.91, x=0.5, xanchor="center", yanchor="middle"),
    width=950, height=450,
    xaxis=dict(title=dict(text=r"Redshift z"), tickvals=tickvals, ticktext=ticktext),
    yaxis=dict(title=dict(text=r"y [Mpc]")),
)

fig.write_html("plots/heatmap_light_cone.html")