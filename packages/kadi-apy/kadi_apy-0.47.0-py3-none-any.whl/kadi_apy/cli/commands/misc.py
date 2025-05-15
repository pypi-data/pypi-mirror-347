# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

import click
from xmlhelpy import Choice
from xmlhelpy import Path
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import RESOURCE_TYPES
from kadi_apy.lib.misc import _copy_records
from kadi_apy.lib.utils import _get_record_identifiers
from kadi_apy.lib.utils import append_identifier_suffix
from kadi_apy.lib.utils import get_resource_type


@kadi_apy.group()
def misc():
    """Commands for miscellaneous functionality."""


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter by title or identifier.",
    default="",
)
def get_deleted_resources(manager, **kwargs):
    """Show a list of deleted resources in the trash."""

    manager.misc.get_deleted_resources(**kwargs)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to restore.",
    param_type=Choice(RESOURCE_TYPES),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to restore.",
    required=True,
)
def restore_resource(manager, item_type, item_id):
    """Restore a resource from the trash."""

    item = get_resource_type(item_type)

    manager.misc.restore(item=item, item_id=item_id)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to purge.",
    param_type=Choice(RESOURCE_TYPES),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to purge.",
    required=True,
)
def purge_resource(manager, item_type, item_id):
    """Purge a resource from the trash."""

    item = get_resource_type(item_type)

    manager.misc.purge(item=item, item_id=item_id)


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter.",
    default="",
)
def get_licenses(manager, **kwargs):
    """Show a list available licenses."""

    manager.misc.get_licenses(**kwargs)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Show only roles of this resource.",
    param_type=Choice(["record", "collection", "template", "group"]),
)
def get_roles(manager, item_type):
    """Show a list of roles and corresponding permissions of all resources."""

    manager.misc.get_roles(item_type)


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter.",
    default="",
)
@option(
    "type",
    char="t",
    description="A resource type to limit the tags to.",
    default=None,
    param_type=Choice(["record", "collection"]),
)
def get_tags(manager, **kwargs):
    """Show a list available tags."""

    manager.misc.get_tags(**kwargs)


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the ELN file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
def import_eln(manager, path):
    """Import an RO-Crate file following the "ELN" file specification."""
    manager.misc.import_eln(path)

    click.echo("File has been imported successfully.")


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the JSON Schema file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
@option(
    "type",
    char="y",
    description="Type of the template to create from JSON Schema.",
    param_type=Choice(["extras", "record"]),
    default="extras",
    var_name="template_type",
)
def import_json_schema(manager, path, template_type):
    """Import JSON Schema file and create a template."""
    manager.misc.import_json_schema(path, template_type)

    click.echo("File has been imported successfully.")


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the SHACl file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
@option(
    "type",
    char="y",
    description="Type of the template to create from SHACL shapes.",
    param_type=Choice(["extras", "record"]),
    default="extras",
    var_name="template_type",
)
def import_shacl(manager, path, template_type):
    """Import SHACL file and create a template."""
    manager.misc.import_shacl(path, template_type)

    click.echo("File has been imported successfully.")


@misc.command()
@apy_command(use_kadi_manager=True)
@option("collection-id", char="c", description="ID of the collection.", required=True)
@option("suffix", char="s", description="Suffix to append to identifiers.")
@option(
    "records",
    char="r",
    description="Specify 'all' to reuse all records without selection. Alternatively,"
    " provide record IDs separated by commas (e.g. 101,205).",
)
def reuse_collection(manager, collection_id, suffix=None, records=None):
    """Reuse the collection with the given ID.

    This command creates a new collection by duplicating all records and their links
    from an existing collection and appending the given suffix to their identifiers.
    """

    def error(message):
        click.secho(message, fg="red", bold=True)
        sys.exit(1)

    def valid_numeric_input(user_input, allow_ranges=False):
        allowed_chars = ",-" if allow_ranges else ","
        cleaned_input = user_input.translate(str.maketrans("", "", allowed_chars))
        return cleaned_input.isdigit()

    collection = manager.collection(id=collection_id)
    id_to_identifier = _get_record_identifiers(collection)
    record_identifiers = list(id_to_identifier.values())

    if records:
        if records.lower() != "all":
            if not valid_numeric_input(records, allow_ranges=False):
                error("Invalid input format.")

            selected_ids = {int(x.strip()) for x in records.split(",")}
            invalid_ids = [id for id in selected_ids if id not in id_to_identifier]

            if invalid_ids:
                error(f"Invalid record IDs: {invalid_ids}.")

            # Select only the identifiers that match the chosen IDs.
            record_identifiers = [id_to_identifier[id] for id in selected_ids]
    else:
        click.echo("Available Record Identifiers:")
        record_identifiers = list(id_to_identifier.values())

        for idx, identifier in enumerate(record_identifiers, start=1):
            click.echo(f"{idx}: {identifier}")

        if not click.confirm("Do you want to reuse all records?", default=True):
            selected_input = click.prompt(
                "Enter record numbers or ranges separated by comma (e.g. 1-3,5)",
                default="",
                show_default=False,
            )

            if not valid_numeric_input(selected_input, allow_ranges=True):
                error("Invalid input format.")

            selected_numbers = set()

            for num in selected_input.split(","):
                if "-" in num:
                    start, end = map(int, num.split("-"))

                    if (
                        start > end
                        or not (1 <= start <= len(record_identifiers))
                        or not (1 <= end <= len(record_identifiers))
                    ):
                        error(
                            f"Invalid range. Please enter numbers in the correct order"
                            f" and within 1-{len(record_identifiers)}."
                        )

                    selected_numbers.update(range(start, end + 1))
                else:
                    x = int(num)

                    if x < 1 or x > len(record_identifiers):
                        error(
                            f"Invalid number: {num}. Please enter numbers within"
                            f" 1-{len(record_identifiers)}."
                        )

                    selected_numbers.add(x)

            record_identifiers = [
                record_identifiers[num - 1] for num in selected_numbers
            ]

    click.echo(f"Selected Identifiers: {record_identifiers}")

    # Validate suffix for characters and length of the identifier.
    if not suffix:
        suffix = click.prompt("Enter a suffix to append to identifiers")

    new_identifier = append_identifier_suffix(collection.meta["identifier"], suffix)
    new_collection = manager.collection(
        title=collection.meta["title"],
        identifier=new_identifier,
        description=collection.meta["description"],
        tags=collection.meta["tags"],
        visibility=collection.meta["visibility"],
        create=True,
    )

    _copy_records(manager, new_collection, record_identifiers, suffix)
    collection.add_collection_link(collection_id=new_collection.id)

    click.echo(f"A collection with {len(record_identifiers)} records has been created.")
