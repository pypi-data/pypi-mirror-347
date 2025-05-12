from typing import TYPE_CHECKING, Optional

import discord
from starbot.core.bot import StarBot
from .cogsutils import CogsUtils
from .chat import humanize_bytes, inline_hum_list, no_colour_rich_markup
from .meta import format_info, get_vex_logger, out_of_date_check
from .__version__ import __version__
from . import cog
from .cog import Cog
from .context import Context
from .loop import Loop
from .menus import Menu, Reactions
from .sentry import SentryHelper
from .settings import Settings
from .shared_cog import SharedCog
from .views import (
    Buttons,
    ChannelSelect,
    ConfirmationAskView,
    Dropdown,
    MentionableSelect,
    Modal,
    RoleSelect,
    Select,
    UserSelect,
)  # NOQA
cog.SharedCog = SharedCog


__author__ = "Scarlet"
__version__ = __version__

__all__ = [
    "CogsUtils",
    "Loop",
    "SharedCog",
    "Cog",
    "Menu",
    "Context",
    "Settings",
    "SentryHelper",
    "ConfirmationAskView",
    "Buttons",
    "Dropdown",
    "Select",
    "ChannelSelect",
    "MentionableSelect",
    "RoleSelect",
    "UserSelect",
    "Modal",
    "Reactions",
    "humanize_bytes",
    "inline_hum_list",
    "no_colour_rich_markup",
    "format_info",
    "get_vex_logger",
    "out_of_date_check",
]