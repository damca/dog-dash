Generally best to follow: https://www.youtube.com/watch?v=goToXTC96Co&t=3157s

See video  "deploy flask app on linux"

The flask app is called "server" in the main.py file.
`gunicorn -w 2 main:server`

Sometimes useful to disable nginx:
    sudo update-rc.d -f nginx disable

SQLite and multithreading:

  * https://davidcaron.dev/sqlalchemy-multiple-threads-and-processes/
  * https://stackoverflow.com/questions/27240278/sharing-memory-in-gunicorn
  * https://stackoverflow.com/questions/19407488/sqlite-flask-occasionally-taking-10-20-seconds-to-return-simple-select-query

  1. import `connection` object into `main.py`
  2. ensure `connect` method in `listen_keys.py` uses kwarg: `check_same_thread=False`
  3. use gunicorn's `--preload` option
  4. check to make sure that multiple processes aren't listening and adding entries by testing a `0` entry



Command to kick off server:
     export FLASK_APP=main.py; sudo env PATH=$PATH gunicorn -w 2 main:server --preload 
