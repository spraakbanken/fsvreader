Migrated to python3

To download, install and run:

```
git clone https://github.com/spraakbanken/fsvreader.git
make install
source .venv/bin/activate

make serve-dev
```

- go to `http://localhost:8000/reader/aldre_lagar/Yvgl.html`

Each time you start from a new terminal, you must do:

`source .venv/bin/activate`

`make serve-dev`


Every time you change the code, the server will reload (but when updating templates you might need to restart the server)
