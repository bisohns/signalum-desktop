# Signalum Desktop

A Desktop application for the [Signalyze CLI Tool](https://github.com/bisoncorps/signalum)

### Development

```bash
  # install dependencies and start in development mode
  make development
```

### Installation

```bash
  # create symbolic link in /usr/local/bin
  make install
```

After modifying any `.ui` file run the `make ui_files` command to update

### Run

```bash
  ./signalum
```

### Examples

![Signal-Graph](assets/signal-graph.png)

![Devices](assets/devices.png)

## TODO

- [x] Integrate signalum Bluetooth
- [x] Integrate Signalum Wifi
- [ ] Include adapter details for wifi and bluetooth
- [ ] Add Deployment for Linux and MAC
- [ ] Add Tests and Documentation
