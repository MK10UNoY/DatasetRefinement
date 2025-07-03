import os
import json
import questionary
from rich.console import Console
from .datasetrefinement import extraction, cleaning, modeling
console = Console()

def get_default_output_path(input_path, action):
    os.makedirs('output', exist_ok=True)
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    if action == 'extract':
        suffix = '_extracted'
    elif action == 'clean':
        suffix = '_cleaned'
    elif action == 'train':
        suffix = '_model'
    else:
        suffix = '_output'
    return os.path.join('output', f"{name}{suffix}{ext if ext else '.out'}")

def main():
    console.print("[bold cyan]Welcome to DataSetRefinement Toolkit![/bold cyan]")

    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Extract data",
                "Clean data",
                "Train model",
                "Exit"
            ]
        ).ask()

        if action == "Extract data":
            extract_type = questionary.select(
                "Select the type of data to extract:",
                choices=[
                    "PDF",
                    "JSON",
                    "CSV",
                    "Web"
                ]
            ).ask()

            if extract_type in ["PDF", "JSON", "CSV"]:
                console.print(f"[bold yellow]{extract_type} Extraction: Please provide the required file paths.[/bold yellow]")
                input_path = questionary.text("Enter the input file path:").ask()
                output_path = questionary.text("Enter the output file path (leave blank for default):").ask()
                if not input_path:
                    console.print("[bold red]Input file path is required![/bold red]")
                    continue
                if not output_path:
                    output_path = get_default_output_path(input_path, 'extract')
                    console.print(f"[bold blue]No output path provided. Using default: {output_path}[/bold blue]")
                try:
                    console.print(f"[yellow]Extracting from {input_path} to {output_path}...[/yellow]")
                    extraction.extract_file(input_path, output_path)
                    console.print("[green]Extraction complete![/green]")
                except Exception as e:
                    console.print(f"[bold red]Extraction failed: {e}[/bold red]")

            elif extract_type == "Web":
                web_option = questionary.select(
                    "Choose web extraction mode:",
                    choices=[
                        "Single website link",
                        "Multiple website links from JSON file"
                    ]
                ).ask()
                if web_option == "Single website link":
                    url = questionary.text("Enter the website URL:").ask()
                    output_path = questionary.text("Enter the output file path (leave blank for default):").ask()
                    if not url:
                        console.print("[bold red]Website URL is required![/bold red]")
                        continue
                    if not output_path:
                        output_path = os.path.join('output', 'web_extracted.json')
                        os.makedirs('output', exist_ok=True)
                        console.print(f"[bold blue]No output path provided. Using default: {output_path}[/bold blue]")
                    try:
                        console.print(f"[yellow]Extracting from {url} to {output_path}...[/yellow]")
                        extraction.extract_from_url(url, output_path)
                        console.print("[green]Web extraction complete![/green]")
                    except Exception as e:
                        console.print(f"[bold red]Web extraction failed: {e}[/bold red]")
                else:
                    json_path = questionary.text("Enter the JSON file path containing website links:").ask()
                    output_path = questionary.text("Enter the output file path (leave blank for default):").ask()
                    if not json_path:
                        console.print("[bold red]JSON file path is required![/bold red]")
                        continue
                    if not output_path:
                        output_path = os.path.join('output', 'web_multi_extracted.json')
                        os.makedirs('output', exist_ok=True)
                        console.print(f"[bold blue]No output path provided. Using default: {output_path}[/bold blue]")
                    try:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            urls = json.load(f)
                        if not isinstance(urls, list):
                            raise ValueError("JSON file must contain a list of URLs.")
                        all_data = []
                        for url in urls:
                            console.print(f"[yellow]Extracting from {url}...[/yellow]")
                            try:
                                data = extraction.extract_from_url(url)
                                all_data.append(data)
                            except Exception as e:
                                console.print(f"[bold red]Failed to extract {url}: {e}[/bold red]")
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        console.print("[green]Batch web extraction complete![/green]")
                    except Exception as e:
                        console.print(f"[bold red]Batch web extraction failed: {e}[/bold red]")

        elif action == "Clean data":
            console.print("[bold yellow]Cleaning: Please provide the required file paths.[/bold yellow]")
            input_path = questionary.text("Enter the input file path:").ask()
            output_path = questionary.text("Enter the output file path (leave blank for default):").ask()
            if not input_path:
                console.print("[bold red]Input file path is required![/bold red]")
                continue
            if not output_path:
                output_path = get_default_output_path(input_path, 'clean')
                console.print(f"[bold blue]No output path provided. Using default: {output_path}[/bold blue]")
            try:
                console.print(f"[yellow]Cleaning {input_path} to {output_path}...[/yellow]")
                cleaning.clean_file(input_path, output_path)
                console.print("[green]Cleaning complete![/green]")
            except ValueError as ve:
                console.print(f"[bold red]{ve}[/bold red]")
            except Exception as e:
                console.print(f"[bold red]Cleaning failed: {e}[/bold red]")

        elif action == "Train model":
            console.print("[bold yellow]Model Training: Please provide the cleaned data file path.[/bold yellow]")
            input_path = questionary.text("Enter the cleaned data file path:").ask()
            if not input_path:
                console.print("[bold red]Input file path is required![/bold red]")
                continue
            try:
                console.print(f"[yellow]Training model on {input_path}...[/yellow]")
                modeling.train_model(input_path)
                console.print("[green]Model training complete![/green]")
            except Exception as e:
                console.print(f"[bold red]Model training failed: {e}[/bold red]")

        else:
            console.print("[bold red]Goodbye![/bold red]")
            break

if __name__ == '__main__':
    main() 