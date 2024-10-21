import psycopg2

# --- Database Configuration ---
# Connects Python to Postgre database
connection = psycopg2.connect(
	dbname="photon",
	user="student"
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

def duplicateChecker(player_id, codename):
    cursor.execute("SELECT * FROM players WHERE id = %s OR codename = %s", (player_id, codename))
    result = cursor.fetchall()
    if result:
        return True
    return False

def insertPlayer(player_id, codename, team, max_players):
    # INSERT RED PLAYERS INTO DATABASE
    if player_id and codename:
        # Inserts all players from red team into table
        if not duplicateChecker(player_id, codename):
            cursor.execute(f"INSERT INTO players VALUES('{player_id}', '{codename}')")
        #else:
            #continue
            #print("Player ID or Codename has already been entered, please try again with different inputs")


def refreshDatabase(app, max_players):
    # INSERT RED PLAYERS INTO DATABASE
    # print("\nRED TEAM INFORMATION:")
    # print("-----------------------")
    for player in range(max_players):
        player_id = app.id_entry_red[player].get()
        codename = app.codename_entry_red[player].get()
        insertPlayer(player_id, codename, "red", max_players)
        hardware_id = app.hardware_id_entry_red[player].get()
        # if player_id and codename and hardware_id:
        #     print(f"ID: {player_id}, Codename: {codename}, Hardware ID: {hardware_id}")


    # INSERT GREEN PLAYERS INTO DATABASE
    # print("\nGREEN TEAM INFORMATION:")
    # print("-------------------------")
    for player in range(max_players):
        player_id = app.id_entry_green[player].get()
        codename = app.codename_entry_green[player].get()
        insertPlayer(player_id, codename, "green", max_players)
        hardware_id = app.hardware_id_entry_green[player].get()
        # if player_id and codename and hardware_id:
        #     print(f"ID: {player_id}, Codename: {codename}, Hardware ID: {hardware_id}")


    # for player in range(max_players):
    #     app.id_entry_red[player].delete(0, 'end')
    #     app.codename_entry_red[player].delete(0, 'end')
    #     app.id_entry_green[player].delete(0, 'end')
    #     app.codename_entry_green[player].delete(0, 'end')


    # print ID and Codename to the console for debug
    # TODO: Remove when finished debugging
    cursor.execute("SELECT * FROM players;")
    playersDB = cursor.fetchall()
    print("\nDATABASE STORAGE:")
    print("-------------------")

    for player in playersDB:
        print(f"ID: {player[0]}, Codename: {player[1]}")
    print("-------------------------")


    # Closes PostgreSQL Connection
    connection.commit()
    connection.close()