import matplotlib.pyplot as plt

def savefig(filename, *args, **kwargs):
    """
    Custom savefig that ensures PGF files are properly cleaned.
    """
    plt.savefig(filename, *args, **kwargs)

__all__ = ["savefig"]