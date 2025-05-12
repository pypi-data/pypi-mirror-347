# NekUpload

**NekUpload** is a Python package designed to streamline the upload and data management process of Nektar++ datasets to AE Datastore. It automates the validation of simulation datasets to ensure consistency and completeness. Furthermore, it extracts relevant parameters embedded within the files, enriching database records with valuable metadata. This aligns with the FAIR principles (Findable, Accessible, Interoperable, Reusable), making your data accessible, understandable and compatible with other NekRDM tools.

# Installation

There are two installation methods. With pip:

```bash
python3 -m pip install NekUpload
```

Or build from source:

```bash
git clone https://gitlab.nektar.info/nektar/NekUpload.git

#if just need the package as a user
python3 -m pip install .
#if you want development tools too
python3 -m pip install .[dev]
```

# User Guide

User guide can be found at https://nekupload.readthedocs.io/en/latest/.