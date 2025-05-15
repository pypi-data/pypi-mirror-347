_FONT_SIZES = {
    "tiny": 7.33325,
    "scriptsize": 8.50012,
    "footnotesize": 10.00002,
    "small": 10.95003,
    "normalsize": 11.74988,
    "large": 14.09984,
    "Large": 15.84985,
    "LARGE": 19.0235,
    "huge": 22.82086,
}

class FontSizes:
    def __getattr__(self, name: str) -> float:
        try:
            return _FONT_SIZES[name]
        except KeyError:
            raise AttributeError(f"No such LaTeX font size: '{name}'")

    def __getitem__(self, name: str) -> float:
        return self.__getattr__(name)

font = FontSizes()