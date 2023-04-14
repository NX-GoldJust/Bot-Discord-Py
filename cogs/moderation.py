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
        


async def setup(bot):
    await bot.add_cog(Moderation(bot))
