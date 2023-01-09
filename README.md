

## Highlights

- **Monitor temperature, humidity, rainfall, and wind speed**: The station makes use of an off the shelf [Wind vane, anemometer and rain bucket](https://shop.pimoroni.com/products/wind-and-rain-sensors-for-weather-station-wind-vane-anemometer-rain-gauge?variant=39350966648915) setup coupled with a high precision I2C [HTU31-d temperature sensor](https://shop.pimoroni.com/products/adafruit-htu31-temperature-humidity-sensor-breakout-board-stemma-qt-qwiic?variant=39337572597843) 
- **Visualize data from one remote dashboard**: Access your customizable environmental data dashboard from anywhere.

![](https://assets.balena.io/blog-common/2021/07/sensev2.png)

## Motivation

I wanted to have hyperlocal weather data that I could check from my bed. Most of the weather prediction sites for my hometown were always pretty far off the actual realtime conditions. It always felt warmer or colder than my phone said it was. Or the predicted level of wind was way lower than the state in my garden. So I decided to build something to give me a sense of what the exact conditions were in my garden, right now :D

### How it works

This project builds heavily on the great work done by my previous teammates at balena.io and is based on their great [balena-sense](https://github.com/balenalabs/balena-sense) project. Balena-sense cleverly utilizes Industrial IO (IIO) and relies on the variety of sensor drivers already included in the Linux kernel itself. (You can learn more about the sensor block and its use of IIO in [this recent blog post](https://www.balena.io/blog/balenablocks-in-depth-sensor-and-pulse/).) This made it super easy to interface with the htu31-d temp sensor and pump data into the influx time series database.

![](/images/weather-vane.jpg)

Unfortunately, the wind and rainfall sensor is not I2C and unsupported by IIO. Instead, it uses an odd/custom serial protocol. For this, I created a simple docker service that uses python to pull data out of the serial interface and then posts it via MQTT to the balena-sense connector block that then marshalls it into the DB.

To insulate and protect the temperature sensor, I created and 3D printed a [Stevenson Screen](https://en.wikipedia.org/wiki/Stevenson_screen) as seen below:

![](/images/Temp-sensor.jpg)
