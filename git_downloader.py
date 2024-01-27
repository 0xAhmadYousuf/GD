# made by billythegoat356, loTus01, and BlueRed

# https://github.com/billythegoat356 https://github.com/loTus04 https://github.com/CSM-BlueRed

# Version : 2.0 (added Colorate.Format, added Banner.Arrow, added Anime.Move, added Center.GroupAlign, added Center.TextAlign, updated Box to Banner, updated Box.Lines))

# based on pyfade anc pycenter, R.I.P

# <3


from os import name as _name, system as _system, get_terminal_size as _terminal_size, terminal_size
from sys import stdout as _stdout
from time import sleep as _sleep
from threading import Thread as _thread


if _name == 'nt':
    from ctypes import c_int, c_byte, Structure, byref, windll

    class _CursorInfo(Structure):
        _fields_ = [("size", c_int),
                    ("visible", c_byte)]


class System:

    """
    1 variable:
        Windows      |      tells if the user is on Windows OS or not
    5 functions:
        Init()       |      initialize the terminal to allow the use of colors
        Clear()      |      clear the terminal
        Title()      |      set the title of terminal, only for Windows
        Size()       |      set the size of terminal, only for Windows
        Command()    |      enter a shell command
    """

    Windows = _name == 'nt'

    def Init():
        _system('')

    def Clear():
        return _system("cls" if System.Windows else "clear")

    def Title(title: str):
        if System.Windows:
            return _system(f"title {title}")

    def Size(x: int, y: int):
        if System.Windows:
            return _system(f"mode {x}, {y}")

    def Command(command: str):
        return _system(command)



class Cursor:

    """
    2 functions:
        HideCursor()      |      hides the white blinking in the terminal
        ShowCursor()      |      shows the white blinking in the terminal
    """

    def HideCursor():
        if _name == 'nt':
            Cursor._cursor(False)
        elif _name == 'posix':
            _stdout.write("\033[?25l")
            _stdout.flush()

    def ShowCursor():
        if _name == 'nt':
            Cursor._cursor(True)
        elif _name == 'posix':
            _stdout.write("\033[?25h")
            _stdout.flush()

    """ ! developper area ! """

    def _cursor(visible: bool):
        ci = _CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, byref(ci))
        ci.visible = visible
        windll.kernel32.SetConsoleCursorInfo(handle, byref(ci))


class _MakeColors:

    """ ! developper area ! """

    def _makeansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"

    def _rmansi(col: str) -> str:
        return col.replace('\033[38;2;', '').replace('m','').replace('50m', '').replace('\x1b[38', '')

    def _makergbcol(var1: list, var2: list) -> list:
        col = list(var1[:12])
        for _col in var2[:12]:
            col.append(_col)
        for _col in reversed(col):
            col.append(_col)
        return col

    def _start(color: str) -> str:
        return f"\033[38;2;{color}m"

    def _end() -> str:
        return "\033[38;2;255;255;255m"

    def _maketext(color: str, text: str, end: bool = False) -> str:
        end = _MakeColors._end() if end else ""
        return color+text+end

    def _getspaces(text: str) -> int:
        return len(text) - len(text.lstrip())

    def _makerainbow(*colors) -> list:
        colors = [color[:24] for color in colors]
        rainbow = []
        for color in colors:
            for col in color:
                rainbow.append(col)
        return rainbow

    def _reverse(colors: list) -> list:
        _colors = list(colors)
        for col in reversed(_colors):
            colors.append(col)
        return colors

    def _mixcolors(col1: str, col2: str, _reverse: bool = True) -> list:
        col1, col2 = _MakeColors._rmansi(col=col1), _MakeColors._rmansi(col=col2)
        fade1 = Colors.StaticMIX([col1, col2], _start=False)      
        fade2 = Colors.StaticMIX([fade1, col2], _start=False)
        fade3 = Colors.StaticMIX([fade1, col1], _start=False)
        fade4 = Colors.StaticMIX([fade2, col2], _start=False)
        fade5 = Colors.StaticMIX([fade1, fade3], _start=False)    
        fade6 = Colors.StaticMIX([fade3, col1], _start=False)
        fade7 = Colors.StaticMIX([fade1, fade2], _start=False)
        mixed = [col1, fade6, fade3, fade5, fade1, fade7, fade2, fade4, col2]
        return _MakeColors._reverse(colors=mixed) if _reverse else mixed 

class Colors:

    """
    54 variables (colors)

    3 lists:
        static_colors      |      colors that are static, ex: 'red' (can't be faded)
        dynamic_colors     |      colors that are dynamic, ex: 'blue_to_purple' (can be faded)
        all_colors         |      every color of static_colors and dynamic_colors
        
    3 functions:
        StaticRGB()        |      create your own fix/static color
        DynamicRGB()       |      create your own faded/dynamic color (soon...)
        StaticMIX()        |      mix two or more static colors
        DynamicMIX()       |      mix two or more dynamic colors
        Symbol()           |      create a colored symbol, ex: '[!]'
    """

    def StaticRGB(r: int, g: int, b: int) -> str:
        return _MakeColors._start(f"{r};{g};{b}")

    def DynamicRGB(r1: int, g1: int, b1: int, r2: int,
                   g2: int, b2: int) -> list: ...

    def StaticMIX(colors: list, _start: bool = True) -> str:
        rgb = []
        for col in colors:
            col = _MakeColors._rmansi(col=col)
            col = col.split(';')
            r = int(int(col[0]))
            g = int(int(col[1]))
            b = int(int(col[2]))
            rgb.append([r, g, b])
        r = round(sum(rgb[0] for rgb in rgb) / len(rgb))
        g = round(sum(rgb[1] for rgb in rgb) / len(rgb))
        b = round(sum(rgb[2] for rgb in rgb) / len(rgb))
        rgb = f'{r};{g};{b}'
        return _MakeColors._start(rgb) if _start else rgb

    def DynamicMIX(colors: list):
        _colors = []
        for color in colors:
            if colors.index(color) == len(colors) - 1:
                break
            _colors.append([color, colors[colors.index(color) + 1]])
        colors = [_MakeColors._mixcolors(col1=color[0], col2=color[1], _reverse=False) for color in _colors]

        final = []
        for col in colors:
            for col in col:
                final.append(col)
        return _MakeColors._reverse(colors=final)
            


    """ symbols """

    def Symbol(symbol: str, col: str, col_left_right: str, left: str = '[', right: str = ']') -> str:
        return f"{col_left_right}{left}{col}{symbol}{col_left_right}{right}{Col.reset}"


    """ dynamic colors """

    black_to_white = ["m;m;m"]
    black_to_red = ["m;0;0"]
    black_to_green = ["0;m;0"]
    black_to_blue = ["0;0;m"]

    white_to_black = ["n;n;n"]
    white_to_red = ["255;n;n"]
    white_to_green = ["n;255;n"]
    white_to_blue = ["n;n;255"]

    red_to_black = ["n;0;0"]
    red_to_white = ["255;m;m"]
    red_to_yellow = ["255;m;0"]
    red_to_purple = ["255;0;m"]

    green_to_black = ["0;n;0"]
    green_to_white = ["m;255;m"]
    green_to_yellow = ["m;255;0"]
    green_to_cyan = ["0;255;m"]

    blue_to_black = ["0;0;n"]
    blue_to_white = ["m;m;255"]
    blue_to_cyan = ["0;m;255"]
    blue_to_purple = ["m;0;255"]

    yellow_to_red = ["255;n;0"]
    yellow_to_green = ["n;255;0"]

    purple_to_red = ["255;0;n"]
    purple_to_blue = ["n;0;255"]

    cyan_to_green = ["0;255;n"]
    cyan_to_blue = ["0;n;255"]


    red_to_blue = ...
    red_to_green = ...

    green_to_blue = ...
    green_to_red = ...

    blue_to_red = ...
    blue_to_green = ...

    rainbow = ...

    """ static colors """

    red = _MakeColors._start('255;0;0')
    green = _MakeColors._start('0;255;0')
    blue = _MakeColors._start('0;0;255')

    white = _MakeColors._start('255;255;255')
    black = _MakeColors._start('0;0;0')
    gray = _MakeColors._start('150;150;150')

    yellow = _MakeColors._start('255;255;0')
    purple = _MakeColors._start('255;0;255')
    cyan = _MakeColors._start('0;255;255')

    orange = _MakeColors._start('255;150;0')
    pink = _MakeColors._start('255;0;150')
    turquoise = _MakeColors._start('0;150;255')

    light_gray = _MakeColors._start('200;200;200')
    dark_gray = _MakeColors._start('100;100;100')

    light_red = _MakeColors._start('255;100;100')
    light_green = _MakeColors._start('100;255;100')
    light_blue = _MakeColors._start('100;100;255')

    dark_red = _MakeColors._start('100;0;0')
    dark_green = _MakeColors._start('0;100;0')
    dark_blue = _MakeColors._start('0;0;100')

    reset = white

    """ ! developper area ! """

    col = (list, str)

    dynamic_colors = [
        black_to_white, black_to_red, black_to_green, black_to_blue,
        white_to_black, white_to_red, white_to_green, white_to_blue,

        red_to_black, red_to_white, red_to_yellow, red_to_purple,
        green_to_black, green_to_white, green_to_yellow, green_to_cyan,
        blue_to_black, blue_to_white, blue_to_cyan, blue_to_purple,

        yellow_to_red, yellow_to_green,
        purple_to_red, purple_to_blue,
        cyan_to_green, cyan_to_blue
    ]

    for color in dynamic_colors:
        _col = 20
        reversed_col = 220

        dbl_col = 20
        dbl_reversed_col = 220

        content = color[0]
        color.pop(0)

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(reversed_col))
                color.append(result)

            _col += 20
            reversed_col -= 20

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(dbl_reversed_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(dbl_col))
                color.append(result)

            dbl_col += 20
            dbl_reversed_col -= 20

    red_to_blue = _MakeColors._makergbcol(red_to_purple, purple_to_blue)
    red_to_green = _MakeColors._makergbcol(red_to_yellow, yellow_to_green)

    green_to_blue = _MakeColors._makergbcol(green_to_cyan, cyan_to_blue)
    green_to_red = _MakeColors._makergbcol(green_to_yellow, yellow_to_red)

    blue_to_red = _MakeColors._makergbcol(blue_to_purple, purple_to_red)
    blue_to_green = _MakeColors._makergbcol(blue_to_cyan, cyan_to_green)

    rainbow = _MakeColors._makerainbow(
        red_to_green, green_to_blue, blue_to_red)

    for _col in (
        red_to_blue, red_to_green,
        green_to_blue, green_to_red,
        blue_to_red, blue_to_green
    ): dynamic_colors.append(_col)

    dynamic_colors.append(rainbow)

    static_colors = [
        red, green, blue,
        white, black, gray,
        yellow, purple, cyan,
        orange, pink, turquoise,
        light_gray, dark_gray,
        light_red, light_green, light_blue,
        dark_red, dark_green, dark_blue,
        reset
    ]

    all_colors = [color for color in dynamic_colors]
    for color in static_colors:
        all_colors.append(color)


Col = Colors


class Colorate:

    """
    6 functions:
        Static colors:
            Color()                 |            color a text with a static color
            Error()                 |            make an error with red text and advanced arguments
            Format()                |            set different colors for different parts of a text
        Dynamic colors:
            Vertical()              |           fade a text vertically
            Horizontal()            |           fade a text horizontally
            Diagonal()              |           fade a text diagonally
            DiagonalBackwards()     |           fade a text diagonally but backwards
    """

    """ fix/static colors """

    def Color(color: str, text: str, end: bool = True) -> str:
        return _MakeColors._maketext(color=color, text=text, end=end)

    def Error(text: str, color: str = Colors.red, end: bool = False, spaces: bool = 1, enter: bool = True, wait: int = False) -> str:
        content = _MakeColors._maketext(
            color=color, text="\n" * spaces + text, end=end)
        if enter:
            var = input(content)
        else:
            print(content)
            var = None

        if wait is True:
            exit()
        elif wait is not False:
            _sleep(wait)

        return var

    """ faded/dynamic colors"""

    def Vertical(color: list, text: str, speed: int = 1, start: int = 0, stop: int = 0, cut: int = 0, fill: bool = False) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = ""

        nstart = 0
        color_n = 0
        for lin in lines:
            colorR = color[color_n]
            if fill:
                result += " " * \
                    _MakeColors._getspaces(
                        lin) + "".join(_MakeColors._makeansi(colorR, x) for x in lin.strip()) + "\n"
            else:
                result += " " * \
                    _MakeColors._getspaces(
                        lin) + _MakeColors._makeansi(colorR, lin.strip()) + "\n"  

            if nstart != start:
                nstart += 1
                continue

            if lin.rstrip():
                if (
                    stop == 0
                    and color_n + speed < len(color)
                    or stop != 0
                    and color_n + speed < stop
                ):
                    color_n += speed
                elif stop == 0:
                    color_n = 0
                else:
                    color_n = stop

        return result.rstrip()

    def Horizontal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = ""

        for lin in lines:
            carac = list(lin)
            color_n = 0
            for car in carac:
                colorR = color[color_n]
                result += " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip())
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 0
            result += "\n"
        return result.rstrip()

    def Diagonal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:

        color = color[cut:]
        lines = text.splitlines()
        result = ""
        color_n = 0
        for lin in lines:
            carac = list(lin)
            for car in carac:
                colorR = color[color_n]
                result += " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip())
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 1
            result += "\n"

        return result.rstrip()

    def DiagonalBackwards(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]

        lines = text.splitlines()
        result = ""
        resultL = ''
        color_n = 0
        for lin in lines:
            carac = list(lin)
            carac.reverse()
            resultL = ''
            for car in carac:
                colorR = color[color_n]
                resultL = " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip()) + resultL
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 0
            result = result + '\n' + resultL
        return result.strip()

    def Format(text: str, second_chars: list, mode, principal_col: Colors.col, second_col: str):
        if mode == Colorate.Vertical:
            ctext = mode(principal_col, text, fill=True)
        else:
            ctext = mode(principal_col, text)
        ntext = ""
        for x in ctext:
            if x in second_chars:
                x = Colorate.Color(second_col, x)
            ntext += x
        return ntext


class Anime:

    """
    2 functions:
        Fade()                  |            make a small animation with a changing color text, using a dynamic color
        Move()                  |            make a small animation moving the text from left to right
        Bar()                   |            a fully customizable charging bar
        Anime()                 |            a mix between Fade() and Move(), available soon
    """

    def Fade(text: str, color: list, mode, time=True, interval=0.05, hide_cursor: bool = True, enter: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(time) == int:
            time *= 15

        global passed
        passed = False

        if enter:
            th = _thread(target=Anime._input)
            th.start()

        if time is True:
            while True:
                if passed is not False:
                    break
                Anime._anime(text, color, mode, interval)
                ncolor = color[1:]
                ncolor.append(color[0])
                color = ncolor

        else:
            for _ in range(time):
                if passed is not False:
                    break
                Anime._anime(text, color, mode, interval)
                ncolor = color[1:]
                ncolor.append(color[0])
                color = ncolor

        if hide_cursor:
            Cursor.ShowCursor()

    def Move(text: str, color: list, time = True, interval = 0.01, hide_cursor: bool = True, enter: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(time) == int:
            time *= 15

        global passed
        passed = False

        columns = _terminal_size().columns

        if enter:
            th = _thread(target = Anime._input)
            th.start()

        count = 0
        mode = 1

        if time is True:
            while not passed:
                if mode == 1:
                    if count >= (columns - (max(len(txt) for txt in text.splitlines()) + 1)):
                        mode = 2
                    count += 1
                elif mode == 2:
                    if count <= 0:
                        mode = 1
                    count -= 1
                Anime._anime('\n'.join((' ' * count) + line for line in text.splitlines()), color or [], lambda a, b: b, interval)
        else:
            for _ in range(time):
                if passed:
                    break
                if mode == 1:
                    if count >= (columns - (max(len(txt) for txt in text.splitlines()) + 1)):
                        mode = 2
                elif mode == 2:
                    if count <= 0:
                        mode = 1
                Anime._anime('\n'.join((' ' * count) + line for line in text.splitlines()), color or [], lambda a, b: b, interval)

                count += 1

        if hide_cursor:
            Cursor.ShowCursor()


    def Bar(length, carac_0: str = '[ ]', carac_1: str = '[0]', color: list = Colors.white, mode=Colorate.Horizontal, interval: int = 0.5, hide_cursor: bool = True, enter: bool = False, center: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(color) == list:
            while not length <= len(color):
                ncolor = list(color)
                for col in ncolor:
                    color.append(col)

        global passed
        passed = False

        if enter:
            th = _thread(target=Anime._input)
            th.start()

        for i in range(length + 1):
            bar = carac_1 * i + carac_0 * (length - i)
            if passed:
                break
            if type(color) == list:
                if center:
                    print(Center.XCenter(mode(color, bar)))
                else:
                    print(mode(color, bar))
            else:
                if center:
                    print(Center.XCenter(color + bar))
                else:
                    print(color + bar)
            _sleep(interval)
            System.Clear()
        if hide_cursor:
            Cursor.ShowCursor()

    def Anime() -> None: ...

    """ ! developper area ! """

    def _anime(text: str, color: list, mode, interval: int):
        _stdout.write(mode(color, text))
        _stdout.flush()
        _sleep(interval)
        System.Clear()

    def _input() -> str:
        global passed
        passed = input()
        return passed


class Write:
    """
    2 functions:
        Print()         |          print a text to the terminal while coloring it and with a fade and write effect
        Input()         |          same than Print() but adds an input to the end and returns its valor
    """

    def Print(text: str, color: list, interval=0.05, hide_cursor: bool = True, end: str = Colors.reset) -> None:
        if hide_cursor:
            Cursor.HideCursor()

        Write._write(text=text, color=color, interval=interval)

        _stdout.write(end)
        _stdout.flush()

        if hide_cursor:
            Cursor.ShowCursor()

    def Input(text: str, color: list, interval=0.05, hide_cursor: bool = True, input_color: str = Colors.reset, end: str = Colors.reset) -> str:
        if hide_cursor:
            Cursor.HideCursor()

        Write._write(text=text, color=color, interval=interval)

        valor = input(input_color)

        _stdout.write(end)
        _stdout.flush()

        if hide_cursor:
            Cursor.ShowCursor()

        return valor

    " ! developper area ! "

    def _write(text: str, color, interval: int):
        lines = list(text)
        if type(color) == list:
            while not len(lines) <= len(color):
                ncolor = list(color)
                for col in ncolor:
                    color.append(col)

        n = 0
        for line in lines:
            if type(color) == list:
                _stdout.write(_MakeColors._makeansi(color[n], line))
            else:
                _stdout.write(color + line)
            _stdout.flush()
            _sleep(interval)
            if line.strip():
                n += 1


class Center:

    """
    2 functions:
        XCenter()                  |             center the given text in X cords
        YCenter()                  |             center the given text in Y cords
        Center()                   |             center the given text in X and Y cords
        GroupAlign()               |             align the given text in a group
        TextAlign()                |             align the given text per lines

    NOTE: the functions of the class can be broken if the text argument has colors in it
    """

    center = 'CENTER'
    left = 'LEFT'
    right = 'RIGHT'

    def XCenter(text: str, spaces: int = None, icon: str = " "):
        if spaces is None:
            spaces = Center._xspaces(text=text)
        return "\n".join((icon * spaces) + text for text in text.splitlines())

    def YCenter(text: str, spaces: int = None, icon: str = "\n"):
        if spaces is None:
            spaces = Center._yspaces(text=text)

        return icon * spaces + "\n".join(text.splitlines())

    def Center(text: str, xspaces: int = None, yspaces: int = None, xicon: str = " ", yicon: str = "\n") -> str:
        if xspaces is None:
            xspaces = Center._xspaces(text=text)

        if yspaces is None:
            yspaces = Center._yspaces(text=text)

        text = yicon * yspaces + "\n".join(text.splitlines())
        return "\n".join((xicon * xspaces) + text for text in text.splitlines())

    def GroupAlign(text: str, align: str = center):
        align = align.upper()
        if align == Center.center:
            return Center.XCenter(text)
        elif align == Center.left:
            return text
        elif align == Center.right:
            length = _terminal_size().columns
            maxLineSize = max(len(line) for line in text.splitlines())
            return '\n'.join((' ' * (length - maxLineSize)) + line for line in text.splitlines())
        else:
            raise Center.BadAlignment()

    def TextAlign(text: str, align: str = center):
        align = align.upper()
        mlen = max(len(i) for i in text.splitlines())
        if align == Center.center:

            return "\n".join((' ' * int(mlen/2 - len(lin)/2)) + lin for lin in text.splitlines())
        elif align == Center.left:
            return text
        elif align == Center.right:
            ntext = '\n'.join(' ' * (mlen - len(lin)) + lin for lin in text.splitlines())
            return ntext
        else:
            raise Center.BadAlignment()


    """ ! developper area ! """

    def _xspaces(text: str):
        try:
            col = _terminal_size().columns
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = max((len(v) for v in textl if v.strip()), default = 0)
        return int((col - ntextl) / 2)

    def _yspaces(text: str):
        try:
            lin = _terminal_size().lines
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = len(textl)
        return int((lin - ntextl) / 2)

    class BadAlignment(Exception):
        def __init__(self):
            super().__init__("Choose a correct alignment: Center.center / Center.left / Center.right")

class Add:

    """
    1 function:
        Add()           |           allow you to add a text to another, and even center it
    """

    def Add(banner1, banner2, spaces=0, center=False):
        if center:
            split1 = len(banner1.splitlines())
            split2 = len(banner2.splitlines())
            if split1 > split2:
                spaces = (split1 - split2) // 2
            elif split2 > split1:
                spaces = (split2 - split1) // 2
            else:
                spaces = 0

        if spaces > max(len(banner1.splitlines()), len(banner2.splitlines())):
            # raise Banner.MaximumSpaces(spaces)
            spaces = max(len(banner1.splitlines()), len(banner2.splitlines()))

        ban1 = banner1.splitlines()
        ban2 = banner2.splitlines()

        ban1count = len(ban1)
        ban2count = len(ban2)

        size = Add._length(ban1)

        ban1 = Add._edit(ban1, size)

        ban1line = 0
        ban2line = 0
        text = ''

        for _ in range(spaces):

            if ban1count >= ban2count:
                ban1data = ban1[ban1line]
                ban2data = ''

                ban1line += 1

            else:
                ban1data = " " * size
                ban2data = ban2[ban2line]

                ban2line += 1

            text = text + ban1data + ban2data + '\n'
        while ban1line < ban1count or ban2line < ban2count:

            ban1data = ban1[ban1line] if ban1line < ban1count else " " * size
            ban2data = ban2[ban2line] if ban2line < ban2count else ""
            text = text + ban1data + ban2data + '\n'

            ban1line += 1
            ban2line += 1
        return text

    """ ! developper area ! """

    class MaximumSpaces(Exception):
        def __init__(self, spaces: str):
            super().__init__(f"Too much spaces [{spaces}].")

    def _length(ban1):
        bigestline = 0

        for line in ban1:
            if len(line) > bigestline:
                bigestline = len(line)
        return bigestline

    def _edit(ban1, size):
        return [line + (size - len(line)) * " " for line in ban1]


class Banner:

    """
    2 functions:
        SimpleCube()                  |             create a simple cube with the given text
        Lines()                       |             create a text framed by two lines
        Arrow()                       |             create a custom arrow
    """

    def Box(content: str, up_left: str, up_right: str, down_left: str, down_right: str, left_line: str, up_line: str, right_line: str, down_line: str) -> str:
        l = 0
        lines = content.splitlines()
        for a in lines:
            if len(a) > l:
                l = len(a)
        if l % 2 == 1:
            l += 1
        box = up_left + (up_line * l) + up_right + "\n"
        #box += "║ " + (" " * int(l / 2)) + (" " * int(l / 2)) + " ║\n"
        for line in lines:
            box += left_line + " " + line + (" " * int((l - len(line)))) + " " + right_line + "\n"
        box += down_left + (down_line * l) + down_right + "\n"
        return box


    def SimpleCube(content: str) -> str:
        l = 0
        lines = content.splitlines()
        for a in lines:
            if len(a) > l:
                l = len(a)
        if l % 2 == 1:
            l += 1
        box = "__" + ("_" * l) + "__\n"
        box += "| " + (" " * int(l / 2)) + (" " * int(l / 2)) + " |\n"
        for line in lines:
            box += "| " + line + (" " * int((l - len(line)))) + " |\n"
        box += "|_" + ("_" * l) + "_|\n"

        return box

    def DoubleCube(content: str) -> str:
        return Box.Box(content, "╔═", "═╗", "╚═", "═╝", "║", "═", "║", "═")

    def Lines(content: str, color = None, mode = Colorate.Horizontal, line = '═', pepite = 'ቐ') -> str:
        l = 1
        for c in content.splitlines():
            if len(c) > l:
                l = len(c)
        mode = Colorate.Horizontal if color is not None else (lambda **kw: kw['text'])
        box = mode(text = f"─{line*l}{pepite * 2}{line*l}─", color = color)
        assembly = box + "\n" + content + "\n" + box
        final = ''
        for lines in assembly.splitlines():
            final += Center.XCenter(lines) + "\n"
        return final

    def Arrow(icon: str = 'a', size: int = 2, number: int = 2, direction = 'right') -> str:
        spaces = ' ' * (size + 1)
        _arrow = ''
        structure = (size + 2, [size * 2, size * 2])
        count = 0
        if direction == 'right':
            for i in range(structure[1][0]):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count += 2

            for i in range(structure[1][0] + 1):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count -= 2
        elif direction == 'left':
            for i in range(structure[1][0]):
                count += 2

            for i in range(structure[1][0]):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count -= 2

            for i in range(structure[1][0] + 1):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count += 2
        return _arrow


Box = Banner

System.Init()































#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################


"""Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zawinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

The WHATWG URL Parser spec should also be considered.  We are not compliant with
it either due to existing user code API behavior expectations (Hyrum's Law).
It serves as a useful guide when making changes.
"""

from collections import namedtuple
import functools
import re
import sys
import types
import warnings
import ipaddress

__all__ = ["urlparse", "urlunparse", "urljoin", "urldefrag",
           "urlsplit", "urlunsplit", "urlencode", "parse_qs",
           "parse_qsl", "quote", "quote_plus", "quote_from_bytes",
           "unquote", "unquote_plus", "unquote_to_bytes",
           "DefragResult", "ParseResult", "SplitResult",
           "DefragResultBytes", "ParseResultBytes", "SplitResultBytes"]

# A classification of schemes.
# The empty string classifies URLs with no scheme specified,
# being the default value returned by “urlsplit” and “urlparse”.

uses_relative = ['', 'ftp', 'http', 'gopher', 'nntp', 'imap',
                 'wais', 'file', 'https', 'shttp', 'mms',
                 'prospero', 'rtsp', 'rtspu', 'sftp',
                 'svn', 'svn+ssh', 'ws', 'wss']

uses_netloc = ['', 'ftp', 'http', 'gopher', 'nntp', 'telnet',
               'imap', 'wais', 'file', 'mms', 'https', 'shttp',
               'snews', 'prospero', 'rtsp', 'rtspu', 'rsync',
               'svn', 'svn+ssh', 'sftp', 'nfs', 'git', 'git+ssh',
               'ws', 'wss']

uses_params = ['', 'ftp', 'hdl', 'prospero', 'http', 'imap',
               'https', 'shttp', 'rtsp', 'rtspu', 'sip', 'sips',
               'mms', 'sftp', 'tel']

# These are not actually used anymore, but should stay for backwards
# compatibility.  (They are undocumented, but have a public-looking name.)

non_hierarchical = ['gopher', 'hdl', 'mailto', 'news',
                    'telnet', 'wais', 'imap', 'snews', 'sip', 'sips']

uses_query = ['', 'http', 'wais', 'imap', 'https', 'shttp', 'mms',
              'gopher', 'rtsp', 'rtspu', 'sip', 'sips']

uses_fragment = ['', 'ftp', 'hdl', 'http', 'gopher', 'news',
                 'nntp', 'wais', 'https', 'shttp', 'snews',
                 'file', 'prospero']

# Characters valid in scheme names
scheme_chars = ('abcdefghijklmnopqrstuvwxyz'
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                '0123456789'
                '+-.')

# Leading and trailing C0 control and space to be stripped per WHATWG spec.
# == "".join([chr(i) for i in range(0, 0x20 + 1)])
_WHATWG_C0_CONTROL_OR_SPACE = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '

# Unsafe bytes to be removed per WHATWG spec
_UNSAFE_URL_BYTES_TO_REMOVE = ['\t', '\r', '\n']

def clear_cache():
    """Clear internal performance caches. Undocumented; some tests want it."""
    urlsplit.cache_clear()
    _byte_quoter_factory.cache_clear()

# Helpers for bytes handling
# For 3.2, we deliberately require applications that
# handle improperly quoted URLs to do their own
# decoding and encoding. If valid use cases are
# presented, we may relax this by using latin-1
# decoding internally for 3.3
_implicit_encoding = 'ascii'
_implicit_errors = 'strict'

def _noop(obj):
    return obj

def _encode_result(obj, encoding=_implicit_encoding,
                        errors=_implicit_errors):
    return obj.encode(encoding, errors)

def _decode_args(args, encoding=_implicit_encoding,
                       errors=_implicit_errors):
    return tuple(x.decode(encoding, errors) if x else '' for x in args)

def _coerce_args(*args):
    # Invokes decode if necessary to create str args
    # and returns the coerced inputs along with
    # an appropriate result coercion function
    #   - noop for str inputs
    #   - encoding function otherwise
    str_input = isinstance(args[0], str)
    for arg in args[1:]:
        # We special-case the empty string to support the
        # "scheme=''" default argument to some functions
        if arg and isinstance(arg, str) != str_input:
            raise TypeError("Cannot mix str and non-str arguments")
    if str_input:
        return args + (_noop,)
    return _decode_args(args) + (_encode_result,)

# Result objects are more helpful than simple tuples
class _ResultMixinStr(object):
    """Standard approach to encoding parsed results from str to bytes"""
    __slots__ = ()

    def encode(self, encoding='ascii', errors='strict'):
        return self._encoded_counterpart(*(x.encode(encoding, errors) for x in self))


class _ResultMixinBytes(object):
    """Standard approach to decoding parsed results from bytes to str"""
    __slots__ = ()

    def decode(self, encoding='ascii', errors='strict'):
        return self._decoded_counterpart(*(x.decode(encoding, errors) for x in self))


class _NetlocResultMixinBase(object):
    """Shared methods for the parsed result objects containing a netloc element"""
    __slots__ = ()

    @property
    def username(self):
        return self._userinfo[0]

    @property
    def password(self):
        return self._userinfo[1]

    @property
    def hostname(self):
        hostname = self._hostinfo[0]
        if not hostname:
            return None
        # Scoped IPv6 address may have zone info, which must not be lowercased
        # like http://[fe80::822a:a8ff:fe49:470c%tESt]:1234/keys
        separator = '%' if isinstance(hostname, str) else b'%'
        hostname, percent, zone = hostname.partition(separator)
        return hostname.lower() + percent + zone

    @property
    def port(self):
        port = self._hostinfo[1]
        if port is not None:
            if port.isdigit() and port.isascii():
                port = int(port)
            else:
                raise ValueError(f"Port could not be cast to integer value as {port!r}")
            if not (0 <= port <= 65535):
                raise ValueError("Port out of range 0-65535")
        return port

    __class_getitem__ = classmethod(types.GenericAlias)


class _NetlocResultMixinStr(_NetlocResultMixinBase, _ResultMixinStr):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition('@')
        if have_info:
            username, have_password, password = userinfo.partition(':')
            if not have_password:
                password = None
        else:
            username = password = None
        return username, password

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition('@')
        _, have_open_br, bracketed = hostinfo.partition('[')
        if have_open_br:
            hostname, _, port = bracketed.partition(']')
            _, _, port = port.partition(':')
        else:
            hostname, _, port = hostinfo.partition(':')
        if not port:
            port = None
        return hostname, port


class _NetlocResultMixinBytes(_NetlocResultMixinBase, _ResultMixinBytes):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition(b'@')
        if have_info:
            username, have_password, password = userinfo.partition(b':')
            if not have_password:
                password = None
        else:
            username = password = None
        return username, password

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition(b'@')
        _, have_open_br, bracketed = hostinfo.partition(b'[')
        if have_open_br:
            hostname, _, port = bracketed.partition(b']')
            _, _, port = port.partition(b':')
        else:
            hostname, _, port = hostinfo.partition(b':')
        if not port:
            port = None
        return hostname, port


_DefragResultBase = namedtuple('DefragResult', 'url fragment')
_SplitResultBase = namedtuple(
    'SplitResult', 'scheme netloc path query fragment')
_ParseResultBase = namedtuple(
    'ParseResult', 'scheme netloc path params query fragment')

_DefragResultBase.__doc__ = """
DefragResult(url, fragment)

A 2-tuple that contains the url without fragment identifier and the fragment
identifier as a separate argument.
"""

_DefragResultBase.url.__doc__ = """The URL with no fragment identifier."""

_DefragResultBase.fragment.__doc__ = """
Fragment identifier separated from URL, that allows indirect identification of a
secondary resource by reference to a primary resource and additional identifying
information.
"""

_SplitResultBase.__doc__ = """
SplitResult(scheme, netloc, path, query, fragment)

A 5-tuple that contains the different components of a URL. Similar to
ParseResult, but does not split params.
"""

_SplitResultBase.scheme.__doc__ = """Specifies URL scheme for the request."""

_SplitResultBase.netloc.__doc__ = """
Network location where the request is made to.
"""

_SplitResultBase.path.__doc__ = """
The hierarchical path, such as the path to a file to download.
"""

_SplitResultBase.query.__doc__ = """
The query component, that contains non-hierarchical data, that along with data
in path component, identifies a resource in the scope of URI's scheme and
network location.
"""

_SplitResultBase.fragment.__doc__ = """
Fragment identifier, that allows indirect identification of a secondary resource
by reference to a primary resource and additional identifying information.
"""

_ParseResultBase.__doc__ = """
ParseResult(scheme, netloc, path, params, query, fragment)

A 6-tuple that contains components of a parsed URL.
"""

_ParseResultBase.scheme.__doc__ = _SplitResultBase.scheme.__doc__
_ParseResultBase.netloc.__doc__ = _SplitResultBase.netloc.__doc__
_ParseResultBase.path.__doc__ = _SplitResultBase.path.__doc__
_ParseResultBase.params.__doc__ = """
Parameters for last path element used to dereference the URI in order to provide
access to perform some operation on the resource.
"""

_ParseResultBase.query.__doc__ = _SplitResultBase.query.__doc__
_ParseResultBase.fragment.__doc__ = _SplitResultBase.fragment.__doc__


# For backwards compatibility, alias _NetlocResultMixinStr
# ResultBase is no longer part of the documented API, but it is
# retained since deprecating it isn't worth the hassle
ResultBase = _NetlocResultMixinStr

# Structured result objects for string data
class DefragResult(_DefragResultBase, _ResultMixinStr):
    __slots__ = ()
    def geturl(self):
        if self.fragment:
            return self.url + '#' + self.fragment
        else:
            return self.url

class SplitResult(_SplitResultBase, _NetlocResultMixinStr):
    __slots__ = ()
    def geturl(self):
        return urlunsplit(self)

class ParseResult(_ParseResultBase, _NetlocResultMixinStr):
    __slots__ = ()
    def geturl(self):
        return urlunparse(self)

# Structured result objects for bytes data
class DefragResultBytes(_DefragResultBase, _ResultMixinBytes):
    __slots__ = ()
    def geturl(self):
        if self.fragment:
            return self.url + b'#' + self.fragment
        else:
            return self.url

class SplitResultBytes(_SplitResultBase, _NetlocResultMixinBytes):
    __slots__ = ()
    def geturl(self):
        return urlunsplit(self)

class ParseResultBytes(_ParseResultBase, _NetlocResultMixinBytes):
    __slots__ = ()
    def geturl(self):
        return urlunparse(self)

# Set up the encode/decode result pairs
def _fix_result_transcoding():
    _result_pairs = (
        (DefragResult, DefragResultBytes),
        (SplitResult, SplitResultBytes),
        (ParseResult, ParseResultBytes),
    )
    for _decoded, _encoded in _result_pairs:
        _decoded._encoded_counterpart = _encoded
        _encoded._decoded_counterpart = _decoded

_fix_result_transcoding()
del _fix_result_transcoding

def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    The result is a named 6-tuple with fields corresponding to the
    above. It is either a ParseResult or ParseResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result)

def _splitparams(url):
    if '/'  in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return url, ''
    else:
        i = url.find(';')
    return url[:i], url[i+1:]

def _splitnetloc(url, start=0):
    delim = len(url)   # position of end of domain part of url, default is end
    for c in '/?#':    # look for delimiters; the order is NOT important
        wdelim = url.find(c, start)        # find first of this delim
        if wdelim >= 0:                    # if found
            delim = min(delim, wdelim)     # use earliest delim position
    return url[start:delim], url[delim:]   # return (domain, rest)

def _checknetloc(netloc):
    if not netloc or netloc.isascii():
        return
    # looking for characters like \u2100 that expand to 'a/c'
    # IDNA uses NFKC equivalence, so normalize for this check
    import unicodedata
    n = netloc.replace('@', '')   # ignore characters already included
    n = n.replace(':', '')        # but not the surrounding text
    n = n.replace('#', '')
    n = n.replace('?', '')
    netloc2 = unicodedata.normalize('NFKC', n)
    if n == netloc2:
        return
    for c in '/?#@:':
        if c in netloc2:
            raise ValueError("netloc '" + netloc + "' contains invalid " +
                             "characters under NFKC normalization")

# Valid bracketed hosts are defined in
# https://www.rfc-editor.org/rfc/rfc3986#page-49 and https://url.spec.whatwg.org/
def _check_bracketed_host(hostname):
    if hostname.startswith('v'):
        if not re.match(r"\Av[a-fA-F0-9]+\..+\Z", hostname):
            raise ValueError(f"IPvFuture address is invalid")
    else:
        ip = ipaddress.ip_address(hostname) # Throws Value Error if not IPv6 or IPv4
        if isinstance(ip, ipaddress.IPv4Address):
            raise ValueError(f"An IPv4 address cannot be in brackets")

# typed=True avoids BytesWarnings being emitted during cache key
# comparison since this API supports both bytes and str input.
@functools.lru_cache(typed=True)
def urlsplit(url, scheme='', allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>

    The result is a named 5-tuple with fields corresponding to the
    above. It is either a SplitResult or SplitResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """

    url, scheme, _coerce_result = _coerce_args(url, scheme)
    # Only lstrip url as some applications rely on preserving trailing space.
    # (https://url.spec.whatwg.org/#concept-basic-url-parser would strip both)
    url = url.lstrip(_WHATWG_C0_CONTROL_OR_SPACE)
    scheme = scheme.strip(_WHATWG_C0_CONTROL_OR_SPACE)

    for b in _UNSAFE_URL_BYTES_TO_REMOVE:
        url = url.replace(b, "")
        scheme = scheme.replace(b, "")

    allow_fragments = bool(allow_fragments)
    netloc = query = fragment = ''
    i = url.find(':')
    if i > 0 and url[0].isascii() and url[0].isalpha():
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            scheme, url = url[:i].lower(), url[i+1:]
    if url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
        if (('[' in netloc and ']' not in netloc) or
                (']' in netloc and '[' not in netloc)):
            raise ValueError("Invalid IPv6 URL")
        if '[' in netloc and ']' in netloc:
            bracketed_host = netloc.partition('[')[2].partition(']')[0]
            _check_bracketed_host(bracketed_host)
    if allow_fragments and '#' in url:
        url, fragment = url.split('#', 1)
    if '?' in url:
        url, query = url.split('?', 1)
    _checknetloc(netloc)
    v = SplitResult(scheme, netloc, url, query, fragment)
    return _coerce_result(v)

def urlunparse(components):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment, _coerce_result = (
                                                  _coerce_args(*components))
    if params:
        url = "%s;%s" % (url, params)
    return _coerce_result(urlunsplit((scheme, netloc, url, query, fragment)))

def urlunsplit(components):
    """Combine the elements of a tuple as returned by urlsplit() into a
    complete URL as a string. The data argument can be any five-item iterable.
    This may result in a slightly different, but equivalent URL, if the URL that
    was parsed originally had unnecessary delimiters (for example, a ? with an
    empty query; the RFC states that these are equivalent)."""
    scheme, netloc, url, query, fragment, _coerce_result = (
                                          _coerce_args(*components))
    if netloc or (scheme and scheme in uses_netloc and url[:2] != '//'):
        if url and url[:1] != '/': url = '/' + url
        url = '//' + (netloc or '') + url
    if scheme:
        url = scheme + ':' + url
    if query:
        url = url + '?' + query
    if fragment:
        url = url + '#' + fragment
    return _coerce_result(url)

def urljoin(base, url, allow_fragments=True):
    """Join a base URL and a possibly relative URL to form an absolute
    interpretation of the latter."""
    if not base:
        return url
    if not url:
        return base

    base, url, _coerce_result = _coerce_args(base, url)
    bscheme, bnetloc, bpath, bparams, bquery, bfragment = \
            urlparse(base, '', allow_fragments)
    scheme, netloc, path, params, query, fragment = \
            urlparse(url, bscheme, allow_fragments)

    if scheme != bscheme or scheme not in uses_relative:
        return _coerce_result(url)
    if scheme in uses_netloc:
        if netloc:
            return _coerce_result(urlunparse((scheme, netloc, path,
                                              params, query, fragment)))
        netloc = bnetloc

    if not path and not params:
        path = bpath
        params = bparams
        if not query:
            query = bquery
        return _coerce_result(urlunparse((scheme, netloc, path,
                                          params, query, fragment)))

    base_parts = bpath.split('/')
    if base_parts[-1] != '':
        # the last item is not a directory, so will not be taken into account
        # in resolving the relative path
        del base_parts[-1]

    # for rfc3986, ignore all base path should the first character be root.
    if path[:1] == '/':
        segments = path.split('/')
    else:
        segments = base_parts + path.split('/')
        # filter out elements that would cause redundant slashes on re-joining
        # the resolved_path
        segments[1:-1] = filter(None, segments[1:-1])

    resolved_path = []

    for seg in segments:
        if seg == '..':
            try:
                resolved_path.pop()
            except IndexError:
                # ignore any .. segments that would otherwise cause an IndexError
                # when popped from resolved_path if resolving for rfc3986
                pass
        elif seg == '.':
            continue
        else:
            resolved_path.append(seg)

    if segments[-1] in ('.', '..'):
        # do some post-processing here. if the last segment was a relative dir,
        # then we need to append the trailing '/'
        resolved_path.append('')

    return _coerce_result(urlunparse((scheme, netloc, '/'.join(
        resolved_path) or '/', params, query, fragment)))


def urldefrag(url):
    """Removes any existing fragment from URL.

    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    url, _coerce_result = _coerce_args(url)
    if '#' in url:
        s, n, p, a, q, frag = urlparse(url)
        defrag = urlunparse((s, n, p, a, q, ''))
    else:
        frag = ''
        defrag = url
    return _coerce_result(DefragResult(defrag, frag))

_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None

def unquote_to_bytes(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""
    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        # Is it a string-like object?
        string.split
        return b''
    if isinstance(string, str):
        string = string.encode('utf-8')
    bits = string.split(b'%')
    if len(bits) == 1:
        return string
    res = [bits[0]]
    append = res.append
    # Delay the initialization of the table to not waste memory
    # if the function is never called
    global _hextobyte
    if _hextobyte is None:
        _hextobyte = {(a + b).encode(): bytes.fromhex(a + b)
                      for a in _hexdig for b in _hexdig}
    for item in bits[1:]:
        try:
            append(_hextobyte[item[:2]])
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)
    return b''.join(res)

_asciire = re.compile('([\x00-\x7f]+)')

def unquote(string, encoding='utf-8', errors='replace'):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if isinstance(string, bytes):
        return unquote_to_bytes(string).decode(encoding, errors)
    if '%' not in string:
        string.split
        return string
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'replace'
    bits = _asciire.split(string)
    res = [bits[0]]
    append = res.append
    for i in range(1, len(bits), 2):
        append(unquote_to_bytes(bits[i]).decode(encoding, errors))
        append(bits[i + 1])
    return ''.join(res)


def parse_qs(qs, keep_blank_values=False, strict_parsing=False,
             encoding='utf-8', errors='replace', max_num_fields=None, separator='&'):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError if there
            are more than n fields read by parse_qsl().

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.

        Returns a dictionary.
    """
    parsed_result = {}
    pairs = parse_qsl(qs, keep_blank_values, strict_parsing,
                      encoding=encoding, errors=errors,
                      max_num_fields=max_num_fields, separator=separator)
    for name, value in pairs:
        if name in parsed_result:
            parsed_result[name].append(value)
        else:
            parsed_result[name] = [value]
    return parsed_result


def parse_qsl(qs, keep_blank_values=False, strict_parsing=False,
              encoding='utf-8', errors='replace', max_num_fields=None, separator='&'):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as blank
            strings.  The default false value indicates that blank values
            are to be ignored and treated as if they were  not included.

        strict_parsing: flag indicating what to do with parsing errors. If
            false (the default), errors are silently ignored. If true,
            errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError
            if there are more than n fields read by parse_qsl().

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.

        Returns a list, as G-d intended.
    """
    qs, _coerce_result = _coerce_args(qs)
    separator, _ = _coerce_args(separator)

    if not separator or (not isinstance(separator, (str, bytes))):
        raise ValueError("Separator must be of type string or bytes.")

    # If max_num_fields is defined then check that the number of fields
    # is less than max_num_fields. This prevents a memory exhaustion DOS
    # attack via post bodies with many fields.
    if max_num_fields is not None:
        num_fields = 1 + qs.count(separator) if qs else 0
        if max_num_fields < num_fields:
            raise ValueError('Max number of fields exceeded')

    r = []
    query_args = qs.split(separator) if qs else []
    for name_value in query_args:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError("bad query field: %r" % (name_value,))
            # Handle case of a control-name with no equal sign
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = nv[0].replace('+', ' ')
            name = unquote(name, encoding=encoding, errors=errors)
            name = _coerce_result(name)
            value = nv[1].replace('+', ' ')
            value = unquote(value, encoding=encoding, errors=errors)
            value = _coerce_result(value)
            r.append((name, value))
    return r

def unquote_plus(string, encoding='utf-8', errors='replace'):
    """Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.

    unquote_plus('%7e/abc+def') -> '~/abc def'
    """
    string = string.replace('+', ' ')
    return unquote(string, encoding, errors)

_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)

def __getattr__(name):
    if name == 'Quoter':
        warnings.warn('Deprecated in 3.11. '
                      'urllib.parse.Quoter will be removed in Python 3.14. '
                      'It was not intended to be a public API.',
                      DeprecationWarning, stacklevel=2)
        return _Quoter
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')

class _Quoter(dict):
    """A mapping from bytes numbers (in range(0,256)) to strings.

    String values are percent-encoded byte values, unless the key < 128, and
    in either of the specified safe set, or the always safe set.
    """
    # Keeps a cache internally, via __missing__, for efficiency (lookups
    # of cached keys don't call Python code at all).
    def __init__(self, safe):
        """safe: bytes object."""
        self.safe = _ALWAYS_SAFE.union(safe)

    def __repr__(self):
        return f"<Quoter {dict(self)!r}>"

    def __missing__(self, b):
        # Handle a cache miss. Store quoted string in cache and return.
        res = chr(b) if b in self.safe else '%{:02X}'.format(b)
        self[b] = res
        return res

def quote(string, safe='/', encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted. The
    quote function offers a cautious (not minimal) way to quote a
    string for most of these parts.

    RFC 3986 Uniform Resource Identifier (URI): Generic Syntax lists
    the following (un)reserved characters.

    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
    reserved      = gen-delims / sub-delims
    gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                  / "*" / "+" / "," / ";" / "="

    Each of the reserved characters is reserved in some component of a URL,
    but not necessarily in all of them.

    The quote function %-escapes all characters that are neither in the
    unreserved chars ("always safe") nor the additional chars set via the
    safe arg.

    The default for the safe arg is '/'. The character is reserved, but in
    typical usage the quote function is being called on a path where the
    existing slash characters are to be preserved.

    Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
    Now, "~" is included in the set of unreserved characters.

    string and safe may be either str or bytes objects. encoding and errors
    must not be specified if string is a bytes object.

    The optional encoding and errors parameters specify how to deal with
    non-ASCII characters, as accepted by the str.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)

def quote_plus(string, safe='', encoding=None, errors=None):
    """Like quote(), but also replace ' ' with '+', as required for quoting
    HTML form values. Plus signs in the original string are escaped unless
    they are included in safe. It also does not have safe default to '/'.
    """
    # Check if ' ' in string, where string may either be a str or bytes.  If
    # there are no spaces, the regular quote will produce the right answer.
    if ((isinstance(string, str) and ' ' not in string) or
        (isinstance(string, bytes) and b' ' not in string)):
        return quote(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '
    string = quote(string, safe + space, encoding, errors)
    return string.replace(' ', '+')

# Expectation: A typical program is unlikely to create more than 5 of these.
@functools.lru_cache
def _byte_quoter_factory(safe):
    return _Quoter(safe).__getitem__

def quote_from_bytes(bs, safe='/'):
    """Like quote(), but accepts a bytes object rather than a str, and does
    not perform string-to-bytes encoding.  It always returns an ASCII string.
    quote_from_bytes(b'abc def\x3f') -> 'abc%20def%3f'
    """
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError("quote_from_bytes() expected bytes")
    if not bs:
        return ''
    if isinstance(safe, str):
        # Normalize 'safe' by converting to bytes and removing non-ASCII chars
        safe = safe.encode('ascii', 'ignore')
    else:
        # List comprehensions are faster than generator expressions.
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    quoter = _byte_quoter_factory(safe)
    return ''.join([quoter(char) for char in bs])

def urlencode(query, doseq=False, safe='', encoding=None, errors=None,
              quote_via=quote_plus):
    """Encode a dict or sequence of two-element tuples into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.

    The components of a query arg may each be either a string or a bytes type.

    The safe, encoding, and errors parameters are passed down to the function
    specified by quote_via (encoding and errors only if a component is a str).
    """

    if hasattr(query, "items"):
        query = query.items()
    else:
        # It's a bother at times that strings and string-like objects are
        # sequences.
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
            # Zero-length sequences of all types will get here and succeed,
            # but that's a minor nit.  Since the original implementation
            # allowed empty dicts that type of behavior probably should be
            # preserved for consistency
        except TypeError as err:
            raise TypeError("not a valid non-string sequence "
                            "or mapping object") from err

    l = []
    if not doseq:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_via(v, safe)
            else:
                v = quote_via(str(v), safe, encoding, errors)
            l.append(k + '=' + v)
    else:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_via(v, safe)
                l.append(k + '=' + v)
            elif isinstance(v, str):
                v = quote_via(v, safe, encoding, errors)
                l.append(k + '=' + v)
            else:
                try:
                    # Is this a sufficient test for sequence-ness?
                    x = len(v)
                except TypeError:
                    # not a sequence
                    v = quote_via(str(v), safe, encoding, errors)
                    l.append(k + '=' + v)
                else:
                    # loop over the sequence
                    for elt in v:
                        if isinstance(elt, bytes):
                            elt = quote_via(elt, safe)
                        else:
                            elt = quote_via(str(elt), safe, encoding, errors)
                        l.append(k + '=' + elt)
    return '&'.join(l)


def to_bytes(url):
    warnings.warn("urllib.parse.to_bytes() is deprecated as of 3.8",
                  DeprecationWarning, stacklevel=2)
    return _to_bytes(url)


def _to_bytes(url):
    """to_bytes(u"URL") --> 'URL'."""
    # Most URL schemes require ASCII. If that changes, the conversion
    # can be relaxed.
    # XXX get rid of to_bytes()
    if isinstance(url, str):
        try:
            url = url.encode("ASCII").decode()
        except UnicodeError:
            raise UnicodeError("URL " + repr(url) +
                               " contains non-ASCII characters")
    return url


def unwrap(url):
    """Transform a string like '<URL:scheme://host/path>' into 'scheme://host/path'.

    The string is returned unchanged if it's not a wrapped URL.
    """
    url = str(url).strip()
    if url[:1] == '<' and url[-1:] == '>':
        url = url[1:-1].strip()
    if url[:4] == 'URL:':
        url = url[4:].strip()
    return url


def splittype(url):
    warnings.warn("urllib.parse.splittype() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splittype(url)


_typeprog = None
def _splittype(url):
    """splittype('type:opaquestring') --> 'type', 'opaquestring'."""
    global _typeprog
    if _typeprog is None:
        _typeprog = re.compile('([^/:]+):(.*)', re.DOTALL)

    match = _typeprog.match(url)
    if match:
        scheme, data = match.groups()
        return scheme.lower(), data
    return None, url


def splithost(url):
    warnings.warn("urllib.parse.splithost() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splithost(url)


_hostprog = None
def _splithost(url):
    """splithost('//host[:port]/path') --> 'host[:port]', '/path'."""
    global _hostprog
    if _hostprog is None:
        _hostprog = re.compile('//([^/#?]*)(.*)', re.DOTALL)

    match = _hostprog.match(url)
    if match:
        host_port, path = match.groups()
        if path and path[0] != '/':
            path = '/' + path
        return host_port, path
    return None, url


def splituser(host):
    warnings.warn("urllib.parse.splituser() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splituser(host)


def _splituser(host):
    """splituser('user[:passwd]@host[:port]') --> 'user[:passwd]', 'host[:port]'."""
    user, delim, host = host.rpartition('@')
    return (user if delim else None), host


def splitpasswd(user):
    warnings.warn("urllib.parse.splitpasswd() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitpasswd(user)


def _splitpasswd(user):
    """splitpasswd('user:passwd') -> 'user', 'passwd'."""
    user, delim, passwd = user.partition(':')
    return user, (passwd if delim else None)


def splitport(host):
    warnings.warn("urllib.parse.splitport() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitport(host)


# splittag('/path#tag') --> '/path', 'tag'
_portprog = None
def _splitport(host):
    """splitport('host:port') --> 'host', 'port'."""
    global _portprog
    if _portprog is None:
        _portprog = re.compile('(.*):([0-9]*)', re.DOTALL)

    match = _portprog.fullmatch(host)
    if match:
        host, port = match.groups()
        if port:
            return host, port
    return host, None


def splitnport(host, defport=-1):
    warnings.warn("urllib.parse.splitnport() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitnport(host, defport)


def _splitnport(host, defport=-1):
    """Split host and port, returning numeric port.
    Return given default port if no ':' found; defaults to -1.
    Return numerical port if a valid number is found after ':'.
    Return None if ':' but not a valid number."""
    host, delim, port = host.rpartition(':')
    if not delim:
        host = port
    elif port:
        if port.isdigit() and port.isascii():
            nport = int(port)
        else:
            nport = None
        return host, nport
    return host, defport


def splitquery(url):
    warnings.warn("urllib.parse.splitquery() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitquery(url)


def _splitquery(url):
    """splitquery('/path?query') --> '/path', 'query'."""
    path, delim, query = url.rpartition('?')
    if delim:
        return path, query
    return url, None


def splittag(url):
    warnings.warn("urllib.parse.splittag() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splittag(url)


def _splittag(url):
    """splittag('/path#tag') --> '/path', 'tag'."""
    path, delim, tag = url.rpartition('#')
    if delim:
        return path, tag
    return url, None


def splitattr(url):
    warnings.warn("urllib.parse.splitattr() is deprecated as of 3.8, "
                  "use urllib.parse.urlparse() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitattr(url)


def _splitattr(url):
    """splitattr('/path;attr1=value1;attr2=value2;...') ->
        '/path', ['attr1=value1', 'attr2=value2', ...]."""
    words = url.split(';')
    return words[0], words[1:]


def splitvalue(attr):
    warnings.warn("urllib.parse.splitvalue() is deprecated as of 3.8, "
                  "use urllib.parse.parse_qsl() instead",
                  DeprecationWarning, stacklevel=2)
    return _splitvalue(attr)


def _splitvalue(attr):
    """splitvalue('attr=value') --> 'attr', 'value'."""
    attr, delim, value = attr.partition('=')
    return attr, (value if delim else None)









#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################


import os
import time
import zipfile
import requests
# import pystyle
# from tqdm import tqdm
# from pystyle import Box
# from pystyle import Center
# from pystyle import Colorate
# from pystyle import Write, Colors
# from urllib.parse import urlparse






logo = """
 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
 ▓▓                                                                   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒ DEV ▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒█████████████▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒  Unkn0wn2603   ▒▒▒▒▒▒▒▒███▒▒▒███▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒███▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒ Git Downloader ▒▒▒▒▒▒▒▒███▒▒▒███▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒       FOR      ▒▒▒▒▒▒▒▒███▒▒▒███▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒  Personal Use  ▒▒▒▒▒▒▒▒███▒▒▒███▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    Main  Version   ▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▓▓
 ▓▓                                                                   ▓▓
 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
╭──────────────────────────────────────────────────────────────────────╮
│     THIS TOOL ONLY FOR MAKING MY WORKS EASY,NO NEED INSTRUCTION      │
╰──────────────────────────────────────────────────────────────────────╯
"""

def make_in_center(texts):
    xc = Center.XCenter(texts); return xc
def make_in_box(texts):
    xc = Box.DoubleCube(texts); return xc
def make_in_2line(texts):
    xc = Box.Lines(texts); return xc

def take_color_input(texts, interval=0.025):
    texts = f"\n{texts}"
    """
    >>> #==========================================================================
    >>> # |                                 defults                               |
    >>> # |         black_to_white          ---         green_to_white            |
    >>> # |         black_to_red            ---         green_to_yellow           |
    >>> # |         black_to_green          ---         green_to_cyan             |
    >>> # |         black_to_blue           ---         blue_to_black             |
    >>> # |         white_to_black          ---         blue_to_white             |
    >>> # |         white_to_red            ---         blue_to_cyan              |
    >>> # |         white_to_green          ---         blue_to_purple            |
    >>> # |         white_to_blue           ---         yellow_to_red             |
    >>> # |         red_to_black            ---         yellow_to_green           |
    >>> # |         red_to_white            ---         purple_to_red             |
    >>> # |         red_to_yellow           ---         purple_to_blue            |
    >>> # |         red_to_purple           ---         cyan_to_green             |
    >>> # |         green_to_black          ---         cyan_to_blue              |
    >>> # |         red_to_blue             ---         red_to_green              |
    >>> # |         green_to_blue           ---         green_to_red              |
    >>> # |         blue_to_red             ---         blue_to_green             |
    >>> # |         rainbow                 ---                                   |

    """
    inputs = Write.Input(texts, Colors.red_to_purple, interval=interval); return inputs





def print_slowly_txt(texts, interval=0.025, texttype="i"):
    texts = f"\n{texts}"
    """
    >>> #==========================================================================
    >>> # |                                 defults                               |
    >>> # |         black_to_white          ---         green_to_white            |
    >>> # |         black_to_red            ---         green_to_yellow           |
    >>> # |         black_to_green          ---         green_to_cyan             |
    >>> # |         black_to_blue           ---         blue_to_black             |
    >>> # |         white_to_black          ---         blue_to_white             |
    >>> # |         white_to_red            ---         blue_to_cyan              |
    >>> # |         white_to_green          ---         blue_to_purple            |
    >>> # |         white_to_blue           ---         yellow_to_red             |
    >>> # |         red_to_black            ---         yellow_to_green           |
    >>> # |         red_to_white            ---         purple_to_red             |
    >>> # |         red_to_yellow           ---         purple_to_blue            |
    >>> # |         red_to_purple           ---         cyan_to_green             |
    >>> # |         green_to_black          ---         cyan_to_blue              |
    >>> # |         red_to_blue             ---         red_to_green              |
    >>> # |         green_to_blue           ---         green_to_red              |
    >>> # |         blue_to_red             ---         blue_to_green             |
    >>> # |         rainbow                 ---                                   |
    """
    if texttype=="i":
        Write.Print(texts, Colors.cyan_to_blue, interval=interval); return True
    elif texttype=="e":
        Write.Print(texts, Colors.red_to_purple, interval=interval); return True
    elif texttype=="s":
        Write.Print(texts, Colors.green_to_blue, interval=interval); return True
    elif texttype=="p":
        Write.Print(texts, Colors.blue_to_green, interval=interval); return True
    elif texttype=="u":
        Write.Print(texts, Colors.purple_to_red, interval=interval); return True
    elif texttype=="c":
        Write.Print(texts, Colors.yellow_to_red, interval=interval); return True
    return False











# import pystyle
# from pystyle import Colors
# from pystyle import Colorate


def rainbow_print(inputs, limtf = True):
    inputs = inputs.split("\n")
    for  banner in inputs:
        line = Colorate.Horizontal(Colors.rainbow, banner)
        if limtf: line = make_in_center(line)
        print(line)
def banner():
    rainbow_print(logo)


def transform_github_url(url):
    # Parse the GitHub URL
    parsed_url = urlparse(url)
    # Extract the username and repository name
    parts = parsed_url.path.split('/')
    username = parts[1]
    repo_name = parts[2]
    # Build the transformed URL
    transformed_url = f'https://github.com/{username}/{repo_name}/archive/refs/heads/master.zip'
    return transformed_url, username, repo_name


def download_from_github(url, output_file):
    # Download the ZIP file
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content to a file
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print_slowly_txt(texts=f'[i] Download successful. File saved as: {output_file}', interval=0.01)
    else:
        print_slowly_txt(texts=f'[e] Failed to download. Status code: {response.status_code}', interval=0.01)

import zipfile
import os

def extract_zip(zip_file, extract_to=None):
    """
    Extracts a ZIP file.

    Parameters:
        - zip_file (str): The path to the ZIP file to be extracted.
        - extract_to (str, optional): The directory to extract the contents to.
          If not provided, it will extract to the current working directory.

    Returns:
        - extracted_to (str): The path where the ZIP file was extracted to.
    """
    if not extract_to:
        extract_to = os.getcwd()

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    extracted_to = os.path.join(extract_to, os.path.splitext(os.path.basename(zip_file))[0])
    return extracted_to




def downloader():
    try:
        banner()
        running=True
        url_done=False
        while running:
            gonext = take_color_input(texts="\n\n[?] Want to Download any Git Repo (y/n): ", interval=0.01) # 'https://github.com/galihap76/collector'
            if gonext == "y" or gonext == "Y":
                running=True
            elif "github.com" in gonext:
                github_url = gonext
                url_done = True
            else:
                running=False
                print_slowly_txt(texts="[x] Oh ok, bye bye", texttype="u")
                return True
            if not url_done: github_url = take_color_input(texts="[?] Enter Git URL : ", interval=0.01) # 'https://github.com/galihap76/collector'
            transformed_url, username, repo_name = transform_github_url(github_url)
            output_file_name = f'{username}__{repo_name}.zip'

            print_slowly_txt(texts=f"[i] Oh... you want to download the {repo_name} reposerory", texttype="i")
            print_slowly_txt(texts=f"[i] Which is {username}'s personal repo", texttype="i")
            print_slowly_txt(texts=f"[!] Making links...", texttype="u")
            time.sleep(1)
            print_slowly_txt(texts=f"[i] Created Link is : {transformed_url}", texttype="s")
            print_slowly_txt(texts=f"[!] Trying to Download...", texttype="u")
            download_from_github(transformed_url, output_file_name)

            extrackfile = take_color_input(texts="[?] Want to extrack the file of Git Repo (n for cancel): ", interval=0.01)
            if extrackfile =="n" or extrackfile == "N":
                print_slowly_txt(texts="[~] Done...", texttype="u")
                return True
            # Example usage:
            extracted_folder = extract_zip(output_file_name)
            print_slowly_txt(f"[i] Extracted to : {extracted_folder}")


    except KeyboardInterrupt:
        print_slowly_txt(texts="[x] ok ok. im sleeping... Zzz", texttype="e")
        return True
    except Exception as e:
        print_slowly_txt(texts=f"[x] {e}", texttype="e")
        return False

downloader()
