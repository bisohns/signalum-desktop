<p align="center">
  <img src="assets/bt.png" height="25"  width="25"/>
  <a href="https://bisoncorps.github.io/signalum-desktop"> <img src="src/main/resources/base/signalum.png" height="100" /> </a>
  <img src="assets/wf.png" height="25"  width="25"/><br/>
  <span> <b style="font-size: 40px;">Signalum Desktop</b></span>
</p>
<br>


A Desktop application on the <a href="https://github.com/bisoncorps/signalum" title="Signalum Library/CLI Tool">Signalum Python Library/CLI Tool</a>.
The Signalum Desktop application is an attempt to develop a single tool for analysing and visualizing your wireless environment over a range of Bluetooth Devices, WiFi Devices and hopefully more.

Written entirely in Python3, Signalum Desktop currently accomplished the following:

- Basic wifi SSID and Bluetooth identification
- Signal Visualization
- Wifi and Bluetooth RSSI Values calculation
- Export - Ability to export values to excel worksheet


This application was bootstrapped with <a href="https://github.com/mherrmann/fbs" title="fbs">Fman Build system</a>
<br> <br>

![Signal-Graph](assets/signal-graph.png)

![Devices](assets/devices.png)

## Supported Protocols

### Bluetooth

<img src="assets/bt.png" height="25"  width="25"/><br/>
Bluetooth operates at frequencies between 2402 and 2480 MHz, or 2400 and 2483.5 MHz including guard bands 2 MHz wide at the bottom end and 3.5 MHz wide at the top. This is in the globally unlicensed (but not unregulated) industrial, scientific and medical (ISM) 2.4 GHz short-range radio frequency band. It is a standard wire-replacement communications protocol primarily designed for low power consumption, with a short range based on low-cost transceiver microchips in each device.

### Wifi

<img src="assets/wf.png" height="25"  width="25"/><br/>
This refers to a family of radio technologies that is commonly used for the wireless local area networking (WLAN) of devices which is based around the IEEE 802.11 family of standards. Wi-Fi most commonly uses the 2.4 gigahertz (12 cm) UHF and 5 gigahertz (6 cm) SHF ISM radio bands. At close range, some versions of Wi-Fi, running on suitable hardware, can achieve speeds of over 1 Gbit/s.

## Dependencies

Apt packages

- bluetooth
- libbluetooth-dev

Application should be run with ```sudo``` priviledges to scan for wireless devices, else there might be unprecedented behaviour

## Development

```bash
  # install dependencies
  make dependencies
```

```bash
  # make ui files and run in development mode
  make dev
```

After modifying any `.ui` file run the `make ui_files` command to update

## Demo

Simple usage of Signalum Desktop to monitor multiple devices

![Demo](assets/output.gif)


## Contributors

Much thanks and appreciation to everyone who made this project possible

- [Manasseh Mmadu](https://mensaah.github.io)
- [Diretnan Domnan](https://diretnandomnan.webnode.com)
- [Wisdom Praise](https://wizzywit.github.io)
- Engr. Ajao Lukman

## TODO

- [x] Integrate signalum Bluetooth
- [x] Integrate Signalum Wifi
- [x] Bind settings to functions
- [ ] Include adapter details for wifi and bluetooth
- [ ] Add Deployment for Linux and MAC
- [ ] Add Tests and Documentation

## Credits

- [Bluetooth](https://en.wikipedia.org/wiki/Bluetooth)
- [Wifi](https://en.wikipedia.org/wiki/Wi-Fi)
- [PyBlueZ](https://pybluez.github.io/)
- [Signalum](https://bisoncorps.github.io/signalum)
- [PyQt5](https://pypi.org/project/PyQt5/)


## Contribution

Please keep a link to the original [repository](https://github.com/bisoncorps/signalum-desktop). If you have made a fork with substantial modifications that you feel may be useful, then please open a new [issue](https://github.com/bisoncorps/signalum-desktop/issues) with a link and short description.
