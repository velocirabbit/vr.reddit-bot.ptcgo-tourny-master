######################################################
## Display strings. Can be formatted with .format() ##
######################################################
strHeader = "~*~*~*~*~*   /r/PTCGO Tournament Manager   *~*~*~*~*~"
strHeaderAuth = "Author: /u/iforgot120"
strStatusNoTourny = "No tournament currently running"
strStatusTourny = "Currently running tournament: {}"
strMenuNoTourny = """    N - New Tournament
    S - Settings
    Q - Quit bot"""
strMenuTourny = """    S - View current tournament status
    M - Manual tournament adjustments
    X - End tournament early
    Q - Quit bot"""
strCreateTournyName = """    Hello there! Glad to meet you! Welcome to the /r/ PTCGO Tournament Manager! I'll be helping you manage your next tournament. At any time during this tournament setup, you can press 'Esc' to cancel and return to the main menu.

    But first, tell me a little about the tournament you're planning. Now tell me: what will the tournament's name be? (name will be formatted as "[name] Tournament")"""
strCreateTournyNameConfirm = "    Right... So the tournament name is {}Tournament? (y/n)"
strCreateTournyStartDate = "    {} is a nice name! And when should this tournament start? You can press 't' to jump to today's date."
strCreateTournyStartDateConfirm = "    Great! Then your tournament will start on {}"