import os
import subprocess
import shutil

from genosha.utils import fully_qualified_to_file, generate_classpath
from genosha.utils import sort_files, gen_export_dir
from genosha.tools import javac


MAJOR_DIR = os.sep.join(['', 'opt', 'tools', 'major'])
MAJOR = os.path.join(MAJOR_DIR, os.sep.join(['bin', 'javac']))
MMLC = os.path.join(MAJOR_DIR, os.sep.join(['bin', 'mmlc']))


def _define_operators(java_class, class_method, subject_path, export_dir,
                      operators):
    x_mutator_sep = ':'

    if operators.endswith('.mml'):
        x_mutator_sep = '='

        with open(os.path.join(subject_path, operators), 'r') as original:
            with open(os.path.join(export_dir, operators), 'w') as new:
                new.writelines(original.readlines())
                new.write('\n\ntargetOp<"{0}::{1}">;'
                          .format(java_class, class_method))
                new.close()
            original.close()

        subprocess.call([MMLC, os.path.join(export_dir, operators)],
                        shell=False, cwd=export_dir)

        operators = os.path.join(export_dir, operators + '.bin')

    return x_mutator_sep + operators


def _exec_major(java_file, classpath, export_dir, mutants_path,
                operators='ROR'):

    dest_dir = os.path.join(mutants_path, 'target', 'classes')

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    command = [
        MAJOR,
        '-encoding', 'UTF-8',
        '-XMutator' + operators,
        '-J-Dmajor.export.context=true',
        '-J-Dmajor.export.mutants=true',
        '-J-Dmajor.export.directory=' + export_dir,
        '-cp', classpath,
        '-d', dest_dir,
        java_file
    ]

    try:
        return subprocess.call(command, shell=False, cwd=export_dir,
                               timeout=(60 * 10))
    except subprocess.TimeoutExpired:
        print("# ERROR: Major generate timed out.")


def generate(target_id, subject_path, source_path, java_class, class_method,
             line_number, classes_path, mutants_path, operators):

    java_file = os.path.join(source_path,
                             fully_qualified_to_file(java_class, '.java'))
    classpath = generate_classpath([classes_path])
    export_dir = gen_export_dir(mutants_path, java_class, class_method,
                                line_number, target_id)

    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)

    os.makedirs(export_dir)

    operators = _define_operators(
        java_class=java_class,
        class_method=class_method,
        subject_path=subject_path,
        export_dir=export_dir,
        operators=operators,
    )

    _exec_major(
        java_file=java_file,
        classpath=classpath,
        export_dir=export_dir,
        mutants_path=mutants_path,
        operators=operators
    )

    _clean_mutants(export_dir, line_number)

    return export_dir


def _clean_mutants(export_dir, line_number):
    log_file = os.sep.join([export_dir, 'mutants.log'])

    with open(log_file) as log:
        for line in log.readlines():
            data = line.split(':')
            if data[5] != str(line_number):
                shutil.rmtree(os.path.join(export_dir, str(data[0])))


def read_log(export_dir, method, target, exclude):
    mutants_data = {}

    log_file = os.sep.join([export_dir, 'mutants.log'])

    line_number = target['line']
    statement = target['statement'].replace(' ', '')

    with open(log_file) as log:
        for line in log.readlines():
            data = line.split(':')
            if (data[4] == method and data[5] == str(line_number)
                    and data[0] not in exclude
                    and (data[6].split('|==>')[0].replace(' ', '')
                         == statement)):
                mutants_data[int(data[0])] = {
                    'id': int(data[0]),
                    'operator': data[1],
                    'original_symbol': data[2],
                    'replacement_symbol': data[3],
                    'method': data[4],
                    'line_number': int(data[5]),
                    'transformation': data[6],
                    'subsume': set(),
                    'subsumed_by': set(),
                    'brothers': set(),
                    'path': os.path.join(export_dir, str(data[0])),
                    'is_brother': False
                }
        log.close()

    return mutants_data


def compile_mutants(java_class, classpath, export_dir):
    mutants_compile = []
    mutants_not_compile = []
    java_file = fully_qualified_to_file(java_class, '.java')

    for mutant in sort_files(os.listdir(export_dir)):
        mutant_dir = os.path.join(export_dir, mutant)
        file = os.path.join(mutant_dir, java_file)

        if os.path.isdir(mutant_dir):
            if javac.compile(classpath, mutant_dir, [file]) == 0:
                mutants_compile.append(mutant)
            else:
                mutants_not_compile.append(mutant)

    return mutants_compile, mutants_not_compile

