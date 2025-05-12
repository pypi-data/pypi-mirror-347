from scientiflow_cli.services.auth_service import AuthService
from scientiflow_cli.services.rich_printer import RichPrinter

def login_user():
    printer = RichPrinter()
    auth_service = AuthService()
    email = printer.prompt_input("[bold cyan]Enter your email[/bold cyan]")
    password = printer.prompt_input("[bold cyan]Enter your password[/bold cyan]", password=True)
    result = auth_service.login(email, password)
    if result["success"]:
        printer.print_message(result["message"], style="bold green")
    else:
        printer.print_error(result["message"])