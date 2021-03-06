#built in
import re
from typing import Tuple
#pip
import discord
from discord.ext import commands

"""
A function that returns the matching role-id(s) in a list (as integers)
Needed Arguments: Comamnd-Context and Role-ID/ Role-Mention/ Role-Name (as a string)

The function will return a tuple of values that contains two values:
- A list with all matching role-id (should be one most of the times)
- The length of that list as secondary return value

Notice: By passing a name into the function you might get more than one result, keep this in mind!

Exaple call: role, length = get_rid(ctx, role_name)
"""
def get_rid(ctx, role_input: list) -> Tuple[list, int]:
	role_name = ""
	for obj in role_input:
		role_name += "%s " %obj
	role_name = role_name.strip()
	#first trying regex to get the id from the message itself (is the case by mention or role ID as intput)
	role_id = re.search(r"\d{18}", role_name)
	roles_list = [] #initializing return list
	if role_id != None: #checking if re found something
		role_id = role_id.group(0) #getting readable id
		roles_list.append(int(role_id)) #getting and appending role-id to list
		#return roles_list, len(roles_list)
	#if role-name was given
	else:
		#iterating through roles, searching for name match (case sensitive)
		for g_role in ctx.guild.roles:
			if role_name in str(g_role.name):
				roles_list.append(int(g_role.id)) #appending to list

	return roles_list, len(roles_list)

#gets you a channel from an ID in a text
#like get_rid but less advanced (no search for names)
def get_chan(guild, channel_input: str):
	channel_id = re.search(r"\d{18}", channel_input)
	channel = None
	if channel_id != None:
		channel_id = channel_id.group(0)
		channel = guild.get_channel(int(channel_id))
	return channel #returning channel object


#creating and returning an embed with keyword arguments
#please note that name and value cant't be empty - good news: they aren't ;)
def make_embed(title="", color=discord.Color.blue(), name="‌", value="‌", text=None):
	emby = discord.Embed(title=title, color=color)
	emby.add_field(name=name, value=value)
	if text:
		emby.set_footer(text=text)

	return emby	


"""
this function takes a (massive) list and fits it into embeds.
yes - this can take multiple embeds which will be created if needed
emby: put your first embed that you already created
head: 
"""
def make_emby(emby, head, content, embed_limit=1, field_limit=3, char_limit = 980, color=discord.Color.green(), footer=""):
	#switcher to make for a more appealing view by only listing the headder once over all emebeds
	switch_headder = {
		0: head,
		1: ""
	}

	field_text = "" #text that fits into a field
	embys = []		#will store all embed objects in a list
	embed_num = 0	#couting embeds - important for breaklimit
	field_num = 0 	#field counter - max 24 possible (here used by default: 6)
	first_emb = 0	#will be switch to one after first headder is written (see switcher)
	i = 1 			#counter to display a name above each field like "entry 1 to 40", starting by one beacuase "normal" counting
	last_i = 1		#stores the last value from i when a embed was created

	for line in content:		

		#if embed full  - an embed takes ~6k characters, the setting for chars. per field is at 1000
		#a full embed will be added to the (return)list - a new one will be created
		if field_num == field_limit:
			embys.append(emby) #appending
			emby = discord.Embed(title="", color=color) #creating
			field_num = 0	#resetting field-number
			first_emb = 1	#disabeling headder (see switch)
			embed_num += 1

		#when embed limit is reached
		if embed_num == embed_limit:
			embys.append(emby)
			break

		#buliding the actual text of the field
		#we need to ensure that the charackters wont exceed 1024 characters
		#so the next line will be calculated before beeing added
		next_text = field_text + "%s\n" %line	#building text with the next line
		
		#making embed field if field is filled (char_limit is by default 1000)
		if len(next_text) >= char_limit:

			#making right headder
			if field_num == 0:
				headder = switch_headder.get(first_emb)
				headder += "\n%s to %s" %(last_i, i-1)
				emby.add_field(name=headder, value=field_text)
				last_i = i

			else:
				name = "%s to %s" %(last_i, i-1)
				emby.add_field(name=name, value= field_text)
				last_i = i 

			#incrementing and overwriting fieldtext with the new line
			field_num += 1
			field_text = line

		else: #saving text with new line as new text
			field_text = next_text
			i += 1

	#when for-loop is finished, there will be a textblock that didn't reach the limits and isn't added yet
	#checking if it exists and adding it to the last embed
	#there is always a place in the last embed, otherwise it would have been finished when reaching 6 fields
	if field_text != "" and embed_num != embed_limit:

		if field_num == 0: #if not full field was added so far
			emby.add_field(name=head, value=field_text)

		else:
			head = "\n%s to %s" %(last_i, i-1)
			emby.add_field(name=head, value=field_text)
		#adding remaining embed if embed was generated trough 
		embys.append(emby) #adding final embed

	return embys #returning list








