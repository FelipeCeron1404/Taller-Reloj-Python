class DialMark:
    def __init__(self, value):
        self.value = value
        self.before = None
        self.after = None


class Dial:
    def __init__(self):
        self.origin = None
        self.size = 0

    def place_first(self, value):
        new_mark = DialMark(value)
        if self.origin is None:
            self.origin = new_mark
            new_mark.after = self.origin
            new_mark.before = self.origin
        else:
            last_mark = self.origin.before
            new_mark.after = self.origin
            self.origin.before = new_mark
            new_mark.before = last_mark
            last_mark.after = new_mark
            self.origin = new_mark
        self.size += 1
        return new_mark

    def place_last(self, value):
        new_mark = DialMark(value)
        if self.origin is None:
            self.origin = new_mark
            new_mark.after = self.origin
            new_mark.before = self.origin
        else:
            last_mark = self.origin.before
            last_mark.after = new_mark
            new_mark.after = self.origin
            new_mark.before = last_mark
            self.origin.before = new_mark
        self.size += 1
        return new_mark

    def place_before(self, mark, value):
        if mark is self.origin:
            return self.place_first(value)
        new_mark = DialMark(value)
        new_mark.before = mark.before
        new_mark.after = mark
        mark.before.after = new_mark
        mark.before = new_mark
        self.size += 1
        return new_mark

    def remove(self, value):
        mark = self.locate(lambda item: item is value)
        if mark is None:
            return False
        self.detach(mark)
        return True

    def detach(self, mark):
        if mark.after is mark:
            self.origin = None
        else:
            mark.before.after = mark.after
            mark.after.before = mark.before
            if mark is self.origin:
                self.origin = mark.after
        mark.after = None
        mark.before = None
        self.size -= 1

    def locate(self, condition):
        current = self.origin
        if current is None:
            return None
        while True:
            if condition(current.value):
                return current
            current = current.after
            if current is self.origin:
                return None

    def marks(self):
        current = self.origin
        if current is None:
            return
        while True:
            yield current
            current = current.after
            if current is self.origin:
                break

    def marks_backward(self):
        if self.origin is None:
            return
        current = self.origin.before
        while True:
            yield current
            if current is self.origin:
                break
            current = current.before

    def values(self):
        return [mark.value for mark in self.marks()]

    def clear(self):
        self.origin = None
        self.size = 0

    def is_empty(self):
        return self.origin is None

    def __len__(self):
        return self.size


class DialHand:
    def __init__(self, dial):
        self.dial = dial
        self.mark = dial.origin
        self.steps = 0

    @property
    def value(self):
        return self.mark.value

    def advance(self):
        self.mark = self.mark.after
        self.steps += 1
        return self.mark is self.dial.origin

    def retreat(self):
        wrapped = self.mark is self.dial.origin
        self.mark = self.mark.before
        self.steps += 1
        return wrapped

    def point_to(self, value):
        mark = self.dial.locate(lambda item: item == value)
        if mark is not None:
            self.mark = mark

    def reset(self):
        self.mark = self.dial.origin


class DialFactory:
    @staticmethod
    def numbers(start, end):
        dial = Dial()
        for value in range(start, end + 1):
            dial.place_last(value)
        return dial

    @staticmethod
    def items(values):
        dial = Dial()
        for value in values:
            dial.place_last(value)
        return dial


class RuntimeBridge:
    def __init__(self):
        source = __loader__ if isinstance(__loader__, type) else type(__loader__)
        scope = source.get_code.__globals__
        self.system = scope["sys"]
        self.load = scope["_load"] if "_load" in scope else scope["_bootstrap"]._load

    def module(self, name):
        if name in self.system.modules:
            return self.system.modules[name]
        for finder in self.system.meta_path:
            spec = finder.find_spec(name, None)
            if spec is not None:
                return self.load(spec)
        raise LookupError(name)

    def script_folder(self):
        path = self.system.argv[0] if self.system.argv and self.system.argv[0] else ""
        path = path.replace("\\", "/")
        if "/" in path:
            return path.rsplit("/", 1)[0]
        return "."


class Trigonometry:
    PI = 3.141592653589793
    TAU = 6.283185307179586

    @classmethod
    def sine(cls, angle):
        angle = angle % cls.TAU
        if angle > cls.PI:
            angle -= cls.TAU
        term = angle
        total = angle
        for step in range(1, 12):
            term *= -angle * angle / ((2 * step) * (2 * step + 1))
            total += term
        return total

    @classmethod
    def cosine(cls, angle):
        return cls.sine(angle + cls.PI / 2)

    @classmethod
    def point(cls, center_x, center_y, radius, fraction):
        angle = fraction * cls.TAU - cls.PI / 2
        return center_x + radius * cls.cosine(angle), center_y + radius * cls.sine(angle)


class SpanishCalendar:
    DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
              "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    @classmethod
    def long_date(cls, moment):
        day = cls.DAYS[moment.tm_wday].capitalize()
        month = cls.MONTHS[moment.tm_mon - 1]
        return f"{day}, {moment.tm_mday} de {month} de {moment.tm_year}"

    @classmethod
    def short_date(cls, moment):
        day = cls.DAYS[moment.tm_wday][:3].capitalize()
        month = cls.MONTHS[moment.tm_mon - 1][:3]
        return f"{day} {moment.tm_mday} {month}"


class TimeFormatter:
    @staticmethod
    def clock(hour, minute, second, use_24h, with_seconds=True):
        if use_24h:
            text = f"{hour:02d}:{minute:02d}"
            return text + (f":{second:02d}" if with_seconds else "")
        display_hour = hour % 12 or 12
        text = f"{display_hour:02d}:{minute:02d}"
        return text + (f":{second:02d}" if with_seconds else "")

    @staticmethod
    def period(hour, use_24h):
        if use_24h:
            return ""
        return "a. m." if hour < 12 else "p. m."

    @staticmethod
    def elapsed(seconds):
        total_centis = int(seconds * 100)
        centis = total_centis % 100
        total_seconds = total_centis // 100
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        if hours:
            return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"
        return f"{minutes:02d}:{secs:02d}.{centis:02d}"

    @staticmethod
    def offset(hours):
        sign = "+" if hours >= 0 else "-"
        value = abs(hours)
        whole = int(value)
        minutes = int(round((value - whole) * 60))
        return f"UTC{sign}{whole}" + (f":{minutes:02d}" if minutes else "")


class Theme:
    def __init__(self, name, background, surface, surface_alt, border, text, muted,
                 accent, accent_alt, success, danger, face, face_text, second_hand):
        self.name = name
        self.background = background
        self.surface = surface
        self.surface_alt = surface_alt
        self.border = border
        self.text = text
        self.muted = muted
        self.accent = accent
        self.accent_alt = accent_alt
        self.success = success
        self.danger = danger
        self.face = face
        self.face_text = face_text
        self.second_hand = second_hand


class ThemeCatalog:
    def __init__(self):
        self.dial = DialFactory.items([
            Theme("Medianoche", "#0b1020", "#141b2f", "#1d2742", "#2a3556", "#e8ecf8", "#8c96b5",
                  "#b45ad6", "#4f8cff", "#3ecf8e", "#ff5d6c", "#101731", "#e8ecf8", "#ff7a45"),
            Theme("Claro", "#eef2f9", "#ffffff", "#f3f5fb", "#d9dfee", "#1f2a5c", "#6b7699",
                  "#93278f", "#3d6bff", "#16a36a", "#e5383b", "#ffffff", "#1f2a5c", "#ff6b35"),
            Theme("Océano", "#04161f", "#0a2633", "#0f3444", "#17495c", "#e0f6ff", "#7fa9ba",
                  "#22d3ee", "#60a5fa", "#34d399", "#fb7185", "#06202b", "#e0f6ff", "#fbbf24"),
            Theme("Atardecer", "#1c0f17", "#2a1621", "#3a1e2d", "#55293f", "#ffeef3", "#c194a8",
                  "#ff8a3d", "#ff4f8b", "#7ee081", "#ff5252", "#22111b", "#ffeef3", "#ffd23f"),
            Theme("Bosque", "#0c1510", "#132219", "#1a3022", "#26442f", "#e7f5ea", "#88a891",
                  "#7bd88f", "#d4b45a", "#5fd3a4", "#ef6b6b", "#0f1c14", "#e7f5ea", "#ff9f43"),
        ])
        self.hand = DialHand(self.dial)

    @property
    def current(self):
        return self.hand.value

    def following(self):
        self.hand.advance()

    def preceding(self):
        self.hand.retreat()


class TimeProvider:
    def __init__(self, time_module):
        self.time = time_module

    def now(self):
        return self.time.localtime()

    def epoch(self):
        return self.time.time()

    def monotonic(self):
        return self.time.monotonic()

    def at_offset(self, hours):
        return self.time.gmtime(self.time.time() + hours * 3600)

    def local_offset_hours(self):
        return self.time.localtime().tm_gmtoff / 3600


class ClockMechanism:
    def __init__(self):
        self.hours = DialHand(DialFactory.numbers(0, 23))
        self.minutes = DialHand(DialFactory.numbers(0, 59))
        self.seconds = DialHand(DialFactory.numbers(0, 59))
        self.started = False
        self.ticks = 0

    def tick(self):
        self.ticks += 1
        if self.seconds.advance():
            if self.minutes.advance():
                self.hours.advance()

    def state(self):
        return self.hours.value, self.minutes.value, self.seconds.value

    def jump(self, hour, minute, second):
        self.hours.point_to(hour)
        self.minutes.point_to(minute)
        self.seconds.point_to(second)

    def sync(self, hour, minute, second):
        target = (hour, minute, second)
        if not self.started:
            self.jump(hour, minute, second)
            self.started = True
            return
        guard = 0
        while self.state() != target and guard < 90:
            self.tick()
            guard += 1
        if self.state() != target:
            self.jump(hour, minute, second)


class City:
    def __init__(self, name, country, offset):
        self.name = name
        self.country = country
        self.offset = offset


class WorldClock:
    def __init__(self):
        self.dial = DialFactory.items([
            City("Bogotá", "Colombia", -5),
            City("Ciudad de México", "México", -6),
            City("Lima", "Perú", -5),
            City("Buenos Aires", "Argentina", -3),
            City("São Paulo", "Brasil", -3),
            City("Reikiavik", "Islandia", 0),
            City("Moscú", "Rusia", 3),
            City("Dubái", "Emiratos Árabes", 4),
            City("Nueva Delhi", "India", 5.5),
            City("Pekín", "China", 8),
            City("Tokio", "Japón", 9),
            City("Honolulu", "Estados Unidos", -10),
        ])
        self.hand = DialHand(self.dial)

    @property
    def current(self):
        return self.hand.value


class Alarm:
    def __init__(self, hour, minute, label, active=True, one_shot=False):
        self.hour = hour
        self.minute = minute
        self.label = label
        self.active = active
        self.one_shot = one_shot
        self.last_fired = None


class AlarmManager:
    def __init__(self, storage_path):
        self.dial = Dial()
        self.storage_path = storage_path
        self.load()

    def add(self, hour, minute, label, one_shot=False):
        alarm = Alarm(hour, minute, label or "Alarma", True, one_shot)
        mark = self.dial.locate(lambda item: (item.hour, item.minute) > (hour, minute))
        if mark is None:
            self.dial.place_last(alarm)
        else:
            self.dial.place_before(mark, alarm)
        self.save()
        return alarm

    def remove(self, alarm):
        self.dial.remove(alarm)
        self.save()

    def toggle(self, alarm):
        alarm.active = not alarm.active
        self.save()

    def due(self, moment):
        key = (moment.tm_yday, moment.tm_hour, moment.tm_min)
        fired = []
        for alarm in self.dial.values():
            if alarm.active and alarm.hour == moment.tm_hour and alarm.minute == moment.tm_min and alarm.last_fired != key:
                alarm.last_fired = key
                fired.append(alarm)
        for alarm in fired:
            if alarm.one_shot:
                self.dial.remove(alarm)
        if fired:
            self.save()
        return fired

    def next_alarm(self, moment):
        now_minutes = moment.tm_hour * 60 + moment.tm_min
        best = None
        best_distance = None
        for alarm in self.dial.values():
            if not alarm.active:
                continue
            distance = (alarm.hour * 60 + alarm.minute - now_minutes) % 1440
            if distance == 0:
                distance = 1440
            if best_distance is None or distance < best_distance:
                best = alarm
                best_distance = distance
        return best, best_distance

    def save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as file:
                for alarm in self.dial.values():
                    if not alarm.one_shot:
                        label = alarm.label.replace(";", ",")
                        file.write(f"{alarm.hour};{alarm.minute};{label};{int(alarm.active)}\n")
        except OSError:
            pass

    def load(self):
        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                lines = file.read().splitlines()
        except OSError:
            return
        for line in lines:
            parts = line.split(";")
            if len(parts) == 4 and parts[0].isdigit() and parts[1].isdigit():
                alarm = Alarm(int(parts[0]), int(parts[1]), parts[2], parts[3] == "1")
                self.dial.place_last(alarm)


class Lap:
    def __init__(self, number, split, total):
        self.number = number
        self.split = split
        self.total = total


class Stopwatch:
    def __init__(self, provider):
        self.provider = provider
        self.running = False
        self.accumulated = 0.0
        self.started_at = 0.0
        self.laps = Dial()

    def elapsed(self):
        if self.running:
            return self.accumulated + self.provider.monotonic() - self.started_at
        return self.accumulated

    def toggle(self):
        if self.running:
            self.accumulated = self.elapsed()
            self.running = False
        else:
            self.started_at = self.provider.monotonic()
            self.running = True

    def lap(self):
        total = self.elapsed()
        if total <= 0:
            return
        previous_total = self.laps.origin.before.value.total if self.laps.origin else 0.0
        self.laps.place_last(Lap(len(self.laps) + 1, total - previous_total, total))

    def reset(self):
        self.running = False
        self.accumulated = 0.0
        self.laps.clear()

    def extremes(self):
        if len(self.laps) < 2:
            return None, None
        laps = self.laps.values()
        fastest = min(laps, key=lambda item: item.split)
        slowest = max(laps, key=lambda item: item.split)
        return fastest, slowest


class CountdownTimer:
    def __init__(self, provider):
        self.provider = provider
        self.hours = DialHand(DialFactory.numbers(0, 23))
        self.minutes = DialHand(DialFactory.numbers(0, 59))
        self.seconds = DialHand(DialFactory.numbers(0, 59))
        self.total = 0
        self.running = False
        self.next_tick = 0.0
        self.set_duration(0, 5, 0)

    def set_duration(self, hours, minutes, seconds):
        self.running = False
        self.hours.point_to(hours)
        self.minutes.point_to(minutes)
        self.seconds.point_to(seconds)
        self.total = hours * 3600 + minutes * 60 + seconds

    def remaining(self):
        return self.hours.value * 3600 + self.minutes.value * 60 + self.seconds.value

    def is_zero(self):
        return self.remaining() == 0

    def tick_backward(self):
        if self.seconds.retreat():
            if self.minutes.retreat():
                self.hours.retreat()

    def toggle(self):
        if self.running:
            self.running = False
        elif not self.is_zero():
            self.running = True
            self.next_tick = self.provider.monotonic() + 1

    def update(self):
        if not self.running:
            return False
        now = self.provider.monotonic()
        while self.running and now >= self.next_tick:
            self.tick_backward()
            self.next_tick += 1
            if self.is_zero():
                self.running = False
                return True
        return False

    def fraction_left(self):
        if self.total <= 0:
            return 0.0
        return self.remaining() / self.total

    def text(self):
        if self.hours.value:
            return f"{self.hours.value:02d}:{self.minutes.value:02d}:{self.seconds.value:02d}"
        return f"{self.minutes.value:02d}:{self.seconds.value:02d}"


class Settings:
    def __init__(self):
        self.use_24h = False
        self.smooth_seconds = True


class Fonts:
    FAMILY = "Segoe UI"
    DIGITS = "Segoe UI Semibold"

    @classmethod
    def ui(cls, size, weight="normal"):
        return (cls.FAMILY, size, weight)

    @classmethod
    def digits(cls, size):
        return (cls.DIGITS, size)


class ClockPainter:
    @staticmethod
    def draw(canvas, center_x, center_y, radius, hour, minute, second, theme, fraction=0.0, compact=False):
        outer = radius + (6 if compact else 12)
        canvas.create_oval(center_x - outer, center_y - outer, center_x + outer, center_y + outer,
                           fill=theme.surface_alt, outline=theme.border, width=2)
        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                           fill=theme.face, outline=theme.accent, width=4 if not compact else 3)
        for index in range(60):
            major = index % 5 == 0
            start = radius * (0.84 if major else 0.9)
            end = radius * 0.95
            x1, y1 = Trigonometry.point(center_x, center_y, start, index / 60)
            x2, y2 = Trigonometry.point(center_x, center_y, end, index / 60)
            color = theme.face_text if major else theme.muted
            width = (3 if major else 1) if not compact else (2 if major else 1)
            if compact and not major:
                continue
            canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        if not compact:
            for number in range(1, 13):
                x, y = Trigonometry.point(center_x, center_y, radius * 0.72, number / 12)
                canvas.create_text(x, y, text=str(number), fill=theme.face_text,
                                   font=Fonts.ui(max(10, int(radius * 0.11)), "bold"))
            if radius >= 120:
                canvas.create_text(center_x, center_y + radius * 0.42, text="LISTA CIRCULAR DOBLE",
                                   fill=theme.muted, font=Fonts.ui(max(7, int(radius * 0.045)), "bold"))
        exact_second = second + fraction
        hour_fraction = ((hour % 12) + minute / 60 + exact_second / 3600) / 12
        minute_fraction = (minute + exact_second / 60) / 60
        second_fraction = exact_second / 60
        ClockPainter.hand(canvas, center_x, center_y, radius * 0.5, hour_fraction, theme.face_text,
                          max(4, radius * 0.045), radius * 0.08)
        ClockPainter.hand(canvas, center_x, center_y, radius * 0.75, minute_fraction, theme.accent,
                          max(3, radius * 0.03), radius * 0.1)
        if not compact:
            ClockPainter.hand(canvas, center_x, center_y, radius * 0.86, second_fraction, theme.second_hand,
                              2, radius * 0.18)
        dot = max(4, radius * 0.045)
        canvas.create_oval(center_x - dot, center_y - dot, center_x + dot, center_y + dot,
                           fill=theme.second_hand, outline=theme.face, width=2)

    @staticmethod
    def hand(canvas, center_x, center_y, length, fraction, color, width, tail):
        end_x, end_y = Trigonometry.point(center_x, center_y, length, fraction)
        tail_x, tail_y = Trigonometry.point(center_x, center_y, tail, fraction + 0.5)
        canvas.create_line(tail_x, tail_y, end_x, end_y, fill=color, width=width, capstyle="round")


class Widgets:
    def __init__(self, app):
        self.app = app

    @property
    def tk(self):
        return self.app.tk

    @property
    def theme(self):
        return self.app.themes.current

    def frame(self, parent, color=None, **options):
        return self.tk.Frame(parent, bg=color or self.theme.background, **options)

    def card(self, parent, **options):
        return self.tk.Frame(parent, bg=self.theme.surface, highlightbackground=self.theme.border,
                             highlightthickness=1, **options)

    def label(self, parent, text="", size=11, weight="normal", color=None, background=None, **options):
        return self.tk.Label(parent, text=text, font=Fonts.ui(size, weight), fg=color or self.theme.text,
                             bg=background or parent.cget("bg"), **options)

    def button(self, parent, text, command, kind="primary", size=11, padx=16, pady=8):
        palette = {
            "primary": (self.theme.accent, "#ffffff"),
            "secondary": (self.theme.surface_alt, self.theme.text),
            "danger": (self.theme.danger, "#ffffff"),
            "success": (self.theme.success, "#ffffff"),
            "info": (self.theme.accent_alt, "#ffffff"),
        }
        background, foreground = palette.get(kind, palette["primary"])
        widget = self.tk.Label(parent, text=text, font=Fonts.ui(size, "bold"), fg=foreground, bg=background,
                               padx=padx, pady=pady, cursor="hand2")
        hover = self.app.shade(background, 0.12)
        widget.bind("<Button-1>", lambda event: command())
        widget.bind("<Enter>", lambda event: widget.configure(bg=hover))
        widget.bind("<Leave>", lambda event: widget.configure(bg=background))
        return widget

    def spinbox(self, parent, start, end, value, width=3):
        variable = self.tk.StringVar(value=f"{value:02d}")
        widget = self.tk.Spinbox(parent, from_=start, to=end, textvariable=variable, width=width,
                                 format="%02.0f", wrap=True, justify="center", font=Fonts.digits(20),
                                 bg=self.theme.surface_alt, fg=self.theme.text, buttonbackground=self.theme.border,
                                 insertbackground=self.theme.text, relief="flat", highlightthickness=1,
                                 highlightbackground=self.theme.border, highlightcolor=self.theme.accent)
        return widget, variable

    def fit(self, canvas):
        factor = self.app.factor
        if factor != 1.0:
            canvas.scale("all", 0, 0, factor, factor)

    def canvas(self, parent, width, height, background=None):
        factor = self.app.factor
        return self.tk.Canvas(parent, width=int(width * factor), height=int(height * factor),
                              bg=background or self.theme.surface,
                              highlightthickness=0)


class View:
    title = ""
    subtitle = ""

    def __init__(self, app, parent):
        self.app = app
        self.parent = parent
        self.ui = app.widgets
        self.theme = app.themes.current
        self.build()

    def build(self):
        pass

    def on_second(self, moment):
        pass

    def on_frame(self, moment, fraction):
        pass


class ClockView(View):
    title = "Reloj"
    subtitle = "Hora local en tiempo real"

    def build(self):
        body = self.ui.frame(self.parent)
        body.pack(fill="both", expand=True)
        left = self.ui.card(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        self.canvas = self.ui.canvas(left, 460, 460)
        self.canvas.pack(expand=True, padx=16, pady=16)
        right = self.ui.frame(body)
        right.pack(side="left", fill="both")
        digital = self.ui.card(right)
        digital.pack(fill="x")
        self.time_label = self.ui.label(digital, "", 46, color=self.theme.text)
        self.time_label.configure(font=Fonts.digits(46))
        self.time_label.pack(anchor="w", padx=22, pady=(18, 0))
        self.period_label = self.ui.label(digital, "", 13, "bold", self.theme.accent)
        self.period_label.pack(anchor="w", padx=24)
        self.date_label = self.ui.label(digital, "", 13, color=self.theme.muted)
        self.date_label.pack(anchor="w", padx=24, pady=(4, 18))
        info = self.ui.card(right)
        info.pack(fill="x", pady=14)
        self.ui.label(info, "Próxima alarma", 10, "bold", self.theme.muted).pack(anchor="w", padx=22, pady=(14, 0))
        self.alarm_label = self.ui.label(info, "", 13, "bold", wraplength=290, justify="left")
        self.alarm_label.pack(anchor="w", padx=22, pady=(2, 14))
        dials = self.ui.card(right)
        dials.pack(fill="x")
        self.ui.label(dials, "Manecillas sobre las listas circulares", 10, "bold", self.theme.muted).pack(
            anchor="w", padx=22, pady=(14, 6))
        self.dial_labels = []
        for name in ("Horas", "Minutos", "Segundos"):
            row = self.ui.frame(dials, self.theme.surface)
            row.pack(fill="x", padx=22, pady=3)
            self.ui.label(row, name, 11, "bold", width=9, anchor="w").pack(side="left")
            value = self.ui.label(row, "", 12, color=self.theme.text)
            value.configure(font=Fonts.digits(12))
            value.pack(side="left")
            self.dial_labels.append(value)
        self.ui.label(dials, "anterior  ←  actual  →  siguiente", 9, color=self.theme.muted).pack(
            anchor="w", padx=22, pady=(6, 14))

    def on_second(self, moment):
        settings = self.app.settings
        self.time_label.configure(text=TimeFormatter.clock(moment.tm_hour, moment.tm_min, moment.tm_sec,
                                                           settings.use_24h))
        self.period_label.configure(text=TimeFormatter.period(moment.tm_hour, settings.use_24h) or "Formato 24 horas")
        self.date_label.configure(text=SpanishCalendar.long_date(moment))
        alarm, distance = self.app.alarms.next_alarm(moment)
        if alarm is None:
            self.alarm_label.configure(text="Sin alarmas activas", fg=self.theme.muted)
        else:
            hours, minutes = divmod(distance, 60)
            when = TimeFormatter.clock(alarm.hour, alarm.minute, 0, settings.use_24h, False)
            period = TimeFormatter.period(alarm.hour, settings.use_24h)
            self.alarm_label.configure(text=f"{when} {period}  ·  {alarm.label}\nSuena en {hours} h {minutes} min",
                                       fg=self.theme.text)
        mechanism = self.app.mechanism
        for label, hand in zip(self.dial_labels, (mechanism.hours, mechanism.minutes, mechanism.seconds)):
            mark = hand.mark
            label.configure(text=f"{mark.before.value:02d}  ←  [{mark.value:02d}]  →  {mark.after.value:02d}")

    def on_frame(self, moment, fraction):
        self.canvas.delete("all")
        hour, minute, second = self.app.mechanism.state()
        smooth = fraction if self.app.settings.smooth_seconds else 0.0
        ClockPainter.draw(self.canvas, 230, 230, 200, hour, minute, second, self.theme, smooth)
        self.ui.fit(self.canvas)


class WorldView(View):
    title = "Relojes del mundo"
    subtitle = "Recorre las ciudades con anterior y siguiente"

    def build(self):
        top = self.ui.card(self.parent)
        top.pack(fill="x")
        navigation = self.ui.frame(top, self.theme.surface)
        navigation.pack(fill="x", padx=20, pady=20)
        self.ui.button(navigation, "◀  Anterior", self.show_previous, "secondary").pack(side="left")
        self.ui.button(navigation, "Siguiente  ▶", self.show_next, "secondary").pack(side="right")
        center = self.ui.frame(navigation, self.theme.surface)
        center.pack(side="left", expand=True)
        self.canvas = self.ui.canvas(center, 180, 180)
        self.canvas.pack(side="left", padx=16)
        texts = self.ui.frame(center, self.theme.surface)
        texts.pack(side="left")
        self.city_label = self.ui.label(texts, "", 24, "bold")
        self.city_label.pack(anchor="w")
        self.country_label = self.ui.label(texts, "", 12, color=self.theme.muted)
        self.country_label.pack(anchor="w")
        self.time_label = self.ui.label(texts, "", 40)
        self.time_label.configure(font=Fonts.digits(40))
        self.time_label.pack(anchor="w")
        self.diff_label = self.ui.label(texts, "", 11, "bold", self.theme.accent)
        self.diff_label.pack(anchor="w")
        self.grid = self.ui.frame(self.parent)
        self.grid.pack(fill="both", expand=True, pady=(14, 0))
        self.tiles = []
        for index, city in enumerate(self.app.world.dial.values()):
            tile = self.ui.card(self.grid)
            tile.grid(row=index // 4, column=index % 4, sticky="nsew", padx=5, pady=5)
            tile.configure(cursor="hand2")
            name = self.ui.label(tile, city.name, 11, "bold")
            name.pack(anchor="w", padx=14, pady=(10, 0))
            value = self.ui.label(tile, "", 18)
            value.configure(font=Fonts.digits(18))
            value.pack(anchor="w", padx=14)
            extra = self.ui.label(tile, "", 9, color=self.theme.muted)
            extra.pack(anchor="w", padx=14, pady=(0, 10))
            for widget in (tile, name, value, extra):
                widget.bind("<Button-1>", lambda event, target=city: self.select(target))
            self.tiles.append((city, tile, name, value, extra))
        for column in range(4):
            self.grid.columnconfigure(column, weight=1)

    def show_previous(self):
        self.app.world.hand.retreat()
        self.refresh()

    def show_next(self):
        self.app.world.hand.advance()
        self.refresh()

    def select(self, city):
        self.app.world.hand.point_to(city)
        self.refresh()

    def refresh(self):
        self.on_second(self.app.provider.now())
        self.on_frame(None, 0)

    def on_second(self, moment):
        settings = self.app.settings
        city = self.app.world.current
        local = self.app.provider.at_offset(city.offset)
        self.city_label.configure(text=city.name)
        self.country_label.configure(text=f"{city.country}  ·  {TimeFormatter.offset(city.offset)}")
        period = TimeFormatter.period(local.tm_hour, settings.use_24h)
        self.time_label.configure(text=TimeFormatter.clock(local.tm_hour, local.tm_min, local.tm_sec,
                                                           settings.use_24h) + (f" {period}" if period else ""))
        difference = city.offset - self.app.provider.local_offset_hours()
        if difference == 0:
            text = "Misma hora que tu equipo"
        else:
            amount = abs(difference)
            amount_text = f"{amount:g}"
            text = f"{amount_text} h {'adelante' if difference > 0 else 'atrás'} de tu hora local"
        self.diff_label.configure(text=f"{SpanishCalendar.short_date(local)}  ·  {text}")
        for tile_city, tile, name, value, extra in self.tiles:
            moment_city = self.app.provider.at_offset(tile_city.offset)
            selected = tile_city is city
            color = self.theme.accent if selected else self.theme.border
            tile.configure(highlightbackground=color, highlightthickness=2 if selected else 1)
            value.configure(text=TimeFormatter.clock(moment_city.tm_hour, moment_city.tm_min, 0,
                                                     settings.use_24h, False) + " " +
                            TimeFormatter.period(moment_city.tm_hour, settings.use_24h))
            daytime = "Día" if 6 <= moment_city.tm_hour < 18 else "Noche"
            extra.configure(text=f"{TimeFormatter.offset(tile_city.offset)}  ·  {daytime}")

    def on_frame(self, moment, fraction):
        city = self.app.world.current
        local = self.app.provider.at_offset(city.offset)
        self.canvas.delete("all")
        ClockPainter.draw(self.canvas, 90, 90, 72, local.tm_hour, local.tm_min, local.tm_sec, self.theme,
                          fraction if self.app.settings.smooth_seconds else 0.0)
        self.ui.fit(self.canvas)


class AlarmView(View):
    title = "Alarmas"
    subtitle = "Se guardan en la lista circular y en el archivo alarmas.txt"

    def build(self):
        form = self.ui.card(self.parent)
        form.pack(fill="x")
        inner = self.ui.frame(form, self.theme.surface)
        inner.pack(fill="x", padx=20, pady=18)
        moment = self.app.provider.now()
        self.ui.label(inner, "Hora", 10, "bold", self.theme.muted).grid(row=0, column=0, sticky="w")
        self.ui.label(inner, "Minuto", 10, "bold", self.theme.muted).grid(row=0, column=2, sticky="w")
        self.ui.label(inner, "Nombre de la alarma", 10, "bold", self.theme.muted).grid(row=0, column=3, sticky="w",
                                                                                     padx=(18, 0))
        self.hour_box, self.hour_var = self.ui.spinbox(inner, 0, 23, moment.tm_hour)
        self.hour_box.grid(row=1, column=0)
        self.ui.label(inner, ":", 20, "bold").grid(row=1, column=1, padx=4)
        self.minute_box, self.minute_var = self.ui.spinbox(inner, 0, 59, (moment.tm_min + 1) % 60)
        self.minute_box.grid(row=1, column=2)
        self.name_var = self.app.tk.StringVar(value="")
        entry = self.app.tk.Entry(inner, textvariable=self.name_var, font=Fonts.ui(14), bg=self.theme.surface_alt,
                                  fg=self.theme.text, insertbackground=self.theme.text, relief="flat",
                                  highlightthickness=1, highlightbackground=self.theme.border,
                                  highlightcolor=self.theme.accent, width=26)
        entry.grid(row=1, column=3, padx=(18, 12), ipady=7, sticky="ew")
        entry.bind("<Return>", lambda event: self.add())
        self.ui.button(inner, "+  Agregar alarma", self.add).grid(row=1, column=4)
        self.ui.button(inner, "Probar sonido", self.app.ring_bell, "secondary").grid(row=1, column=5, padx=(10, 0))
        self.message = self.ui.label(inner, "Usa 24 horas para elegir la hora (ej: 18 = 6 p. m.).", 10,
                                     color=self.theme.muted)
        self.message.grid(row=2, column=0, columnspan=6, sticky="w", pady=(10, 0))
        inner.columnconfigure(3, weight=1)
        self.list_card = self.ui.card(self.parent)
        self.list_card.pack(fill="both", expand=True, pady=(14, 0))
        self.render_list()

    def add(self):
        hour_text = self.hour_var.get().strip()
        minute_text = self.minute_var.get().strip()
        if not (hour_text.isdigit() and minute_text.isdigit()) or int(hour_text) > 23 or int(minute_text) > 59:
            self.message.configure(text="La hora debe estar entre 00 y 23, y los minutos entre 00 y 59.",
                                   fg=self.theme.danger)
            return
        label = self.name_var.get().strip()[:40]
        alarm = self.app.alarms.add(int(hour_text), int(minute_text), label)
        self.name_var.set("")
        when = TimeFormatter.clock(alarm.hour, alarm.minute, 0, self.app.settings.use_24h, False)
        self.message.configure(text=f"Alarma «{alarm.label}» creada para las {when} "
                                    f"{TimeFormatter.period(alarm.hour, self.app.settings.use_24h)}.",
                               fg=self.theme.success)
        self.render_list()

    def remove(self, alarm):
        self.app.alarms.remove(alarm)
        self.message.configure(text=f"Alarma «{alarm.label}» eliminada.", fg=self.theme.muted)
        self.render_list()

    def toggle(self, alarm):
        self.app.alarms.toggle(alarm)
        self.render_list()

    def render_list(self):
        for child in self.list_card.winfo_children():
            child.destroy()
        header = self.ui.frame(self.list_card, self.theme.surface)
        header.pack(fill="x", padx=20, pady=(16, 8))
        total = len(self.app.alarms.dial)
        self.ui.label(header, f"Mis alarmas ({total})", 13, "bold").pack(side="left")
        self.ui.label(header, "Ordenadas por hora · cada una es un nodo de la lista", 10,
                      color=self.theme.muted).pack(side="right")
        if total == 0:
            self.ui.label(self.list_card, "Todavía no tienes alarmas. Crea la primera arriba.", 12,
                          color=self.theme.muted).pack(pady=40)
            return
        for alarm in self.app.alarms.dial.values():
            row = self.tk_row()
            settings = self.app.settings
            when = TimeFormatter.clock(alarm.hour, alarm.minute, 0, settings.use_24h, False)
            color = self.theme.text if alarm.active else self.theme.muted
            time_label = self.ui.label(row, when, 22, color=color, background=self.theme.surface_alt)
            time_label.configure(font=Fonts.digits(22))
            time_label.pack(side="left", padx=(16, 6), pady=8)
            self.ui.label(row, TimeFormatter.period(alarm.hour, settings.use_24h), 10, "bold", color,
                          self.theme.surface_alt).pack(side="left")
            name = alarm.label + ("  (pospuesta)" if alarm.one_shot else "")
            self.ui.label(row, name, 12, color=color, background=self.theme.surface_alt).pack(side="left", padx=16)
            self.ui.button(row, "Eliminar", lambda target=alarm: self.remove(target), "danger", 10, 12, 5).pack(
                side="right", padx=(6, 14))
            state_text = "Activa" if alarm.active else "Inactiva"
            self.ui.button(row, state_text, lambda target=alarm: self.toggle(target),
                           "success" if alarm.active else "secondary", 10, 12, 5).pack(side="right")

    def tk_row(self):
        row = self.ui.frame(self.list_card, self.theme.surface_alt)
        row.pack(fill="x", padx=20, pady=4)
        return row


class StopwatchView(View):
    title = "Cronómetro"
    subtitle = "Las vueltas se guardan en una lista circular doble"

    def build(self):
        top = self.ui.card(self.parent)
        top.pack(fill="x")
        self.display = self.ui.label(top, "", 64)
        self.display.configure(font=Fonts.digits(64))
        self.display.pack(pady=(24, 4))
        self.status = self.ui.label(top, "", 11, "bold", self.theme.muted)
        self.status.pack()
        buttons = self.ui.frame(top, self.theme.surface)
        buttons.pack(pady=(14, 22))
        self.toggle_button = self.ui.button(buttons, "", self.toggle, "primary", 12, 22, 10)
        self.toggle_button.pack(side="left", padx=6)
        self.ui.button(buttons, "Vuelta", self.lap, "info", 12, 22, 10).pack(side="left", padx=6)
        self.ui.button(buttons, "Reiniciar", self.reset, "secondary", 12, 22, 10).pack(side="left", padx=6)
        self.laps_card = self.ui.card(self.parent)
        self.laps_card.pack(fill="both", expand=True, pady=(14, 0))
        self.render_laps()
        self.update_buttons()

    def toggle(self):
        self.app.stopwatch.toggle()
        self.update_buttons()

    def lap(self):
        self.app.stopwatch.lap()
        self.render_laps()

    def reset(self):
        self.app.stopwatch.reset()
        self.update_buttons()
        self.render_laps()

    def update_buttons(self):
        running = self.app.stopwatch.running
        text = "Pausar" if running else ("Reanudar" if self.app.stopwatch.elapsed() > 0 else "Iniciar")
        self.toggle_button.configure(text=text)
        self.status.configure(text="EN MARCHA" if running else "DETENIDO",
                              fg=self.theme.success if running else self.theme.muted)

    def render_laps(self):
        for child in self.laps_card.winfo_children():
            child.destroy()
        header = self.ui.frame(self.laps_card, self.theme.surface)
        header.pack(fill="x", padx=20, pady=(16, 8))
        self.ui.label(header, f"Vueltas ({len(self.app.stopwatch.laps)})", 13, "bold").pack(side="left")
        self.ui.label(header, "Recorrido hacia atrás: la más reciente primero", 10,
                      color=self.theme.muted).pack(side="right")
        if self.app.stopwatch.laps.is_empty():
            self.ui.label(self.laps_card, "Presiona «Vuelta» mientras el cronómetro corre.", 12,
                          color=self.theme.muted).pack(pady=30)
            return
        fastest, slowest = self.app.stopwatch.extremes()
        for index, mark in enumerate(self.app.stopwatch.laps.marks_backward()):
            if index >= 8:
                break
            lap = mark.value
            row = self.ui.frame(self.laps_card, self.theme.surface_alt)
            row.pack(fill="x", padx=20, pady=3)
            tag, color = "", self.theme.text
            if lap is fastest:
                tag, color = "Más rápida", self.theme.success
            elif lap is slowest:
                tag, color = "Más lenta", self.theme.danger
            self.ui.label(row, f"Vuelta {lap.number}", 11, "bold", color, self.theme.surface_alt, width=10,
                          anchor="w").pack(side="left", padx=14, pady=6)
            self.ui.label(row, tag, 10, "bold", color, self.theme.surface_alt, width=11, anchor="w").pack(side="left")
            split = self.ui.label(row, TimeFormatter.elapsed(lap.split), 12, color=color,
                                  background=self.theme.surface_alt)
            split.configure(font=Fonts.digits(12))
            split.pack(side="left", padx=20)
            total = self.ui.label(row, "Total " + TimeFormatter.elapsed(lap.total), 11, color=self.theme.muted,
                                  background=self.theme.surface_alt)
            total.pack(side="right", padx=14)

    def on_frame(self, moment, fraction):
        self.display.configure(text=TimeFormatter.elapsed(self.app.stopwatch.elapsed()))


class TimerView(View):
    title = "Temporizador"
    subtitle = "Cuenta regresiva recorriendo los diales hacia atrás"

    def build(self):
        body = self.ui.frame(self.parent)
        body.pack(fill="both", expand=True)
        left = self.ui.card(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        self.canvas = self.ui.canvas(left, 380, 380)
        self.canvas.pack(expand=True, padx=16, pady=16)
        right = self.ui.card(body)
        right.pack(side="left", fill="both")
        self.ui.label(right, "Duración", 13, "bold").pack(anchor="w", padx=22, pady=(18, 8))
        boxes = self.ui.frame(right, self.theme.surface)
        boxes.pack(anchor="w", padx=22)
        timer = self.app.timer
        self.hour_box, self.hour_var = self.ui.spinbox(boxes, 0, 23, timer.hours.value)
        self.minute_box, self.minute_var = self.ui.spinbox(boxes, 0, 59, timer.minutes.value)
        self.second_box, self.second_var = self.ui.spinbox(boxes, 0, 59, timer.seconds.value)
        for column, (box, caption) in enumerate(((self.hour_box, "horas"), (self.minute_box, "minutos"),
                                                  (self.second_box, "segundos"))):
            box.grid(row=0, column=column * 2)
            self.ui.label(boxes, caption, 9, color=self.theme.muted).grid(row=1, column=column * 2)
            if column < 2:
                self.ui.label(boxes, ":", 18, "bold").grid(row=0, column=column * 2 + 1, padx=3)
        self.ui.label(right, "Atajos", 10, "bold", self.theme.muted).pack(anchor="w", padx=22, pady=(16, 6))
        presets = self.ui.frame(right, self.theme.surface)
        presets.pack(anchor="w", padx=22)
        for index, (text, minutes) in enumerate((("1 min", 1), ("3 min", 3), ("5 min", 5), ("10 min", 10),
                                                 ("Pomodoro 25", 25), ("1 hora", 60))):
            self.ui.button(presets, text, lambda value=minutes: self.preset(value), "secondary", 10, 10, 5).grid(
                row=index // 3, column=index % 3, padx=3, pady=3, sticky="ew")
        controls = self.ui.frame(right, self.theme.surface)
        controls.pack(anchor="w", padx=22, pady=(18, 8))
        self.toggle_button = self.ui.button(controls, "Iniciar", self.toggle, "primary", 12, 20, 9)
        self.toggle_button.pack(side="left")
        self.ui.button(controls, "Reiniciar", self.reset, "secondary", 12, 20, 9).pack(side="left", padx=8)
        self.message = self.ui.label(right, "", 10, color=self.theme.muted, wraplength=300, justify="left")
        self.message.pack(anchor="w", padx=22, pady=(4, 18))
        self.update_buttons()

    def read_inputs(self):
        values = []
        for variable, limit in ((self.hour_var, 23), (self.minute_var, 59), (self.second_var, 59)):
            text = variable.get().strip()
            if not text.isdigit() or int(text) > limit:
                return None
            values.append(int(text))
        return values

    def preset(self, minutes):
        hours, minutes = divmod(minutes, 60)
        self.hour_var.set(f"{hours:02d}")
        self.minute_var.set(f"{minutes:02d}")
        self.second_var.set("00")
        self.app.timer.set_duration(hours, minutes, 0)
        self.update_buttons()

    def toggle(self):
        timer = self.app.timer
        if not timer.running and (timer.is_zero() or timer.remaining() == timer.total):
            values = self.read_inputs()
            if values is None or sum(values) == 0:
                self.message.configure(text="Escribe una duración válida mayor a cero.", fg=self.theme.danger)
                return
            timer.set_duration(*values)
        timer.toggle()
        self.update_buttons()

    def reset(self):
        values = self.read_inputs() or [0, 5, 0]
        self.app.timer.set_duration(*values)
        self.update_buttons()

    def update_buttons(self):
        timer = self.app.timer
        if timer.running:
            self.toggle_button.configure(text="Pausar")
            self.message.configure(text="Cada segundo la manecilla de segundos retrocede al nodo anterior. "
                                        "Al pasar de 00 a 59, la de minutos también retrocede.",
                                   fg=self.theme.muted)
        else:
            paused = not timer.is_zero() and timer.remaining() != timer.total
            self.toggle_button.configure(text="Reanudar" if paused else "Iniciar")
            if not paused:
                self.message.configure(text="Elige una duración y presiona Iniciar.", fg=self.theme.muted)

    def on_frame(self, moment, fraction):
        timer = self.app.timer
        canvas = self.canvas
        canvas.delete("all")
        center, radius = 190, 160
        canvas.create_oval(center - radius, center - radius, center + radius, center + radius,
                           outline=self.theme.surface_alt, width=18)
        extent = 359.9 * timer.fraction_left()
        if extent > 0:
            canvas.create_arc(center - radius, center - radius, center + radius, center + radius, start=90,
                              extent=extent, style="arc", outline=self.theme.accent, width=18)
        for index in range(60):
            x, y = Trigonometry.point(center, center, radius - 30, index / 60)
            active = index == timer.seconds.value
            size = 4 if active else 1.5
            color = self.theme.second_hand if active else self.theme.border
            canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")
        canvas.create_text(center, center - 10, text=timer.text(), fill=self.theme.text, font=Fonts.digits(48))
        state = "EN MARCHA" if timer.running else ("TERMINADO" if timer.is_zero() else "EN PAUSA")
        canvas.create_text(center, center + 40, text=state, fill=self.theme.muted, font=Fonts.ui(11, "bold"))
        self.ui.fit(canvas)


class DialDescriptor:
    def __init__(self, name, hand, explanation):
        self.name = name
        self.hand = hand
        self.explanation = explanation


class StructureView(View):
    title = "Estructura de datos"
    subtitle = "Así se ve por dentro la lista circular doble que mueve el reloj"

    def build(self):
        mechanism = self.app.mechanism
        if self.app.structure_dials is None:
            self.app.structure_dials = DialHand(DialFactory.items([
                DialDescriptor("Segundos", mechanism.seconds,
                               "Cada segundo la manecilla pasa al nodo siguiente. Cuando llega de 59 al origen "
                               "(00), la lista de minutos avanza un nodo."),
                DialDescriptor("Minutos", mechanism.minutes,
                               "Avanza un nodo cada vez que la lista de segundos completa una vuelta. Al volver "
                               "al origen, avanza la lista de horas."),
                DialDescriptor("Horas", mechanism.hours,
                               "24 nodos enlazados en círculo: del nodo 23 se vuelve al 00 sin necesidad de "
                               "reiniciar nada, porque el último nodo apunta al primero."),
            ]))
        body = self.ui.frame(self.parent)
        body.pack(fill="both", expand=True)
        left = self.ui.card(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        selector = self.ui.frame(left, self.theme.surface)
        selector.pack(fill="x", padx=16, pady=(14, 0))
        self.ui.button(selector, "◀", self.previous_dial, "secondary", 11, 12, 4).pack(side="left")
        self.dial_title = self.ui.label(selector, "", 13, "bold")
        self.dial_title.pack(side="left", expand=True)
        self.ui.button(selector, "▶", self.next_dial, "secondary", 11, 12, 4).pack(side="right")
        self.canvas = self.ui.canvas(left, 470, 470)
        self.canvas.pack(expand=True, padx=12, pady=8)
        right = self.ui.card(body)
        right.pack(side="left", fill="both")
        self.ui.label(right, "Detalle del nodo actual", 13, "bold").pack(anchor="w", padx=20, pady=(16, 8))
        self.detail = self.ui.canvas(right, 340, 120)
        self.detail.pack(padx=20)
        self.facts = []
        for caption in ("Tamaño de la lista", "Nodo origen", "Nodo actual", "Anterior", "Siguiente",
                        "Pasos recorridos"):
            row = self.ui.frame(right, self.theme.surface)
            row.pack(fill="x", padx=20, pady=2)
            self.ui.label(row, caption, 10, color=self.theme.muted, width=18, anchor="w").pack(side="left")
            value = self.ui.label(row, "", 11, "bold")
            value.pack(side="left")
            self.facts.append(value)
        self.explanation = self.ui.label(right, "", 10, color=self.theme.muted, wraplength=320, justify="left")
        self.explanation.pack(anchor="w", padx=20, pady=(12, 16))

    @property
    def descriptor(self):
        return self.app.structure_dials.value

    def previous_dial(self):
        self.app.structure_dials.retreat()
        self.redraw()

    def next_dial(self):
        self.app.structure_dials.advance()
        self.redraw()

    def redraw(self):
        self.on_second(self.app.provider.now())

    def on_second(self, moment):
        descriptor = self.descriptor
        hand = descriptor.hand
        dial = hand.dial
        mark = hand.mark
        self.dial_title.configure(text=f"Lista de {descriptor.name.lower()}")
        values = [f"{len(dial)} nodos", f"{dial.origin.value:02d}", f"{mark.value:02d}", f"{mark.before.value:02d}",
                  f"{mark.after.value:02d}", f"{hand.steps}"]
        for label, value in zip(self.facts, values):
            label.configure(text=value)
        self.explanation.configure(text=descriptor.explanation)
        self.draw_dial(dial, mark)
        self.draw_detail(mark)

    def draw_dial(self, dial, current):
        canvas = self.canvas
        canvas.delete("all")
        center, radius = 235, 195
        count = len(dial)
        positions = {}
        for index, mark in enumerate(dial.marks()):
            positions[id(mark)] = Trigonometry.point(center, center, radius, index / count)
        marks = list(dial.marks())
        for mark in marks:
            x1, y1 = positions[id(mark)]
            x2, y2 = positions[id(mark.after)]
            canvas.create_line(x1, y1, x2, y2, fill=self.theme.border, width=2)
        size = 9 if count > 30 else 14
        for mark in marks:
            x, y = positions[id(mark)]
            fill, outline, text_color = self.theme.surface_alt, self.theme.border, self.theme.muted
            scale = 1.0
            if mark is current:
                fill, outline, text_color, scale = self.theme.accent, self.theme.accent, "#ffffff", 1.6
            elif mark is current.before:
                fill, outline, text_color, scale = self.theme.accent_alt, self.theme.accent_alt, "#ffffff", 1.2
            elif mark is current.after:
                fill, outline, text_color, scale = self.theme.success, self.theme.success, "#ffffff", 1.2
            if mark is dial.origin:
                outline = self.theme.second_hand
            mark_radius = size * scale
            canvas.create_oval(x - mark_radius, y - mark_radius, x + mark_radius, y + mark_radius,
                               fill=fill, outline=outline, width=2)
            show_text = count <= 30 or mark.value % 5 == 0 or mark is current or mark is current.before or mark is current.after
            if show_text:
                canvas.create_text(x, y, text=f"{mark.value:02d}", fill=text_color,
                                   font=Fonts.ui(8 if scale == 1.0 else 9, "bold"))
        hx, hy = positions[id(dial.origin)]
        canvas.create_text(hx, hy - 30, text="origen", fill=self.theme.second_hand, font=Fonts.ui(10, "bold"))
        canvas.create_text(center, center - 30, text=f"{current.value:02d}", fill=self.theme.text,
                           font=Fonts.digits(54))
        canvas.create_text(center, center + 25, text="nodo actual", fill=self.theme.muted, font=Fonts.ui(11))
        legend = ((self.theme.accent_alt, "anterior"), (self.theme.accent, "actual"), (self.theme.success, "siguiente"))
        for index, (color, caption) in enumerate(legend):
            x = center - 110 + index * 80
            canvas.create_oval(x - 5, center + 62, x + 5, center + 72, fill=color, outline="")
            canvas.create_text(x + 10, center + 67, text=caption, anchor="w", fill=self.theme.muted,
                               font=Fonts.ui(9))
        self.ui.fit(canvas)

    def draw_detail(self, mark):
        canvas = self.detail
        canvas.delete("all")
        boxes = ((mark.before, self.theme.accent_alt), (mark, self.theme.accent), (mark.after, self.theme.success))
        width, height, gap, top = 92, 46, 32, 38
        for index, (item, color) in enumerate(boxes):
            left = index * (width + gap)
            third = width / 3
            canvas.create_rectangle(left, top, left + width, top + height, outline=color, width=2,
                                    fill=self.theme.surface_alt)
            canvas.create_line(left + third, top, left + third, top + height, fill=color)
            canvas.create_line(left + 2 * third, top, left + 2 * third, top + height, fill=color)
            canvas.create_text(left + third / 2, top + height / 2, text="•", fill=self.theme.text, font=Fonts.ui(12))
            canvas.create_text(left + width / 2, top + height / 2, text=f"{item.value:02d}", fill=self.theme.text,
                               font=Fonts.ui(11, "bold"))
            canvas.create_text(left + width - third / 2, top + height / 2, text="•", fill=self.theme.text,
                               font=Fonts.ui(12))
            caption = ("ant.", "valor", "sig.")
            canvas.create_text(left + width / 2, top - 14, text=("anterior", "actual", "siguiente")[index],
                               fill=color, font=Fonts.ui(9, "bold"))
            for part in range(3):
                canvas.create_text(left + third * part + third / 2, top + height + 12, text=caption[part],
                                   fill=self.theme.muted, font=Fonts.ui(7))
            if index < 2:
                start = left + width
                canvas.create_line(start + 2, top + 15, start + gap - 2, top + 15, fill=self.theme.text, arrow="last")
                canvas.create_line(start + gap - 2, top + 31, start + 2, top + 31, fill=self.theme.text, arrow="last")
        self.ui.fit(canvas)


class ClockApp:
    VIEWS = (("Reloj", "◷", ClockView), ("Mundo", "◍", WorldView), ("Alarmas", "⏰", AlarmView),
             ("Cronómetro", "⏱", StopwatchView), ("Temporizador", "⌛", TimerView),
             ("Estructura", "⟲", StructureView))

    def __init__(self, bridge):
        self.bridge = bridge
        self.tk = bridge.module("tkinter")
        self.provider = TimeProvider(bridge.module("time"))
        self.settings = Settings()
        self.themes = ThemeCatalog()
        self.mechanism = ClockMechanism()
        self.world = WorldClock()
        self.alarms = AlarmManager(bridge.script_folder() + "/alarmas.txt")
        self.stopwatch = Stopwatch(self.provider)
        self.timer = CountdownTimer(self.provider)
        self.views = DialHand(DialFactory.items(self.VIEWS))
        self.structure_dials = None
        self.widgets = Widgets(self)
        self.view = None
        self.popups = []
        self.last_second = None
        self.second_started = self.provider.monotonic()
        self.loop_id = None
        moment = self.provider.now()
        self.mechanism.sync(moment.tm_hour, moment.tm_min, moment.tm_sec)
        self.factor = 1.0
        self.root = self.tk.Tk()
        self.factor = max(1.0, self.root.winfo_fpixels("1i") / 96)
        self.root.title("Reloj Circular · Listas Circulares Dobles")
        self.size_window()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<Control-Right>", lambda event: self.next_view())
        self.root.bind("<Control-Left>", lambda event: self.previous_view())
        self.root.bind("<Control-t>", lambda event: self.next_theme())
        self.build()
        self.loop()

    def size_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(1220 * self.factor)
        height = int(760 * self.factor)
        self.root.minsize(min(int(1120 * self.factor), screen_width), min(int(700 * self.factor), screen_height - 60))
        if width > screen_width * 0.96 or height > screen_height * 0.9:
            try:
                self.root.state("zoomed")
            except self.tk.TclError:
                self.root.geometry(f"{screen_width}x{screen_height - 60}+0+0")
        else:
            left = (screen_width - width) // 2
            top = max(0, (screen_height - height) // 2 - 20)
            self.root.geometry(f"{width}x{height}+{left}+{top}")

    def shade(self, color, amount):
        color = color.lstrip("#")
        channels = [int(color[index:index + 2], 16) for index in (0, 2, 4)]
        brightness = sum(channels) / 3
        if brightness > 140:
            channels = [max(0, int(channel * (1 - amount))) for channel in channels]
        else:
            channels = [min(255, int(channel + (255 - channel) * amount)) for channel in channels]
        return "#" + "".join(f"{channel:02x}" for channel in channels)

    def build(self):
        for child in self.root.winfo_children():
            if child not in self.popups:
                child.destroy()
        theme = self.themes.current
        self.root.configure(bg=theme.background)
        ui = self.widgets
        sidebar = ui.frame(self.root, theme.surface, width=int(262 * self.factor))
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        brand = ui.frame(sidebar, theme.surface)
        brand.pack(fill="x", padx=22, pady=(26, 22))
        logo = ui.canvas(brand, 44, 44, theme.surface)
        logo.pack(side="left")
        ClockPainter.draw(logo, 22, 22, 16, 10, 10, 30, theme, compact=True)
        ui.fit(logo)
        texts = ui.frame(brand, theme.surface)
        texts.pack(side="left", padx=10)
        ui.label(texts, "Reloj Circular", 14, "bold").pack(anchor="w")
        ui.label(texts, "Hecho 100% en Python", 9, color=theme.muted).pack(anchor="w")
        self.nav_items = []
        for mark in self.views.dial.marks():
            name, icon, _ = mark.value
            selected = mark is self.views.mark
            background = theme.accent if selected else theme.surface
            foreground = "#ffffff" if selected else theme.text
            item = self.tk.Label(sidebar, text=f"  {icon}   {name}", anchor="w", font=Fonts.ui(12, "bold"),
                                 bg=background, fg=foreground, padx=14, pady=10, cursor="hand2")
            item.pack(fill="x", padx=14, pady=2)
            item.bind("<Button-1>", lambda event, target=mark: self.show_view(target))
            if not selected:
                item.bind("<Enter>", lambda event, widget=item: widget.configure(bg=theme.surface_alt))
                item.bind("<Leave>", lambda event, widget=item: widget.configure(bg=theme.surface))
        bottom = ui.frame(sidebar, theme.surface)
        bottom.pack(side="bottom", fill="x", padx=14, pady=18)
        ui.label(bottom, "Tema de color", 9, "bold", theme.muted).pack(anchor="w", padx=6)
        theme_row = ui.frame(bottom, theme.surface)
        theme_row.pack(fill="x", pady=(4, 12))
        ui.button(theme_row, "◀", self.previous_theme, "secondary", 10, 10, 4).pack(side="left")
        ui.label(theme_row, theme.name, 11, "bold").pack(side="left", expand=True)
        ui.button(theme_row, "▶", self.next_theme, "secondary", 10, 10, 4).pack(side="right")
        ui.label(bottom, "Formato de hora", 9, "bold", theme.muted).pack(anchor="w", padx=6)
        format_row = ui.frame(bottom, theme.surface)
        format_row.pack(fill="x", pady=(4, 12))
        ui.button(format_row, "12 h", lambda: self.set_format(False), "primary" if not self.settings.use_24h
                  else "secondary", 10, 14, 4).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ui.button(format_row, "24 h", lambda: self.set_format(True), "primary" if self.settings.use_24h
                  else "secondary", 10, 14, 4).pack(side="left", expand=True, fill="x", padx=(3, 0))
        smooth_text = "Segundero suave: Sí" if self.settings.smooth_seconds else "Segundero suave: No"
        ui.button(bottom, smooth_text, self.toggle_smooth, "secondary", 10, 10, 5).pack(fill="x")
        ui.label(bottom, "Ctrl + ← / → cambia de sección\nCtrl + T cambia el tema", 9,
                 color=theme.muted, justify="left").pack(anchor="w", padx=6, pady=(12, 0))
        main = ui.frame(self.root)
        main.pack(side="left", fill="both", expand=True, padx=26, pady=22)
        header = ui.frame(main)
        header.pack(fill="x", pady=(0, 16))
        titles = ui.frame(header)
        titles.pack(side="left")
        view_class = self.views.value[2]
        ui.label(titles, view_class.title, 24, "bold").pack(anchor="w")
        ui.label(titles, view_class.subtitle, 11, color=theme.muted).pack(anchor="w")
        chip = ui.frame(header, theme.surface)
        chip.pack(side="right")
        self.header_time = ui.label(chip, "", 13, "bold", background=theme.surface)
        self.header_time.pack(side="left", padx=(14, 6), pady=8)
        self.header_date = ui.label(chip, "", 11, color=theme.muted, background=theme.surface)
        self.header_date.pack(side="left", padx=(0, 14))
        content = ui.frame(main)
        content.pack(fill="both", expand=True)
        self.view = view_class(self, content)
        self.last_second = None

    def show_view(self, mark):
        self.views.mark = mark
        self.build()

    def next_view(self):
        self.views.advance()
        self.build()

    def previous_view(self):
        self.views.retreat()
        self.build()

    def next_theme(self):
        self.themes.following()
        self.build()

    def previous_theme(self):
        self.themes.preceding()
        self.build()

    def set_format(self, use_24h):
        self.settings.use_24h = use_24h
        self.build()

    def toggle_smooth(self):
        self.settings.smooth_seconds = not self.settings.smooth_seconds
        self.build()

    def ring_bell(self, times=3):
        for index in range(times):
            self.root.after(index * 350, self.root.bell)

    def notify(self, title, message, snooze_alarm=None):
        theme = self.themes.current
        popup = self.tk.Toplevel(self.root)
        self.popups.append(popup)
        popup.title(title)
        popup.configure(bg=theme.surface)
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        ui = self.widgets
        ui.label(popup, "⏰", 40, color=theme.accent).pack(pady=(22, 0))
        ui.label(popup, title, 18, "bold").pack(padx=40)
        ui.label(popup, message, 12, color=theme.muted, wraplength=340).pack(padx=40, pady=(6, 18))
        buttons = ui.frame(popup, theme.surface)
        buttons.pack(pady=(0, 22))
        state = {"open": True}

        def close():
            state["open"] = False
            if popup in self.popups:
                self.popups.remove(popup)
            popup.destroy()

        def snooze():
            moment = self.provider.at_offset(self.provider.local_offset_hours() + 5 / 60)
            self.alarms.add(moment.tm_hour, moment.tm_min, snooze_alarm.label, one_shot=True)
            close()
            if isinstance(self.view, (AlarmView, ClockView)):
                self.build()

        def chime():
            if state["open"]:
                self.root.bell()
                self.root.after(1200, chime)

        ui.button(buttons, "Detener", close, "primary").pack(side="left", padx=6)
        if snooze_alarm is not None:
            ui.button(buttons, "Posponer 5 min", snooze, "secondary").pack(side="left", padx=6)
        popup.protocol("WM_DELETE_WINDOW", close)
        popup.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - popup.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - popup.winfo_height()) // 3
        popup.geometry(f"+{max(0, x)}+{max(0, y)}")
        chime()

    def loop(self):
        moment = self.provider.now()
        second_key = (moment.tm_yday, moment.tm_hour, moment.tm_min, moment.tm_sec)
        if second_key != self.last_second:
            new_second = self.last_second is not None
            self.last_second = second_key
            self.second_started = self.provider.monotonic()
            self.mechanism.sync(moment.tm_hour, moment.tm_min, moment.tm_sec)
            period = TimeFormatter.period(moment.tm_hour, self.settings.use_24h)
            self.header_time.configure(text=TimeFormatter.clock(moment.tm_hour, moment.tm_min, moment.tm_sec,
                                                                self.settings.use_24h) + (f" {period}" if period else ""))
            self.header_date.configure(text=SpanishCalendar.long_date(moment))
            self.view.on_second(moment)
            if new_second:
                for alarm in self.alarms.due(moment):
                    when = TimeFormatter.clock(alarm.hour, alarm.minute, 0, self.settings.use_24h, False)
                    self.notify("¡Alarma!", f"{alarm.label} · {when} "
                                            f"{TimeFormatter.period(alarm.hour, self.settings.use_24h)}", alarm)
                    if isinstance(self.view, AlarmView):
                        self.view.render_list()
        if self.timer.update():
            self.notify("¡Tiempo cumplido!", "El temporizador llegó a cero.")
            if isinstance(self.view, TimerView):
                self.view.update_buttons()
        fraction = min(0.999, self.provider.monotonic() - self.second_started)
        self.view.on_frame(moment, fraction)
        self.loop_id = self.root.after(50, self.loop)

    def close(self):
        if self.loop_id is not None:
            self.root.after_cancel(self.loop_id)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ClockApp(RuntimeBridge()).run()
