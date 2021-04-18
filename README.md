# sway-devour
```
Usage: sway-devour.py [OPTIONS] EXECUTEABLE

  sway-devour: a sway script to mimic the behavour of x11 window devourers  
      (such as bspwm's devour functionality or devour.c (SalmanAbedin@disroot.org)), 
      using a workspace instead of x11 (un)mapping to devour. 

  Version: 0.1

  Arguments:

      EXECUTEABLE    Some shell command to launch.

Options:
  --workspace TEXT  Set name of workspace to devour to
  --help            Show this message and exit. 
```

Technically this also works for i3 (as it uses i3ipc-python). However, please do not use it there, 
as Salman Abedin's devour.c does a much better job (it doesn't use a workspace as a hack to hide the window; 
it is available at <https://github.com/salman-abedin/devour>. 


## Install 

1. `wget -O ~/.local/bin https://github.com/deafmute1/sway-devour/blob/master/sway-devour.py`
2. Make it executable (or simply call it with python in you config, whatever you prefer): `chmod +x ~/.local/bin/sway-devour.py`
2. Install the requirements: `pip3 install click i3ipc` / `pip3 install -r requirements.txt`
3. Add a line to your sway config: `bindsym <KEYBIND> ~/.local/bin/sway-devour.py`

## TODO 
- Remove click usage in favour of stdlib (argparse), as it seems pointless to pull another dep in for a small project like this. 

## Copyright 
Copyright 2020 Ethan Djeric <ethan@ethandjeric.com> 

Licensed under the terms of the GPL3 or (optionally) any later version. 





