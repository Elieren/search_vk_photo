Android (apk)

## Edit the file before compiling

```
nano main.py

server = ''
```
In '' insert the ip address of the server.

## Installing buildozer

We will use google colab as a virtual machine for building apk.

Buildozer.ipynd is a file for google colab containing commands to install buildozer and build apk.

You need to move the entire android folder to the virtual machine.

```
android \
    background.png
    banner.png
    buildozer.spec
    main.py
```

Run each command from the file in order.

Wait for the file to finish compiling.

The file will be in the bin/.

Everything