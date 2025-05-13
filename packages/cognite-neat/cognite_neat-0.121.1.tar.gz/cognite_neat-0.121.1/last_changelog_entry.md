
### Fixed

- Reading a data model from CDF with `neat.read.cdf.data_model(...)`
with a reverse direct relation that points to a direct relation that is
not pointing in the opposite direction now gives a warning instead of an
error.