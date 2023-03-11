import os
import discord
import mysql.connector

# Get the bot token and MySQL configuration from environment variables
bot_token = os.environ.get('BOT_TOKEN')
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

# Configure the MySQL connection
mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_password,
  database=db_name
)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!create'):
        # Send a private message to the user requesting their account name and password
        await message.author.send("Please enter your account name:")
        account_name = await client.wait_for('message', check=lambda m: m.author == message.author)
        await message.author.send("Please enter your password:")
        password = await client.wait_for('message', check=lambda m: m.author == message.author)

        # Prompt the user to confirm their account name and password
        confirmation = f"Please confirm your account name: {account_name.content}\n" \
                       f"Please confirm your password: ||{password.content}||\n" \
                       f"Type 'yes' to confirm or anything else to cancel."
        await message.author.send(confirmation)
        response = await client.wait_for('message', check=lambda m: m.author == message.author)
        if response.content.lower() != 'yes':
            await message.author.send("Account creation cancelled.")
            return

        # Store the user's Discord ID as their email address
        email = str(message.author.id) + "@discord.com"

        # Hash the password using SHA256
        crypt_password = Account.ConvertSHA256(account_name.content + ":" + password.content)

        # Connect to the MySQL database and insert the new account
        mycursor = mydb.cursor()
        sql = "INSERT INTO war_accounts.accounts (Username, Password, CryptPassword, Ip, GmLevel) VALUES (%s, %s, %s, %s, %s)"
        val = (account_name.content, password.content, crypt_password, email, 0)
        mycursor.execute(sql, val)
        mydb.commit()

        # Respond to the user with a success message
        await message.author.send("Account created successfully!")

client.run(bot_token)
