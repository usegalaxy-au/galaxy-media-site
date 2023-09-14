## **How to use the international Vertebrate Genome Project workflows in Galaxy Australia**

Anna Syme

## What are the VGP workflows?

* These are workflows for genome assembly, developed for the Vertebrate Genome Project
* Website: https://vertebrategenomesproject.org/
* Data at Genome Ark  https://vgp.github.io/genomeark/
* Paper: Rhie, A., McCarthy, S.A., Fedrigo, O. et al. Towards complete and error-free genome assemblies of all vertebrate species. Nature 592, 737–746 (2021). https://doi.org/10.1038/s41586-021-03451-0
* This paper covers the testing of tools and workflows. We recommend also looking at the Supplementary Information which is very informative.

## Are the VGP workflows in Galaxy Australia?

* An international team is working to create these workflows in Galaxy: for more information see [https://galaxyproject.org/projects/vgp/](https://galaxyproject.org/projects/vgp/)
* In Galaxy Australia, you can access a set of these workflows by going to the [Genome Lab](https://genome.usegalaxy.org.au/), scroll to the Genome Assembly section, click on the Workflows tab.
* The workflows to import are:
  * Assembly with PacBio HiFi data:
    * BAM to FASTQ + QC v1.0
  * Assembly with PacBio Hifi and HiC data:
    * Kmer profiling
    * Hifi assembly and HiC phasing
    * HiC scaffolding
    * Decontamination

## Can I use the VGP workflows in Galaxy Australia?

* Yes. You can run these on test data or real data. They are designed to work for vertebrate genomes where you have PacBio Hifi data and HiC data. 
* The workflows are described in Galaxy Training Network materials. 
* [VGP assembly pipeline - short version, although still with complete workflow](https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_workflow_training/tutorial.html)
* [VGP assembly pipeline - long version](https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_genome_assembly/tutorial.html)
   
## What data do I need? 

Overall, you need these inputs: 
* HiFi reads as collection
  * If HiFi data in BAM format, convert to FASTQ using the BAM to FASTQ + QC v1.0 workflow
  * then group output FASTQ files into a single collection
* HiC reads as R1 and R2

For each of the other workflows, you will need these inputs:

* WF1 Kmer profiling
  * Inputs:
    *  HiFi reads in collection
* WF4 Hifi assembly and HiC phasing
  * Inputs: 
    * HiFi reads in collection
    * HiC R1, HiC R2, 
    * from WF1: genomescope model parameters, genomescope summary, mery db
* WF8a HiC scaffolding
  * Inputs:
    * From WF4: Assembly in gfa format
    * From WF4: estimated genome size
    * HiC R1, Hi C R2
  * Settings:
    * For restriction enzymes: set correctly
    * For Input GFA: Generates the initial set of paths: set true (if using assembly from Hifiasm) 
* WF9 Decontamination
  * Inputs:
    * From WF8a: Scaffolded assembly in FASTA format
  * Settings:
    * For step "ID non-target contaminants": select Kraken 2 database : choose: Prebuilt Refseq indexes: PlusPF (Standard plus protozoa and fungi)
    * For step "blast mitochondria db": choose locally installed blast database: choose RefSeq mitochondrion

## Do I need any background knowledge before I run these workflows? 

* We recommend the Galaxy Training Network tutorials. 
* Introduction to Galaxy: https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/tutorial.html
* Assembly: https://training.galaxyproject.org/training-material/topics/assembly/tutorials/general-introduction/tutorial.html
* QC: https://training.galaxyproject.org/training-material/topics/sequence-analysis/tutorials/quality-control/tutorial.html
* VGP: https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_genome_assembly/tutorial.html
* These should be enough to get you started running the VGP workflows, but there are many additional tutorials that would also be useful. 
* As most species have never had their genome sequenced, it is not possible to guarantee existing workflows are optimal for new data. 
* It is most likely that any new genome assembly will have its own set of required workflow and analysis customisations to account for things such as ploidy and repeats. 
* Usually, an assembly workflow will need testing and customising, in concert with reading the biological domain literature. 

## What is going on in the workflows?

* The workflows are large and have many steps. 
* To better understand the workflow, look at the workflow canvas, view each tool and its settings, see how each step is connected. 
* Consider what outputs you would require and make sure it is clear where they are and what they are called. 
* For a description of many of the tools and the default parameters that have been set, see the [Galaxy tutorial for VGP workflows](https://training.galaxyproject.org/training-material/topics/assembly/tutorials/vgp_genome_assembly/tutorial.html).

## Run the workflows on test data

* Look at the outputs and see if it makes sense and all tools ran. 

## Import real data

* If you will be using real vertebrate genome data, it is likely you will need more Galaxy storage. Contact the Galaxy Australia team to discuss/request. 
* Import your real data sets into Galaxy.
* Or, to use real VGP data, go to **Upload Data: Choose remote files: Genome Ark: species** and choose a species. 
* Note: not all species have data from all Hifi and HiC sources. 
* Note that you will likely have to convert the data into the correct formats required. Alternatively, modify the workflows themselves to accept the data in the formats you have. 

## Is there anything I need to change in the workflows?

* Most likely, yes. Look at every tool and the parameters to check it suits your data and aims. 
* Examples of things that might need changing:
* Set the kmer size in the meryl tool, and make sure the setting in the Genomescope tool matches this. There is no absolute answer for what this setting should be; a common setting is 21. 
* In the Quast tool (used several times), set the lineage appropriately (e.g. eukaryote) and set as "large genome" 
* In the Busco tool (used several times), set the lineage appropriately (e.g. Vertebrata)

## Do I need to keep all of the output files from the workflow?

* No. In particular, some of the intermediate output files are very large, e.g., BAM files. You may wish to not keep these. 
* To automatically not keep these files during the workflow run: go to the workflow canvas, see the box for a tool, see the output files, and untick any files you will not need. 

## Run the workflows on real data

* Modify workflows as needed: label or tag outputs, change tool parameters, swap tools, add or delete steps. 
* For large data we would recommend testing tools and workflows on a subset of the data first.

## Where to see the outputs

* Your Galaxy history holds the outputs from the workflow run.
* Some files may be hidden - click on "show hidden" to see.
* In the top Galaxy menu, go to User: Workflow invocations to see details of the workflow run. 

## What to do if a tool or workflow fails?

* Read the error message to see if you can troubleshoot the issue. Otherwise, contact help@genome.edu.au
* If you are able to, re-run the tool or workflow in case it was a temporary connection issue. 
