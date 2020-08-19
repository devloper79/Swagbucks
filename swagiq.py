

'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'fetch' # change to what you need
BOT_OWNER_ROLE_ID = "495639450936803369"
  
 

 
oot_channel_id_list = [
    "732600186232242177",    #Official Gamers
    "736042800650387517",    #Challenge Phoenix
    "726448126260412537",    #Trivia Galaxy
    "737818050891350076",    #Trivia Flipkart Bots
    "735434568454373396",    #Google Pro Bot
    "726448126260412537",    #Velocity Bots
    "702001878594224210",    #Trivia Duck
    "729535056594337812",    #Viper King
    "736042800650387517",    #Smart Family Bots
    "729535056594337812",    #Trivia Allen
    "735203522617802772",    #Dragon World
]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf|c|w)?(\?)?$', re.IGNORECASE)

apgscore = 1000
nomarkscore = 400
markscore = 400

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Swagbucks Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    #@bot.event
    
    #async def on_message(message):
       #if message.content.startswith('+1'):
     # await message.channel.send('1\1\1\1\1\1')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="__**SWAGBUCKS LIVE**__", description="**Stardom**",color=0xFF0000)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/738654832489678568/98fae5dd7d6ae2b2078b851a0c2a45d8.png?size=256")
        self.embed.add_field(name="**Answer I**", value="0.0", inline=False)
        self.embed.add_field(name="**Answer II**", value="0.0", inline=False)
        self.embed.add_field(name="**Answer III**", value="0.0", inline=False)
        self.embed.add_field(name="Best Answer",value="<a:loading:695158657565851658>")
        self.embed.set_footer(text=f"Swagbucks", \
            icon_url="https://cdn.discordapp.com/emojis/65144659163194133.gif?v=1")
        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best_answer=":mag:"

        if highest > 0:
            if answer == 1:
                one_check = ":white_check_mark:"
            else:
                one_check=":x:"
            if answer ==1:
                best_answer=":one: :tada:"
            if answer == 2:
                two_check = ":white_check_mark:"
            else:
                two_check=":x:"
            if answer==2:
                best_answer=":two: :tada:"
            if answer == 3:
                three_check = ":white_check_mark:"
            else:
                three_check=":x:"
            if answer ==3:
                best_answer=":three: :tada:"
                
#         if lowest < 0:
#             if answer == 1:
#                 one_check = ":x:"
#             if answer == 2:
#                 two_check = ":x:"
#             if answer == 3:
#                 three_check = ":x:"            
 
        self.embed.set_field_at(0, name="**Answer I**", value="{0}{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**Answer II**", value="{0}{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**Answer III**", value="{0}{1}".format(lst_scores[2],three_check))
        self.embed.set_field_at(3,name="Best Answer",value=best_answer)

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Swagbucks")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name='Swagbucks Live...'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("✅")
                #await self.embed_msg.add_reaction("âœ”")
                await self.embed_msg.add_reaction("❎")
                #await self.embed_msg.add_reaction("âœ”")
                self.embed_channel_id = message.channel.id

            else:
                await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

        if message.content.startswith('&help'):
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="**__Swagbucks__**", description="**Private Bot**", color=0x0000FF)
           embed.add_field(name="__Game__", value="*Swagbucks Live*", inline=False)
           embed.add_field(name="__Bot Command__", value="+", inline=False)
           embed.add_field(name="__Made By__", value="*Anonymous*", inline=False)
           await message.channel.send(embed=embed)

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzM5NDTkasiBs2csb2354sk1.XyasKQ.E-Fajk51cs56afCT-a-Lm0TopUtg8'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('Fuajl542DxgT-a-Lm0TopUtg8nsccoh5649fqhi.492u6cA0pFLEiYrbkm2UdvExc3w',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()

