from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess

mod = "mod4"
terminal = "kitty"
browser = "firefox"

colors = {
        'background' : '#072C45',
        'foreground' : '#0d4b74', #slightly lighter than the bg, "selected"
        'focused' : '#b70bca',
        'unfocused' : '#301070',
        'alt-secondary' : '#BEC10B',
        'alert' : '#C10E0B',
        'black' : '#000000',
        'gray' : '#8b83a3',
        'white': '#FFFFFF'
        }

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys = [
    # Switch between windows
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod, "control"], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             ),
    Key([mod, "control"], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             ),
    Key([mod, "control"], "s",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.previous_layout()),
    Key([mod, "shift"], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "m", lazy.layout.maximize()),

    #Media Keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),    

    #Perso Keybinds
    Key([mod], "d", lazy.spawn("rofi -modi drun, run -show drun")),
    Key([mod], "b", lazy.spawn(browser)),
    Key([mod], "a", lazy.to_screen(1)),
    Key([mod], "e", lazy.to_screen(0)),

    Key([mod,"shift", "control"],  "Left",  lazy.function(window_to_next_screen)),
    Key([mod,"shift", "control"],  "Right", lazy.function(window_to_previous_screen)),
]

groups = [
        Group(
            name = "ampersand",
            layout = "monadtall".lower(),
            label = "",
            matches = [Match(wm_class=["Firefox"])]
            ),
        Group(
            name = "eacute",
            layout = "monadtall".lower(),
            label = "󰇮",
            matches = [Match(wm_class=["Thunderbird"])]
            ),
        Group(
            name = "quotedbl",
            layout = "columns".lower(),
            label = "",
            matches = [Match(wm_class=["discord", "Caprine"])]
            ),
        Group(
            name = "apostrophe",
            label = "",
            matches = [Match(wm_class=["Spotify", "spotify"])]
            ),
        Group(
            name = "parenleft",
            label = ""
            ),
        Group(
            name = "section",
            label = "󰕷"
            ),
        Group(
            name = "egrave",
            label = "󰈡"
            ),
        Group(
            name = "exclam",
            label = "󰊠"
            ),
        Group(
            name = "ccedilla",
            label = "󰏿"
            ),
        Group(
            name = "agrave",
            label = "󰊗",
            layout = "max".lower()
            )
        ]

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": colors["focused"],
                "border_normal": colors["unfocused"]
                }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
]

widget_defaults = dict(
    font='roboto',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
        widgets_list = [
                widget.GroupBox(
                    margin_y = 5,
                    margin_x = 0,
                    padding_y = 3,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors["white"],
                    inactive = colors["gray"],
                    rounded = False,
                    highlight_color = colors["foreground"],
                    highlight_method = "line",
                    this_current_screen_border = colors["focused"],
                    this_screen_border = colors ["unfocused"],
                    other_current_screen_border = colors["focused"],
                    other_screen_border = colors["unfocused"],
                    foreground = colors["foreground"],
                    background = colors["background"]
                    ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CurrentLayoutIcon(
                    scale = 0.7
                    ),
                widget.CurrentLayout(),
                widget.PulseVolume(
                    fmt = '󰕾 {}',
                    padding = 6,
                    background = colors["foreground"]
                    ),
                widget.CPU(
                    padding = 6,
                    format = '󰍛 {load_percent}%'
                    ),
                widget.Net(
                       interface = "enp3s0",
                       format = '󰒪 {down} ↓↑ {up}',
                       padding = 6,
                       background = colors["foreground"]
                       ),
                #widget.Clipboard(),
                #widget.Sep(),
                widget.Clock(
                    padding = 6,
                    format='󰥔 %d-%m-%Y %a %I:%M %p'
                    ),
                widget.Systray(),
                widget.Systray(
                    background = colors["foreground"],
                    icon_size = 15
                    ),
                ]
        return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[3:]
    return widgets_screen1

def init_screens():
    return [Screen(
            top = bar.Bar(widgets = init_widgets_list(), 
                size = 20, 
                background = colors["background"]),
                ),
        Screen(
            top = bar.Bar(widgets = init_widgets_screen1(),
                size = 20, 
                background=colors["background"]),
    )]

screens = init_screens();

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click ="floating_only"
#cursor_warp = True #send cursor whereever there is a new window or change in focus, ver annoying.
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='League Of Legends'), #League client
    Match(wm_class='leagueclientux.exe'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

#AutoStart
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([script])

wmname = "LG3D"
