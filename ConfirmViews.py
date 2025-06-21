from discord.ui import View,button,Button
import discord

class ConfirmView(View):

    def __init__(self):
        super().__init__()
        self.value = None

    @button(label="Si",style=discord.ButtonStyle.success)
    async def yes(self,interaction: discord.Interaction,button:Button):
        self.value = True
        await interaction.response.defer()
        self.stop()

    @button(label="No", style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.defer()
        self.stop()
    