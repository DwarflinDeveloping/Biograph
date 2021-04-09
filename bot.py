from discord.ext import commands
from discord import Intents, Embed
import os

bot = commands.Bot(command_prefix="%bio ", intents=Intents.all())
bot.help_command = None


def generate_help_embed(user):
    help_embed = Embed(
        title=
        "Usage help",
        description=
        "**Variants:**\n"
        " • `%bio u set \"<biography>\"`\n"
        " • `%bio u get <username/user id/user mention>`\n\n"
        "**The principle:**\n"
        "With the help of this bot, each user and each server can define "
        "custom texts that can be queried up by other users.\n\n"
        "You can find detailed instructions with pictures [here]"
        "(https://github.com/DwarflinDeveloping/Linker/blob/main/README.md)"
    )
    help_embed.set_footer(text=f"Request of {user}", icon_url=user.avatar_url)

    return help_embed


@bot.listen("on_message")
async def test(message):from discord.ext import commands
from discord import Intents, Embed
import os

bot = commands.Bot(command_prefix="%bio ", intents=Intents.all())
bot.help_command = None


def generate_help_embed(user):
    help_embed = Embed(
        title=
        "Usage help",
        description=
        "**Variants:**\n"
        " • `%bio u set \"<biography>\"`\n"
        " • `%bio u get <username/user id/user mention>`\n\n"
        "**The principle:**\n"
        "With the help of this bot, each user and each server can define "
        "custom texts that can be queried up by other users.\n\n"
        "You can find detailed instructions with pictures [here]"
        "(https://github.com/DwarflinDeveloping/Linker/blob/main/README.md)"
    )
    help_embed.set_footer(text=f"Request of {user}", icon_url=user.avatar_url)

    return help_embed


@bot.listen("on_message")
async def test(message):
    if message.content == "%bio":
        await message.channel.send(embed=generate_help_embed(message.author))


@bot.listen("on_ready")
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def u(ctx, *args):
    if len(args) == 0:
        await ctx.send(embed=generate_help_embed(ctx.author))
        return

    if args[0] == "get" or args[0] == "query":
        from utils import ReturnCodes
        if len(args) == 1:
            get_family_process = get_family(ctx.author.id)
        elif len(args) == 2:
            try:
                get_family_process = get_family(int(args[1]))
            except ValueError:
                if args[1].startswith("<@!"):
                    try:
                        get_family_process = get_family(int(args[1].split("<@!")[1].split(">")[0]))
                    except IndexError:
                        from embeds import create_custom_embed
                        from discord import Colour
                        await ctx.send(
                            embed=create_custom_embed(
                                    embed_message=
                                    "You have to enter either the mention or the ID of "
                                    "the user whose biography you want to know.",
                                    user=ctx.author,
                                    colour=Colour.dark_red()
                                )
                        )
                        return
                else:
                    from embeds import create_custom_embed
                    from discord import Colour
                    await ctx.send(
                        embed=create_custom_embed(
                            embed_message=
                            "You have to enter either the mention or the ID of "
                            "the user whose biography you want to know.",
                            user=ctx.author,
                            colour=Colour.dark_red()
                        )
                    )
                    return

        else:
            await ctx.send(embed=generate_help_embed(ctx.author))
            return

        if get_family_process == ReturnCodes.NOT_FOUND:
            from embeds import create_custom_embed
            from discord import Colour
            await ctx.send(
                embed=create_custom_embed(
                    embed_message="This user no biography.",
                    user=ctx.author,
                    colour=Colour.dark_red()
                )
            )
        else:
            from embeds import create_custom_embed
            from discord import Colour
            await ctx.send(
                embed=create_custom_embed(
                    embed_title="biography",
                    embed_message=f"This users biography is:```{get_family_process}```",
                    user=ctx.author,
                    colour=Colour.blue()
                )
            )

    elif args[0] == "set":
        from utils import get_confirmation, ReturnCodes
        from embeds import create_custom_embed
        from discord import Colour
        confirmation_message = await ctx.send(
            embed=create_custom_embed(
                embed_title=
                "Confirmation",
                embed_message=
                "You are about to change your biography.\n"
                "Do you want to continue?",
                user=ctx.author,
                colour=Colour.blue()
            )
        )

        confirmation = await get_confirmation(confirmation_message, ctx.author, bot)
        if confirmation == ReturnCodes.SUCCESS:
            biography = ""
            for arg in args:
                if arg != "set":
                    biography += arg + " "
            set_process = set_family(ctx.author.id, biography)
            if set_process == ReturnCodes.SUCCESS:
                user_family_file = open(f"data/user_biographies/{ctx.author.id}.txt", "r")
                await ctx.send(
                    embed=create_custom_embed(
                        embed_title="Success",
                        embed_message=f"Your biography has been changed to```{user_family_file.read()}```",
                        user=ctx.author,
                        colour=Colour.dark_green()
                    )
                )
                user_family_file.close()
            elif set_process == ReturnCodes.VARIABLE_INVAILED:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="You didn't use `%ARTICLE%` in the biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )
            elif set_process == ReturnCodes.NO_CHANGES:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="There are no changes in the biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )
            elif set_process == ReturnCodes.OTHER_ERROR:
                from embeds import handle_error
                await ctx.send(embed=handle_error(set_process, ctx.author))
        elif confirmation == ReturnCodes.CANCELLED:
            await confirmation_message.delete()

        elif confirmation == ReturnCodes.TIMEOUT_ERROR:
            await confirmation.delete()

        elif confirmation == ReturnCodes.OTHER_ERROR:
            from embeds import handle_error
            await ctx.send(embed=handle_error(confirmation, ctx.author))
    elif args[0] == "clear" or args[0] == "delete":
        from utils import get_confirmation, ReturnCodes
        from embeds import create_custom_embed
        from discord import Colour
        confirmation_message = await ctx.send(
            embed=create_custom_embed(
                embed_title=
                "Confirmation",
                embed_message=
                "You are about to clear your biography.\n"
                "Do you want to continue?",
                user=ctx.author,
                colour=Colour.blue()
            )
        )

        confirmation = await get_confirmation(confirmation_message, ctx.author, bot)

        if confirmation == ReturnCodes.SUCCESS:
            clear_process = clear_family(ctx.author.id)

            if clear_process == ReturnCodes.SUCCESS:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_title="Success",
                        embed_message=f"Your biography has been successfully reset.",
                        user=ctx.author,
                        colour=Colour.dark_green()
                    )
                )

            elif clear_process == ReturnCodes.NOT_FOUND:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="You have no biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )

        elif confirmation == ReturnCodes.CANCELLED or confirmation == ReturnCodes.TIMEOUT_ERROR:
            await confirmation_message.delete()

        elif confirmation == ReturnCodes.OTHER_ERROR:
            from embeds import handle_error
            await ctx.send(embed=handle_error(confirmation, ctx.author))
    else:
        from commands.help import send_userfamily_help
        await send_userfamily_help(ctx)
    return


def set_family(user_id, description):
    from utils import ReturnCodes

    try:
        from utils import ReturnCodes

        import os
        if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
            user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "r")
            if description == user_biography_file.read():
                user_biography_file.close()
                return ReturnCodes.NO_CHANGES
            user_biography_file.close()

        user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "w")
        user_biography_file.write(description)
        user_biography_file.close()

        return ReturnCodes.SUCCESS
    except:
        return ReturnCodes.OTHER_ERROR


def clear_family(user_id):
    from utils import ReturnCodes

    import os
    if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
        os.remove(f"data/user_biographies/{str(user_id)}.txt")
        return ReturnCodes.SUCCESS
    else:
        return ReturnCodes.NOT_FOUND


def get_family(user_id):
    from utils import ReturnCodes
    import os

    if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
        user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "r")
        user_biography = user_biography_file.read()
        user_biography_file.close()
        return user_biography
    else:
        return ReturnCodes.NOT_FOUND


bot.run(os.getenv("TOKEN"))

    if message.content == "%bio":
        await message.channel.send(embed=generate_help_embed(message.author))


@bot.listen("on_ready")
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def u(ctx, *args):
    if len(args) == 0:
        await ctx.send(embed=generate_help_embed(ctx.author))
        return

    if args[0] == "get" or args[0] == "query":
        from utils import ReturnCodes
        if len(args) == 1:
            get_family_process = get_family(ctx.author.id)
        elif len(args) == 2:
            try:
                get_family_process = get_family(int(args[1]))
            except ValueError:
                if args[1].startswith("<@!"):
                    try:
                        get_family_process = get_family(int(args[1].split("<@!")[1].split(">")[0]))
                    except IndexError:
                        from embeds import create_custom_embed
                        from discord import Colour
                        await ctx.send(
                            embed=create_custom_embed(
                                    embed_message=
                                    "You have to enter either the mention or the ID of "
                                    "the user whose biography you want to know.",
                                    user=ctx.author,
                                    colour=Colour.dark_red()
                                )
                        )
                        return
                else:
                    from embeds import create_custom_embed
                    from discord import Colour
                    await ctx.send(
                        embed=create_custom_embed(
                            embed_message=
                            "You have to enter either the mention or the ID of "
                            "the user whose biography you want to know.",
                            user=ctx.author,
                            colour=Colour.dark_red()
                        )
                    )
                    return

        else:
            await ctx.send(embed=generate_help_embed(ctx.author))
            return

        if get_family_process == ReturnCodes.NOT_FOUND:
            from embeds import create_custom_embed
            from discord import Colour
            await ctx.send(
                embed=create_custom_embed(
                    embed_message="This user no biography.",
                    user=ctx.author,
                    colour=Colour.dark_red()
                )
            )
        else:
            from embeds import create_custom_embed
            from discord import Colour
            await ctx.send(
                embed=create_custom_embed(
                    embed_title="biography",
                    embed_message=f"This users biography is:```{get_family_process}```",
                    user=ctx.author,
                    colour=Colour.blue()
                )
            )

    elif args[0] == "set":
        from utils import get_confirmation, ReturnCodes
        from embeds import create_custom_embed
        from discord import Colour
        confirmation_message = await ctx.send(
            embed=create_custom_embed(
                embed_title=
                "Confirmation",
                embed_message=
                "You are about to change your biography.\n"
                "Do you want to continue?",
                user=ctx.author,
                colour=Colour.blue()
            )
        )

        confirmation = await get_confirmation(confirmation_message, ctx.author, bot)
        if confirmation == ReturnCodes.SUCCESS:
            biography = ""
            for arg in args:
                if arg != "set":
                    biography += arg + " "
            set_process = set_family(ctx.author.id, biography)
            if set_process == ReturnCodes.SUCCESS:
                user_family_file = open(f"data/user_biographies/{ctx.author.id}.txt", "r")
                await ctx.send(
                    embed=create_custom_embed(
                        embed_title="Success",
                        embed_message=f"Your biography has been changed to```{user_family_file.read()}```",
                        user=ctx.author,
                        colour=Colour.dark_green()
                    )
                )
                user_family_file.close()
            elif set_process == ReturnCodes.VARIABLE_INVAILED:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="You didn't use `%ARTICLE%` in the biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )
            elif set_process == ReturnCodes.NO_CHANGES:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="There are no changes in the biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )
            elif set_process == ReturnCodes.OTHER_ERROR:
                from embeds import handle_error
                await ctx.send(embed=handle_error(set_process, ctx.author))
        elif confirmation == ReturnCodes.CANCELLED:
            await confirmation_message.delete()

        elif confirmation == ReturnCodes.TIMEOUT_ERROR:
            await confirmation.delete()

        elif confirmation == ReturnCodes.OTHER_ERROR:
            from embeds import handle_error
            await ctx.send(embed=handle_error(confirmation, ctx.author))
    elif args[0] == "clear" or args[0] == "delete":
        from utils import get_confirmation, ReturnCodes
        from embeds import create_custom_embed
        from discord import Colour
        confirmation_message = await ctx.send(
            embed=create_custom_embed(
                embed_title=
                "Confirmation",
                embed_message=
                "You are about to clear your biography.\n"
                "Do you want to continue?",
                user=ctx.author,
                colour=Colour.blue()
            )
        )

        confirmation = await get_confirmation(confirmation_message, ctx.author, bot)

        if confirmation == ReturnCodes.SUCCESS:
            clear_process = clear_family(ctx.author.id)

            if clear_process == ReturnCodes.SUCCESS:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_title="Success",
                        embed_message=f"Your biography has been successfully reset.",
                        user=ctx.author,
                        colour=Colour.dark_green()
                    )
                )

            elif clear_process == ReturnCodes.NOT_FOUND:
                await ctx.send(
                    embed=create_custom_embed(
                        embed_message="You have no biography.",
                        user=ctx.author,
                        colour=Colour.dark_red()
                    )
                )

        elif confirmation == ReturnCodes.CANCELLED or confirmation == ReturnCodes.TIMEOUT_ERROR:
            await confirmation_message.delete()

        elif confirmation == ReturnCodes.OTHER_ERROR:
            from embeds import handle_error
            await ctx.send(embed=handle_error(confirmation, ctx.author))
    else:
        from commands.help import send_userfamily_help
        await send_userfamily_help(ctx)
    return


def set_family(user_id, description):
    from utils import ReturnCodes

    try:
        from utils import ReturnCodes

        import os
        if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
            user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "r")
            if description == user_biography_file.read():
                user_biography_file.close()
                return ReturnCodes.NO_CHANGES
            user_biography_file.close()

        user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "w")
        user_biography_file.write(description)
        user_biography_file.close()

        return ReturnCodes.SUCCESS
    except:
        return ReturnCodes.OTHER_ERROR


def clear_family(user_id):
    from utils import ReturnCodes

    import os
    if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
        os.remove(f"data/user_biographies/{str(user_id)}.txt")
        return ReturnCodes.SUCCESS
    else:
        return ReturnCodes.NOT_FOUND


def get_family(user_id):
    from utils import ReturnCodes
    import os

    if os.path.isfile(f"data/user_biographies/{str(user_id)}.txt"):
        user_biography_file = open(f"data/user_biographies/{str(user_id)}.txt", "r")
        user_biography = user_biography_file.read()
        user_biography_file.close()
        return user_biography
    else:
        return ReturnCodes.NOT_FOUND


bot.run(os.getenv("TOKEN"))
