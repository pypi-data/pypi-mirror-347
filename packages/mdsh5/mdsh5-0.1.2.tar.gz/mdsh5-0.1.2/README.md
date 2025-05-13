# mdsh5

[![Test](https://github.com/anchal-physics/mdsh5/actions/workflows/test.yml/badge.svg)](https://github.com/anchal-physics/mdsh5/actions/workflows/test.yml)
![Codecov](https://img.shields.io/codecov/c/github/anchal-physics/mdsh5)

A higher level python package that uses [`mdsthin`](https://github.com/MDSplus/mdsthin) to read MDSPlus data and store it in hdf5 formate for easy caching, viewing, distribution, and analysis.

## Usage:

### Installation (Recommended)
If you plan to use this package often, you can install it locally using PyPi.
```
pip install mdsh5
```
This will also install a script `read_mds` in your `bin` that you can call as:
```
read_mds
```
No need to even write python and you can call this script from anywhere in your computer. Note that if you installed this package in a conda environment, the script would go to conda environment's bin directory which is typically present in `$HOME/anaconda3/envs/<env_name>/bin` and this might not be in your path by default.

### Don't want to install
You can download the [read_mds.py](https://github.com/anchal-physics/mdsh5/blob/main/mdsh5/read_mds.py) file from mdsh5 directory and use it directly or import it in your python code as per your need. You'll need to install `h5py`, `PyYaml`, `tqdm`, and [`mdsthin`](https://github.com/MDSplus/mdsthin). For your convinience, a conda environment is provided in this repository to install the required packages in a separate environment. To use:

```
conda env create -f conda_env.yml
conda activate mdsh5
```

## Purpose

If you want to run custom analysis on your shot data from the device, it can become tedious to download data using existing tools. To this end, [`mdsthin`](https://github.com/MDSplus/mdsthin) now provides an excellent pythonic solution to download MDSPlus data
from remote servers.

This package is one level higher data management tool. It uses [`mdsthin`](https://github.com/MDSplus/mdsthin) to download data but provides a functionality to provide required shot numbers, tree names, and point names in an organized yaml format and creates a fast transversible data dictionary in HDF5 format. HDF5 is simple self-describing fiole format which is supported on multiple platforms and has well developed libraries for reading and writing in almost all programming languages. The msot important aspect is that when python opens an HDF5 file, it can navigate through the data dictionary and read only the required portion of the data file. Thus it requires much less RAM and even if the accumulated data is in GigaBytes, you can read small particular portions of it very fast.

Additionally, if you use VSCode, I highly recomment installing the [H5Web extension](https://marketplace.visualstudio.com/items?itemName=h5web.vscode-h5web) which let's you quickly visualize the data stored in the HDF5 files created by this package.

![KSTAR_data](https://raw.githubusercontent.com/anchal-physics/mdsh5/main/H5WebExample.png)

## Documentation

**NOTE:** All tree and pointnames will be converted to upper case regardless of how you enter them. This is a chosen convention to keep the cache consistent even if you change the case of a pointname.

Additional documentation would come soon. For now, please refer to the [config_examples](https://github.com/anchal-physics/mdsh5/tree/main/mdsh5/config_examples) to get started on how to provide the input configuration.

Additionally, use the help flag to print out the help message from `read_mds`:
```
% read_mds -h
usage: read_mds [-h] [-n SHOT_NUMBERS [SHOT_NUMBERS ...]] [-t TREES [TREES ...]] [-p POINT_NAMES [POINT_NAMES ...]] [-s SERVER] [-x PROXY_SERVER]
                [-r RESAMPLE [RESAMPLE ...]] [--rescale RESCALE [RESCALE ...]] [-o OUT_FILENAME] [--reread_data] [-f] [-c CONFIG] [--configTemplate]

Read data from MDSPlus server for provided shot numbers, trees, and pointnames.

options:
  -h, --help            show this help message and exit
  -n, --shot_numbers SHOT_NUMBERS [SHOT_NUMBERS ...]
                        Shot number(s). You can provide a range using double quotes to pass a string.eg. -n "12345 to 12354"
  -t, --trees TREES [TREES ...]
                        Tree name(s)
  -p, --point_names POINT_NAMES [POINT_NAMES ...]
                        Point name(s). Must match number of trees provided unless a single tree is given.
  -s, --server SERVER   MDSPlus server in the format of username@ip_address:port Default is None
  -x, --proxy_server PROXY_SERVER
                        Proxy server to use to tunnel through to the server. If provided, the username part from server definition will be used to ssh into the proxy
                        server from where it assumed that you have access to the MDSplus server. If the username for proxy-server is different, add it as a prefix here
                        with @. Default is None
  -r, --resample RESAMPLE [RESAMPLE ...]
                        Resample signal(s) by providing a list of start, stop, and increment values. For negative value, enclose them withing double quotes and add a space
                        at the beginning.Example: --resample " -0.1" 10.0 0.1
  --rescale RESCALE [RESCALE ...]
                        Rescale time dimension of trees to ensure that all of are in same units. Especially important if resample is used. Provide a rescaling factor to be
                        multiplied by time axis for each tree provides in trees option.Example: --resample " -0.1" 10.0 0.1
  -o, --out_filename OUT_FILENAME
                        Output filename for saving data in file. Default is None. in which case it does not save files.
  --reread_data         Will overwrite on existing data for corresponding data entries in out_file. Default behavior is to skip readingpointnames whose data is present.
  -f, --force_full_data_read
                        If resample fails, full data read will be attempted without resampling. This is useful in cases where the time axis is stored in other than dim0
                        data field.
  -c, --config CONFIG   Configuration file containing shot_numbers, trees, point_names, server, and other settings. If provided, corresponding command line arguments are
                        take precedence over arguments provided in configuration file.
  --configTemplate      If provided, configuration templates will be copied to current directory. All other arguments will be ignored.
```

You can also search shots using `search_shots`:
```
% search_shots -h
usage: search_shots [-h] [-c SEARCH_CONFIG] [-s SERVER] [-o OUT_FILENAME] [-x PROXY_SERVER] [--configTemplate]

Search MDSPlus server for provided search criteria and return a list of shots

options:
  -h, --help            show this help message and exit
  -c, --search_config SEARCH_CONFIG
                        Configuration file containing search criteria.
  -s, --server SERVER   Server address. Default is None (read from search_config).
  -o, --out_filename OUT_FILENAME
                        Output filename for saving selected shot numbers. Default is None in which case it looks for the value in search_config otherwise the selected
                        shots are simply printed out.
  -x, --proxy_server PROXY_SERVER
                        Proxy server to use to tunnel through to the server. If provided, the username part from server definition will be used to ssh into the proxy
                        server from where it assumed that you have access to the MDSplus server. If the username for proxy-server is different, add it as a prefix here
                        with @. Default is None
  --configTemplate      If provided, configuration templates will be copied to current directory. All other arguments will be ignored.
```

Again, using `--configTemplate` option would locally copy D3D and KSTAR config files for you and from there it is self-explaintory on how to use them.

Note, that if you are outside the network from where MDSplus server can be queries, you can provide ssh details of a proxy server or the gateway node from where you can access the MDSplus serve. See the template files for examples.

For queries, contanct Anchal Gupta (guptaa@fusion.gat.com). If you face any issues or have feature requests, please submit them at the [issue tracker](https://github.com/anchal-physics/mdsh5/issues).

## Recommended ssh key configurations

It would be very useful if you can access the proxy server (or gateway node) without password. For setting that up, do:

### Create ssh key pair if you donot have it already
```
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```

### Copy the public key to Gateway node
```
ssh-copy-id remote_username@GatewayNodeAddress -i path_to_creates_ssh_id_file
```
This step will prompt you for password of the Gateway node. Once this step is completed,
you should be able to ssh into the gateway node without need of password using:
```
ssh remote_username@GatewayNodeAddress -p port_number
```

### Add gateway to ssh config for ease (Optional)
```
Host <GatewayShortName> <GatewayNodeAddress>
  Hostname <GatewayNodeAddress>
  IdentityFile <path_to_creates_ssh_id_file>
  User <your_username>
  Port <required_port_if_different_from_22>
```
