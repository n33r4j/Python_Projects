# Virtual Sensors

## Why?
Sometimes, you just want to know if your code works the way you expect it to without actually assembling everything(bench testing or bread boarding?). You also don't have/don't want to damage/are too lazy to use real hardware.

This project was conceived when I wanted to test code for an RPi project but didn't have any hardware with me. While mocking pins with `gpiozero` was helpful, I also wanted have a physical way to see what was happening.

## Goals

- To model as many common sensors as possible in as detail as possible (perhaps being able to choose the level of detail).
- Allow testing with and without GUI (on the terminal) as sometimes, you don't have access to a GUI.

## Hardware/Sensors

1. PIR Motion Sensor
2. LCD 16x2
3. Mini Servo


