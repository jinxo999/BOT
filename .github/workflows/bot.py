import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import aiohttp
import asyncio
import os
import random
import hashlib
import socket
from aiohttp import web

# ------- Bot Setup -------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ------- Helper Functions -------
def generate_fake_ip(user_id: int) -> str:
    h = hashlib.sha256(str(user_id).encode()).hexdigest()
    return ".".join(str(max(11, min(int(h[i:i + 2], 16), 249))) for i in (0, 2, 4, 6))


# ------- Replit Web Server -------
async def handle_root(request):
    return web.Response(text="✅ witness bot is alive working", content_type="text/plain")

async def start_webserver():
    port = int(os.environ.get("PORT", 8080))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("0.0.0.0", port)) == 0:
            print(f"⚠️ Port {port} is already in use. Skipping web server startup.")
            return

    app = web.Application()
    app.router.add_get("/", handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server started on port its working {port}")


# ------- Events -------
@bot.event
async def on_ready():
    await tree.sync()
    print(f"🤖 Bot logged in as {bot.user} nigga")
    bot.loop.create_task(start_webserver())


# ------- Views -------
class GitHubPingToolView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="📶 Join Modify.Net", url="https://discord.gg/8jjZv7wQuC", style=discord.ButtonStyle.link))


# ------- Commands -------
@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title="📡 Ping Response", description="`I'm up gang 🤑 go do somin`", color=discord.Color.green())
    embed.set_footer(text="fsociety • live and online")
    await interaction.response.send_message(embed=embed)


@tree.command(name="ip", description="Getsa real local/private IP for a user")
@app_commands.describe(user="User to scan")
async def ip(interaction: discord.Interaction, user: discord.User = None):
    target = user or interaction.user
    fake_ip = generate_fake_ip(target.id)
    embed = discord.Embed(
        title="🧬 Trace Report",
        description=f"🎯 Target: {target.mention}\n🧾 IP: `{fake_ip}`\n🔐 Status: Active\n✅ Confidence: 100%",
        color=discord.Color.dark_gray()
    )
    embed.set_footer(text="fsociety • trace complete")
    await interaction.response.send_message(embed=embed)


@tree.command(name="gaydetector", description="Scan user with 100% accuracy 🎯")
@app_commands.describe(user="User to scan")
async def gaydetector(interaction: discord.Interaction, user: discord.User = None):
    target = user or interaction.user
    h = hashlib.sha256(str(target.id).encode()).hexdigest()
    percent = int(h[:2], 16) % 101

    description = f"🧠 Target: **{target.display_name}**\n📊 Result: **{percent}%**\n🎯 Accuracy: `100%`"
    if percent > 60:
        description += f"\n\n{target.mention} is gay"

    embed = discord.Embed(title="🌈 Gay Percentage Scan", description=description, color=discord.Color.magenta())
    embed.set_footer(text="fsociety • gaydetector v1.0")
    await interaction.response.send_message(embed=embed)


@tree.command(name="traceall", description="Trace all users' private IPs")
async def traceall(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ Server only.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    for member in interaction.guild.members:
        if member.bot:
            continue
        fake_ip = generate_fake_ip(member.id)
        embed = discord.Embed(title="📡 Tracing Member", description=f"🧑‍💻 **{member.display_name}**\n📍 IP: `{fake_ip}`", color=discord.Color.dark_gray())
        await interaction.channel.send(embed=embed)
        await asyncio.sleep(1.5)

    await interaction.followup.send("✅ All users traced.", ephemeral=True)


@tree.command(name="raidv2", description="Send your message 16 times")
@app_commands.describe(message="Message to send repeatedly")
async def raidv2(interaction: discord.Interaction, message: str):
    # Send initial message and delete it
    first_msg = await interaction.response.send_message(message, ephemeral=False)
    sent_msg = await interaction.original_response()
    await sent_msg.delete()  # Deletes the first message

    # Send 16 messages
    for _ in range(16):
        await interaction.followup.send(message)



@tree.command(name="echo", description="Repeat your message")
@app_commands.describe(message="Message to echo")
async def echo(interaction: discord.Interaction, message: str):
    embed = discord.Embed(title="🔊 Echo", description=f"`{message}`", color=discord.Color.blue())
    embed.set_footer(text="fsociety • echo command")
    await interaction.response.send_message(embed=embed)


@tree.command(name="iplookup", description="Look up real IP info using ip-api.com")
@app_commands.describe(ip="IP address to lookup")
async def iplookup(interaction: discord.Interaction, ip: str):
    await interaction.response.defer(thinking=True)
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,isp,org,as,lat,lon,query"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if data["status"] != "success":
        await interaction.followup.send(f"❌ Could not find data for IP: `{ip}`")
        return

    embed = discord.Embed(
        title="📡 Trace Report",
        description=(
            f"🌍 **Country:** `{data['country']}`\n"
            f"🏙️ **Region:** `{data['regionName']}`\n"
            f"🏘️ **City:** `{data['city']}`\n"
            f"🌐 **IP:** `{data['query']}`\n"
            f"📡 **ISP:** `{data['isp']}`\n"
            f"🏢 **Org:** `{data['org']}`\n"
            f"📮 **ZIP:** `{data['zip']}`\n"
            f"🧭 **Coords:** `{data['lat']}, {data['lon']}`\n"
            f"📶 **Status:** Active ✅\n"
            f"📊 **Confidence:** 100%"
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text="fsociety • lookup active")
    await interaction.followup.send(embed=embed, view=GitHubPingToolView())


@tree.command(name="dice", description="Roll a dice")
@app_commands.describe(sides="Number of sides")
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("❌ Dice must have at least 2 sides!", ephemeral=True)
        return
    result = random.randint(1, sides)
    embed = discord.Embed(title="🎲 Dice Roll", description=f"**{result}** (1-{sides})", color=discord.Color.orange())
    embed.set_footer(text="fsociety • dice roll")
    await interaction.response.send_message(embed=embed)


@tree.command(name="8ball", description="Ask the magic 8-ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain", "Outlook good", "Yes", "No", "Very doubtful",
        "Reply hazy", "Ask again later", "Definitely", "Not likely"
    ]
    answer = random.choice(responses)
    embed = discord.Embed(title="🎱 Magic 8-Ball", description=f"**Q:** {question}\n**A:** {answer}", color=discord.Color.purple())
    embed.set_footer(text="fsociety • magic 8-ball")
    await interaction.response.send_message(embed=embed)
     

@tree.command(name="websiteinfo", description="Get info about a website (domain, IP, etc.)")
@app_commands.describe(url="Website to scan (example: https://example.com/)")
async def websiteinfo(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)

    # Normalize input
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        domain = url.split("/")[2]
    except IndexError:
        await interaction.followup.send("Invalid URL format.")
        return

    try:
        ip = socket.gethostbyname(domain)
        hostname = socket.gethostbyaddr(ip)[0]
    except Exception:
        ip = "Unavailable"
        hostname = "Unavailable"

    # Make HTTP request to get status and headers
    status = "Unavailable"
    content_type = "Unavailable"
    online = False

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                status = response.status
                content_type = response.headers.get("Content-Type", "Unavailable")
                online = True
    except Exception:
        pass

    # Create Embed
    embed = discord.Embed(
        title="🌐 Web Scanner Report",
        description=(
            f"🟢 **Domain**: `{domain}`\n"
            f"🔗 **URL**: {url}\n"
            f"📶 **Status**: {'🟢 Online' if online else '🔴 Offline'}\n"
            f"📡 **HTTP Code**: `{status}`\n"
            f"🗂️ **Content-Type**: `{content_type}`\n"
            f"🧭 **IP Address**: `{ip}`\n"
            f"🧠 **Hostname**: `{hostname}`"
        ),
        color=discord.Color.green() if online else discord.Color.red()
    )

    embed.set_footer(text="fsociety • website lookup")
    await interaction.followup.send(embed=embed)

@tree.command(name="mock", description="Mock text")
@app_commands.describe(text="Text to mock")
async def mock(interaction: discord.Interaction, text: str):
    mocked = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
    embed = discord.Embed(title="🤡 Mocking Text", description=f"`{mocked}`", color=discord.Color.yellow())
    embed.set_footer(text="fsociety • mock command")
    await interaction.response.send_message(embed=embed)


@tree.command(name="reverse", description="Reverse your message")
@app_commands.describe(text="Text to reverse")
async def reverse(interaction: discord.Interaction, text: str):
    reversed_text = text[::-1]
    embed = discord.Embed(title="🔄 Reversed Text", description=f"`{reversed_text}`", color=discord.Color.teal())
    embed.set_footer(text="fsociety • reverse command")
    await interaction.response.send_message(embed=embed)


@tree.command(name="userinfo", description="Show info about a user")
@app_commands.describe(user="User to lookup")
async def userinfo(interaction: discord.Interaction, user: discord.User = None):
    target = user or interaction.user
    member = interaction.guild.get_member(target.id) if interaction.guild else None

    joined_at = member.joined_at.strftime("%B %d, %Y") if member and member.joined_at else "Unknown"
    roles = [role.name for role in member.roles[1:]] if member and len(member.roles) > 1 else ["None"]
    roles_text = ", ".join(roles[:10]) + ("..." if len(roles) > 10 else "")

    created_at = target.created_at.strftime("%B %d, %Y")

    embed = discord.Embed(title="👤 User Information", color=discord.Color.blurple())
    embed.add_field(name="Username", value=target.name, inline=True)
    embed.add_field(name="Display Name", value=target.display_name, inline=True)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(name="Account Created", value=created_at, inline=True)
    embed.add_field(name="Joined Server", value=joined_at, inline=True)
    embed.add_field(name="Roles", value=roles_text, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
    embed.set_footer(text="fsociety • user info")
    await interaction.response.send_message(embed=embed)


@tree.command(name="randomnumber", description="Generate a random number")
@app_commands.describe(min_num="Minimum", max_num="Maximum")
async def randomnumber(interaction: discord.Interaction, min_num: int = 1, max_num: int = 100):
    if min_num >= max_num:
        await interaction.response.send_message("❌ Minimum must be less than maximum!", ephemeral=True)
        return
    result = random.randint(min_num, max_num)
    embed = discord.Embed(title="🎲 Random Number", description=f"**{result}** ({min_num}-{max_num})", color=discord.Color.green())
    embed.set_footer(text="fsociety • random number")
    await interaction.response.send_message(embed=embed)


@tree.command(name="serverinfo", description="Show server details")
async def serverinfo(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ Server only.", ephemeral=True)
        return

    guild = interaction.guild
    embed = discord.Embed(title="🏠 Server Info", color=discord.Color.dark_blue())
    embed.add_field(name="Name", value=guild.name, inline=True)
    embed.add_field(name="ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text="fsociety • server info")
    await interaction.response.send_message(embed=embed)


# ------- Run Bot -------
bot.run(os.getenv("DISCORD_TOKEN"))
