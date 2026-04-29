import py21cmfast as p21c
import numpy as np
import tools21cm as t2c
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import sample_colorscale, make_colorscale

# --- UTILITY FUNCTIONS ---
def mincut_colorscale(scalename, min, max, cutoff, N=15):
    return make_colorscale(sample_colorscale(scalename, np.linspace(cutoff,max,N)/max, low=min, high=max))

def GET_Z_CONE_RANGE(z_min, z_max, dz=None, BOX_PARAM=50, BOX_LEN=50): 
    # Calculates the exact redshifts corresponding to equal comoving distance steps
    z_full_range = np.round(t2c.lightcone.redshifts_at_equal_comoving_distance(5,35,BOX_PARAM,BOX_LEN),4)
    z_range = np.array([z for z in z_full_range if z_min <= z <= z_max])
    if dz is None:
        return z_range
    z_linspace = np.linspace(z_min, z_max, int(max(1,(z_max-z_min)//dz)))
    indices = []
    for zx in z_linspace:
        for i, z in enumerate(z_range):
            if zx-z < 0:
                indices.append(i)
                break
    return z_range[indices]

# --- CORE SIMULATION FUNCTION ---
# This runs the standard 21cmFAST pipeline: Initial Conditions -> Perturb -> Ionize -> Spin Temp
def get_brightness_temp_box(box, box_len, redshift, hubble, matter, baryon, save=False):
    filename = f"dTb_BOX_PARAM_{box}_Z_PARAM_{redshift}.npy"
    if os.path.exists(filename):
        return np.load(filename)

    initial_conditions = p21c.initial_conditions(
        user_params={"HII_DIM": box, "BOX_LEN": box_len, "N_THREADS": 2},
        cosmo_params=p21c.CosmoParams(SIGMA_8=0.8, hlittle=hubble, OMm=matter, OMb=baryon),
        random_seed=54321
    )
    perturbed_field = p21c.perturb_field(redshift=redshift, init_boxes=initial_conditions)
    ionized_field = p21c.ionize_box(perturbed_field=perturbed_field)
    brightness_temp = p21c.brightness_temperature(ionized_box=ionized_field, perturbed_field=perturbed_field)
    
    dTb_box = brightness_temp.brightness_temp
    if save: np.save(filename, dTb_box)
    return dTb_box

# Set up simulation boundaries
BOX_PARAM = 50
BOX_LEN = BOX_PARAM
Z_STEP = 0.2
Z_PARAM_RANGE = GET_Z_CONE_RANGE(7, 13, Z_STEP)

# Generate a dictionary of 3D data cubes keyed by their redshift
dTb_array = {
    Z_PARAM: get_brightness_temp_box(
        box=BOX_PARAM, box_len=BOX_LEN, redshift=Z_PARAM,
        hubble=0.69, matter=0.31, baryon=0.02, save=True
    ) for Z_PARAM in Z_PARAM_RANGE
}

dTb_max = np.nanmax([np.nanmax(dTb_array[z]) for z in Z_PARAM_RANGE])
dTb_min = np.nanmin([np.nanmin(dTb_array[z]) for z in Z_PARAM_RANGE])

# Averages the 3D box into a 2D plane and loops over the redshift range to create a slider
def plot_tomographic_slice(boxes, box_len, redshift_range, cmap="Turbo", slice_plane='z'):
    def box_mean(box):
        return np.array([[np.mean(box[i, j, :]) for j in range(len(box[i]))] for i in range(len(box))])

    fig = go.Figure()
    slice_index = 0
    
    # Add a heatmap trace for every redshift
    for redshift in redshift_range:
        fig.add_trace(go.Heatmap(
            z=box_mean(boxes[redshift]),
            hoverinfo="z",
            zmax=dTb_max, zmin=dTb_min,
            colorscale=cmap,
            colorbar=dict(title="δT_b [mK]") # <-- Add this line
        ))

    # Build the slider to toggle trace visibility
    sliders = [dict(
        active=len(redshift_range)-1,
        pad={"t": 50},
        steps=[dict(
            method="update",
            args=[
                {"visible": [_z == z for _z in redshift_range]},
                {"title": dict(text=f"Mean Brightness Temperature at redshift z={z}", y=0.91, x=0.5, xanchor="center", yanchor="middle")}
            ],
            label=f"z={z}",
        ) for z in redshift_range]
    )]

    fig.update_layout(
        yaxis_scaleanchor="x", width=550, height=600,
        title=dict(text=f"Mean Brightness Temperature at redshift z={redshift_range[-1]}", y=0.91, x=0.5, xanchor="center", yanchor="middle"),
        xaxis=dict(title=dict(text=r"x [Mpc]")),
        yaxis=dict(title=dict(text=r"y [Mpc]")),
        sliders=sliders
    )
    
    fig.write_html("plots/mean2d_brightness_temperature.html")
    return fig

plot_tomographic_slice(boxes=dTb_array, box_len=BOX_PARAM, redshift_range=Z_PARAM_RANGE)