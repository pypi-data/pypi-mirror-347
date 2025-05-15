"""The plugin."""
from typing import Any

from poetry.console.application import Application
from poetry.console.commands.install import InstallCommand
from poetry.packages.locker import Locker
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.repositories.lockfile_repository import LockfileRepository


class NoDevelopLocker:
    """A Locker which forces installation of all packages in non-editable mode."""

    def __init__(self, locker: Locker) -> None:
        self.__locker = locker

    def __getattr__(self, attr: str) -> Any:
        """Defer (almost) all attribute lookups to the original Locker."""
        return getattr(self.__locker, attr)

    def __setattr__(self, attr: str, val: Any) -> None:
        """Defer (almost) all attribute setting to the original Locker."""
        if attr == "_NoDevelopLocker__locker":
            return super().__setattr__(attr, val)

        return setattr(self.__locker, attr, val)

    def locked_repository(self) -> LockfileRepository:
        """Return a lockfile repository with all packages marked as non-editable."""
        repository = self.__locker.locked_repository()
        for package in repository.packages:
            package.develop = False
        return repository


class InstallProdCommand(InstallCommand):
    """An install command which forces all packages to be installed as non-editable."""

    name = "install-prod"
    description = (
        InstallCommand.description[:-1]
        + ", ignoring all <info>develop = true</info> options in path dependencies."
    )
    help = (
        "This is identical to the <info>install</> command with the two key\n"
        "differences being that packages marked with <comment>develop = true</>\n"
        "(editable) will be fully installed rather than installed via symbolic link,\n"
        "and installation can only be done from the <comment>poetry.lock</> file (and\n"
        "not directly from the <comment>pyproject.toml</> file). See\n\n"
        "<info>poetry install --help</>\n\n"
        "for more information on the <info>install</> command."
    )

    def handle(self) -> int:
        """Install the packages."""
        self.installer.set_locker(
            NoDevelopLocker(  # type: ignore[arg-type]
                self.installer._locker  # pylint: disable=protected-access
            )
        )
        if not self.installer._locker.is_locked():  # pylint: disable=protected-access
            raise FileNotFoundError("poetry.lock not found")
        return super().handle()


def install_prod_command_factory() -> InstallProdCommand:
    """Return a new InstallProdCommand instance."""
    return InstallProdCommand()


class InstallProdPlugin(ApplicationPlugin):
    """The plugin."""

    def activate(self, application: Application) -> None:
        """Activate the plugin."""
        application.command_loader.register_factory(
            "install-prod", install_prod_command_factory
        )
