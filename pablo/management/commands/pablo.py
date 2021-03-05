import json

from django.core.management.base import BaseCommand
from pablo.utils import get_models, generate_model_fixture


class Command(BaseCommand):
    help = (
        "Generate (sometimes)meaningful fixtures for your django project"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "args", metavar="app_label[.ModelName]", nargs="*",
            help="Restricts fixture to the specified app_label or app_label.ModelName",
        )
        parser.add_argument(
            "-l", "--limit", type=int, default=1,
            help="Limit number of fixtures generated for a model"
        )
        parser.add_argument(
            "-e", "--exclude", action="append", default=[],
            help="An app_label or app_label.ModelName to exclude "
                 "(use multiple --exclude to exclude multiple apps/models)",
        )

    def handle(self, *app_labels, **options):
        excludes = options['exclude']
        limit = options["limit"]
        debug = options["verbosity"]
        _models = get_models(*app_labels, excludes=excludes)
        generated_fixtures = []
        for model in _models:
            model_name = "{}.{}".format(model._meta.app_label, model._meta.model_name)
            fixture = generate_model_fixture(model, limit)
            if debug:
                print("...............................................................\n")
                print("Fixture for model {}\n\n".format(model_name))
            fixture_dump = json.dumps(fixture, sort_keys=True, indent=4)
            if debug:
                print(fixture_dump)
                print("\n\nSaving fixture at {}.json".format(model_name))
                print("...............................................................")
            with open("{}.json".format(model_name), "w") as f:
                f.write(fixture_dump)
                generated_fixtures.append("{}.json".format(model_name))
        print("\nFixtures saved at")
        print("\n".join(generated_fixtures))









