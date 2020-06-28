# Speedrun
Grabs speedrun data from [speedrun.com](https://speedrun.com) and plot run times since the release of a chosen game with plotly.js.
Currently only supports 'per-game' categories.

[Demo](https://speedrun.hrfee.pw)

# Install
Grab a .whl from the release section to install with pip, or

```
git clone https://github.com/hrfee/speedrun.git
cd speedrun
poetry update
poetry install
```
A dockerfile is also available.

# Usage

`speedrun-serve` starts the web interface on `0.0.0.0:8059`.
