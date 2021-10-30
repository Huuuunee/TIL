import re
import discord
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta

from requests.api import get

client = discord.Client()
KEY = "2da21189f1fc4a2fb0d6ec7eddbd22fc"
SCHUL_NM = "광주소프트웨어마이스터고등학교"
ATPT_OFCDC_SC_CODE = "F10"  # 교육청 코드
SD_SCHUL_CODE = "7380292"  # 학교 코드
def get_date():
    return str(datetime.now() + timedelta(days=0))[:10]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!오늘 아침'):
      url = "https://open.neis.go.kr/hub/mealServiceDietInfo?"  # 기본 URL
      url += "ATPT_OFCDC_SC_CODE=" + ATPT_OFCDC_SC_CODE + "&"  # 교육청코드
      url += "SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&"  # 학교코드
      url += "MMEAL_SC_CODE=" + "1" + "&"  # 1, 2, 3 : 아침, 점심, 저녁
      url += "MLSV_YMD=" + get_date().replace('-',"")  # 날짜
      response = requests.get(url).text
      print(response)
      soup = bs(response, "lxml")

      if soup.find("code").get_text() == "INFO-000":  # 급식 데이터가 있을 때

        for linebreak in soup.find_all("br"):
            linebreak.replace_with("\n")
        result = soup.find("ddish_nm").get_text()
        result = re.sub("[/>\]]+", "", result)

        await message.channel.send(result.split("\n"))

      else:  # 급식 데이터가 없을 때

        await message.channel.send("아침 정보가 없어.")
    if message.content.startswith('!오늘 점심'):
      url = "https://open.neis.go.kr/hub/mealServiceDietInfo?"
      url += "ATPT_OFCDC_SC_CODE=" + ATPT_OFCDC_SC_CODE + "&"
      url += "SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&"  # 
      url += "MMEAL_SC_CODE=" + "2" + "&"  # 1, 2, 3 : 
      url += "MLSV_YMD=" + get_date().replace('-',"") 
      print(url)
      response = requests.get(url).text
      print(response)
      soup = bs(response, "lxml")
      if soup.find("code").get_text() == "INFO-000":  #
        for linebreak in soup.find_all("br"):
            linebreak.replace_with("\n")
        result = soup.find("ddish_nm").get_text()
        result = re.sub("[/>\]]+", "", result)
         
        await message.channel.send(result.split[0]("\n"))

      else:  # 급식 데이터가 없을 때
        await message.channel.send("점심 정보가 없어.")  
    if message.content.startswith("!오늘 저녁"):
      url = "https://open.neis.go.kr/hub/mealServiceDietInfo?"
      url += "ATPT_OFCDC_SC_CODE=" + ATPT_OFCDC_SC_CODE + "&"
      url += "SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&"  # 
      url += "MMEAL_SC_CODE=" + "3" + "&"  # 1, 2, 3 : 1은 아침 2는 점심 3은 저녁
      url += "MLSV_YMD=" + get_date().replace('-',"") 
      print(url)
      response = requests.get(url).text
      print(response)
      soup = bs(response,"lxml")
      if soup.find("code").get_text() == "IFON-000":
        for linebreak in soup.find_all("br"):
            linebreak.replace_with("\n")
        result = soup.find("ddish_nm").get_text()
        result = re.sub("[/>\]]+","",result)
        
        await message.channel.send(result.split('\n'))

      else:
        await message.channel.send("저녁 정보가 없어.")


client.run('TOKEN')
