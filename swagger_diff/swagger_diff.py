import json
import argparse
from swagger_parser import SwaggerParser


class Diff(object):
    new_parsed = None
    old_parsed = None

    def __init__(self, new, old):
        self.new_parsed = new
        self.old_parsed = old


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


def diff(config: Config):
    parsed_new = SwaggerParser(swagger_path=config.new_spec)
    parsed_old = SwaggerParser(swagger_path=config.old_spec)
    return Diff(parsed_new, parsed_old)


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
    processed_diff = diff(loaded_config)

    with open('data.txt', 'w') as outfile:
        json.dump(processed_diff, outfile)




