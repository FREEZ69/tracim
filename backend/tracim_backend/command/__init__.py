# -*- coding: utf-8 -*-
import argparse
import sys
import typing
from copy import deepcopy

import transaction
from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager
from pyramid.paster import get_appsettings
from sqlalchemy.orm import Session

from tracim_backend import CFG
from tracim_backend.exceptions import InvalidSettingFile
from tracim_backend.lib.utils.utils import DEFAULT_TRACIM_CONFIG_FILE
from tracim_backend.models.setup_models import get_engine
from tracim_backend.models.setup_models import get_session_factory
from tracim_backend.models.setup_models import get_tm_session


class TracimCLI(App):
    def __init__(self) -> None:
        super(TracimCLI, self).__init__(
            description='TracimCli',
            version='0.1',
            command_manager=CommandManager('tracimcli'),
            deferred_help=True,
            )

    def initialize_app(self, argv) -> None:
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd) -> None:
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err) -> None:
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = TracimCLI()
    return myapp.run(argv)


if __name__ == "__main__":
    main()


class AppContextCommand(Command):
    """
    Command who initialize app context at beginning of take_action method.
    """
    auto_setup_context = True
    default_settings = {}

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        super(AppContextCommand, self).take_action(parsed_args)
        if self.auto_setup_context:
            config_uri = parsed_args.config_file
            settings = self.setup_settings(config_uri)
            engine = get_engine(settings)
            app_config = CFG(settings)
            app_config.configure_filedepot()
            session_factory = get_session_factory(engine)
            session = get_tm_session(session_factory, transaction.manager)
            try:
                self.take_app_action(parsed_args, app_config, session)
            except Exception as exc:
                session.rollback()
                transaction.abort()
                raise exc
            finally:
                transaction.commit()
                session.close_all()

    def setup_settings(self, config_uri) -> typing.Dict[str, str]:
        settings = self.default_settings
        local_settings = get_appsettings(config_uri)
        global_settings = local_settings.global_conf
        settings.update(global_settings)
        settings.update(local_settings)
        if 'sqlalchemy.url' not in settings or not settings[
            'sqlalchemy.url']:
            raise InvalidSettingFile(
                'Wrong or empty sqlalchemy database url,'
                'check config file')
        return settings

    def take_app_action(
            self,
            parsed_args: argparse.Namespace,
            app_config: CFG,
            session: Session,
    ):
        pass

    def get_parser(self, prog_name: str) -> argparse.ArgumentParser:
        parser = super(AppContextCommand, self).get_parser(prog_name)

        parser.add_argument(
            "-c",
            "--config",
            help='application config file to read (default: {})'.format(
                DEFAULT_TRACIM_CONFIG_FILE
            ),
            dest='config_file',
            default=DEFAULT_TRACIM_CONFIG_FILE,
        )
        return parser

class Extender(argparse.Action):
    """
    Copied class from http://stackoverflow.com/a/12461237/801924
    """
    def __call__(self, parser, namespace, values, option_strings=None):
        # Need None here incase `argparse.SUPPRESS` was supplied for `dest`
        dest = getattr(namespace, self.dest, None)
        # print dest,self.default,values,option_strings
        if not hasattr(dest, 'extend') or dest == self.default:
            dest = []
            setattr(namespace, self.dest, dest)
            # if default isn't set to None, this method might be called
            # with the default as `values` for other arguements which
            # share this destination.
            parser.set_defaults(**{self.dest: None})
        try:
            dest.extend(values)
        except ValueError:
            dest.append(values)
