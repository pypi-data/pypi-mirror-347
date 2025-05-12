import logging
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markdown import Markdown

from sbomgrader.core.formats import SBOMFormat
from sbomgrader.core.logging import setup_logger
from sbomgrader.grade.choose_cookbooks import select_cookbook_bundle
from sbomgrader.grade.cookbook_bundles import CookbookBundle
from sbomgrader.grade.cookbooks import Cookbook
from sbomgrader.core.documents import Document
from sbomgrader.core.enums import Grade, SBOMTime, OutputType, SBOMType
from sbomgrader.core.utils import get_mapping, validation_passed
from sbomgrader.translate.choose_map import choose_map, get_all_map_list_markdown
from sbomgrader.translate.translation_map import TranslationMap

LOGGER = logging.getLogger(__name__)


def _input_format(arg: str) -> dict[str, Any]:
    """
    Function to ensure input SBOM reading. Exits the process on error.
    :param arg: The value that is passed to the argument parser.
    :return: Loaded dictionary of the SBOM doc.
    """
    mapping = get_mapping(arg)
    if not mapping:
        LOGGER.error("Could not read SBOM from input or file!")
        exit(1)
    return mapping


def _safe_load_doc(mapping: dict[str, Any]) -> Document:
    """
    Load an SBOM document from dictionary to the `Document` object.
    Ensures that the content is actually a supported SBOM type.
    Exits the process otherwise.

    :param mapping: The mapping containing the SBOM.
    :return: The SBOM `Document` object.
    """
    try:
        doc = Document(mapping)
        # Test if this actually is an SBOM doc
        assert doc.sbom_format
        return doc
    except NotImplementedError as e:
        LOGGER.error("Please supply a valid and supported SBOM!")
        LOGGER.debug("Problem info: ", exc_info=e)
        exit(1)


@dataclass
class GradeConfig:
    input_file: dict[str, Any]
    cookbook_references: list[str]
    content_type: SBOMType
    sbom_type: SBOMTime
    passing_grade: Grade
    output_type: OutputType

    @staticmethod
    def from_args(args: Namespace) -> "GradeConfig":
        return GradeConfig(
            input_file=args.input,
            cookbook_references=args.cookbook or [],
            content_type=args.content_type,
            sbom_type=args.sbom_type,
            passing_grade=args.passing_grade,
            output_type=args.output,
        )


def create_grade_parser(parser: ArgumentParser):
    parser.add_argument(
        "input",
        type=_input_format,
        help="SBOM File to grade. Currently supports JSON.",
    )
    parser.add_argument(
        "--cookbook",
        "-c",
        action="append",
        type=str,
        help="Cookbooks to use for validation. "
        "Might reference default cookbook, directories or files. "
        "Only files with '.yml' or '.yaml' extensions are taken into account if files or directories are specified.",
    )
    parser.add_argument(
        "--content-type",
        "-ct",
        choices=[v.value for v in SBOMType if v is not SBOMType.UNSPECIFIED],
        default=SBOMType.UNSPECIFIED.value,
        help="Specify SBOM content type. Ignored if cookbooks argument is specified.",
    )
    parser.add_argument(
        "--sbom-type",
        "-st",
        choices=[v.value for v in SBOMTime if v is not SBOMTime.UNSPECIFIED],
        default=None,
        help="If using the standard validation, specify which SBOM type (by time) is being validated. "
        "Ignored if cookbooks argument is specified.",
    )
    parser.add_argument(
        "--passing-grade",
        "-g",
        choices=[v.value for v in Grade],
        default=Grade.B.value,
        help="Minimal passing grade. Default is B.",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=[v.value for v in OutputType],
        default=OutputType.VISUAL.value,
        help="Specify the output format.",
    )


def grade(config: GradeConfig) -> None:
    console = Console()

    doc = _safe_load_doc(config.input_file)

    if config.cookbook_references:
        cookbook_bundle = select_cookbook_bundle(config.cookbook_references)
        if not cookbook_bundle.cookbooks:
            LOGGER.error("No cookbook(s) could be found.")
            exit(1)
    else:
        # Cookbooks weren't specified, using defaults
        type_ = SBOMType(config.content_type)
        if type_ is SBOMType.UNSPECIFIED:
            type_ = doc.sbom_type
        cookbook_bundle = CookbookBundle.for_document_type(
            type_, SBOMTime(config.sbom_type)
        )

    result = cookbook_bundle(doc)

    output_type = OutputType(config.output_type)
    if output_type is OutputType.VISUAL:
        markdown = Markdown(result.output(output_type))
        console.print(markdown)
    else:
        console.print(result.output(output_type))
    if validation_passed(result.grade, Grade(config.passing_grade)):
        exit(0)
    exit(1)


@dataclass
class ConvertConfig:
    input_file: dict[str, Any]
    output_format: Enum
    custom_maps: list[Path]

    @staticmethod
    def from_args(args: Namespace) -> "ConvertConfig":
        return ConvertConfig(
            input_file=args.input,
            output_format=args.output_format,
            custom_maps=args.custom_map or [],
        )


def create_convert_parser(parser: ArgumentParser):
    parser.add_argument(
        "input",
        type=_input_format,
        help="SBOM File to convert. Currently supports JSON.",
    )
    parser.add_argument(
        "--output-format",
        "-f",
        choices=[v.value for v in SBOMFormat],
        required=True,
        help="SBOM format to create.",
    )
    parser.add_argument(
        "--custom-map",
        "-m",
        type=str,
        help="Custom translation map file.",
        action="append",
    )


def convert(config: ConvertConfig) -> None:

    custom_maps = [TranslationMap.from_file(f) for f in config.custom_maps]

    doc = _safe_load_doc(config.input_file)

    target_format: Enum = SBOMFormat(config.output_format)

    t_map = choose_map(doc, target_format, *custom_maps)
    print(t_map.convert(doc, target_format).json_dump)
    exit(0)


@dataclass
class ListConfig:
    maps: bool
    cookbooks: bool

    @staticmethod
    def from_args(args: Namespace) -> "ListConfig":
        return ListConfig(maps=args.maps, cookbooks=args.cookbooks)


def create_list_parser(parser: ArgumentParser):
    mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument(
        "--maps",
        "-m",
        action="store_true",
        default=False,
        help="List available default translation maps and exit.",
    )
    mutually_exclusive.add_argument(
        "--cookbooks",
        "-c",
        action="store_true",
        default=False,
        help="List available default cookbooks and exit.",
    )


def list_(config: ListConfig):
    console = Console()
    if config.cookbooks:
        default_cookbooks = Cookbook.load_all_defaults()
        console.print(Markdown("\n".join(f"- {cb.name}" for cb in default_cookbooks)))
    if config.maps:
        console.print(Markdown(get_all_map_list_markdown()))
    exit(0)


def main():
    # Temporary logger for errors & warnings stemming from argument parsing
    setup_logger()
    parser = ArgumentParser("sbomgrader")
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="Set the verbosity level of the application.",
    )
    subparsers = parser.add_subparsers(required=True, dest="command")
    grade_parser = subparsers.add_parser("grade")
    create_grade_parser(grade_parser)
    convert_parser = subparsers.add_parser("convert")
    create_convert_parser(convert_parser)
    list_parser = subparsers.add_parser("list")
    create_list_parser(list_parser)
    args = parser.parse_args()
    setup_logger(verbosity_level=args.verbosity, overwrite_handlers=True)

    map_ = {
        "grade": (grade, GradeConfig),
        "convert": (convert, ConvertConfig),
        "list": (list_, ListConfig),
    }
    func, config_class = map_[args.command]
    return func(config_class.from_args(args))


if __name__ == "__main__":
    main()
