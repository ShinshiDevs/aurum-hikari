from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Dict

import attrs
from hikari import AutocompleteInteraction
from hikari.api import ComponentBuilder
from hikari.channels import PartialChannel
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.files import Resourceish
from hikari.guilds import GatewayGuild, PartialRole
from hikari.interactions import (
    CommandInteraction,
    CommandInteractionOption,
    ComponentInteraction,
    InteractionMember,
    ResponseType,
)
from hikari.messages import Message, MessageFlag
from hikari.snowflakes import Snowflake, SnowflakeishSequence
from hikari.traits import GatewayBotAware
from hikari.undefined import UNDEFINED, UndefinedOr
from hikari.users import PartialUser

from aurum.commands.app_command import AppCommand

if TYPE_CHECKING:
    from aurum.client import Client

__all__: Sequence[str] = ("InteractionContext", "AutocompleteContext")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class InteractionContext:
    """Represents an interaction context.

    Attributes:
        interaction (CommandInteraction | ComponentInteraction): The interaction of context.
        bot (GatewayBotAware): The instance of the bot.
        client (Client): The client.
        command (AppCommand): Command of interaction.
            !!! note
                Available only for commands.
        locale (Any): An any locale object for the interaction.
        arguments (Dict[str, Any]): Arguments to the interaction.
            !!! note
                Available only for commands.
    """

    interaction: CommandInteraction | ComponentInteraction = attrs.field(eq=False)

    bot: GatewayBotAware = attrs.field(eq=False, repr=False)
    client: Client = attrs.field(eq=False, repr=False)

    command: AppCommand | None = attrs.field(eq=False, default=None, repr=False)
    locale: Any = attrs.field(eq=False)
    arguments: Dict[str, Any] = attrs.field(factory=dict, eq=False)

    @property
    def user(self) -> PartialUser:
        """User of the interaction."""
        return self.interaction.user

    @property
    def member(self) -> InteractionMember | None:
        """Member of the interaction."""
        return self.interaction.member

    @property
    def guild(self) -> GatewayGuild | None:
        """Guild of the interaction."""
        return self.interaction.get_guild()

    @property
    def channel(self) -> PartialChannel | None:
        """Channel of the interaction."""
        return self.interaction.get_channel()

    async def defer(
        self, flags: MessageFlag = MessageFlag.NONE, *, ephemeral: bool = False
    ) -> None:
        """Create a deferred response to the interaction.

        Note:
            The interaction will be available in the next 15 minutes.

        Arguments:
            flags (MessageFlag): An optional flags for response.
            ephemeral (bool): An optional flag to create ephemeral response.
                Ephemeral messages that only the author of the interaction can see.
                They are similar to Clyde's messages.
        """
        if ephemeral:
            flags |= MessageFlag.EPHEMERAL
        return await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            flags=flags,
            response_type=ResponseType.DEFERRED_MESSAGE_CREATE,
        )

    async def create_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        flags: MessageFlag = MessageFlag.NONE,
        ephemeral: bool = False,
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
        """Create a response to the interaction.

        Note:
            - If the interaction appears and is not deferred, it will be available for the next three seconds.
                After that, it will no longer be available.
                If your callback takes more than 3 seconds, please use `InteractionContext.defer` to delay the response.
            - If the interaction already has a response: default, deferred, you has to `InteractionContext`
                or you'll catch a error `Interaction was already acknowledged` from Discord API.

        Arguments:
            content (Any): The content of response.
            flags (MessageFlag): An optional flags of response.
            ephemeral (bool): An optional flag to create ephemeral response.
                Ephemeral messages that only the author of the interaction can see.
                They are similar to Clyde's messages.
            attachment (Resourceish): A single attachment of response.
            attachments (Sequence[Resourceish]): A list of attachments of response.
            component (ComponentBuilder): A single component builder of response.
            components (Sequence[ComponentBuilder]): A list of component builders of response.
            embed (Embed): A single embed of response.
            embeds (Sequence[Embed]): A list of embeds of response.
            mentions_everyone (bool): Allows `@everyone` and `@here` to ping users if set to `True`.
            user_mentions:
                - Allows to ping users is set to `True`.
                - A list of users that can be pinged in response.
            role_mentions:
                - Allows to ping roles is set to `True`.
                - A list of roles that can be pinged in response.
        """
        if ephemeral:
            flags |= MessageFlag.EPHEMERAL
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
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
    ) -> Message | None:
        """Edit the response of the interaction.

        Arguments:
            content (Any): The content of response.
            attachment (Resourceish): A single attachment of response.
            attachments (Sequence[Resourceish]): A list of attachments of response.
            component (ComponentBuilder): A single component builder of response.
            components (Sequence[ComponentBuilder]): A list of component builders of response.
            embed (Embed): A single embed of response.
            embeds (Sequence[Embed]): A list of embeds of response.
        """
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
        """Delete the interaction's response."""
        await self.bot.rest.delete_interaction_response(
            application=self.interaction.application_id, token=self.interaction.token
        )

    def resolve_command_argument(self, option: CommandInteractionOption) -> Any:
        if not self.interaction.resolved or not isinstance(option.value, Snowflake):
            return option.value
        match option.type:
            case OptionType.USER:
                return self.interaction.resolved.members.get(
                    option.value,
                    self.interaction.resolved.users.get(option.value),
                )
            case OptionType.CHANNEL:
                return self.interaction.resolved.channels.get(option.value)
            case OptionType.ROLE:
                return self.interaction.resolved.roles.get(option.value)
            case OptionType.MENTIONABLE:
                return self.interaction.resolved.members.get(
                    option.value,
                    self.interaction.resolved.roles.get(option.value),
                )
            case OptionType.ATTACHMENT:
                return self.interaction.resolved.attachments.get(option.value)
            case _:
                return None


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class AutocompleteContext:
    """Represents an autocomplete interaction context.

    Attributes:
        interaction (AutocompleteInteraction): The interaction of context.
        bot (GatewayBotAware): The instance of the bot.
        client (Client): The client.
        locale (Any): An any locale object for the interaction.
    """
    interaction: AutocompleteInteraction = attrs.field(eq=False)

    bot: GatewayBotAware = attrs.field(eq=False, repr=False)
    client: Client = attrs.field(eq=False, repr=False)

    locale: Any = attrs.field(eq=False)
