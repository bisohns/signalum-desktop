<p align="center">
  <img src="src/main/resources/base/signalum.png" height="100" /><br/>
  <span> <b style="font-size: 40px;">Signalum Desktop</b></span>
</p>
<br>


A Desktop application for the <a href="https://github.com/bisoncorps/signalum" title="Signalyze CLI Tool">Signalyze CLI Tool</a>

This application was bootstrapped with <a href="https://github.com/mherrmann/fbs" title="fbs">Fman Build system</a>
<br> <br>

![Signal-Graph](assets/signal-graph.png)

![Devices](assets/devices.png)


### Development

```bash
  # install dependencies
  make dependencies
```

```bash
  # make ui files and run in development mode
  make dev
```

### Demo

![Demo](assets/output.gif)


After modifying any `.ui` file run the `make ui_files` command to update


## TODO

- [x] Integrate signalum Bluetooth
- [x] Integrate Signalum Wifi
- [x] Bind settings to functions
- [ ] Include adapter details for wifi and bluetooth
- [ ] Add Deployment for Linux and MAC
- [ ] Add Tests and Documentation
