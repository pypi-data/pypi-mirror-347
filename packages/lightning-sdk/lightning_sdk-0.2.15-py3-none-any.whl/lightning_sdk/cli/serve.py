import concurrent.futures
import os
import re
import socket
import subprocess
import time
import webbrowser
from datetime import datetime
from enum import Enum
from pathlib import Path
from threading import Thread
from typing import Any, Dict, List, Optional, TypedDict, Union
from urllib.parse import urlencode

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Confirm
from rich.syntax import Syntax

from lightning_sdk import Machine, Teamspace
from lightning_sdk.api import UserApi
from lightning_sdk.api.lit_container_api import LitContainerApi
from lightning_sdk.api.utils import _get_registry_url
from lightning_sdk.cli.teamspace_menu import _TeamspacesMenu
from lightning_sdk.cli.upload import (
    _dump_current_upload_state,
    _resolve_previous_upload_state,
    _start_parallel_upload,
)
from lightning_sdk.lightning_cloud import env
from lightning_sdk.lightning_cloud.login import Auth, AuthServer
from lightning_sdk.lightning_cloud.openapi import V1CloudSpace
from lightning_sdk.lightning_cloud.rest_client import LightningClient
from lightning_sdk.serve import _LitServeDeployer
from lightning_sdk.studio import Studio
from lightning_sdk.utils.resolve import _get_authed_user, _get_studio_url, _resolve_teamspace

_MACHINE_VALUES = tuple([machine.name for machine in Machine.__dict__.values() if isinstance(machine, Machine)])
_POLL_TIMEOUT = 600
LITSERVE_CODE = os.environ.get("LITSERVE_CODE", "j39bzk903h")


class _ServeGroup(click.Group):
    def parse_args(self, ctx: click.Context, args: list) -> click.Group:
        # Check if first arg is a file path and not a command name
        if args and os.path.exists(args[0]) and args[0] not in self.commands:
            # Insert the 'api' command before the file path
            args.insert(0, "api")
        return super().parse_args(ctx, args)


@click.group("deploy", cls=_ServeGroup)
def deploy() -> None:
    """Deploy a LitServe model.

    Example:
        lightning deploy server.py --cloud # deploy to the cloud

    Example:
        lightning deploy server.py  # run locally

    You can deploy the API to the cloud by running `lightning deploy server.py --cloud`.
    This will build a docker container for the server.py script and deploy it to the Lightning AI platform.
    """


@deploy.command("api")
@click.argument("script-path", type=click.Path(exists=True))
@click.option(
    "--easy",
    is_flag=True,
    default=False,
    flag_value=True,
    help="Generate a client for the model",
)
@click.option(
    "--cloud",
    is_flag=True,
    default=False,
    flag_value=True,
    help="Run the model on cloud",
)
@click.option("--name", default=None, help="Name of the deployed API (e.g., 'classification-api', 'Llama-api')")
@click.option(
    "--non-interactive",
    "--non_interactive",
    is_flag=True,
    default=False,
    flag_value=True,
    help="Do not prompt for confirmation",
)
@click.option(
    "--machine",
    default="CPU",
    show_default=True,
    type=click.Choice(_MACHINE_VALUES),
    help="Machine type to deploy the API on. Defaults to CPU.",
)
@click.option(
    "--devbox",
    default=None,
    show_default=True,
    type=click.Choice(_MACHINE_VALUES),
    help="Machine type to build the API on. Setting this argument will open the server in a Studio.",
)
@click.option(
    "--interruptible",
    is_flag=True,
    default=False,
    flag_value=True,
    help="Whether the machine should be interruptible (spot) or not.",
)
@click.option(
    "--teamspace",
    default=None,
    help="The teamspace the deployment should be associated with. Defaults to the current teamspace.",
)
@click.option(
    "--org",
    default=None,
    help="The organization owning the teamspace (if any). Defaults to the current organization.",
)
@click.option("--user", default=None, help="The user owning the teamspace (if any). Defaults to the current user.")
@click.option(
    "--cloud-account",
    "--cloud_account",
    default=None,
    help=(
        "The cloud account to run the deployment on. "
        "Defaults to the studio cloud account if running with studio compute env. "
        "If not provided will fall back to the teamspaces default cloud account."
    ),
)
@click.option("--port", default=8000, help="The port to expose the API on.")
@click.option("--min_replica", "--min-replica", default=0, help="Number of replicas to start with.")
@click.option("--max_replica", "--max-replica", default=1, help="Number of replicas to scale up to.")
@click.option("--replicas", default=1, help="Deployment will start with this many replicas.")
@click.option(
    "--no_credentials",
    "--no-credentials",
    is_flag=True,
    default=False,
    flag_value=True,
    help="Whether to include credentials in the deployment.",
)
def api(
    script_path: str,
    easy: bool,
    cloud: bool,
    name: Optional[str],
    non_interactive: bool,
    machine: Optional[str],
    devbox: Optional[str],
    interruptible: bool,
    teamspace: Optional[str],
    org: Optional[str],
    user: Optional[str],
    cloud_account: Optional[str],
    port: Optional[int],
    min_replica: Optional[int],
    max_replica: Optional[int],
    replicas: Optional[int],
    no_credentials: Optional[bool],
) -> None:
    """Deploy a LitServe model script."""
    return api_impl(
        script_path=script_path,
        easy=easy,
        cloud=cloud,
        name=name,
        non_interactive=non_interactive,
        machine=machine,
        devbox=devbox,
        interruptible=interruptible,
        teamspace=teamspace,
        org=org,
        user=user,
        cloud_account=cloud_account,
        port=port,
        replicas=replicas,
        min_replica=min_replica,
        max_replica=max_replica,
        include_credentials=not no_credentials,
    )


def api_impl(
    script_path: Union[str, Path],
    easy: bool = False,
    cloud: bool = False,
    name: Optional[str] = None,
    tag: Optional[str] = None,
    non_interactive: bool = False,
    machine: str = "CPU",
    devbox: Optional[str] = None,
    interruptible: bool = False,
    teamspace: Optional[str] = None,
    org: Optional[str] = None,
    user: Optional[str] = None,
    cloud_account: Optional[str] = None,
    port: Optional[int] = 8000,
    min_replica: Optional[int] = 0,
    max_replica: Optional[int] = 1,
    replicas: Optional[int] = 1,
    include_credentials: Optional[bool] = True,
) -> None:
    """Deploy a LitServe model script."""
    console = Console()
    script_path = Path(script_path)
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
    if not script_path.is_file():
        raise ValueError(f"Path is not a file: {script_path}")

    _LitServeDeployer.generate_client() if easy else None

    if not name:
        timestr = datetime.now().strftime("%b-%d-%H_%M")
        name = f"litserve-{timestr}".lower()

    if not cloud:
        try:
            subprocess.run(
                ["python", str(script_path)],
                check=True,
                text=True,
            )
            return None
        except subprocess.CalledProcessError as e:
            error_msg = f"Script execution failed with exit code {e.returncode}\nstdout: {e.stdout}\nstderr: {e.stderr}"
            raise RuntimeError(error_msg) from None

    if devbox:
        return _handle_devbox(name, script_path, console, non_interactive, devbox, interruptible, teamspace, org, user)

    machine = Machine.from_str(machine)
    return _handle_cloud(
        script_path,
        console,
        repository=name,
        tag=tag,
        non_interactive=non_interactive,
        machine=machine,
        interruptible=interruptible,
        teamspace=teamspace,
        org=org,
        user=user,
        cloud_account=cloud_account,
        port=port,
        min_replica=min_replica,
        max_replica=max_replica,
        replicas=replicas,
        include_credentials=include_credentials,
    )


class _AuthMode(Enum):
    DEVBOX = "dev"
    DEPLOY = "deploy"


class _AuthServer(AuthServer):
    def __init__(self, mode: _AuthMode, *args: Any, **kwargs: Any) -> None:
        self._mode = mode
        super().__init__(*args, **kwargs)

    def get_auth_url(self, port: int) -> str:
        redirect_uri = f"http://localhost:{port}/login-complete"
        params = urlencode({"redirectTo": redirect_uri, "mode": self._mode.value, "okbhrt": LITSERVE_CODE})
        return f"{env.LIGHTNING_CLOUD_URL}/sign-in?{params}"


class _Auth(Auth):
    def __init__(self, mode: _AuthMode, shall_confirm: bool = False) -> None:
        super().__init__()
        self._mode = mode
        self._shall_confirm = shall_confirm

    def _run_server(self) -> None:
        if self._shall_confirm:
            proceed = Confirm.ask(
                "Authenticating with Lightning AI. This will open a browser window. Continue?", default=True
            )
            if not proceed:
                raise RuntimeError(
                    "Login cancelled. Please login to Lightning AI to deploy the API."
                    " Run `lightning login` to login."
                ) from None
        print("Opening browser for authentication...")
        print("Please come back to the terminal after logging in.")
        time.sleep(3)
        _AuthServer(self._mode).login_with_browser(self)


def authenticate(mode: _AuthMode, shall_confirm: bool = True) -> None:
    auth = _Auth(mode, shall_confirm)
    auth.authenticate()


def select_teamspace(teamspace: Optional[str], org: Optional[str], user: Optional[str]) -> Teamspace:
    if teamspace is None:
        user = _get_authed_user()
        menu = _TeamspacesMenu()
        possible_teamspaces = menu._get_possible_teamspaces(user)
        if len(possible_teamspaces) == 1:
            name = next(iter(possible_teamspaces.values()))["name"]
            return Teamspace(name=name, org=org, user=user)

        return menu._resolve_teamspace(teamspace)

    return _resolve_teamspace(teamspace=teamspace, org=org, user=user)


class _UserStatus(TypedDict):
    verified: bool
    onboarded: bool


def poll_verified_status(timeout: int = _POLL_TIMEOUT) -> _UserStatus:
    """Polls the verified status of the user until it is True or a timeout occurs."""
    user_api = UserApi()
    user = _get_authed_user()
    start_time = datetime.now()
    result = {"onboarded": False, "verified": False}
    while True:
        user_resp = user_api.get_user(name=user.name)
        result["onboarded"] = user_resp.status.completed_project_onboarding
        result["verified"] = user_resp.status.verified
        if user_resp.status.verified:
            return result
        if (datetime.now() - start_time).total_seconds() > timeout:
            break
        time.sleep(5)
    return result


class _OnboardingStatus(Enum):
    NOT_VERIFIED = "not_verified"
    ONBOARDING = "onboarding"
    ONBOARDED = "onboarded"


class _Onboarding:
    def __init__(self, console: Console) -> None:
        self.console = console
        self.user = _get_authed_user()
        self.user_api = UserApi()
        self.client = LightningClient(max_tries=7)

    @property
    def verified(self) -> bool:
        return self.user_api.get_user(name=self.user.name).status.verified

    @property
    def is_onboarded(self) -> bool:
        return self.user_api.get_user(name=self.user.name).status.completed_project_onboarding

    @property
    def can_join_org(self) -> bool:
        return len(self.client.organizations_service_list_joinable_organizations().joinable_organizations) > 0

    @property
    def status(self) -> _OnboardingStatus:
        if not self.verified:
            return _OnboardingStatus.NOT_VERIFIED
        if self.is_onboarded:
            return _OnboardingStatus.ONBOARDED
        return _OnboardingStatus.ONBOARDING

    def _wait_user_onboarding(self, timeout: int = _POLL_TIMEOUT) -> None:
        """Wait for user onboarding if they can join the teamspace otherwise move to select a teamspace."""
        status = self.status
        if status == _OnboardingStatus.ONBOARDED:
            return

        self.console.print("Waiting for account setup. Visit lightning.ai")
        start_time = datetime.now()
        while self.status != _OnboardingStatus.ONBOARDED:
            time.sleep(5)
            if self.is_onboarded:
                return
            if (datetime.now() - start_time).total_seconds() > timeout:
                break

        raise RuntimeError("Timed out waiting for onboarding status")

    def get_cloudspace_id(self, teamspace: Teamspace) -> Optional[str]:
        cloudspaces: List[V1CloudSpace] = self.client.cloud_space_service_list_cloud_spaces(teamspace.id).cloudspaces
        cloudspaces = sorted(cloudspaces, key=lambda cloudspace: cloudspace.created_at, reverse=True)
        if len(cloudspaces) == 0:
            raise RuntimeError("Error creating deployment! Finish account setup at lightning.ai first.")
        # get the first cloudspace
        cloudspace = cloudspaces[0]
        if "scratch-studio" in cloudspace.name or "scratch-studio" in cloudspace.display_name:
            return cloudspace.id
        return None

    def select_teamspace(self, teamspace: Optional[str], org: Optional[str], user: Optional[str]) -> Teamspace:
        """Select a teamspace while onboarding.

        If user is being onboarded and can't join any org, the teamspace it will be resolved to the default
         personal teamspace.
        If user is being onboarded and can join an org then it will select default teamspace from the org.
        """
        if self.is_onboarded:
            return select_teamspace(teamspace, org, user)

        # Run only when user hasn't completed onboarding yet.
        menu = _TeamspacesMenu()
        self._wait_user_onboarding()
        # Onboarding has been completed - user already selected organization if they could
        possible_teamspaces = menu._get_possible_teamspaces(self.user)
        if len(possible_teamspaces) == 1:
            # User didn't select any org
            value = next(iter(possible_teamspaces.values()))
            return Teamspace(name=value["name"], org=value["org"], user=value["user"])

        for _, value in possible_teamspaces.items():
            # User select an org
            # Onboarding teamspace will be the default teamspace in the selected org
            if value["org"]:
                return Teamspace(name=value["name"], org=value["org"], user=value["user"])
        raise RuntimeError("Unable to select teamspace. Visit lightning.ai")


def is_connected(host: str = "8.8.8.8", port: int = 53, timeout: int = 10) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False


def _upload_container(
    console: Console,
    ls_deployer: _LitServeDeployer,
    repository: str,
    tag: str,
    resolved_teamspace: Teamspace,
    lit_cr: LitContainerApi,
    cloud_account: Optional[str],
) -> bool:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        try:
            push_task = progress.add_task("Uploading container to Lightning registry", total=None)
            for line in ls_deployer.push_container(
                repository, tag, resolved_teamspace, lit_cr, cloud_account=cloud_account
            ):
                progress.update(push_task, advance=1)
                if not ("Pushing" in line["status"] or "Waiting" in line["status"]):
                    console.print(line["status"])
            progress.update(push_task, description="[green]Push completed![/green]")
        except Exception as e:
            console.print(f"❌ Deployment failed: {e}", style="red")
            return False
    console.print(f"\n✅ Image pushed to {repository}:{tag}")
    return True


# TODO: Move the rest of the devbox logic here
class _LitServeDevbox:
    """Build LitServe API in a Studio."""

    def resolve_previous_upload(self, studio: Studio, folder: str) -> Dict[str, str]:
        remote_path = "."
        pairs = {}
        for root, _, files in os.walk(folder):
            rel_root = os.path.relpath(root, folder)
            for f in files:
                pairs[os.path.join(root, f)] = os.path.join(remote_path, rel_root, f)
        return _resolve_previous_upload_state(studio, remote_path, pairs)

    def upload_folder(self, studio: Studio, folder: str, upload_state: Dict[str, str]) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = _start_parallel_upload(executor, studio, upload_state)
            total_files = len(upload_state)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=Console(),
                transient=True,
            ) as progress:
                upload_task = progress.add_task(f"[cyan]Uploading {total_files} files to Studio...", total=total_files)
                for f in concurrent.futures.as_completed(futures):
                    upload_state.pop(f.result())
                    _dump_current_upload_state(studio, ".", upload_state)
                    progress.update(upload_task, advance=1)


def _detect_port(script_path: Path) -> int:
    with open(script_path) as f:
        content = f.read()

    # Try to match server.run first and then any variable name and then default port=8000
    match = re.search(r"server\.run\s*\([^)]*port\s*=\s*(\d+)", content) or re.search(
        r"\w+\.run\s*\([^)]*port\s*=\s*(\d+)", content
    )
    return int(match.group(1)) if match else 8000


def _handle_devbox(
    name: str,
    script_path: Path,
    console: Console,
    non_interactive: bool = False,
    devbox: Union[Machine, str] = Machine.CPU,
    interruptible: bool = False,
    teamspace: Optional[str] = None,
    org: Optional[str] = None,
    user: Optional[str] = None,
) -> None:
    if script_path.suffix != ".py":
        console.print("❌ Error: Only Python files (.py) are supported for development servers", style="red")
        return

    authenticate(_AuthMode.DEVBOX, shall_confirm=not non_interactive)
    user_status = poll_verified_status()
    if not user_status["verified"]:
        console.print("❌ Verify phone number to continue. Visit lightning.ai.", style="red")
        return
    if not user_status["onboarded"]:
        console.print("onboarding user")
        onboarding = _Onboarding(console)
        resolved_teamspace = onboarding.select_teamspace(teamspace, org, user)
    else:
        resolved_teamspace = select_teamspace(teamspace, org, user)
    studio = Studio(name=name, teamspace=resolved_teamspace)
    studio.install_plugin("custom-port")
    lit_devbox = _LitServeDevbox()

    studio_url = _get_studio_url(studio, turn_on=True)
    pathlib_path = Path(script_path).resolve()
    browser_opened = False
    studio_path = f"{studio.owner.name}/{studio.teamspace.name}/{studio.name}"

    console.print("\n=== Lightning Studio Setup ===")
    console.print(f"🔧 [bold]Setting up Studio:[/bold] {studio_path}")
    console.print(f"📁 [bold]Local project:[/bold] {pathlib_path.parent}")

    upload_state = lit_devbox.resolve_previous_upload(studio, str(pathlib_path.parent))
    if non_interactive:
        console.print(f"🌐 [bold]Opening Studio:[/bold] [link={studio_url}]{studio_url}[/link]")
        browser_opened = webbrowser.open(studio_url)
    else:
        if Confirm.ask("Would you like to open your Studio in the browser?", default=True):
            console.print(f"🌐 [bold]Opening Studio:[/bold] [link={studio_url}]{studio_url}[/link]")
            browser_opened = webbrowser.open(studio_url)

    if not browser_opened:
        console.print(f"🔗 [bold]Access Studio:[/bold] [link={studio_url}]{studio_url}[/link]")

    # Start the Studio in the background and return immediately using threading
    console.print("\n⚡ Initializing Studio in the background...")
    studio_thread = Thread(target=studio.start, args=(devbox, interruptible))
    studio_thread.start()

    console.print("📤 Syncing project files to Studio...")
    lit_devbox.upload_folder(studio, pathlib_path.parent, upload_state)

    # Wait for the Studio to start
    console.print("⚡ Waiting for Studio to start...")
    studio_thread.join()

    try:
        console.print("🚀 Starting server...")
        studio.run_and_detach(f"python {script_path}", timeout=10)
    except Exception as e:
        console.print("❌ Error while starting server", style="red")
        syntax = Syntax(f"{e}", "bash", theme="monokai")
        console.print(syntax)
        console.print(f"\n🔄 [bold]To fix:[/bold] Edit your code in Studio and run with: [u]python {script_path}[/u]")
        return

    port = _detect_port(pathlib_path)
    console.print("🔌 Configuring server port...")
    port_url = studio.run_plugin("custom-port", port=port)

    # Add completion message with next steps
    console.print("\n✅ Studio ready!")
    console.print("\n📋 [bold]Next steps:[/bold]")
    console.print("  [bold]1.[/bold] Server code will be available in the Studio")
    console.print("  [bold]2.[/bold] The Studio is now running with the specified configuration")
    console.print("  [bold]3.[/bold] Modify and run your server directly in the Studio")
    console.print(f"  [bold]4.[/bold] Your server will be accessible on [link={port_url}]{port_url}[/link]")
    # TODO: Once server running is implemented


def _handle_cloud(
    script_path: Union[str, Path],
    console: Console,
    repository: str = "litserve-model",
    tag: Optional[str] = None,
    non_interactive: bool = False,
    machine: Machine = "CPU",
    interruptible: bool = False,
    teamspace: Optional[str] = None,
    org: Optional[str] = None,
    user: Optional[str] = None,
    cloud_account: Optional[str] = None,
    port: Optional[int] = 8000,
    min_replica: Optional[int] = 0,
    max_replica: Optional[int] = 1,
    replicas: Optional[int] = 1,
    include_credentials: Optional[bool] = True,
) -> None:
    if not is_connected():
        console.print("❌ Internet connection required to deploy to the cloud.", style="red")
        console.print("To run locally instead, use: `lightning serve [SCRIPT | server.py]`")
        return

    deployment_name = os.path.basename(repository)
    tag = tag if tag else "latest"

    if non_interactive:
        console.print("[italic]non-interactive[/italic] mode enabled, skipping confirmation prompts", style="blue")

    port = port or 8000
    ls_deployer = _LitServeDeployer(name=deployment_name, teamspace=None)
    path = ls_deployer.dockerize_api(script_path, port=port, gpu=not machine.is_cpu(), tag=tag, print_success=False)

    console.print(f"\nPlease review the Dockerfile at [u]{path}[/u] and make sure it is correct.", style="bold")
    correct_dockerfile = True if non_interactive else Confirm.ask("Is the Dockerfile correct?", default=True)
    if not correct_dockerfile:
        console.print("Please fix the Dockerfile and try again.", style="red")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        try:
            # Build the container
            build_task = progress.add_task("Building Docker image", total=None)
            for line in ls_deployer.build_container(path, repository, tag):
                console.print(line.strip())
                progress.update(build_task, advance=1)
            progress.update(build_task, description="[green]Build completed![/green]", completed=1.0)
            progress.remove_task(build_task)

        except Exception as e:
            console.print(f"❌ Deployment failed: {e}", style="red")
            return

    # Push the container to the registry
    console.print("\nPushing container to registry. It may take a while...", style="bold")
    # Authenticate with LitServe affiliate
    authenticate(_AuthMode.DEPLOY, shall_confirm=not non_interactive)
    user_status = poll_verified_status()
    cloudspace_id: Optional[str] = None
    from_onboarding = False
    if not user_status["verified"]:
        console.print("❌ Verify phone number to continue. Visit lightning.ai.", style="red")
        return
    if not user_status["onboarded"]:
        console.print("onboarding user")
        onboarding = _Onboarding(console)
        resolved_teamspace = onboarding.select_teamspace(teamspace, org, user)
        cloudspace_id = onboarding.get_cloudspace_id(resolved_teamspace)
        from_onboarding = True
    else:
        resolved_teamspace = select_teamspace(teamspace, org, user)

    # list containers to create the project if it doesn't exist
    lit_cr = LitContainerApi()
    lit_cr.list_containers(resolved_teamspace.id, cloud_account=cloud_account)

    registry_url = _get_registry_url()
    container_basename = repository.split("/")[-1]
    image = (
        f"{registry_url}/lit-container{f'-{cloud_account}' if cloud_account is not None else ''}/"
        f"{resolved_teamspace.owner.name}/{resolved_teamspace.name}/{container_basename}"
    )

    if from_onboarding:
        thread = Thread(
            target=ls_deployer.run_on_cloud,
            kwargs={
                "deployment_name": deployment_name,
                "image": image,
                "teamspace": resolved_teamspace,
                "metric": None,
                "machine": machine,
                "spot": interruptible,
                "cloud_account": cloud_account,
                "port": port,
                "min_replica": min_replica,
                "max_replica": max_replica,
                "replicas": replicas,
                "include_credentials": include_credentials,
                "cloudspace_id": cloudspace_id,
                "from_onboarding": from_onboarding,
            },
        )
        thread.start()
        console.print("🚀 Deployment started")
        if not _upload_container(console, ls_deployer, repository, tag, resolved_teamspace, lit_cr, cloud_account):
            thread.join()
            return
        thread.join()
        return

    if not _upload_container(console, ls_deployer, repository, tag, resolved_teamspace, lit_cr, cloud_account):
        return

    deployment_status = ls_deployer.run_on_cloud(
        deployment_name=deployment_name,
        image=image,
        teamspace=resolved_teamspace,
        metric=None,
        machine=machine,
        spot=interruptible,
        cloud_account=cloud_account,
        port=port,
        min_replica=min_replica,
        max_replica=max_replica,
        replicas=replicas,
        include_credentials=include_credentials,
        cloudspace_id=cloudspace_id,
        from_onboarding=from_onboarding,
    )
    console.print(f"🚀 Deployment started, access at [i]{deployment_status.get('url')}[/i]")
    if user_status["onboarded"]:
        webbrowser.open(deployment_status.get("url"))
