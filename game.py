import random
import discord
import questions
import user_db


async def gethighscores():
    output = discord.Embed(
        title='Covid Trivia Game Highscores',
        color = 0xb23831,
    )

    arr = await tensort()
    OV = ""

    for e in range(0, len(arr)):
        OV += f"{e+1}. {arr[e][0]}: {arr[e][1]}\n"

    #print(OV)
    if(OV != ""):
        output.description = ""
        output.add_field(name= "Top 10:", value = OV)
    else:
        output.description = "No one has played a match yet.\nEnter ~game to start"
    return output


async def tensort():
    whitelist = []
    output = []
    for e in range(0,len(user_db.userhighscore_name)):
        if len(whitelist) == 10:
            return output
        biggest = 0
        biggestkey = ""
        for key, val in user_db.userhighscore_name.items():
            if val > biggest and not key in whitelist:
                biggest = val
                biggestkey = key
        whitelist.append(biggestkey)
        output.append([str(biggestkey), str(biggest)])
    return output


class gameplayinstance:
    def __init__(self):
        self.score = 0
        self.strikes = 3
        self.AVarr = []
        for i in range(0,len(questions.questions)):
            self.AVarr.append(i)

    async def newV(self):
        randV = random.randint(0,len(self.AVarr)-1)
        self.qindex = self.AVarr.pop(randV)
        OV = "\n" + questions.questions[self.qindex][0]
        return OV

    async def iterate(self, prompt, playername):
        output = discord.Embed(color = 0xb23831)
        if not hasattr(self,'qindex'):
            output.title = "Covid Trivia"
            output.description="Use ~answer {a/A or b/B} to respond to a question.\nEnter ~game to see your question again"
            output.add_field(name = "Question: ", value = await self.newV())
            return output
        #print(self.qindex)

        if not prompt.lower() in questions.conversions:
            #output += "Invalid entry, use yes/no or true/false"
            output.title = "Invalid Entry"
            output.description="Use ~answer {a/A or b/B} to respond to a question.\nEnter ~game to see your question again"
            return output

        if(questions.questions[self.qindex]):
            if(questions.questions[self.qindex][1] == questions.conversions[prompt.lower()]):
                self.score +=1
                output.title ='Correct!'
                output.add_field(name="Explanation", value=questions.questions[self.qindex][2])
                output.add_field(name="Current Score", value=f'{self.score}', inline=False)
                output.add_field(name="Next Question: ", value=await self.newV(), inline=False)
                return output
            else:
                self.strikes-=1
                output.title ='Incorrect!'
                output.add_field(name="Explanation", value=questions.questions[self.qindex][2])
                if(self.strikes == 0):
                    output.title="Game Over"
                    output.add_field(name="Current Score", value=f'{self.score}', inline=False)
                    output.description = "Game over, you've used up all your chances.\nEnter ~game again to start a new round"
                    user_db.usergameinstance.pop(playername)
                    if playername in user_db.userhighscore_name:
                        user_db.userhighscore_name[playername] = max(user_db.userhighscore_name[playername], self.score)
                    else:
                        user_db.userhighscore_name[playername] = self.score
                    return output
                else:
                    output.description = f'You have {self.strikes} chances left.'
                    output.add_field(name="Next Question: ", value=await self.newV(),inline=False)
                    return output