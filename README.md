Generally best to follow: https://www.youtube.com/watch?v=goToXTC96Co&t=3157s

I also downloaded this video as "deploy flask app on linux"

The flask app is called "server" in the main.py file.
`gunicorn -w 9 main:server`


# WSL 2 project setup

Both python's `webbrowser` and `python-xlib` need to work.

## Register chrome with webbrowser

```python
import webbrowser
chrome_path = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', webbrowser.Chrome(chrome_path), instance=webbrowser.Chrome(chrome_path),
preferred=True)
```


## Setup display

This will fix python-xlib

Install `vcxsrv`
Roughly can follow: https://www.youtube.com/watch?v=ymV7j003ETA
But after installing just add this to .zshrc / .bashrc etc.
```
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=1
```

