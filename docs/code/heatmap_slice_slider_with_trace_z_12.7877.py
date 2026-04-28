from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

#@title Brightness tempertature, Slide through a specific slice of the box
def plot_tomographic_slice(box_data, box_len, redshift, cmap="Turbo", slice_plane='z'):
    # Select the specific slice
    def select_slice(data, index, plane):
        if plane.lower() == 'x':
            data_slice = data[index, :, :]
        elif plane.lower() == 'y':
            data_slice = data[:, index, :]
        else:
            data_slice = data[:, :, index]
        return data_slice

    maketitle = lambda index, z: f"Brightness Temperature Slice {index} – Redshift z = {z}"

    # Create subplots: 1 row for 2D heatmap, 1 row for 3D Volume
    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{"type": "xy"}], [{"type": "scene"}]],
        row_heights=[0.4, 0.6],
        vertical_spacing=0.08
    )

    L = box_len - 1

    # --- 1. Add 2D Heatmap Traces (Indices 0 to box_len-1) ---
    for slice_index in range(box_len):
        fig.add_trace(go.Heatmap(
            z=select_slice(box_data, slice_index, slice_plane),
            hoverinfo="z",
            zmax=dTb_max,
            zmin=dTb_min,
            colorscale=cmap,
            visible=(slice_index == L), # Make only the last one visible by default
            showscale=True,
            colorbar=dict(title="Brightness Temperature δT_b [mK]", len=0.45, y=0.8, yanchor="middle")
        ), row=1, col=1)

    # --- 2. Add 3D Volume Trace (Index: box_len) ---
    # Downsample the volume array slightly (step=2) to ensure smooth browser performance 
    # when rendering it alongside 50 heatmaps and 50 border lines.
    step = 2
    X, Y, Z = np.mgrid[0:box_len:step, 0:box_len:step, 0:box_len:step]
    vol_data = box_data[::step, ::step, ::step]

    fig.add_trace(go.Volume(
        x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
        value=vol_data.flatten(),
        isomin=dTb_min, isomax=dTb_max,
        opacity=0.1, surface_count=5,
        colorscale=cmap,
        showscale=False, # Hide the second colorbar to prevent clutter
        visible=True
    ), row=2, col=1)

    # --- 3. Add 3D Red Border Traces (Indices: box_len+1 to 2*box_len) ---
    for slice_index in range(box_len):
        # Calculate the 4 corners of the slice to draw the red outline
        if slice_plane.lower() == 'z':
            bx = [0, L, L, 0, 0]; by = [0, 0, L, L, 0]; bz = [slice_index]*5
        elif slice_plane.lower() == 'y':
            bx = [0, L, L, 0, 0]; by = [slice_index]*5; bz = [0, 0, L, L, 0]
        else: # 'x'
            bx = [slice_index]*5; by = [0, L, L, 0, 0]; bz = [0, 0, L, L, 0]

        fig.add_trace(go.Scatter3d(
            x=bx, y=by, z=bz,
            mode='lines',
            line=dict(color='red', width=8),
            visible=(slice_index == L), # Make only the last one visible by default
            showlegend=False,
            hoverinfo='skip'
        ), row=2, col=1)

    # --- 4. Setup Sliders ---
    steps = []
    for i in range(box_len):
        # Determine the visibility array for this specific step
        vis = [False] * len(fig.data)
        vis[i] = True                           # Activate i-th Heatmap
        vis[box_len] = True                     # Keep Volume always active
        vis[box_len + 1 + i] = True             # Activate i-th Red Border

        steps.append(dict(
            method="update",
            args=[
                {"visible": vis},
                {"title": dict(
                    text=maketitle(i, redshift),
                    y=0.98, x=0.5, xanchor="center", yanchor="top"
                )}
            ],
            label=f"{i}"
        ))

    sliders = [dict(
        active=box_len - 1,
        pad={"t": 30},
        steps=steps
    )]

    fig.update_layout(
        width=700, height=1000, # Increased height to accommodate the stacked plots
        title=dict(
            text=maketitle(L, redshift),
            y=0.98, x=0.5, xanchor="center", yanchor="top"
        ),
        xaxis=dict(title="x [Mpc]", scaleanchor="y"),
        yaxis=dict(title="y [Mpc]"),
        scene=dict(
            xaxis=dict(title="x [Mpc]", range=[0, box_len]),
            yaxis=dict(title="y [Mpc]", range=[0, box_len]),
            zaxis=dict(title="z [Mpc]", range=[0, box_len]),
            aspectmode='cube'
        ),
        sliders=sliders,
        margin=dict(t=60, b=50, l=50, r=50)
    )

    fig.show()

    fig.update_layout(autosize=True, width=None, height=None)
    fig.write_html(f"plots/heatmap_slice_slider_with_trace_z_{redshift}.html")

# Execution Call
Z_PARAM = 20
Z_PARAM = Z_validate(Z_PARAM)
plot_tomographic_slice(
    box_data=dTb_array[Z_PARAM],
    box_len=BOX_PARAM,
    redshift=Z_PARAM
)