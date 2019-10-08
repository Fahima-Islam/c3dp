## Manual conda build

Assuming our conda installation is in `/sw/conda/anaconda3` with python 3.6,
we build the package and upload to the neutrons organization by issuing the
following commands in the terminal.

```
conda-build c3dp/condabld
anaconda upload --user neutrons /sw/conda/anaconda3/conda-bld/linux-64/c3dp-v0.1.0-py36h39e3cac_0.tar.bz2
```
