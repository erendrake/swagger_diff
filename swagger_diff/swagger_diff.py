import json
import argparse
from swagger_parser import SwaggerParser


class Diff(object):
    new_parsed = None
    old_parsed = None

    added_definitions = []
    removed_definitions = []
    added_operations = []
    removed_operations = []
    added_paths = []
    removed_paths = []

    def __init__(self, new, old):
        self.new_parsed = new
        self.old_parsed = old

    @classmethod
    def is_compatible(cls):
        return len(cls.removed_definitions) + len(cls.removed_paths) + len(cls.removed_operations) == 0

    @classmethod
    def from_config(cls, config):
        parsed_new = SwaggerParser(swagger_path=config.new_spec)
        parsed_old = SwaggerParser(swagger_path=config.old_spec)

        cls.old_parsed = parsed_old
        cls.new_parsed = parsed_new
        cls.generate()
        return cls

    @classmethod
    def generate(cls):
        cls.find_changed_operations()
        cls.find_changed_paths()
        cls.find_changed_definitions()
        return cls

    @classmethod
    def find_changed_definitions(cls):
        definitions_in_new = set(cls.new_parsed.definitions_example)
        definitions_in_old = set(cls.old_parsed.definitions_example)
        cls.added_definitions = list(definitions_in_new - definitions_in_old)
        cls.removed_definitions = list(definitions_in_old - definitions_in_new)

    @classmethod
    def find_changed_paths(cls):
        paths_in_new = set(cls.new_parsed.paths)
        paths_in_old = set(cls.old_parsed.paths)
        cls.added_paths = list(paths_in_new - paths_in_old)
        cls.removed_paths = list(paths_in_old - paths_in_new)

    @classmethod
    def find_changed_operations(cls):
        operations_in_new = set(cls.new_parsed.operation)
        operations_in_old = set(cls.old_parsed.operation)
        cls.added_operations = list(operations_in_new - operations_in_old)
        cls.removed_operations = list(operations_in_old - operations_in_new)


class Config(object):
    new_spec = None
    old_spec = None
    output = None

    @classmethod
    def from_json(cls, filename):
        config = Config()
        raw_config = json.loads(filename)
        config.new_spec = raw_config['new_spec']
        config.old_spec = raw_config['old_spec']
        return config


def load_config(args):
    if args.config is not None:
        config = Config.from_json(args.config)
    else:
        config = Config()

    if args.new is not None:
        config.new_spec = args.new

    if args.old is not None:
        config.old_spec = args.old

    if args.output is not None:
        config.output = args.output

    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='JSON config file')
    parser.add_argument('--new', help='after swagger spec')
    parser.add_argument('--old', help='before swagger spec')
    parser.add_argument('--output', help='where do you want the diff?')
    parsed_args, leftovers = parser.parse_known_args()
    loaded_config = load_config(parsed_args)
    processed_diff = Diff.from_config(loaded_config)

    print(processed_diff.is_compatible())





