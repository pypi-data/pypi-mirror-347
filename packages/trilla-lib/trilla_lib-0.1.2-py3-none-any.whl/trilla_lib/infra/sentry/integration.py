import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from typing import Literal
from trilla_lib.infra.sentry.settings import sentry_settings



def init_sentry(
    plugins: set[Literal['fastapi', 'sqlalchemy', 'redis', 'celery']],
) -> None:

    if not sentry_settings.enabled:
        return

    plugins_map = {
        'fastapi': FastApiIntegration(),
        'sqlalchemy': SqlalchemyIntegration(),
        'redis': RedisIntegration(),
        'celery': CeleryIntegration(),
    }

    sentry_sdk.init(
        dsn=sentry_settings.dsn,
        environment=sentry_settings.environment,
        release=sentry_settings.release,
        traces_sample_rate=sentry_settings.traces_sample_rate,
        integrations=[
            plugin
            for plugin_key, plugin in plugins_map.items()
            if plugin_key in plugins
        ],
        debug=sentry_settings.debug,
    )
