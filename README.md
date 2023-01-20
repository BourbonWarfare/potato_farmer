# Potato Farmer

Manages `potato_field` and `potato_plants`. Main way to administrate containers.

## Setup

### Dependencies

There are several dependencies required for the development and deployment of this project.
The first is Docker Engine and Docker Compose. The second is Python3.
The following list links to the installation instructions for each of these:

* [Docker Engine installation instructions.](https://docs.docker.com/engine/install/)
* [Docker Compose installation instructions.](https://docs.docker.com/compose/install/)
* [Python3 installation instructions.](https://www.python.org/downloads/)

### Sub-repository management

The tool `setup.py` can be used to clone (or symlink) project repositories for deployment.

For instance, the following command will clone the `potato_plant_dashboard` and `potato_plant_missions` 
repositories (hosted in the BourbonWarfare organization) into the project root:
```bash
python3 setup.py add plant_dashboard plant_missions
```
The resulting repositories would then be cloned into `potato_field/` and are symlinked into the
`potato/` directory.

<!-- TODO: add demonstration of `link` command. -->
