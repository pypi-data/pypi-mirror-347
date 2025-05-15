Welcome!

This is a python repository to generate HCR v3.0 probes for in situ hybridization visualization of mRNA in Anopheles Gambiae.
The module allows for quick and easy design of probe pairs for the Hybridization Chain Reaction approach (Choi et al. Development 2018.)

You can install the HCR probe design tool to first create a virtual environment using conda:

```
conda create --name HCR python=3.10.0
conda activate HCR
```

You can then use pip to install the HCR probe design tool:

```
pip install AGambiaeHCRdesign
```



Dependencies: 
BLAST+
Install BLAST+ by downloading executable from https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/

The A. Gambiae PEST genome data is available to download at https://vectorbase.org/vectorbase/app/downloads/Current_Release/AgambiaePEST/fasta/data
This dataset should be formatted into a BLAST database.

To build a BLAST database, use the BLAST+ 'makeblastdb' command. 
Detailed instructions are available on the NIH website at https://www.ncbi.nlm.nih.gov/books/NBK569841/
