from collections import OrderedDict
import re

from django.core.management.utils import parse_apps_and_model_labels
from django.apps import apps
from django.core import serializers
from django.db import models
from django.core.management.base import CommandError

from faker import Faker
fake = Faker()


def get_models(*app_labels, excludes):
    excluded_models, excluded_apps = parse_apps_and_model_labels(excludes)
    if not app_labels:
        app_list = OrderedDict.fromkeys(
            app_config for app_config in apps.get_app_configs()
            if app_config.models_module is not None and app_config not in excluded_apps
        )
    else:
        app_list = OrderedDict()
        for label in app_labels:
            try:
                app_label, model_label = label.split('.')
                try:
                    app_config = apps.get_app_config(app_label)
                except LookupError as e:
                    raise CommandError(str(e))
                if app_config.models_module is None or app_config in excluded_apps:
                    continue
                try:
                    model = app_config.get_model(model_label)
                except LookupError:
                    raise CommandError("Unknown model: %s.%s" % (app_label, model_label))

                app_list_value = app_list.setdefault(app_config, [])

                # We may have previously seen a "all-models" request for
                # this app (no model qualifier was given). In this case
                # there is no need adding specific models to the list.
                if app_list_value is not None:
                    if model not in app_list_value:
                        app_list_value.append(model)
            except ValueError:
                # This is just an app - no model qualifier
                app_label = label
                try:
                    app_config = apps.get_app_config(app_label)
                except LookupError as e:
                    raise CommandError(str(e))
                if app_config.models_module is None or app_config in excluded_apps:
                    continue
                app_list[app_config] = None
    models = serializers.sort_dependencies(app_list.items())
    return [m for m in models if m not in excluded_models]


def get_fake_value(field):
    if field.__class__ == models.AutoField:
        return fake.random_digit()
    if field.__class__ == models.CharField:
        if field.choices:
            return fake.random_choices(field.choices, 1)[0][0]
        if re.match(r".*city.*", field.attname, re.IGNORECASE):
            return fake.city()
        if re.match(r".*phone.*", field.attname, re.IGNORECASE):
            return str(fake.random_number(digits=10, fix_len=True))
        if re.match(r".*pin\_?code.*", field.attname, re.IGNORECASE):
            return fake.zipcode()
        if re.match(r".*name.*", field.attname, re.IGNORECASE):
            return fake.first_name()
        if re.search(r".*address.*", field.attname, re.IGNORECASE):
            return fake.address()
        if re.match(r".*email.*", field.attname, re.IGNORECASE):
            return fake.ascii_safe_email()
        return "".join(fake.random_letters(length=min(field.max_length, 10)))
    if field.__class__ == models.TextField:
        if re.search(r".*address.*", field.attname, re.IGNORECASE):
            return fake.address()
        return fake.text()
    if field.__class__ == models.EmailField:
        return fake.ascii_safe_email()
    if field.__class__ == models.UUIDField:
        return fake.uuid4()
    if field.__class__ in [models.IntegerField, models.BigIntegerField, models.PositiveIntegerField]:
        return fake.random_number()
    if field.__class__ in [models.SmallIntegerField, models.PositiveSmallIntegerField]:
        if field.choices:
            return fake.random_choices(field.choices, 1)[0][0]
        return fake.random_digit()
    if field.__class__ == models.FloatField:
        return fake.pyfloat(positive=True)
    if field.__class__ == models.DecimalField:
        return str(fake.pydecimal(positive=True))
    if field.__class__ == models.DateField:
        return str(fake.date_between(start_date="-1y"))
    if field.__class__ == models.DateTimeField:
        return str(fake.date_time_between(start_date="-1y"))
    if field.__class__ == models.BooleanField:
        return fake.boolean()
    if field.__class__ == models.URLField:
        return fake.url()
    if field.__class__ == models.IPAddressField:
        return fake.ipv4()
    if field.__class__ == models.ImageField:
        return fake.image_url()
    if field.__class__ in [models.ForeignKey, models.OneToOneField]:
        rel_field = field.foreign_related_fields[0]
        return get_fake_value(rel_field)


def generate_model_fixture(model, limit):
    """
    [
        {
            "fields": {
                "field_name":<fake_value>
            },
            "model":""
        }
    ]
    """
    result = []
    for ctr in range(limit):
        fixture = {}
        fields = {}
        for f in model._meta.fields:
            fields[f.attname] = get_fake_value(f)
        fixture["fields"] = fields
        fixture["model"] = "{}.{}".format(model._meta.app_label, model._meta.model_name)
        result.append(fixture)
    return result