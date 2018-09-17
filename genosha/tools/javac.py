import os
import shutil
import subprocess

from genosha.utils import get_class_files

JDK_DIR = os.sep.join(['', 'opt', 'tools', 'major'])
JAVAC = os.path.join(JDK_DIR, os.sep.join(['bin', 'javac']))


def compile(classpath, source_dir, files, dest_dir=None):
    command = [JAVAC, '-encoding', 'UTF-8', '-cp', classpath]

    if dest_dir is not None:
        command.append('-d')
        command.append(dest_dir)

    for input_file in files:
        command.append(os.path.join(source_dir, input_file))

    try:
        return subprocess.call(command, shell=False, timeout=(60 * 10))
    except subprocess.TimeoutExpired:
        print("# ERROR: Compiling timed out.")


def compile_all(classpath, source_dir, classes_dir):
    full_qualified_java = get_class_files(source_dir, ext='.java')

    if os.path.exists(classes_dir):
        shutil.rmtree(classes_dir)

    os.makedirs(classes_dir)

    compile(classpath=classpath, source_dir=source_dir,
            files=full_qualified_java, dest_dir=classes_dir)
