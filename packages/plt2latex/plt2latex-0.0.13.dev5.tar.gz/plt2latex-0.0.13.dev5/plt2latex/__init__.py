from .config import Config
from .figure import set_figsize, set_font
from .renderer import savefig
from .patcher import enable_all_patches
from .rcsetup import rcParams

Config.initial_update_rcparams()
enable_all_patches()

use_tex = Config.use_tex
get_tex_mode = Config.get_use_tex

__all__ = ["use_tex", "get_tex_mode", rcParams]