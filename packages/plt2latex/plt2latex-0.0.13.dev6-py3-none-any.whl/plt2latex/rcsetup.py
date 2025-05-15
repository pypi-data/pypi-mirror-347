from matplotlib import RcParams as MatplotlibRcParams
import matplotlib.rcsetup as rcsetup
import matplotlib as mpl
from typing import Any
from .units import parse_unit


def validate_font_size_method(val: Any) -> str:
    valid_options = ['default', 'precise']
    if val not in valid_options:
        raise ValueError(
            f"Invalid value for 'font_size_method': {val!r}. "
            f"Expected one of: {valid_options}"
        )
    return val


def validate_positive_unit_float(val: Any) -> float:
    """
    Accepts a string with unit (e.g. '12pt', '0.3mm', '2.5in') or a number.
    Converts to pt and validates it's positive.
    """
    try:
        pt = parse_unit(val, to="pt")
    except Exception as e:
        raise ValueError(f"Invalid font size: {val!r}. Expected a number or unit string (e.g. '12pt', '5mm')") from e

    if pt <= 0:
        raise ValueError(f"Font size must be positive, got {pt!r} pt")
    return pt


class Plt2LatexRcParams(MatplotlibRcParams):
    """
    Minimal RcParams subclass that only includes plt2latex-specific parameters.
    Fully supports validation, rc-like API, and optional sync with matplotlib.
    """

    _custom_params = {
        'font_size_method': (
            'default',
            validate_font_size_method,
            '[default | precise]'
        ),

        'latex_documentclass': (
            r'\documentclass{article}',
            rcsetup.validate_string,
            r'LaTeX \documentclass'
        ),

        # Font size definitions (in pt)
        'fontsizes.tiny':         ( 6.8, validate_positive_unit_float, r'font size for \tiny'),
        'fontsizes.scriptsize':   ( 8.0, validate_positive_unit_float, r'font size for \scriptsize'),
        'fontsizes.footnotesize': ( 8.5, validate_positive_unit_float, r'font size for \footnotesize'),
        'fontsizes.small':        ( 9.3, validate_positive_unit_float, r'font size for \small'),
        'fontsizes.normalsize':   (10.0, validate_positive_unit_float, r'font size for \normalsize'),
        'fontsizes.large':        (11.8, validate_positive_unit_float, r'font size for \large'),
        'fontsizes.Large':        (14.0, validate_positive_unit_float, r'font size for \Large'),
        'fontsizes.LARGE':        (15.9, validate_positive_unit_float, r'font size for \LARGE'),
        'fontsizes.huge':         (19.0, validate_positive_unit_float, r'font size for \huge'),
        'fontsizes.Huge':         (22.8, validate_positive_unit_float, r'font size for \Huge'),
    }

    def __init__(self):
        # Register validators for each custom param
        for key, (_, validator, _) in self._custom_params.items():
            rcsetup._validators.setdefault(key, validator)

        # Initialize with only custom parameters
        init_dict = {
            key: mpl.rcParams.get(key, default)
            for key, (default, _, _) in self._custom_params.items()
        }

        super().__init__(init_dict)

    def __setitem__(self, key: str, val: Any):
        # Validate and store
        super().__setitem__(key, val)

    def describe(self):
        print("plt2latex rcParams:")
        for key, (default, _, desc) in self._custom_params.items():
            print(f"  {key} = {self.get(key)!r}  {desc}")

rcParams = Plt2LatexRcParams()
