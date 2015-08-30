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
strCreateTournyNameConfirm = "    Right... So the tournament name is {} Tournament? (y/n)"
strCreateTournyStartDate = "    {} is a nice name! And when should this tournament start? You can press 't' to jump to today's date."
strCreateTournyStartTime = "    What about the start time?"
strCreateTournyStartDateTimeConfirm = "    Great! Then your tournament will start on {} at {}. Now, how many days should a round last?"
strCreateTournyRoundLengthConfirm = "    So a round will last {} days? (y/n)"
strCreateTournyMaxPlayers = "Okay! And what's the max number of players this tournament will have?"
strCreateTournyMaxPlayersConfirm = "    So this tournament will have at most {} players? (y/n)"
strCreateTournyFormat = "    And what will the format be?"
strCreateTournyFormatWithRR = "    Should we allow more than the max number of players by having a round robin before the elimination bracket? (y/n)"
strCreateTournyFormatWithRRNumRounds = "    Assuming it's necessary, how many round robin rounds should there be before the elimination bracket starts?"
strCreateTournyFormatRRFull = "    Should it be a full round robin? (y/n)"
strCreateTournyFormatRRNumRounds = "    Sure thing! How many rounds should it last then? The maximum number of rounds is {}."
strCreateTournyRulesBase = "    Almost done! We just need to determine the rules. First, select from PTCGO's base formats:"
strCreateTournyRulesCustom = "    Now, what custom rules would you like to select? Press the spacebar to select a rule."
strCreateTournyRulesConfirm = "        Does that look right? (y/n)"
strCreateTournyComplete = """    Okay! Your tournament has been created! On the starting time and date, the tournament should start automatically. Three weeks before (or right now if the tournament is sooner than that!), signups will open! Have a great tournament!

(Press any key to continue...)"""