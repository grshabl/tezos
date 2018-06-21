using docker for bake monitor
-----------------------------

nix >= 2.0 is required:

```shell
$ nix-build --version
nix-build (Nix) 2.0
```

```shell
$ git checkout https://gitlab.com/obsidian.systems/tezos-baking-platform.git tz
$ cd tz
$ git submodule sync
$ git submodule update --recursive --init
```

create docker image (with nix)

    $ docker load -i $(nix-build -A bake-central-docker --no-out-link)
    $ docker run -p=127.0.0.1:8000:8000 tezos-bake-monitor --pg-connection=<conn string> --route=http://172.0.0.1:8000


