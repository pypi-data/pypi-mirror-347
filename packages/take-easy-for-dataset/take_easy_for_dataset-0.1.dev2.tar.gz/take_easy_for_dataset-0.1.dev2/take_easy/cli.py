from typing import List

import typer

from take_easy.converter.parquet_and_csv import parquet_to_csv, csv_to_parquet, create_csv_template

app = typer.Typer(
    name="Take easy for dataset",
    no_args_is_help=True,
)


@app.command()
def convert(
        fmt: str = typer.Argument(..., help="Output format (parquet or csv)"),
        input_path: str = typer.Argument(..., help="Input file path"),
        output_path: str = typer.Argument(..., help="Output file path"),
):
    """
    Convert dataset to specified format.
    """
    assert fmt in ["parquet", "csv"], "Format must be either 'parquet' or 'csv'"
    if fmt == "parquet":
        csv_to_parquet(csv_path=input_path, parquet_path=output_path)
    elif fmt == "csv":
        parquet_to_csv(parquet_path=input_path, csv_path=output_path)
    else:
        raise ValueError("Don't try to hack me !")


@app.command(name="create-template")
def create_template(
        params: List[str] = typer.Argument(..., help="List of parameters"),
        file_path: str = typer.Argument("template.csv", help="Output file path"),
):
    """
    Create a csv template based on the provided parameters.
    """
    create_csv_template(params=params, file_path=file_path)


def main():
    app()


if __name__ == "__main__":
    main()
