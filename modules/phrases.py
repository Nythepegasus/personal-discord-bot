import discord, json, os
from discord.ext import commands


class PhrasesCog(commands.Cog, name="Phrases Commands"):
    def __init__(self, client):
        self.client = client
        self.db_file = "phrases.json"
        if not os.path.isfile(self.db_file):
            initial_json = '{"phrases": []}'
            json.dump(initial_json, open(db_file, "w"), indent=4)



    @commands.command(name="add_phrase", aliases=["ap"])
    async def add_phrase(self, ctx, phrase):
        data = json.load(open(self.db_file))
        try:
            cur_index = data["phrases"][-1]["uid"] + 1
        except IndexError:
            cur_index = 1
        for line in data["phrases"]:
            if phrase == line["phrase"]:
                ctx.send("Phrase already exists!")
                return
            elif len(phrase) <= 2:
                ctx.send("Phrase too short!")
                return
            elif len(phrase) >= 35:
                ctx.send("Phrase too long!")
                return
            elif any(bad in phrase for bad in tonys_a_cunt):
                await ctx.send("You're a cunt!")
                return
        add_phrase = {
            "uid": cur_index,
            "phrase": phrase,
            "times_said": 0,
        }
        with open(self.db_file, "w") as f:
            data["phrases"].append(add_phrase)
            f.write(json.dumps(data, indent=4))
            await ctx.send("Phrase added!")


    def update_phrase(self, phrase):
        data = json.load(open(self.db_file))
        for d in data["phrases"]:
            if d.get("phrase").lower() in phrase.lower():
                d["times_said"] += 1
        with open(self.db_file, "w") as f:
            f.write(json.dumps(data, indent=4))
            return "Updated phrase!"


    @commands.command(name="remove_phrase", aliases=["rp"])
    async def remove_phrase(self, ctx, phrase):
        data = json.load(open(self.db_file))
        with open(self.db_file, "w") as f:
            data["phrases"] = [d for d in data["phrases"] if d.get("phrase") != phrase]
            f.write(json.dumps(data, indent=4))
            await ctx.send("Removed phrase!")


    @commands.command(name="phrase_counts", aliases=["pc"])
    async def phrase_counts(self, ctx):
        data = json.load(open(self.db_file))
        string_to_print = ""
        for phrase in data["phrases"]:
            string_to_print += f"{phrase['phrase']}: {phrase['times_said']}\n"
        await ctx.send(string_to_print)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        self.update_phrase(message.content)
        await self.client.process_commands(message)



def setup(client):
    client.add_cog(PhrasesCog(client))