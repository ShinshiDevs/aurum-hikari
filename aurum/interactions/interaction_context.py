from __future__ import annotations

import typing
from dataclasses import dataclass

from hikari.interactions import ResponseType
from hikari.undefined import UNDEFINED

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.api import ComponentBuilder
    from hikari.embeds import Embed
    from hikari.files import Resourceish
    from hikari.guilds import PartialRole
    from hikari.impl import GatewayBot
    from hikari.interactions import (
        CommandInteraction,
        ComponentInteraction,
    )
    from hikari.messages import Message, MessageFlag
    from hikari.snowflakes import SnowflakeishSequence
    from hikari.undefined import UndefinedOr
    from hikari.users import PartialUser

    from aurum.client import Client
    from aurum.l10n import Locale


@dataclass(slots=True, kw_only=True)
class InteractionContext:
    interaction: CommandInteraction | ComponentInteraction

    bot: GatewayBot
    client: Client

    locale: Locale

    async def defer(self, flags: UndefinedOr[MessageFlag] = UNDEFINED) -> None:
        return await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            flags=flags,
            response_type=ResponseType.DEFERRED_MESSAGE_CREATE,
        )

    async def create_response(
        self,
        content: UndefinedOr[typing.Any] = UNDEFINED,
        *,
        flags: UndefinedOr[MessageFlag] = UNDEFINED,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[SnowflakeishSequence[PartialUser] | bool] = UNDEFINED,
        role_mentions: UndefinedOr[SnowflakeishSequence[PartialRole] | bool] = UNDEFINED,
    ) -> None:
        return await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            response_type=ResponseType.MESSAGE_CREATE,
            token=self.interaction.token,
            content=content,
            flags=flags,
            attachment=attachment,
            attachments=attachments,
            component=component,
            components=components,
            embed=embed,
            embeds=embeds,
            mentions_everyone=mentions_everyone,
            user_mentions=user_mentions,
            role_mentions=role_mentions,
        )

    async def edit_response(
        self,
        content: UndefinedOr[typing.Any] = UNDEFINED,
        *,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
    ) -> Message | None:
        return await self.bot.rest.edit_interaction_response(
            application=self.interaction.application_id,
            token=self.interaction.token,
            content=content,
            attachment=attachment,
            attachments=attachments,
            component=component,
            components=components,
            embed=embed,
            embeds=embeds,
        )

    async def delete_response(self) -> None:
        await self.bot.rest.delete_interaction_response(
            application=self.interaction.application_id, token=self.interaction.token
        )
