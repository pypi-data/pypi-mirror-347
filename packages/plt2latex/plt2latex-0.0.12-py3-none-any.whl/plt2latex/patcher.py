from matplotlib.legend import Legend
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from matplotlib import rcParams
from matplotlib import RcParams
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import functools

from collections.abc import Iterable

from .fontsizes import font
from .units import parse_unit
from .config import Config

_already_patched = False


def convert_units(val, *, target="pt"):
    if isinstance(val, (int, float)):
        return val

    if isinstance(val, str):
        val = val.strip()
        try:
            return parse_unit(val, to=target)
        except Exception:
            try:
                return getattr(font, val)
            except AttributeError:
                return val

    if isinstance(val, Iterable) and not isinstance(val, (str, bytes)):
        return type(val)(convert_units(v, target=target) for v in val)

    return val


def patch_units():
    """Патчит Matplotlib для поддержки LaTeX-стилей и единиц в строковом виде."""

    # === 1. Artist.update (все визуальные объекты) ===
    if not hasattr(Artist, "_original_update"):
        Artist._original_update = Artist.update

        def _patched_update(self, props):
            converted = {k: convert_units(v) for k, v in props.items()}
            return Artist._original_update(self, converted)

        Artist.update = _patched_update

    # === 2. rcParams[...] = ... (глобальные стили) ===
    if not hasattr(rcParams, "_original_setitem"):
        rcParams._original_setitem = rcParams.__setitem__

        def _patched_rc_setitem(self, key, value):
            converted = convert_units(value)
            return rcParams._original_setitem(self, key, converted)

        rcParams.__setitem__ = _patched_rc_setitem.__get__(rcParams)

    # === 3. FontProperties.set_size (шрифты: legend, label и т.д.) ===
    if not hasattr(FontProperties, "_original_set_size"):
        FontProperties._original_set_size = FontProperties.set_size

        def _patched_set_size(self, size):
            size = convert_units(size)
            return FontProperties._original_set_size(self, size)

        FontProperties.set_size = _patched_set_size

    # === 4. Figure.__init__ (физический размер Figure — в дюймах!) ===
    if not hasattr(Figure, "_original_init"):
        Figure._original_init = Figure.__init__

        def _patched_figure_init(self, *args, **kwargs):
            if "figsize" in kwargs:
                kwargs["figsize"] = convert_units(kwargs["figsize"], target="in")
            return Figure._original_init(self, *args, **kwargs)

        Figure.__init__ = _patched_figure_init

    # === 5. Перехват функций pyplot (text, xlabel, plot, legend, ...) ===
    def _patch_pyplot_function(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs = {k: convert_units(v) for k, v in kwargs.items()}
            return func(*args, **kwargs)
        return wrapper

    _pyplot_funcs = [
        "plot", "scatter", "bar", "barh", "hist", "boxplot", "errorbar", "pie",
        "xlabel", "ylabel", "title", "legend", "text", "annotate"
    ]

    for name in _pyplot_funcs:
        if hasattr(plt, name):
            original = getattr(plt, name)
            if not hasattr(original, "_is_units_patched"):
                wrapped = _patch_pyplot_function(original)
                wrapped._is_units_patched = True
                setattr(plt, name, wrapped)
    

def patch_font_properties():
    if not hasattr(FontProperties, "_original_set_size"):
        FontProperties._original_set_size = FontProperties.set_size

        def _patched_set_size(self, size):
            try:
                size = convert_units(size)  # ← используем твой convert_units
            except Exception:
                pass
            return FontProperties._original_set_size(self, size)

        FontProperties.set_size = _patched_set_size


def patch_legend_frame_style_from_axes():
    _original_init = Legend.__init__

    def _patched_init(self, *args, **kwargs):
        user_linewidth = kwargs.pop("frame_linewidth", None)
        _original_init(self, *args, **kwargs)
        axes = getattr(self, "axes", None)

        if user_linewidth is None and isinstance(axes, Axes):
            linewidth = axes.spines['left'].get_linewidth()
        elif user_linewidth is not None:
            linewidth = user_linewidth
        else:
            linewidth = 0.8  # fallback по умолчанию

        self.get_frame().set_linewidth(linewidth)

    Legend.__init__ = _patched_init


def patch_bar_tick_hiding():
    _original_bar = Axes.bar
    _original_barh = Axes.barh
    _original_hist = Axes.hist

    def _patched_hist(self, *args, **kwargs):
        self._suppress_bar_tick_patch = True
        try:
            return _original_hist(self, *args, **kwargs)
        finally:
            self._suppress_bar_tick_patch = False

    def _patched_bar(self, *args, **kwargs):
        # Если вызов из barh или hist — ничего не делаем
        if getattr(self, "_suppress_bar_tick_patch", False):
            return _original_bar(self, *args, **kwargs)

        bars = _original_bar(self, *args, **kwargs)
        self.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
        return bars

    def _patched_barh(self, *args, **kwargs):
        self._suppress_bar_tick_patch = True  # подавим вызов bar()
        bars = _original_barh(self, *args, **kwargs)
        self._suppress_bar_tick_patch = False
        self.tick_params(axis='y', which='both', left=False, right=False, labelleft=True)
        return bars

    Axes.bar = _patched_bar
    Axes.barh = _patched_barh
    Axes.hist = _patched_hist


def limit_tick_density(fig, font_factor=2, min_ratio=10):
    """
    Ограничивает плотность тиков только на тех осях, где
    размер шрифта превышает axis_size / min_ratio.
    """
    for ax in fig.axes:
        for axis_name in ['x', 'y']:
            axis = ax.xaxis if axis_name == 'x' else ax.yaxis
            locator = axis.get_major_locator()
            if not isinstance(locator, MaxNLocator):
                continue

            # Размер шрифта → в пикселях
            fontsize_pt = rcParams.get(f"{axis_name}tick.labelsize", 10)
            dpi = fig.dpi
            fontsize_px = fontsize_pt * dpi / parse_unit("1in", to="pt")

            # Размер оси
            bbox = ax.get_window_extent()
            axis_px = bbox.width if axis_name == 'x' else bbox.height

            # Если размер оси достаточно велик — пропускаем
            if axis_px / fontsize_px > min_ratio:
                continue

            # Ограничиваем количество тиков
            label_width = fontsize_px * font_factor
            max_ticks = max(2, int(axis_px / label_width))
            locator.set_params(nbins=max_ticks)

def patch_tick_density_auto(font_factor=2, min_ratio=15):
    """Патчит Figure.draw для авто-ограничения плотности тиков."""
    if hasattr(Figure, "_tick_density_patched"):
        return
    Figure._tick_density_patched = True

    _original_draw = Figure.draw

    def _patched_draw(self, renderer):
        _original_draw(self, renderer)
        limit_tick_density(self, font_factor=font_factor, min_ratio=min_ratio)

    Figure.draw = _patched_draw


def patch_font_size_autoupdate():
    """
    Monkey-patch matplotlib.rcParams.__class__.__setitem__ to hook font.size changes.
    """
    _original_setitem = RcParams.__setitem__

    def patched_setitem(self, key, val):
        _original_setitem(self, key, val)
        if key == "font.size" and not self.get("text.usetex", False):
            Config.update_fontsizes()

    RcParams.__setitem__ = patched_setitem


def enable_all_patches():
    global _already_patched
    if _already_patched:
        return
    _already_patched = True

    patch_legend_frame_style_from_axes()
    patch_bar_tick_hiding()
    patch_units()
    patch_font_properties()
    patch_tick_density_auto()
    patch_font_size_autoupdate()