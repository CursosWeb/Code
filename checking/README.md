# Scripts for checking practices

## retrieve_repos.py

Retrieve repositories from the EIF GitLab instance which are forked from a template repository, and are in a list of students.

For each practice, there is a dictionary in `retrieve_repos.py`, `practices`, specifying the name of the template repository, and the name of the repository in the GitLab API.

For each subject, there is a CSV file **exported from the Aulavirtual subject** with the role **Estudiante** filtered in. 

```
"Nombre","Apellido(s)","Dirección de correo"
```

Cloned repositories, by default, go to directory retrieved/<students_file_name>/id (being `id` the identified of  the practice in the `practices` repository).

To run the script, a file `token` with a valid EIF GitLub token should be in the directory from which the script is run.

**IMPORTANT**: If the lab username of the students are not available, this script should be executed in a **lab.eif machine** since it executes the `finger` command for matching the URJC username to the EIF lab username. See __Returned files section__ for further information.

### Returned files: 

By default, the script will return two useful files:
- `not_founds.txt`: file with those students with problems finding their fork
- `<students_filename>_enriched.csv`: csv enriched with the lab username and gitlab username (if found) of the students. And this csv could be used in the next executions for retrieving the practises without being in a lab etsit machine.

### Example

```commandline
python3 retrieve_repos.py --students isam-ltaw-2026.csv --practice servidor-carrito --cloning_dir ../../retrieved-2026
```