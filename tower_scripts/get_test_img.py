#clear out yesterday's photos
copy_to = "~/TITS/daily_check/"
command = 'rm -rf {}*.bmp'.format(copy_to)
terminal(command)

#download pictures from all pis to local directory for overview
if "Puzzle" in pi[0] or "Social" in pi[0]:
    copy_from = "APAPORIS/CURRENT/debug.bmp"
    command = 'scp pi@{}:{} {}{}.bmp'.format(pi[1],copy_from,copy_to,pi[0])
    terminal(command)
