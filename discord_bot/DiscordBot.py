# Name: Discord Bot
# Author: Robert Ciborowski
# Date: 15/04/2020
# Description: Outputs updated regarding pump and dumps to Discord.


import asyncio
from asyncio import AbstractEventLoop
from typing import Dict

import discord
import csv
import threading as th
import json

from events.Event import Event
from events.EventListener import EventListener
from stock_data.StockDataObtainer import StockDataObtainer


class DiscordBot(discord.Client, EventListener):
    TOKEN: str
    status: str
    USTrackedIndices: Dict[str, str]
    CATrackedIndices: Dict[str, str]

    _helpString: str
    _stockUpdatesID: int
    _runThread: th.Thread
    _loop: AbstractEventLoop
    _obtainer: StockDataObtainer
    _priceFormat: str

    def __init__(self, obtainer: StockDataObtainer, propertiesFileLocation="bot_properties.json",
                 secretPropertiesFileLocation="bot_secret_properties.json", priceFormat="2"):
        super().__init__()
        self._update_properties(propertiesFileLocation)
        self._update_secret_properties(secretPropertiesFileLocation)
        self._setupHelpString()
        self._loop = asyncio.get_event_loop()
        self._obtainer = obtainer
        self._priceFormat = priceFormat

    def runOnSeperateThread(self):
        self._runThread = th.Thread(target=self._run, daemon=False)
        self._runThread.start()

    def stopRunning(self):
        asyncio.run_coroutine_threadsafe(self.close(), self._loop)

    def _run(self):
        super().run(self.TOKEN)

    async def on_ready(self):
        print(str(self.user) + " is online!")
        await self.change_presence(activity=discord.Game(self.status))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content[0] == "$":
            await self._processCommand(message)

    async def on_member_remove(member):
        """
        Prints to terminal when a member in discord leaves the server
        :param member: member object
        """
        print(f'{member} has left the server')
        # await client.send(str(member) + " has left.")

    def onEvent(self, event: Event):
        asyncio.run_coroutine_threadsafe(self._onEvent(event), self._loop)

    async def _onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            channel = self.get_channel(self._stockUpdatesID)
            await channel.send("Pump & dump detected! " + event.data["Ticker"]
                               + " at {:.7f}".format(event.data["Price"]))

    async def _processCommand(self, message):
        filteredContent = message.content[1:len(message.content)]

        if filteredContent == 'ping':
            await message.channel.send(
                f'Pong! Latency: {round(self.latency * 1000)}ms')
        elif filteredContent.startswith("market"):
            await self._onMarketCommand(message, filteredContent)
        elif filteredContent == "help":
            await message.channel.send(str(message.author.mention) + " needs " \
                    "help.\n " + self._helpString)

    def _update_secret_properties(self, propertiesPath: str) -> str:
        try:
            with open(propertiesPath, mode='r') as file:
                data = json.load(file)
                self.TOKEN = data["Token"]
                self._stockUpdatesID = data["Updates Channel"]
        except csv.Error as e:
            print(
                "You are missing " + propertiesPath + ". You must have not "\
                "git pulled properly.")
            print(e)

    def _update_properties(self, propertiesPath: str) -> str:
        try:
            with open(propertiesPath, mode='r') as file:
                data = json.load(file)
                self.status = data["Status"]
                self.USTrackedIndices = data["US Tracked Indices"]
                self.CATrackedIndices = data["CA Tracked Indices"]
        except:
            print(
                "You are missing " + propertiesPath + ". Please ask Robert" \
                    "(robert.ciborowski@mail.utoronto.ca) for help.")

    def _setupHelpString(self):
        self._helpString = "All commands start with a '$'.\n```" \
                            "$market X: outputs the value of stock X.\n" \
                            "$market US: gives a summary of the US market.\n" \
                            "$market CA: gives a summary of the CA market.\n" \
                            "$ping: outputs latency.\n" \
                            "```"

    async def _onMarketCommand(self, message, filteredContent: str):
        lst = filteredContent.split()
        if len(lst) == 1:
            await message.channel.send(
                str(message.author.mention) + " Please input a stock ticker " \
                    "use .market!")
            return

        if lst[1] == "US":
            output = str(message.author.mention) + " Here's how the US " \
                    "market is doing. \n"

            for key, value in self.USTrackedIndices.items():
                price = self._obtainer.obtainPrice(key)

                if price < 0:
                    continue

                output += ("**" + key + "**: ${:.2f} (" + value + ")\n") \
                    .format(price)

            await message.channel.send(output)
            return

        if lst[1] == "CA":
            output = str(message.author.mention) + " Here's how the Canadian " \
                    "market is doing. \n"

            for key, value in self.CATrackedIndices.items():
                price = self._obtainer.obtainPrice(key)

                if price < 0:
                    continue

                output += ("**" + key + "**: ${:.2f} (" + value + ")\n") \
                    .format(price)

            await message.channel.send(output)
            return

        price = self._obtainer.obtainPrice(lst[1])

        if price < 0:
            await message.channel.send(
                str(message.author.mention) + " " + lst[1] + " is not " \
                    "available or is invalid!")
        else:
            await message.channel.send(
                (str(message.author.mention) + " **" + lst[1] + "**: ${:." + self._priceFormat + "f}") \
                    .format(price))




