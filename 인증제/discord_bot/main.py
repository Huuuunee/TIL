import discord
import random
import time
import asyncio
client = discord.Client()
from selenium.webdriver.chrome.options import *
from selenium import webdriver

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    def check(m):
      return m.author == message.author and m.channel == message.channel
    if message.content.startswith('!ping'):
        await message.channel.send('pong')
    if message.content == "가위" or message.content == "바위" or message.content == "보":
          menu = 1,2,3
          bot_response = random.choice(menu)
          if(bot_response == 1):
            if message.content == "가위":
              await message.channel.send("비겼습니다")
            elif message.content == "바위":
              await message.channel.send("봇이 졌어요")
            else:
              await message.channel.send("봇이 이겼어요!")
          elif bot_response == 2:
            if message.content == "가위":
              await message.channel.send("봇이 졌어요")
            elif message.content == "바위":
              await message.channel.send("비겼습니다")
            else:
              await message.channel.send("봇이 이겼어요!")
          else:
            if message.content == "가위":
              await message.channel.send("봇이 이겼어요")
            elif message.content == "바위":
              await message.channel.send("봇이 졌어요")
            else:
              await message.channel.send("비겼습니다")
    if message.content.startswith("?번역"):
        KOR_EN = "https://papago.naver.com/?sk=ko&tk=en"
        EN_KOR = "https://papago.naver.com/?sk=en&tk=ko&hn=0"

        Selectembed = discord.Embed(title="한국어 -> 영어 번역은 1,\n영어 -> 한국어 번역은 2를 입력해주세요!", color=0xFF9900)
        Selectmsg = await message.channel.send(embed=Selectembed)

        try:
            cmsg = await client.wait_for("message",check=check,timeout=10)

            if cmsg.content=="1":
              await Selectmsg.delete()

              KO_ENembed = discord.Embed(title="한국어 -> 영어 번역입니다.\n번역할 문장을 입력해주세요!",color =0xFF9900)
              await message.channel.send(embed=KO_ENembed)

              try:
                  translateMsg = await client.wait_for("message", check=check, timeout=30)

                  message_content = translateMsg.content
                  timeembed = discord.Embed(title="잠시만 기다려주세요!\n데이터를 수집 중이므로 다소 시간이 걸릴 수 있습니다.", color=0xFF9900)
                  timemsg = await message.channel.send(embed=timeembed)

                  options = Options()
                  options.headless = True
                  browser = webdriver.Chrome(executable_path="discord_bot\chromedriver.exe", options=options)
                  browser.get(KOR_EN)

                  time.sleep(1)
                  browser.find_element_by_xpath('//*[@id="sourceEditArea"]/label').send_keys(message_content)
                  browser.find_element_by_xpath('//*[@id="btnTranslate"]').click()
                  time.sleep(1)
                  transResult = browser.find_element_by_xpath('//*[@id="txtTarget"]').text

                  await timemsg.delete()

                  ResultEmbed = discord.Embed(title="한국어 -> 영어 번역 결과", color=0xFF9900)
                  ResultEmbed.add_field(name="Korean", value=f"```{message_content}```", inline=True)
                  ResultEmbed.add_field(name="English", value=f"```{transResult}```", inline=True)
                  ResultEmbed.set_footer(text="Papago에서 얻어온 번역 결과입니다.", icon_url="https://cdn.discordapp.com/attachments/704169918777655317/807856285545529344/papago_og.png")
                  await message.channel.send(embed=ResultEmbed)

              except asyncio.exceptions.TimeoutError:
                  timeoutEmbed = discord.Embed(title="시간을 초과하셨습니다.\n30초 내로 입력해주세요.", color=0xFF9900)
                  timeoutEmbed.set_footer(text="다시 시도는 ?번역을 입력해주세요.")
                  await message.channel.send(embed=timeoutEmbed)
            if cmsg.content == "2":
                await Selectmsg.delete()

                EN_KOembed = discord.Embed(title="영어 -> 한국어 번역입니다.\n번역할 문장을 입력해주세요!", color=0xFF9900)
                await message.channel.send(embed=EN_KOembed)

                try:
                    translateMsg = await client.wait_for("message", check=check, timeout=30)

                    message_content = translateMsg.content
                    timeembed = discord.Embed(title="잠시만 기다려주세요!\n데이터를 수집 중이므로 다소 시간이 걸릴 수 있습니다.", description="", color=0xFF9900)
                    timemsg = await message.channel.send(embed=timeembed)

                    options = Options()
                    options.headless = True
                    browser = webdriver.Chrome(executable_path="discord_bot\chromedriver.exe", options=options)
                    browser.get(EN_KOR)

                    time.sleep(1)
                    browser.find_element_by_xpath('//*[@id="sourceEditArea"]/label').send_keys(message_content)
                    browser.find_element_by_xpath('//*[@id="btnTranslate"]').click()
                    time.sleep(1)
                    transResult = browser.find_element_by_xpath('//*[@id="txtTarget"]').text

                    await timemsg.delete()

                    ResultEmbed = discord.Embed(title="영어 -> 한국어 번역 결과", color=0xFF9900)
                    ResultEmbed.add_field(name="English", value=f"```{message_content}```", inline=True)
                    ResultEmbed.add_field(name="Korean", value=f"```{transResult}```", inline=True)
                    ResultEmbed.set_footer(text="Papago에서 얻어온 번역 결과입니다.", icon_url="https://cdn.discordapp.com/attachments/704169918777655317/807856285545529344/papago_og.png")
                    await message.channel.send(embed=ResultEmbed)

                except asyncio.exceptions.TimeoutError:
                    timeoutEmbed = discord.Embed(title="시간을 초과하셨습니다.\n30초 내로 입력해주세요.", color=0xFF9900)
                    timeoutEmbed.set_footer(text="다시 시도는 ?번역을 입력해주세요.")
                    await message.channel.send(embed=timeoutEmbed)

        except asyncio.exceptions.TimeoutError:
            timeoutEmbed = discord.Embed(title="시간을 초과하셨습니다.\n10초 내로 입력해주세요.", color=0xFF9900)
            timeoutEmbed.set_footer(text="다시 시도는 ?번역을 입력해주세요.")
            await message.channel.send(embed=timeoutEmbed)
client.run('token')