import os
import json

from hunor.main import Hunor
from hunor.args import Options

from genosha.utils import gen_export_dir


def main():

    config_file = '/home/marcioaug/PycharmProjects/genosha/examples/relational/relational/config.json'
    mutants_dir = '/home/marcioaug/PycharmProjects/genosha/examples/relational/mutants'

    with open(config_file) as f:
        config = json.loads(f.read())

    for target in config['targets']:
        run_hunor(
            config_file=config_file,
            mutants=gen_export_dir(
                mutants_path=mutants_dir,
                java_class=target['class'],
                class_method=target['method'],
                line_number=target['line'],
                target_id=target['id']),
            sut_class=target['class'],
            mutation_tool='major'
        )


def run_hunor(config_file, mutants, sut_class, mutation_tool):
    options = Options(
        maven_home='/home/marcioaug/Tools/maven/current',
        java_home='/home/marcioaug/Tools/java/jdk1.8.0_181',
        config_file=config_file,
        mutants=mutants,
        sut_class=sut_class,
        mutation_tool=mutation_tool,
        is_randoop_disabled=True,
        output=os.path.join(mutants, 'hunor-output')
    )

    return Hunor(options=options).run()


if __name__ == '__main__':
    main()
