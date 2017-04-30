### Build [xwiimote](https://github.com/dvdhrm/xwiimote)

- dependencies: [ref](https://github.com/dvdhrm/xwiimote-bindings/pull/8)
    - swig
    - autoconf
    - libtool
    - python-dev
- the pre-compiled package found in the Debian Jessie repo is too old ([ref](https://github.com/dvdhrm/xwiimote-bindings/issues/13))
- `./configure --prefix=/usr` **or** append `LD_LIBRARY_PATH` later on ([ref](https://askubuntu.com/questions/633949/failed-to-build-xwiimote-bindings))


### Build [xwiimote-bindings](https://github.com/dvdhrm/xwiimote-bindings)

```
./autogen.sh
make
sudo make install
```

### Connect Wii Remote as Bluetooth device

```
$ bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent 
[bluetooth]# scan on
[bluetooth]# pair <MAC>
[bluetooth]# connect <MAC>
...
Connection successful
```

### Use xwiimote Python binding

```bash
# optional
# export LD_LIBRARY_PATH=/usr/local/lib
python test.py [--debug]
```
