import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @app_commands.command(name="ban", description="Bannir un membre")
    @app_commands.describe(user = "Qui ?")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(raison = "Pouquoi ?")
    async def ban(self, interaction: discord.Interaction, user : discord.User, raison: str):    
        await interaction.guild.ban(user, reason = raison)
        embed = discord.Embed(title = "***Bannissement***", description = "Ban Effectué", color=discord.Colour.red())

        embed.add_field(name = "Membre banni", value =f"Nom: {user.name}\nId: {user.id}", inline = False)
        embed.add_field(name = "Raison", value = raison, inline = False)
        embed.add_field(name = "Modérateur", value = interaction.user.mention, inline = False)
        await interaction.response.send_message(embed=embed)
    


    @app_commands.command(name="unban", description="Débannir un membre")
    @app_commands.describe(id = "Qui ? Mettez son ID")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(raison = "Pouquoi ?")
    async def unban(self, i: discord.Interaction, id : str, raison: str):    
        try:
            id = int(id)
            user = await self.bot.fetch_user(id)
            await i.guild.unban(user)
            from datetime import datetime
            embed = discord.Embed(title="Unban", timestamp=datetime.now(), color=discord.Colour.red())
            embed.add_field(name="Membre", value=f"Nom: {user.name}\nId: {user.id}", inline=False)
            embed.add_field(name="Raison", value=raison, inline=False)
            embed.add_field(name="Modérateur", value=i.user.mention, inline=False)

            
            await i.response.send_message(embed=embed)
            
        except:
            from datetime import datetime
            embed = discord.Embed(title="Erreur", timestamp=datetime.now(), description="Mettez un id valide. Ou cette utilisateur n'est pas banni.")
            await i.response.send_message(embed=embed)
        
        
    @app_commands.command(name='kick', description='Virer une personne')
    @app_commands.describe(user = "Qui ?")
    @app_commands.describe(raison = "Pourquoi ?")
    @app_commands.default_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, user: discord.User, raison: str):


        await interaction.guild.kick(user, reason = raison)
        embed = discord.Embed(title="Kick", timestamp=datetime.now())
        embed.add_field(name="Membre", value=f"Nom: {user.name}\nId: {user.id}", inline=False)
        embed.add_field(name="Raison", value=raison, inline=False)
        embed.add_field(name="Modérateur", value=interaction.user.mention, inline=False)
        await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name="clear", description="Supprimé des messages")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.describe(nombre="Combien ?")
    async def clear(self, interaction: discord.Interaction, nombre: int=None):
        await interaction.response.defer(ephemeral=True)
        amount = nombre
        if amount:
            
            await interaction.channel.purge(limit=amount)
            embed=discord.Embed(title="Clear", description=f"{amount} messages ont est bien était supprimés")
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        else:
            channel = interaction.channel
            new_channel = await channel.clone()
            ancien_position = channel.position
            await channel.delete()
            await new_channel.edit(position=ancien_position)
            
            
            
            embed = discord.Embed(title="Clear", description="Le salon a bien été recréé.")
            await new_channel.send(embed=embed, delete_after=10, content=interaction.user.mention)







    @app_commands.command(name="mute", description="Mute une personne")
    @app_commands.describe(user="Qui")
    @app_commands.choices(temps=[
        app_commands.Choice(name="1 Minute", value="0"),
        app_commands.Choice(name="5 Minutes", value="1"),
        app_commands.Choice(name="10 Minutes", value="2"),
        app_commands.Choice(name="30 Minutes", value="3"),
        app_commands.Choice(name="45 Minutes", value="4"),
        app_commands.Choice(name="1 Heure", value="5"),
        app_commands.Choice(name="12 Heures", value="6"),
        app_commands.Choice(name="1 Jour", value="7"),
        app_commands.Choice(name="3 Jour", value="8"),
        app_commands.Choice(name="1 Semaine", value="9")
        ])
    @app_commands.describe(raison="Pourquoi ?")
    @app_commands.default_permissions(mute_members=True)
    async def mute(self, i: discord.Interaction, user: discord.Member, temps: app_commands.Choice[str], raison: str):
        from datetime import timedelta, datetime
         
        t = int(temps.value)
        min = 0
        heure = 0
        day = 0
        if t == 0:
            min += 1
        elif t == 1:
            min += 5
        elif t == 2:
            min += 10
            
        elif t == 3:
            min += 30
            
        elif t == 4:
            min += 45
            
        elif t == 5:
            heure += 1
        elif t == 6:
            heure += 12
        elif t == 7:
            day += 1
        elif t == 8:
            day += 3
        elif t == 9:
            day += 7

        if i.user.top_role>user.top_role:
            
            temp = timedelta(minutes=min, hours=heure, days=day)
            embed = discord.Embed(title="Mute", timestamp=datetime.now(), color=discord.Colour.red())
            embed.add_field(name="User", value=f"Nom: {user.name}\nId: {user.id}", inline=False)
            
            time = int(int(datetime.now().timestamp())+int(temp.total_seconds()))
            embed.add_field(name="Temps", value=f"Date d'unmute: <t:{time}>\n\nTemps restant: <t:{time}:R>")
            embed.add_field(name="Raison", value=raison, inline=False)
            embed.add_field(name="Modérateur", value=i.user.mention+f" ({i.user.name})", inline=False)
            embed.add_field(name="Serveur", value=i.guild.name, inline=False)
            
            await user.timeout(temp)
            await i.response.send_message(embed=embed)
        else:
            await i.response.send_message("Vous devez avoir un role plus haut !!", ephemeral=True)
         
    @app_commands.command(name="unmute", description="Unmute un membre")
    @app_commands.default_permissions(mute_members=True)
    @app_commands.describe(user="Qui ?")
    async def unmute(self, i: discord.Interaction, user: discord.Member):
        if i.user.top_role > user.top_role:
            
            if user.is_timed_out():
                from datetime import timedelta
                await user.timeout(timedelta(seconds=1))
                await i.response.send_message(f"Le membre {user.mention} a été unmute")
            else:
                await i.response.send_message("Ce membre n'est pas mute !", ephemeral=True)
        else:
            await i.response.send_message("Vous devez avoir un role plus haut !!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
