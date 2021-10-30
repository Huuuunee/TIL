import discord
import boto3
import random
from datetime import datetime, timedelta


def get_instance_list(key_id, key):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    res = []
    for instance in ec2.instances.all():
        if instance.tags is not None:
            for tag in instance.tags:
                if tag["Key"] == "Name":
                    res.append([instance.id, {instance.state["Name"]}, tag["Value"]])
    return res


def instanceCreate(userChoose, key_id, key, keypair):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )

    file = open("userdata.txt", "r")
    userdata = file.read()
    print(userdata)

    instances = ec2.create_instances(
        ImageId=userChoose["amiID"],
        InstanceType=userChoose["instanceType"],
        KeyName=keypair,
        MaxCount=userChoose["instanceMax"],
        MinCount=userChoose["instanceMin"],
        Monitoring={"Enabled": True},
        ElasticInferenceAccelerators=[
            {"Type": "eia1.medium", "Count": 1},
        ],
        SecurityGroupIds=["sg-00d35aef8f22dfd23"],
        SecurityGroups=["test-sg"],
        UserData=userdata,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": userChoose["instanceName"]},
                ],
            },
        ],
    )
    return instances, ec2


def terminateInstance(key_id, key, instance_id):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    client = boto3.client(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    for instance in ec2.instances.all():
        if instance.id == instance_id:
            client.terminate_instances(InstanceIds=[instance_id])
            instance.wait_until_terminated()


def startInstance(key_id, key, instance_id):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    client = boto3.client(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    for instance in ec2.instances.all():
        if instance.id == instance_id:
            client.start_instances(InstanceIds=[instance_id])
            instance.wait_until_running()
            instance.reload()

            for network in instance.network_interfaces_attribute:
                publicip = network["Association"]
                return str(publicip["PublicIp"])


def stopInstance(key_id, key, instance_id):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )
    client = boto3.client(
        "ec2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key,
        region_name="ap-northeast-2",
    )

    for instance in ec2.instances.all():
        if instance.id == instance_id:
            client.stop_instances(InstanceIds=[instance_id])
            instance.wait_until_stopped()


client = discord.Client()

data = []
keys = []
question = []

ami = [
    [
        "아마존 리눅스 2",
        "ami-08c64544f5cfcddd0",
    ],
    [
        "우분투 서버 20.04",
        "ami-04876f29fd3a5e8ba",
    ],
    [
        "우분투 서버 18.04",
        "ami-0ba5cd124d7a79612",
    ],
    ["윈도우 서버 2019", "ami-01dd8a88a17ff5466"],
    [
        "데비안 10",
        "ami-0b4a713d12660d96c",
    ],
]

instance_type = [
    ["t2.nano", 1, 0.5],
    ["t2.micro", 1, 1],
    ["t2.small", 1, 2],
    ["t2.medium", 2, 4],
    ["t2.large", 2, 8],
    ["t3.nano", 2, 0.5],
    ["t3.micro", 2, 1],
    ["t3.small", 2, 2],
    ["t3.medium", 2, 4],
    ["t3.large", 2, 8],
]

security_groups = [
    ["모든 트래픽 열기 (프로덕션 환경에선 사용 주의)", "0"],
    ["웹HTTP 포트(80), ssh 포트(22) 열기 (개발환경에서 사용 추천!)", "80,22"],
    ["웹HTTPS 포트(443), 웹HTTP 포트(80), ssh 포트(22) 열기 (웹 서버 추천!)", "443,80,22"],
]


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_message(message):
    try:
        cmd = message.content.split(" ")[1]
    except:
        cmd = message.content.split(" ")[0]
    args = message.content.split(" ")[2:]

    if cmd == "중지":
        for i in keys:
            if i[0] == message.author.id:
                data.append(
                    {"id": message.author.id, "qnum": 5, "key_id": i[1], "key": i[2]}
                )
                await message.reply("중지할 인스턴스를 선택해주세요")
                string = "```"
                for j, k in enumerate(get_instance_list(i[1], i[2])):
                    data[-1][j + 1] = k[0]
                    string += f"{j+1}. ID: {k[0]}  Status: {k[1]}  Name: {k[2]}\n"
                string += "```"
                if len(string) == 6:
                    await message.reply("중지할 인스턴스가 없습니다.")
                else:
                    await message.channel.send(string)

    if cmd == "종료":
        for i in keys:
            if i[0] == message.author.id:
                data.append(
                    {"id": message.author.id, "qnum": 6, "key_id": i[1], "key": i[2]}
                )
                await message.reply("종료할 인스턴스를 선택해주세요")
                string = "```"
                for j, k in enumerate(get_instance_list(i[1], i[2])):
                    data[-1][j + 1] = k[0]
                    string += f"{j+1}. ID: {k[0]}  Status: {k[1]}  Name: {k[2]}\n"
                string += "```"
                if len(string) == 6:
                    await message.reply("종료할 인스턴스가 없습니다.")
                else:
                    await message.channel.send(string)

    if cmd == "시작":
        for i in keys:
            if i[0] == message.author.id:
                data.append(
                    {"id": message.author.id, "qnum": 7, "key_id": i[1], "key": i[2]}
                )
                await message.reply("시작할 인스턴스를 선택해주세요")
                string = "```"
                for j, k in enumerate(get_instance_list(i[1], i[2])):
                    data[-1][j + 1] = k[0]
                    string += f"{j+1}. ID: {k[0]}  Status: {k[1]}  Name: {k[2]}\n"
                string += "```"

                if len(string) == 6:
                    await message.reply("시작할 인스턴스가 없습니다.")
                else:
                    await message.channel.send(string)

    if cmd == "액세스키":
        for i in keys:
            if i[0] == message.author.id:
                i[1] = args[0]
                break
        else:
            keys.append([message.author.id, args[0], None, None])

        await message.add_reaction("✅")

    if cmd == "시크릿키":
        for i in keys:
            if i[0] == message.author.id:
                i[2] = args[0]
                break
        else:
            keys.append([message.author.id, None, args[0], None])

        await message.add_reaction("✅")

    if cmd == "키페어":
        for i in keys:
            if i[0] == message.author.id:
                i[3] = args[0]
                break
        else:
            keys.append([message.author.id, None, None, args[0]])

        await message.add_reaction("✅")

    if cmd in ["안녕", "안녕?", "안녕!", "ㅎㅇ?", "ㅎㅇ!"]:
        await message.channel.send(random.choice(["안녕하세요", "안녕하세요!", "ㅎㅇ"]))

    if cmd == "도와줘":
        embed = discord.Embed(
            title="구름이 도움말 목록",
            color=0x62C1CC,
        )
        embed.add_field(
            name=":computer: EC2",
            value="`구름아 생성 <이름>`\n > 객관식 답변 1,2,3 ~~~\n\n"
            + "`구름아 시작`\n > 인스턴스를 시작합니다\n\n"
            + "`구름아 액세스키 <액세스키>`\n > 액세스키를 등록합니다. DM으로도 가능합니다.\n\n"
            + "`구름아 시크릿키 <시크릿키>`\n > 시크릿키를 등록합니다. DM으로도 가능합니다.\n\n"
            + "`구름아 키페어 <키페어>`\n > 키페어를 등록합니다. DM으로도 가능합니다.\n\n"
            + "`구름아 중지`\n > 인스턴스ㄹ를 중지합니다\n\n"
            + "`구름아 종료`\n > 인스턴스를 종료합니다\n\n",
            inline=False,
        )
        embed.add_field(
            name=":guitar: 기타",
            value="`액세스키, 퍼블릭키 확인`\n > aws > 로그인 > 오른쪽위 프로필 > 내 보안 자격 증명 > 새 액세스 키 생성 > 키 표시 >  복사\n\n"
            + "`구름아 자폭해`\n > 구름이가 자폭합니다.",
            inline=False,
        )
        await message.channel.send(embed=embed)

    if cmd == "생성":
        for i in data:
            if i["id"] == message.author.id:
                embed = discord.Embed(
                    description="먼저 설정을 완료해 주세요.",
                    color=0xFFFF00,
                    timestamp=datetime.now() + timedelta(hours=-9),
                )
                embed.set_footer(
                    text=message.author.name, icon_url=message.author.avatar_url
                )
                await message.channel.send(embed=embed)
                break
        else:
            data.append({"id": message.author.id, "qnum": 1, "instanceName": args[0]})

            await message.reply("생성할 인스턴스의 이미지를 선택해주세요")
            string = "```"
            for i in range(len(ami)):
                string += str(i + 1) + ". " + ami[i][0] + "\n"
            string += "```"
            await message.channel.send(string)

    if cmd in ["자폭해", "폭파해", "펑"]:
        await message.channel.send(":boom: 펑!:boom: ")

    if cmd.isdigit():
        for i in data:
            if i["id"] == message.author.id:
                if i["qnum"] == 1:
                    i["amiID"] = ami[int(cmd) - 1][1]
                    i["qnum"] += 1

                    await message.reply("생성할 인스턴스의 타입을 설정해주세요")
                    string = "```"
                    for i in range(len(instance_type)):
                        align1 = " " if i < 9 else ""  # 줄맞춤용 공백
                        align2 = " " * (12 - len(instance_type[i][0]))  # 줄맞춤용 공백
                        string += f"{i+1}.{align1} {instance_type[i][0]} {align2} CPU Core: {instance_type[i][1]} \t RAM: {instance_type[i][2]} Gb\n"
                    string += "```"
                    await message.channel.send(string)

                elif i["qnum"] == 2:
                    i["instanceType"] = instance_type[int(cmd) - 1][0]
                    i["qnum"] += 1

                    await message.reply("생성할 인스턴스의 보안 옵션을 선택해주세요")
                    string = "```"
                    for i in range(len(security_groups)):
                        string += f"{i+1}. {security_groups[i][0]}\n"
                    string += "```"
                    await message.channel.send(string)

                elif i["qnum"] == 3:
                    i["security"] = security_groups[int(cmd) - 1][1].split(" ")
                    i["qnum"] += 1

                    await message.reply("생성할 인스턴스의 개수를 선택해주세요")

                elif i["qnum"] == 4:
                    del i["qnum"]
                    i["instanceMax"] = int(cmd)
                    i["instanceMin"] = int(cmd)
                    i["sgID"] = "sg-0702a901d46d58fd2"
                    i["sgName"] = "boto3-test-sg"

                    await message.reply("인스턴스를 생성중이에요...")

                    for j in keys:
                        if j[0] == message.author.id:
                            key_id = j[1]
                            key = j[2]
                            keypair = j[3]

                    instances, ec2 = instanceCreate(i, key_id, key, keypair)
                    for instance in instances:
                        instanceID = ec2.Instance(instance.id)
                        instance.wait_until_running()
                        for network in instanceID.network_interfaces_attribute:
                            publicip = network.get("Association")
                            for tags in instance.tags:  # 인스턴스의 태그
                                if tags["Key"] == "Name":  # 이름이 Name인 것 찾기
                                    instance_name = tags["Value"]  # 해당하는 태그의 값을 저장

                            if message.author.dm_channel:
                                ip = publicip.get("PublicIp")
                                await message.author.dm_channel.send(
                                    f"{instance_name} 인스턴스 만들기 성공!\nIP주소: {ip}"
                                )
                                await message.channel.send(
                                    f"{instance_name} 인스턴스 만들기 성공!"
                                )
                            elif message.author.dm_channel is None:
                                channel = await message.author.create_dm()
                                ip = publicip.get("PublicIp")
                                await message.author.dm_channel.send(
                                    f"{instance_name} 인스턴스 만들기 성공!\nIP주소: {ip}"
                                )
                                await message.channel.send(
                                    f"{instance_name} 인스턴스 만들기 성공!"
                                )

                    del data[data.index(i)]

                elif i["qnum"] == 6:
                    msg = await message.channel.send("인스턴스를 종료중입니다...")
                    for i in data:
                        if i["id"] == message.author.id:
                            instance_id = i[int(cmd)]
                            terminateInstance(i["key_id"], i["key"], instance_id)

                            await msg.edit(content="인스턴스 종료 성공!")
                            del data[data.index(i)]

                elif i["qnum"] == 5:
                    msg = await message.channel.send("인스턴스를 중지중입니다...")
                    for i in data:
                        if i["id"] == message.author.id:
                            instance_id = i[int(cmd)]
                            stopInstance(i["key_id"], i["key"], instance_id)
                            await msg.edit(content="인스턴스 중지 성공!")
                            del data[data.index(i)]

                elif i["qnum"] == 7:
                    msg = await message.channel.send("인스턴스를 시작중입니다...")
                    for i in data:
                        if i["id"] == message.author.id:

                            instance_id = i[int(cmd)]
                            ip = startInstance(i["key_id"], i["key"], instance_id)
                            await msg.edit(content="인스턴스 시작 성공!")
                            if message.author.dm_channel:
                                await message.author.dm_channel.send(
                                    f"인스턴스 시작 성공!\nIP주소: {ip}"
                                )
                            elif message.author.dm_channel is None:
                                await message.author.create_dm()
                                await message.author.dm_channel.send(
                                    f"인스턴스 시작 성공!\nIP주소: {ip}"
                                )
                            del data[data.index(i)]


client.run("your_token")