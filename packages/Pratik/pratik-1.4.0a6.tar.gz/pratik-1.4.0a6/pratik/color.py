class Color:
    @staticmethod
    def by_hsv(h, s, v, alpha=1.0):
        """ To convert from HSV to RGB

        Arguments:
            h (float): Hue H ∈ [0, 1]
            s (float): Saturation S ∈ [0, 1]
            v (float): Value V ∈ [0, 1]
            alpha (float): Alpha ∈ [0, 1]

        Returns:
            (Color): Color of HSV values.

        Raises:
            ValueError: If the values are not between 0 and 1.
        """
        if h < 0 or 1 < h:
            raise ValueError("Hue must be between 0 and 1 (include)")
        if s < 0 or 1 < s:
            raise ValueError("Saturation must be between 0 and 1 (include)")
        if v < 0 or 1 < v:
            raise ValueError("Value must be between 0 and 1 (include)")
        if alpha < 0 or 1 < alpha:
            raise ValueError("Alpa must be between 0 and 1 (include)")

        def f(n):
            k = (n + h * 6) % 6
            return v - (v * s * max(0, min(k, 4 - k, 1)))

        return Color(f(5), f(3), f(1))

    @staticmethod
    def by_hsl(h, s, l, alpha=1.0):
        """ To convert from HSL to RGB

        Arguments:
            h (float): Hue H ∈ [0, 1]
            s (float): Saturation S ∈ [0, 1]
            l (float): Lightness L ∈ [0, 1]
            alpha (float): Alpha ∈ [0, 1]

        Returns:
            (Color): Color of HSL values.

        Raises:
            ValueError: If the values are not between 0 and 1.
        """

        def hue(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        if h < 0 or 1 < h:
            raise ValueError("Hue must be between 0 and 1 (include)")
        if s < 0 or 1 < s:
            raise ValueError("Saturation must be between 0 and 1 (include)")
        if l < 0 or 1 < l:
            raise ValueError("Light must be between 0 and 1 (include)")
        if alpha < 0 or 1 < alpha:
            raise ValueError("Alpa must be between 0 and 1 (include)")

        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue(p, q, h + 1 / 3)
            g = hue(p, q, h)
            b = hue(p, q, h - 1 / 3)

        return Color(r, g, b)

    @staticmethod
    def by_rgb255(r, g, b, alpha=255):
        """ To convert from RGB ∈ [0, 255] to RGB ∈ [0, 1]

        Arguments:
            r (int): Red ∈ [0, 255]
            g (int): Green ∈ [0, 255]
            b (int): Blue ∈ [0, 255]
            alpha (int): Alpha ∈ [0, 255]

        Returns:
            Color: Color of RGB values.

        Raises:
            ValueError: If the values are not between 0 and 255.
        """
        if r < 0 or 255 < r:
            raise ValueError("Red must be between 0 and 255 (include)")
        if g < 0 or 255 < g:
            raise ValueError("Green must be between 0 and 255 (include)")
        if b < 0 or 255 < b:
            raise ValueError("Blue must be between 0 and 255 (include)")
        if alpha < 0 or 255 < alpha:
            raise ValueError("Alpa must be between 0 and 255 (include)")
        return Color(r / 255.0, g / 255.0, b / 255.0)

    @staticmethod
    def by_hexadecimal(hexadecimal):
        """ To convert from hexadecimal

        Arguments:
            hexadecimal (str): The hexadecimal value to convert.

        Returns:
            (Color): Color of hexadecimal values.
        """
        hexadecimal = hexadecimal.removeprefix('#')
        if len(hexadecimal) == 6:
            return Color.by_rgb255(
                int(hexadecimal[:2], 16),
                int(hexadecimal[2:4], 16),
                int(hexadecimal[4:], 16)
            )
        else:
            return Color.by_rgb255(
                int(hexadecimal[2:4], 16),
                int(hexadecimal[4:6], 16),
                int(hexadecimal[6:], 16),
                int(hexadecimal[:2], 16)
            )

    def __init__(self, r, g, b, alpha=1.0):
        """ Color Constructor

        Arguments:
            r (float): Red ∈ [0, 1]
            g (float): Green ∈ [0, 1]
            b (float): Blue ∈ [0, 1]
            alpha (float): Alpha ∈ [0, 1]

        Raises:
            ValueError: If the values are not between 0 and 1.
        """
        if r < 0 or 1 < r:
            raise ValueError("Red must be between 0 and 1 (include)")
        if g < 0 or 1 < g:
            raise ValueError("Green must be between 0 and 1 (include)")
        if b < 0 or 1 < b:
            raise ValueError("Blue must be between 0 and 1 (include)")
        if alpha < 0 or 1 < alpha:
            raise ValueError("Alpa must be between 0 and 1 (include)")

        self.red: float = r
        self.green: float = g
        self.blue: float = b
        self.alpha: float = alpha

    def __str__(self):
        return f"({self.red255}, {self.green255}, {self.blue255})"

    def __repr__(self):
        return f"<red:{self.red255}, green:{self.green255}, blue:{self.blue255}" + (
            f", alpha:{self.alpha255}>" if self.alpha != 1.0 else ">")

    def __int__(self):
        return int(self.hexadecimal[1:], 16)

    def __index__(self):
        return int(self)

    @property
    def hexadecimal(self):
        return f"#{f'{hex(self.alpha255)[2:]:02}' if self.alpha != 1.0 else ''}{hex(self.red255)[2:]:02}{hex(self.green255)[2:]:02}{hex(self.blue255)[2:]:02}".upper()

    @property
    def rgb255(self):
        return self.red255, self.green255, self.blue255

    @property
    def red255(self):
        return round(self.red * 255)

    @property
    def green255(self):
        return round(self.green * 255)

    @property
    def blue255(self):
        return round(self.blue * 255)

    @property
    def alpha255(self):
        return round(self.alpha * 255)

    @property
    def max(self):
        return max(self.red, self.green, self.blue)

    @property
    def min(self):
        return min(self.red, self.green, self.blue)

    @property
    def hsl(self):
        v_max = self.max
        v_min = self.min

        l = (v_max + v_min) / 2
        if v_max == v_min:
            return 0, 0, l
        else:
            d = v_max - v_min
            s = d / (2 - v_max - v_min) if l > 0.5 else d / (v_max + v_min)

            if v_max == self.red:
                h = (self.green - self.blue) / d + (6 if self.green < self.blue else 0)
            elif v_max == self.green:
                h = (self.blue - self.red) / d + 2
            else:
                h = (self.red - self.green) / d + 4

            h /= 6

            return h, s, l

    @property
    def range(self):
        return self.max - self.min

    @property
    def value(self):
        return self.max

    @property
    def chroma(self):
        return self.range

    @property
    def lightness(self):
        return round((self.max + self.min) / 2, 2)

    @property
    def hue(self):
        v_max = self.max
        v_min = self.min
        if v_max == v_min:
            return 0
        else:
            d = v_max - v_min

            if v_max == self.red:
                hue = (self.green - self.blue) / d + (6 if self.green < self.blue else 0)
            elif v_max == self.green:
                hue = (self.blue - self.red) / d + 2
            else:
                hue = (self.red - self.green) / d + 4

            hue /= 6

            return round(hue, 2)

    @property
    def saturation_value(self):
        return 0 if self.value == 0 else self.chroma / self.value

    @property
    def saturation_lightness(self):
        v_max = self.max
        v_min = self.min
        return round(
            0
            if v_max == v_min else
            (
                (v_max - v_min) / (2 - v_max - v_min)
                if ((v_max + v_min) / 2) > 0.5 else
                (v_max - v_min) / (v_max + v_min)
            ), 2
        )

    @property
    def ascii(self):
        return f"\033[38;2;{self.red255};{self.green255};{self.blue255}m"

    def copy(self):
        return Color(self.red, self.green, self.blue, self.alpha)


if __name__ == '__main__':
    print(int(Color.by_hexadecimal("#00FF00")))
