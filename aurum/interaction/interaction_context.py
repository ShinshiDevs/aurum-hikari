from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict

from hikari.api import ComponentBuilder
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.files import Resourceish
from hikari.guilds import GatewayGuild, PartialRole
from hikari.impl.gateway_bot import GatewayBot
from hikari.interactions import (
    CommandInteraction,
    CommandInteractionOption,
    ComponentInteraction,
    InteractionChannel,
    InteractionMember,
    ResponseType,
)
from hikari.messages import Message, MessageFlag
from hikari.snowflakes import SnowflakeishSequence
from hikari.undefined import UNDEFINED, UndefinedOr
from hikari.users import PartialUser

from aurum.i18n import ILocalizationEngine

if TYPE_CHECKING:
    from aurum.impl.client import Client

EMPTY_DICT: Dict[str, Any] = {}
ARGUMENT_TYPES = (
    InteractionMember
    | InteractionChannel
    | PartialUser
    | PartialRole
    | Resourceish
    | str
    | int
    | float
    | bool
    | None
)


@dataclass(kw_only=True, slots=True)
class InteractionContext:
    interaction: CommandInteraction | ComponentInteraction

    bot: GatewayBot
    client: Client
    l10n: ILocalizationEngine

    arguments: Dict[str, Any] = field(default_factory=dict)

    _has_created_response: bool = False
    _has_deferred_response: bool = False

    @property
    def locale(self) -> None:
        return self.l10n.get_locale(
            self.interaction.locale or self.interaction.guild_locale
        )

    @property
    def guild(self) -> GatewayGuild | None:
        return self.interaction.get_guild()

    @property
    def user(self) -> PartialUser | None:
        return self.interaction.user

    @property
    def member(self) -> InteractionMember | None:
        return self.interaction.member

    async def defer(self, flags: UndefinedOr[MessageFlag] = UNDEFINED) -> None:
        await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            flags=flags,
            response_type=ResponseType.DEFERRED_MESSAGE_CREATE,
        )
        self._has_deferred_response = True

    async def create_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        flags: UndefinedOr[MessageFlag] = UNDEFINED,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[
            SnowflakeishSequence[PartialUser] | bool
        ] = UNDEFINED,
        role_mentions: UndefinedOr[
            SnowflakeishSequence[PartialRole] | bool
        ] = UNDEFINED,
    ) -> None:
        if self._has_deferred_response:
            await self.edit_response(
                content=content,
                attachment=attachment,
                attachments=attachments,
                component=component,
                components=components,
                embed=embed,
                embeds=embeds,
            )
            return
        await self.bot.rest.create_interaction_response(
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
        return

    async def edit_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
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

    def resolve_command_option(
        self, option: CommandInteractionOption
    ) -> ARGUMENT_TYPES:
        if not self.interaction.resolved:
            return option.value
        match option.type:
            case OptionType.USER:
                return self.interaction.resolved.members.get(
                    option.value,  # type: ignore
                    self.interaction.resolved.users.get(option.value),  # type: ignore
                )
            case OptionType.CHANNEL:
                return self.interaction.resolved.channels.get(option.value)  # type: ignore
            case OptionType.ROLE:
                return self.interaction.resolved.roles.get(option.value)  # type: ignore
            case OptionType.MENTIONABLE:
                return self.interaction.resolved.users.get(
                    option.value,  # type: ignore
                    self.interaction.resolved.roles.get(option.value),  # type: ignore
                )
            case OptionType.ATTACHMENT:
                return self.interaction.resolved.attachments.get(option.value)  # type: ignore
            case _:
                return option.value
