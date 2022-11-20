# ICA_Transform
Implements Independent Component Analysis on a tif image.  In signal processing, independent component analysis (ICA) is a computational method for separating a multivariate signal into additive subcomponents. This is done by assuming that at most one subcomponent is Gaussian and that the subcomponents are statistically independent from each other.

## Usage

While ICA can be used as a Python library, the more common use is to use the Command Line Interface (CLI).

```
$ python3 ICA.py
usage: ICA.py [-h] -i INPUT [-b BANDS] -o OUTFILE [-ft FT] [--verbose VERBOSE]
arguments:
  -h, --help            
                        show this help message and exit
  -i INPUT, --input INPUT
                        Input image (Required) (default: None)
  -b BANDS, --bands     
                        Number of output bands (optional)
                        (default: 3)
  -o, OUTFILE, --outfile OUTFILE
                        Required, Output geotif name
                        (default: None )
  -ft FT, --filetype FT
                        Output Filetype (optional)
                        (default: float16)
```

### Docker
A Dockerfile and a docker-compose.yml are included for ease of development. The built docker image provides all the system dependencies needed to run the library. The library can also be tested locally, but all system dependencies must be installed first, and the use of a virtualenv is recommended.

To build the docker image use the included docker-compose tasks:

    $ docker-compose build

Which will build an image called that can be run

    # this will run the image in interactive mode (open bash script)
    $ docker-compose run bash

    # this willl run the tests using the locally available image
    $ docker-compose run test