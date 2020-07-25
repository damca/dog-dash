Generally best to follow: https://www.youtube.com/watch?v=goToXTC96Co&t=3157s

I also downloaded this video as "deploy flask app on linux"

The flask app is called "server" in the main.py file.
`gunicorn -w 4 main:server`

Sometimes useful to disable nginx:
    sudo update-rc.d -f nginx disable

