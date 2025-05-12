from rich.console import Console
import questionary
import sys
import subprocess
from orgm.qstyle import custom_style_fancy

console = Console()


def menu():
    """Menú interactivo para comandos de IA."""

    console.print("[bold blue]===== Menú de Configuración =====[/bold blue]")

    opciones = [
        {"name": "📤 Build", "value": "build"},
        {"name": "📤 Build (sin cache)", "value": "build_no_cache"},
        {"name": "📤 Save", "value": "save"},
        {"name": "📤 Push", "value": "push"},
        {"name": "📤 Tag", "value": "tag"},
        {"name": "📤 Create prod context", "value": "create_prod_context"},
        {"name": "� Deploy", "value": "deploy"},
        {"name": "📤 Remove prod context", "value": "remove_prod_context"},
        {"name": "📤 Login", "value": "login"},
        {"name": "🔍 Ayuda", "value": "docker -h"},
        {"name": "❌ Salir", "value": "exit"},
    ]

    selected = questionary.checkbox(
        "Selecciona las operaciones a ejecutar:",
        choices=[c["name"] for c in opciones],
        style=custom_style_fancy,
    ).ask()

    if not selected:
        console.print("[yellow]No se seleccionaron operaciones.[/yellow]")
        return

    # Map from displayed name to internal id
    mapping = {opcion["name"]: opcion["value"] for opcion in opciones}
    for choice_name in selected:
        # Handle exit case first
        if choice_name == "❌ Salir":
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)

        op = mapping[choice_name]
        
        if op == "login":
            from orgm.apps.docker.login import login
            login()

        elif op == "build":
            from orgm.apps.docker.build import build

            build()
        elif op == "build_no_cache":
            from orgm.apps.docker.build import build_no_cache

            build_no_cache()
        elif op == "save":
            from orgm.apps.docker.save import save

            push()
        elif op == "tag":
            from orgm.apps.docker.tag import tag

            save()
        elif op == "push":
            from orgm.apps.docker.push import push

            tag()
        elif op == "create_prod_context":
            from orgm.apps.docker.create_prod_context import create_prod_context
            create_prod_context()


        elif op == "remove_prod_context":
            from orgm.apps.docker.remove_prod_context import remove_prod_context
            remove_prod_context()

        elif op == "deploy":
            from orgm.apps.docker.deploy import deploy
            deploy()


        elif op == "docker -h":
            subprocess.run(["orgm", "docker", "-h"])
            menu()
