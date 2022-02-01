#!/bin/sh

#xrandr --output DP-4 --primary --right-of DP-2 --rate 144 &&
librewolf &
setxkbmap -layout be &
feh --bg-fill /home/smuky/Pictures/1.png /home/smuky/Pictures/2.png &
picom  --backend glx --xrender-sync-fence &
thunderbird &
discord &
caprine &
