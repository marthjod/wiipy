### build xwiimote

- dependencies: [ref](https://github.com/dvdhrm/xwiimote-bindings/pull/8)
    - swig
    - autoconf
    - libtool
    - python-dev
- the pre-compiled package found in the Debian Jessie repo is too old ([ref](https://github.com/dvdhrm/xwiimote-bindings/issues/13))
- `./configure --prefix=/usr` **or** append `LD_LIBRARY_PATH` later on ([ref](https://askubuntu.com/questions/633949/failed-to-build-xwiimote-bindings))


### build xwiimote-bindings

```
./autogen.sh
make
sudo make install
```

### use xwiimote python binding

```bash
# optional
# export LD_LIBRARY_PATH=/usr/local/lib
python examples/python/xwiimote_test.py
```
