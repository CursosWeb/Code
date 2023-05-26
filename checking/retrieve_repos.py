#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program to retrieve practices
Uses a CSV file with the list of students retrieved from Aulavirtual filtering by Student role:
"Nombre","Apellido(s)","Dirección de correo"

Example of how to run the script:
retrieve_repos.py --practice :all: --students ist-saro-2022.csv --cloning_dir ../../retrieved-2022

It will return always the folloing files:
- "not_founds.txt": file with those students with problems finding their fork
- "<students>_enriched.csv": csv enriched with the lab username and gitlab username (if found) of the students
"""

import argparse
import csv
import json
import os
import subprocess
import urllib.request
import re

from shutil import copyfile
from distutils.dir_util import copy_tree
from unicodedata import normalize

from git.repo.base import Repo
from git.exc import GitCommandError


def add_api (practices):
    for number, practice in practices.items():
        practice['repo_api'] = practice['repo'].replace('/', '%2F')

practices = {
    "01-calculadora": {
        'repo': 'cursosweb/2022-2023/calculadora',
        'repo_api': 'cursosweb%2F2022-2023%2Fcalculadora'
    },
    "02-descargaweb": {
        'repo': 'cursosweb/2022-2023/descarga-documentos-web',
        'repo_api': 'cursosweb%2F2022-2023%2Fdescarga-documentos-web',
    },
    "03-descargawebmodulos": {
        'repo': 'cursosweb/2022-2023/descarga-documentos-web-modulos',
        'repo_api': 'cursosweb%2F2022-2023%2Fddescarga-documentos-web-modulos',
    },
    "04-redir": {
        'repo': 'cursosweb/2022-2023/aplicacion-redirectora',
        'repo_api': 'cursosweb%2F2022-2023%2Faplicacion-redirectora',
    },
    # Solo para SAT/SARO
    "05-contentapp": {
        'repo': 'cursosweb/2022-2023/contentapp',
        'repo_api': 'cursosweb%2F2022-2023%2Fcontentapp',
    },
    "06-contentpostapp": {
        'repo': 'cursosweb/2022-2023/contentpostapp',
        'repo_api': 'cursosweb%2F2022-2023%2Fcontentpostapp',
    },
    "07-cms-put": {
        'repo': 'cursosweb/2022-2023/django-cms-put',
        'repo_api': 'cursosweb%2F2022-2023%django-cms-put',
    },
    "minip1": {
        'repo': 'cursosweb/2022-2023/mini-1-acortadora',
        'repo_api': 'cursosweb%2F2022-2023%2Fmini-1-acortadora',
    },
    "minip2": {
        'repo': 'cursosweb/2022-2023/mini-2-acortadora',
        'repo_api': 'cursosweb%2F2022-2023%2Fmini-2-acortadora',
    },
    "final": {
        'repo': 'cursosweb/2022-2023/final-decharla',
        'repo_api': 'cursosweb%2F2022-2023%2Ffinal-decharla',
    }

}

add_api(practices)


def get_token() -> str:
    try:
        with open('token', 'r') as token_file:
            token: str = token_file.readline().rstrip()
            return token
    except FileNotFoundError:
        return ''


def get_forks(repo: str, token: str = ''):
    req_headers = {}
    if token != '':
        req_headers['PRIVATE-TOKEN'] = token
    # Pages are ints starting in 1, so these are just initialization values
    this_page, total_pages = 1, None
    forks = []
    while (total_pages is None) or (this_page <= total_pages):
        url = f"https://gitlab.etsit.urjc.es/api/v4/projects/{repo}/forks?per_page=50&page={this_page}"
        req = urllib.request.Request(url=url, headers=req_headers)
        with urllib.request.urlopen(req) as response:
            contents = response.read()
            resp_headers = response.info()
            total_pages = int(resp_headers['x-total-pages'])
            this_page += 1
            contents_str = contents.decode('utf8')
            forks = forks + json.loads(contents_str)
    return forks


def clone(url, dir, token=''):
#    auth_url = url.replace('https://', f"https://Api Read Access:{token}@", 1)
    auth_url = url.replace('https://', f"https://jesus.gonzalez.barahona:{token}@", 1)
    print("Cloning:", dir, auth_url)
    try:
        Repo.clone_from(auth_url, dir)
    except GitCommandError as err:
        print(f"Error: git error {err}")


def read_csv(file):
    students = {}
    file_modified = False
    with open(file, 'r', newline='', encoding="utf-8") as cvsfile:
        rows = csv.DictReader(cvsfile)
        for row in rows:
            # We have the infor about the name, surname and email, we get the email as uid
            usuariocorreo = row['Dirección de correo'].split("@")[0]

            students[usuariocorreo] = {
                'usuario_correo_completo': row['Dirección de correo'],
                'usuario_correo': usuariocorreo,
                'apellidos': row['Apellido(s)'],
            }

            # Sometimes Nombre in the csv of aulavirtual is not well displayed
            if '\ufeffNombre' in row:
                students[usuariocorreo]['nombre'] = row['\ufeffNombre']
                students[usuariocorreo]['nombre_apellidos'] = "{} {}".format(row['\ufeffNombre'], row['Apellido(s)']).lower()
                students[usuariocorreo]['nombre_apellidos_formatted'] = remove_tildes(
                    students[usuariocorreo]['nombre_apellidos'])
            elif 'Nombre' in row:
                students[usuariocorreo]['nombre'] = row['Nombre']
                students[usuariocorreo]['nombre_apellidos'] = "{} {}".format(row['Nombre'], row['Apellido(s)']).lower()
                students[usuariocorreo]['nombre_apellidos_formatted'] = remove_tildes(
                    students[usuariocorreo]['nombre_apellidos'])



            # Sometimes the gitlab username is the lab username, so let's retrieve the laboratory usernames
            if 'Usuario Lab' in row:
                students[usuariocorreo]['usuario_lab'] = row["Usuario Lab"]
            else:
                usuariolab = get_lab_username(students[usuariocorreo])
                students[usuariocorreo]['usuario_lab'] = usuariolab
                file_modified = True

            if 'Usuario Gitlab' in row and row['Usuario Gitlab']:
                students[usuariocorreo]['usuario_gitlab'] = row["Usuario Gitlab"]
                students[usuariocorreo]['foundingitlab'] = True

    if file_modified:
        print("Students file modified, writting new version")
        export_csv_enriched(file, students)
    return students


def get_lab_username(student):
    # Command finger in etsit labs, removing tildes, extra spaces and "ñ"
    stdoutfinger = os.popen("finger {} | grep 'Name: '".format(student['nombre_apellidos_formatted'])).read().split("\n")
    for entry in stdoutfinger:
        alumno_name = entry.split("\t\t\tName: ")[-1].lower().replace(" ", "")
        if alumno_name in student['nombre_apellidos_formatted'].replace(" ", ""):
            # Return the lab username
            return entry.split("\n")[0].split("\t\t\tName: ")[0].split("Login: ")[-1].strip()

    return ""


def remove_tildes(name):
    # -> NFD y eliminar diacríticos
    name = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", name), 0, re.I
    )

    # -> NFC
    name = normalize('NFC', name)

    # ñ -> n
    name = name.replace("ñ", "n")

    return name


def run_tests(dir: str, solved_dir: str, silent: bool=False):
    """Run tests for this directory"""
    print("Running tests for", dir)
    # Copy tests to evaltests in analyzed directory
    tests_dir = os.path.join(solved_dir, 'tests')
    copy_tree(tests_dir, os.path.join(dir, 'evaltests'))
    # Copy check.py to analyzed directory
    copyfile(os.path.join(solved_dir, 'check.py'), os.path.join(dir, 'check.py'))
    test_call = ['python3', 'check.py', '--silent', '--testsdir', 'evaltests']
    if silent:
        test_call.append('--silent')
        stderr = subprocess.PIPE
    else:
        stderr = None
    result = subprocess.run(test_call,
                            cwd=dir, stdout=subprocess.PIPE,
                            stderr=stderr, text=True)
#    print("Tests result:", result.stdout.splitlines()[-1])
    print("Tests result:", result.stdout)
    if result.returncode == 0:
        print(f"Running tests OK: {dir}")
        return True
    else:
        print(f"Running tests Error: {dir}")
        return False


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate practices.')
    parser.add_argument('--silent', action='store_true',
                        help="silent output, only summary is written")
    parser.add_argument('--no_clone', action='store_true',
                        help="don't clone repos, assume repos were already cloned")
    parser.add_argument('--students', required=True,
                        help="name of csv file with students, exported from Moodle")
    parser.add_argument('--practice', default=list(practices.keys())[-1],
                        help="practice number (:all: to retrieve all practices, default: last practice")
    parser.add_argument('--cloning_dir', default='retrieved',
                        help="directory for cloning retrieved practices")
    parser.add_argument('--testing_dir', default='/tmp/p',
                        help="directory for tests")
    args = parser.parse_args()
    return(args)


def retrieve_practice(practice_id, cloning_dir, token):
    practice = practices[practice_id]
    forks = get_forks(repo=practice['repo_api'], token=token)
    repos_found = 0
    #    print(forks)

    students = read_csv(args.students)
    file_modified = False

    for fork in forks:
        # Each fork is a repo to consider
        fork_data = {
            'url': fork['http_url_to_repo'],
            'name': fork['namespace']['name'],
            'path': fork['namespace']['path']
        }

        for student_data in students.values():
            # Check in order to match the gitlab username with the student lab/correo
            if "foundingitlab" not in student_data:
                student_data['foundingitlab'] = False
                if 'usuario_gitlab' not in student_data:
                    student_data['usuario_gitlab'] = ""

            if student_data['usuario_correo'] == fork_data['path']:
                student_data['foundingitlab'] = True
                if 'usuario_gitlab' not in student_data or student_data['usuario_gitlab'] != fork_data['path']:
                    student_data['usuario_gitlab'] = fork_data['path']
                    file_modified = True
            elif student_data['usuario_lab'] == fork_data['path']:
                student_data['foundingitlab'] = True
                if 'usuario_gitlab' not in student_data or student_data['usuario_gitlab'] != fork_data['path']:
                    student_data['usuario_gitlab'] = fork_data['path']
                    file_modified = True
            else:
                continue

            # If I found the match between gitlab username and student, clone the repo
            if student_data['foundingitlab']:
                # We're only interested in repos in the list of students
                print(f"Found: {fork_data['path']}")
                repos_found += 1
                if not args.no_clone:
                    dir = os.path.join(cloning_dir, args.students.split(".csv")[0], practice_id, fork_data['path'])
                    try:
                        clone(fork_data['url'], dir, token)
                    except GitCommandError:
                        pass

        # # Run tests in the cloned repo
        # print("About to run tests:", os.path.join(testing_dir, fork_data['path']))
        # run_tests(dir=os.path.join(testing_dir, fork_data['path']),
        #           solved_dir=practice['solved_dir'],
        #           silent=args.silent)
    print(f"Total forks: {len(forks)}, repos found: {repos_found}, students in the csv: {len(students)}")

    if file_modified:
        print("Students file modified, writting new version")
        export_csv_enriched(args.students, students)
    return students


def export_not_founds(students):
    errorlog = "not_founds.txt"
    with open(errorlog, "w") as f:
        for student in students.values():
            # Error, no ha sido posible clonar el repositorio
            if not student["foundingitlab"]:
                f.write(f"No se ha encontrado el repositorio del estudiante "
                        f"{student['nombre']} {student['apellidos']}"
                        f" con login de correo {student['usuario_correo']} y usuario de laboratorio "
                        f"{student['usuario_lab']}\n")
            # Usuario de lab no encontrado
            if not student["usuario_lab"]:
                f.write(f"No se ha encontrado el usuario de laboratorio del estudiante "
                        f"{student['nombre']} {student['apellidos']}"
                        f" con login de correo {student['usuario_correo']}\n")


def export_csv_enriched(studentsfile, students):
    with open(f'{studentsfile.split(".csv")[0]}_enriched.csv', 'w', newline='') as csvenriched:
        csvwriter = csv.writer(csvenriched)
        csvwriter.writerow(["Nombre", "Apellido(s)", "Dirección de correo", "Usuario Lab", "Usuario Gitlab"])
        for student in students.values():
            # Enriquecer con los datos obtenidos
            csvwriter.writerow([student["nombre"],
                                student["apellidos"],
                                student["usuario_correo_completo"],
                                student.get("usuario_lab", ""),
                                student.get("usuario_gitlab", "")])


if __name__ == "__main__":
    args = parse_args()
    testing_dir = args.testing_dir
    cloning_dir = args.cloning_dir
    token: str = get_token()

    if args.practice == ':all:':
        practice_ids = practices.keys()
    else:
        practice_ids = [args.practice]
    for practice_id in practice_ids:
        print(f"Retrieving practice {practice_id}")
        students = retrieve_practice(practice_id, cloning_dir, token)
        export_not_founds(students)
#        export_csv_enriched(args.students, students)
