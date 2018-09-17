import os
import re


def fully_qualified_to_file(fully_qualified, extension=''):
    return fully_qualified.replace('.', os.sep) + extension


def target_to_dir(fully_qualified, target_id):
    path = fully_qualified_to_file(fully_qualified).split(os.sep)

    if len(path) > 0:
        path[-1] = '{0}-{1}'.format(target_id, path[-1])

    return os.sep.join(path)


def gen_export_dir(mutants_path, java_class, class_method, line_number,
                   target_id):
    return os.path.join(mutants_path, '{0}-{1}-{2}'
                        .format(target_to_dir(java_class, target_id),
                                class_method.replace(',', '_'), line_number))


def sort_files(files):
    return sorted(files, key=lambda x: (int(0 if re.sub(r'[^0-9]+', '', x) == ''
                                            else re.sub(r'[^0-9]+', '', x)), x))


def generate_classpath(paths):
    return os.pathsep.join(paths)


def get_class_files(path, package='', ext='.class'):
    files = []

    for node in os.listdir(path):
        node_path = os.path.join(path, node)
        if os.path.isdir(node_path):
            package = os.path.join(package, node)
            files += get_class_files(node_path, package, ext)
        elif os.path.splitext(node_path)[1] == ext:
            files.append(os.path.join(package, node))

    return files