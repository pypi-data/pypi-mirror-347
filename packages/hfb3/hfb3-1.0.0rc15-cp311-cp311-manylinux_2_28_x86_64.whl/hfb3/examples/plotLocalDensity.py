#!/usr/bin/env python3

# Plot the local 1-body density of a state.

# ==============================================================================
# ==============================================================================
# ==============================================================================

import sys
import hfb3

# ==============================================================================
# ==============================================================================
# ==============================================================================


def plot_matplotlib(_state, zmin, zmax, xmin, xmax):
    """plot using Matplotlib"""

    discrete = hfb3.Discrete(_state.basis, hfb3.Mesh.regular(xmin, 0, zmin, xmax, 0, zmax, 101, 1, 201))
    denst = discrete.getLocalXZ(_state.rho(hfb3.NEUTRON) + _state.rho(hfb3.PROTON), True)

    import numpy as np
    from matplotlib.pyplot import cm
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    fig, ax = plt.subplots()
    im = ax.imshow(np.flip(denst, axis=0), cmap=cm.inferno, extent=[zmin, zmax, xmin, xmax])
    plt.xlabel(r'$z$ [fm]')
    plt.ylabel(r'$r$ [fm]')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im, cax=cax)

    plt.ylabel(r'$\rho_{tot}$ [fm$^{-3}$]')
    plt.show()

# ==============================================================================
# ==============================================================================
# ==============================================================================


def plot_bokeh(_state, zmin, zmax, xmin, xmax):
    """plot using Bokeh"""

    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show
    from bokeh.models import ColorBar, LinearColorMapper

    # from bokeh.io import output_notebook
    # output_notebook()

    discrete = hfb3.Discrete(_state.basis, hfb3.Mesh.regular(xmin, 0, zmin, xmax, 0, zmax, 101, 1, 201))
    denst = discrete.getLocalXZ(_state.rho(hfb3.NEUTRON) + _state.rho(hfb3.PROTON), True)

    p = figure(tools="pan, reset, save, wheel_zoom",  # height=300, width=800,
               active_drag="pan", active_scroll="wheel_zoom", match_aspect=True,
               x_axis_label='z [fm]', y_axis_label='r [fm]')
    color = LinearColorMapper(palette="Inferno256")
    p.image(image=[denst], x=zmin, y=xmin, dw=zmax - zmin, dh=xmax - xmin, color_mapper=color)
    color_bar = ColorBar(color_mapper=color, label_standoff=10, location=(0, 0), width=10)
    p.add_layout(color_bar, 'right')

    # show(p)  # inside a notebook
    show(gridplot([p,], ncols=1, sizing_mode='stretch_both'))

# ==============================================================================
# ==============================================================================
# ==============================================================================


if __name__ == "__main__":

    fileName = "42Ca_deformed_1x11.msg.gz"
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

    state = hfb3.State(fileName)
    plot_matplotlib(state, -20, 20, -10, 10)
    # plot_bokeh(state, -20, 20, -10, 10)
