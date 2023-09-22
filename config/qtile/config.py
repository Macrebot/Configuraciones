# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

from libqtile import bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from os import path
import subprocess


mod = "mod4"
terminal = "alacritty"
color1 = "#2b88e1"
colorR = "#D45F5F"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Lanzadores Personalizados
    Key([mod], "e", lazy.spawn("thunar"), desc="Spawn FileManager"),
    Key([mod], "b", lazy.spawn("brave"), desc="Brave Launcher"),
    Key([mod], "c", lazy.spawn("code"), desc="VSCode Launcher"),

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show run")),
    Key([mod, "shift"], "m", lazy.spawn("rofi -show")),

]

# groups = [Group(i) for i in "123456789"]
__groups = {
    1: Group("", matches=[Match(wm_class=["alacritty"])]),
    2: Group("󰒍", matches=[Match(wm_class=["brave"])]),
    3: Group("󰈮"),
    4: Group("󰚯"),
    5: Group("󰂫"),
    6: Group("󰋊"),
    7: Group("", matches=[Match(wm_class=["FileManager"])]),
    8: Group(""),
    9: Group("󰂺"),
    0: Group(""),
}

groups = [__groups[i] for i in __groups]

def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(get_group_key(i.name)),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(get_group_key(i.name)),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus = color1,
        border_focus_stack=["#222222", "#222222"],
        border_width=4),
    layout.MonadTall(
        border_width = 3,
        border_focus = color1,
        margin = 6,
        border_normal = "#222222",
        change_size = 10,
    ),
    layout.Max(),
    layout.Floating(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    # layout.Matrix(
    #     border_width = 3,
    #     border_focus = color1,
    #     margin = 6,
    #     border_normal = "#222222",
    #     change_size = 10,
    # ),
    # layout.MonadWide(
    #     border_width = 3,
    #     border_focus = color1,
    #     margin = 6,
    #     border_normal = "#222222",
    #     change_size = 10,
    # ),
    #layout.RatioTile(),
    #layout.Tile(),
    # layout.TreeTab(
    #     active_bg = color1,
    #     font = "Hurmit Nerd Font",
    #     inactive_bg = "#511e47",
    #     sections = [''],
    # ),
    #layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Hurmit Nerd Font",
    fontsize=20,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    background = color1,
                    foreground = "#000",
                    width = 120,
                ),
                # widget.TextBox(
                #     fmt='', 
                #     font="Hurmit Nerd Font",
                #     foreground= color1,
                #     fontsize = 60,
                # ),
                widget.GroupBox(
                    highlight_method = 'line',
                    highlight_color = ['#000', color1],
                    active = color1,
                    fontsize = 30,
                    padding_x = 10,
                    padding_y = 10,
                    margin_y = 5,
                    disable_drag = True,
                ),
                widget.WindowName(
                    foreground = color1,
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.CheckUpdates(
                    custom_command = "CheckUpdates",
                    update_interval = 1800,
                    display_format = "Actualizaciones: {updates}",
                ),
                widget.TextBox(
                    fmt='',
                    font="Hurmit Nerd Font",
                    foreground= color1,
                    fontsize = 60,
                    padding = 0,

                ),
                widget.Battery(
                    background = color1,
                    low_background = colorR,
                    low_foreground = "#fff",
                    low_percentage = 0.2,
                ),
                widget.TextBox(
                    fmt='',
                    font="Hurmit Nerd Font",
                    foreground= "#000",
                    background = color1,
                    fontsize = 60,
                    padding = 0,
                ),
                widget.Clock(format="%d-%m-%Y %a %H:%M %p"),
                widget.TextBox(
                    fmt='',
                    font="Hurmit Nerd Font",
                    foreground= color1,
                    fontsize = 60,
                    padding = 0,
                ),
                widget.QuickExit(
                    background = color1,
                ),
            ],

            30,
            border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            border_color=[color1, "000000", color1, "000000"],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


os.system("python .autostart.py")
