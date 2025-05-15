import os
import matplotlib
from .plt2latex_pgf import get_latex_font_sizes
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from .units import parse_unit
from .rcsetup import rcParams
import importlib.resources as pkg_resources


def sync_fontsize_rcparams_from_named_fonts():
    """
    Synchronize Matplotlib font-related rcParams with the named font sizes
    from plt2latex.rcParams['fontsizes.*'].

    This updates:
    - General font size (`font.size`)
    - Axes titles and labels
    - Tick label sizes
    - Legend font and title
    - Figure title font

    Use this function after updating 'fontsizes.*' or switching LaTeX modes
    to ensure consistency across all plot elements.
    """
    base = rcParams['fontsizes.normalsize']
    matplotlib.rcParams.update({
        'legend.title_fontsize': base,
        'axes.titlesize': base,
        'axes.labelsize': base,
        'xtick.labelsize': base,
        'ytick.labelsize': base,
        'legend.fontsize': rcParams['fontsizes.footnotesize'],
        'figure.titlesize': base,
    })


class Config:
    """
    Global configuration manager for plt2latex.

    This class manages:
    - Whether to use LaTeX (`use_tex`).
    - The selected LaTeX engine (`xelatex`, `lualatex`, `pdflatex`).
    - The backend switch between `pgf` and the original user backend.

    Attributes:
        _USE_TEX (bool): Whether LaTeX rendering is enabled.
        _LATEX_ENGINE (str): The LaTeX engine to use when `use_tex` is enabled.
        _DEFAULT_BACKEND (str): The original Matplotlib backend before any changes.
    """

    _USE_TEX = False  # Default: LaTeX disabled
    _LATEX_ENGINE = "xelatex"  # Default LaTeX engine
    _DEFAULT_BACKEND = None  # Stores the original backend


    @classmethod
    def update_fontsizes(cls, base_size: str | float | None = None):
        """
        Update fontsizes.* in rcParams depending on LaTeX mode.

        Parameters:
            base_size (str | float | None): Base font size to use if not using LaTeX.
                Can be a plain float (assumed pt) or a string with unit (e.g. "10pt", "3mm").
                If None, will use matplotlib.rcParams["font.size"].

        - If use_tex is True → read real sizes from LaTeX via LatexManager.
        - If use_tex is False → calculate sizes from base_size or rcParams["font.size"].
        """
        scale = {
            "tiny":         0.68056,
            "scriptsize":   0.79722,
            "footnotesize": 0.85001,
            "small":        0.92499,
            "normalsize":   1.00,
            "large":        1.17499,
            "Large":        1.40998,
            "LARGE":        1.58498,
            "huge":         1.90235,
            "Huge":         2.28208,
        }

        scale_names = scale.keys()

        if cls._USE_TEX:
            tex_sizes = get_latex_font_sizes()
            for name in scale_names:
                key = f"fontsizes.{name}"
                rcParams[key] = tex_sizes[name]
        else:
            if base_size is None:
                base_val = matplotlib.rcParams.get("font.size", 10)
                base_pt = FontProperties(size=base_val).get_size_in_points()
            else:
                base_pt = parse_unit(base_size, to="pt")

            for name in scale_names:
                key = f"fontsizes.{name}"
                rcParams[key] = round(base_pt * scale[name], 2)

        sync_fontsize_rcparams_from_named_fonts()


    @classmethod
    def use_tex(cls, use_tex: bool, engine: str = "xelatex", backend: str = "plt2latex_pgf"):
        """
        Enables or disables LaTeX rendering in the library.

        Args:
            use_tex (bool): If `True`, LaTeX mode is enabled.
                         If `False`, the library will use the default Matplotlib renderer.
            engine (str, optional): The LaTeX engine to use.
                                    Choices: "xelatex" (default), "lualatex", "pdflatex".
            backend (str, optional): The Matplotlib backend to use when LaTeX is enabled.
                                     Choices: "plt2latex_pgf" (default), "pgf".

        Raises:
            ValueError: If `flag` is not a boolean.
            ValueError: If `engine` is not a valid LaTeX engine.
            ValueError: If `backend` is not a valid backend.

        Example:
            >>> import plt2latex as p2l
            >>> p2l.use_tex(True)  # Uses xelatex (default)
            >>> p2l.use_tex(True, "pdflatex", "pgf")  # Uses pdflatex with default pgf backend
            >>> p2l.use_tex(False)  # Disables LaTeX
        """
        if not isinstance(use_tex, bool):
            raise ValueError("use_tex must be 'True' or 'False', got: {}".format(type(use_tex).__name__))

        valid_engines = {"xelatex", "lualatex", "pdflatex"}
        valid_backends = {"plt2latex_pgf", "pgf"}

        if use_tex and engine not in valid_engines:
            raise ValueError(f"Invalid LaTeX engine: '{engine}'. Choose from {valid_engines}")
        
        if use_tex and backend not in valid_backends:
            raise ValueError(f"Invalid backend for LaTeX mode: '{backend}'. Choose from {valid_backends}")

        cls._USE_TEX = use_tex
        cls._LATEX_ENGINE = engine if use_tex else None

        if cls._DEFAULT_BACKEND is None:
            cls._DEFAULT_BACKEND = matplotlib.get_backend()

        if use_tex:
            backend_map = {
                "plt2latex_pgf": "module://plt2latex.plt2latex_pgf",
                "pgf": "pgf"
            }
            matplotlib.use(backend_map[backend])
            matplotlib.rcParams.update({
                'pgf.texsystem': cls._LATEX_ENGINE if use_tex else "pdflatex",
                'text.usetex': cls._USE_TEX,
                'pgf.rcfonts': False,
                'font.family': 'serif'})
            cls.update_fontsizes()
        else:
            matplotlib.use(cls._DEFAULT_BACKEND)

        # if not use_tex and "inline" in cls._DEFAULT_BACKEND:
        #     IPython.get_ipython().run_line_magic("matplotlib", "inline")


    @classmethod
    def get_use_tex(cls):
        """
        Returns the current LaTeX mode and engine.

        Returns:
            tuple: (bool, str or None) - (LaTeX enabled, selected engine)

        Example:
            >>> Config.get_use_tex()
            (True, "xelatex")
        """
        return cls._USE_TEX, cls._LATEX_ENGINE
    

    @classmethod
    def initial_update_rcparams(cls):
        """
        Updates Matplotlib's rcParams based on the current configuration.
        This method is called automatically when `set_use_tex()` is used.
        """
        # with pkg_resources.path(styles, "base.mplstyle") as style_path:
        #     plt.style.use(str(style_path))
        # style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "base.mplstyle")
        # plt.style.use(style_path)
        style_path = os.path.join(os.path.dirname(__file__), "base.mplstyle")
        plt.style.use(style_path)
        use_tex, latex_engine = cls.get_use_tex()

        cls.update_fontsizes()

        matplotlib.rcParams.update({
            'pgf.texsystem': latex_engine if use_tex else "pdflatex",
            'text.usetex': use_tex,
            'pgf.rcfonts': False,
            'font.family': 'serif'})


        matplotlib.rcParams.update({
            'lines.linewidth': 0.8,
            'boxplot.boxprops.linewidth': 0.4,
            'boxplot.whiskerprops.linewidth': 0.4,
            'boxplot.capprops.linewidth': 0.4,
            'boxplot.medianprops.linewidth': 0.4,
            'boxplot.meanprops.linewidth': 0.4,
            'axes.linewidth': 0.4,

            'legend.title_fontsize': rcParams['fontsizes.normalsize'],
            'font.size': rcParams['fontsizes.normalsize'],
            'axes.titlesize': rcParams['fontsizes.normalsize'],
            'axes.labelsize': rcParams['fontsizes.normalsize'],
            'xtick.labelsize': rcParams['fontsizes.normalsize'],
            'ytick.labelsize': rcParams['fontsizes.normalsize'],
            'legend.fontsize': rcParams['fontsizes.normalsize'],
            'figure.titlesize': rcParams['fontsizes.normalsize'],

            'figure.constrained_layout.use': True,
            'figure.constrained_layout.h_pad': 0.1/72.27,
            'figure.constrained_layout.w_pad': 0.1/72.27,
            'figure.constrained_layout.hspace': 2/72.27,
            'figure.constrained_layout.wspace': 2/72.27,

            'axes.autolimit_mode': "data",
            # 'axes.axisbelow': False,

            # 'legend.borderpad': 0.1,
            # 'legend.framelinewidth': 0.4,
            # 'figure.figsize': (textwidth, textwidth/ratio),
            # 'axes.grid': True,
            # 'axes.titlepad': 4.0,
            # 'axes.labelpad': 2.0,
            # 'legend.fancybox': False,
            # 'legend.borderpad': 0.4,
            'axes.xmargin': .05,
            'axes.ymargin': .05,
            'axes.zmargin': .05,
            # 'errorbar.capsize': 1,
            # 'axes.grid.which': "both",
            # 'legend.numpoints': 1,
            'figure.dpi': 100,
            # 'figure.facecolor': "white",
        })


        # === Cubehelix palette generator ===


