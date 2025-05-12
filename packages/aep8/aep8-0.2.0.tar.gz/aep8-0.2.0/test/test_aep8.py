import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

import aep8


def test_version():
    assert isinstance(aep8.__version__, str)


@pytest.mark.parametrize("particle", ["e", "p"])
@pytest.mark.parametrize("solar", ["min", "max"])
@pytest.mark.parametrize("kind", ["differential", "integral"])
@pytest.mark.mpl_image_compare
@plt.style.context("seaborn-v0_8-notebook")
def test_plot_flux(particle, solar, kind):
    lon = np.linspace(-180, 180, 100) * u.deg
    lat = np.linspace(-90, 90, 100) * u.deg
    height = 500 * u.km
    location = EarthLocation.from_geodetic(*np.meshgrid(lon, lat), height)
    time = Time("2025-01-01")
    energy = 1 * u.MeV
    flux = aep8.flux(location, time, energy, kind=kind, solar=solar, particle=particle)
    fig, ax = plt.subplots()
    ax.set_title(f"{kind} {solar} {particle} flux: {height}, {energy}")
    ax.set_xlabel(f"Longitude ({lon.unit})")
    ax.set_ylabel(f"Longitude ({lon.unit})")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.tick_params(direction="out")
    ax.xaxis.set_major_locator(MultipleLocator(90))
    ax.yaxis.set_major_locator(MultipleLocator(45))
    ax.grid(color="white", linestyle="-", alpha=0.5)
    plt.colorbar(ax.pcolor(lon.value, lat.value, flux.value, cmap="inferno")).set_label(
        f"Flux ({flux.unit})"
    )
    return fig
