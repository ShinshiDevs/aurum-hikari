from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import attrs
from hikari.api import special_endpoints as api
from hikari.interactions import ResponseType
from hikari.messages import MessageFlag
from hikari.undefined import UNDEFINED, UndefinedOr

if TYPE_CHECKING:
    from hikari.channels import TextableGuildChannel
    from hikari.embeds import Embed
    from hikari.files import Resourceish
    from hikari.guilds import GatewayGuild, PartialRole
    from hikari.impl import GatewayBot
    from hikari.interactions import CommandInteraction, ComponentInteraction, InteractionMember
    from hikari.messages import Message
    from hikari.snowflakes import SnowflakeishSequence
    from hikari.users import PartialUser, User

__all__: Sequence[str] = ("InteractionContext",)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class InteractionContext:
    """Represents a context for interaction handling."""

    interaction: CommandInteraction | ComponentInteraction = attrs.field(eq=False)
    """The interaction object associated with this context."""

    bot: GatewayBot = attrs.field(eq=False, repr=False)
    """The bot instance handling this interaction."""

    arguments: dict[str, Any] = attrs.field(factory=dict, eq=False)
    """
    The arguments provided to this interaction.

    Notes
    -----
        Only available for command interactions.
    """

    @property
    def user(self) -> User:
        """Returns the user who triggered this interaction."""
        return self.interaction.user

    @property
    def member(self) -> InteractionMember | None:
        """Returns the guild member who triggered this interaction, if applicable."""
        return self.interaction.member

    @property
    def guild(self) -> GatewayGuild | None:
        """Returns the guild where this interaction occurred, if any."""
        return self.interaction.get_guild()

    @property
    def channel(self) -> TextableGuildChannel | None:
        """Returns the channel where this interaction occurred."""
        return self.interaction.get_channel()

    async def defer(self, flags: MessageFlag = MessageFlag.NONE, *, ephemeral: bool = False) -> None:
        """Creates a deferred response to the interaction.

        Parameters
        ----------
        flags : MessageFlag, optional
            Optional flags to apply to the response. Default is MessageFlag.NONE.
        ephemeral : bool, optional
            Whether to make the response ephemeral (only visible to the interaction author).
            Similar to Clyde bot responses. Default is False.

        Returns
        -------
        None

        Notes
        -----
        The interaction token will remain valid for 15 minutes after deferring.
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
        component: UndefinedOr[api.ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[api.ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[SnowflakeishSequence[PartialUser] | bool] = UNDEFINED,
        role_mentions: UndefinedOr[SnowflakeishSequence[PartialRole] | bool] = UNDEFINED,
    ) -> None:
        """Creates an immediate response to the interaction.

        Parameters
        ----------
        content : Any
            The response content.
        flags : MessageFlag
            Response flags to apply.
        ephemeral : bool
            Makes response only visible to interaction author.
        attachment : Resourceish
            Single file attachment.
        attachments : Sequence[Resourceish]
            Multiple file attachments.
        component : api.ComponentBuilder
            Single message component.
        components : Sequence[api.ComponentBuilder]
            Multiple message components.
        embed : Embed
            Single embed.
        embeds : Sequence[Embed]
            Multiple embeds.
        mentions_everyone : bool
            Whether to allow @everyone/@here mentions.
        user_mentions : SnowflakeishSequence[PartialUser] or bool
            True to allow user pings, or list of allowed user mentions.
        role_mentions : SnowflakeishSequence[PartialRole] or bool
            True to allow role pings, or list of allowed role mentions.

        Returns
        -------
        None

        Notes
        -----
        Without deferring, interactions must be responded to within 3 seconds.
        For longer operations, use InteractionContext.defer first.

        If the interaction already has a response (default or deferred), you must use
        InteractionContext.edit_response instead or you'll receive an 'Already Acknowledged' error.
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
        component: UndefinedOr[api.ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[api.ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
    ) -> Message | None:
        """Modifies a previously sent interaction response.

        Parameters
        ----------
        content : Any
            The response content.
        attachment : Resourceish
            Single file attachment.
        attachments : Sequence[Resourceish]
            Multiple file attachments.
        component : api.ComponentBuilder
            Single message component.
        components : Sequence[api.ComponentBuilder]
            Multiple message components.
        embed : Embed
            Single embed.
        embeds : Sequence[Embed]
            Multiple embeds.

        Returns
        -------
        Message or None
            The modified message response if successful.
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
        """Deletes the response to this interaction if one exists."""
        await self.bot.rest.delete_interaction_response(
            application=self.interaction.application_id, token=self.interaction.token
        )
