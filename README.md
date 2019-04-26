[![Build Status](https://travis-ci.com/RagingCub/team7-design3-2019.svg?token=osUKSXp2YedetsxPAmp3&branch=master)](https://travis-ci.com/RagingCub/team7-design3-2019)

# team7-design3-2019

A school project which forces three different domains to squash their skills and build a self-working robot.
This automaton has to do various tasks given by teachers and reflects the Cody-2009 project.

## Pain

Named after the Naruto character "[Pain](https://naruto.fandom.com/wiki/Nagato)".
Its purpose is to transport specific objects from point A to B using an electromagnet powered by a condensator.
By reading QRCodes and some magic algorithms, it knows what to get and where to travel.

## Launch

The project is divided between two stations, the robot and the base. Both need to work together in order to achieve their goal.

### First

Run this on both stations.

```
pip install -r requirements.txt
```

### Second

On Pain.
```
python run pain.py [-m (remote|champsionship|display-command-remote)] [-p <PORT>]
```

On Base Station.
```
python run baseStation.py [-m (remote|champsionship|ui-remote)] [-p <PORT>]  [-a <BROADCAST_ADRESS>]
```

You need to use a Wi-Fi which lets you broadcast to other computers.

## Unit used

`Orientation.py` uses radians to define its angle. Front is zero and angles are calculated in the same manner as normal mathematics ditacte. Degrees can also be used. `Angle.py` follows the same rules.

`Distance.py` uses centimeters.

# LICENSE

See our project's [license notice](LICENSE.md).
