# 📦 Raspberry Pi V2G

This is the Raspberry Pi **V2G repository README** in which we will explain all the parts of the code **we know**.
For any sort of code should be a description written down here so that other programmers can easily read and understand here what the code does, no matter their skill level.


## 🌟 Highlights

- First start of the **README** file for better understanding
- Some code is written by previous semester we'll do our best to explain it as good as possible but there could be some mistakes.

### ✍️ Authors

- Mike Weijts | m.weijts@student.fontys.nl | 3rd Semester
- Adam van der velden | adam.vandervelden@student.fontys.nl | 3rd Semester


## 🚀 Structure


**main.py**
**services**
**statemachine**
**pyplc/openv2gx**
**tests
  testDigipotService.py**
    In this file you can test the DigipotService
    **IMPORTANT**
    We used a Digi Pot 6 Click

  **testMosfetService.py**
    In this file you can test the MosfetService
    **IMPORTANT**
    We used a **6R190P6 Mosfet** and a **Bi-Directional Logic Level Converter** to control the mosfets with a raspberry Pi.
    *update: we changed our mosfets because we could not toggle them with the 3.3v output of the GPIO pins on the raspberry Pi,
    after other considerations we eventually chose to switch them out with different ones.*


## ⬇️ Installation

Simple, understandable installation instructions!

Turn on SPI for digital potentiometer
```sudo raspi-config```
Interface options -> SPI -> YES -> OK -> FINISH

pip install RPi.GPIO
```

And be sure to specify any other minimum requirements like Python versions or operating systems.

*You may be inclined to add development instructions here, don't.*
