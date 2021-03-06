#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# -= C'hoari 0.1.0 =-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phk@FreeBSD.ORG> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
# ----------------------------------------------------------------------------

import os
import sys
import curses
import shutil
import subprocess

# CONSTANTS
CFG_DIR = os.path.expanduser('~/.choari')
PADDING_Y = 2;
PADDING_X = 2;

class Choari:
    def __init__(self):
        self.games = {'fav':[], 'ams':[], 'bfs':[], 'cods':[], 'crs':[], 'd3s':[], 'dm3s':[], 'efs':[],
                        'fcs':[], 'grs':[], 'h2s':[], 'hl2s':[], 'hls':[], 'hrs':[], 'hws':[], 'jk3s':[],
                        'kps':[], 'mhs':[], 'netp':[], 'nexuizs':[], 'preys':[], 'prs':[], 
                        'q2s':[], 'q3s':[], 'q4s':[], 'qs':[], 'qws':[], 'rss':[], 'rws':[], 
                        'sas':[], 'sfs':[], 'sgs':[], 'sms':[], 'sns':[], 'sof2s':[],
                        't2s':[], 'tbs':[], 'tm':[], 'tremulous':[], 'ts2':[], 
                        'uns':[], 'ut2004s':[], 'ut2s':[], 'warsows':[], 'woets':[]}
        self.alias = {'favorite':'fav',
                        'aa':'ams',     # query America's Army v2.x server
                        'bf':'bts',     # query BFRIS server
                        'cod':'cods',   # query Call of Duty server
                        'cc':'crs',     # query Command and Conquer: Renegade server
                        'd3':'d3s',     # query Descent3 server
                        'doom3':'dm3s', # query Doom 3 server
                        'ef':'efs',     # query Star Trek: Elite Force server
                        'fc':'fcs',     # query FarCry server
                        'gr':'grs',     # query Ghost Recon server
                        'hx2':'h2s',    # query Hexen II server
                        'hl2':'hl2s',   # query Half-Life 2 server
                        'hl':'hls',     # query Half-Life server
                        'hr2':'hrs',    # query Heretic II server
                        'hw':'hws',     # query HexenWorld server
                        'jk':'jk3s',    # query Jedi Knight: Jedi Academy server
                        'jk3':'jk3s',   # query Jedi Knight: Jedi Academy server
                        'kp':'kps',     # query Kingpin server
                        'moh':'mhs',    # query Medal of Honor: Allied Assault server
                        'mohaa':'mhs',  # query Medal of Honor: Allied Assault server
                        'np':'netp',    # query NetPanzer server
                        'nexuiz':'nexuizs', # query Nexuiz server
                        'prey':'preys', # query PREY server
                        'pr':'prs',     # query Pariah server
                        'q2':'q2s',     # query Quake II server
                        'q3':'q3s',     # query Quake III: Arena server
                        'q4':'q4s',     # query Quake 4 server
                        'q1':'qs',      # query Quake server
                        'qw':'qws',     # query QuakeWorld server
                        'rs':'rss',     # query Ravenshield server
                        'rw':'rws',     # query Return to Castle Wolfenstein server
                        'sa':'sas',     # query Savage server
                        'sf':'sfs',     # query Soldier of Fortune server
                        'sg':'sgs',     # query Shogo: Mobile Armor Division server
                        'sm':'sms',     # query Serious Sam server
                        'sn':'sns',     # query Sin server
                        'sof2':'sof2s', # query Soldier of Fortune 2 server
                        't2':'t2s',     # query Tribes 2 server
                        'tb':'tbs',     # query Tribes server
                        'tm':'tm',      # query TrackMania server
                        'tremulous':'tremulous', # query Tremulous server
                        'ts2':'ts2',    # query Teamspeak 2 server
                        'un':'uns',     # query Unreal server
                        'ut2004':'ut2004s', # query UT2004 server
                        'ut2k4':'ut2004s', # query UT2004 server
                        'ut2':'ut2s',   # query Unreal Tournament 2003 server
                        'warsow':'warsows',
                        'ws':'warsows', # query Warsow server
                        'et':'woets'}   # query Enemy Territory server

        try:
            if not os.path.isdir(CFG_DIR):
                os.mkdir(CFG_DIR)
                f = open(CFG_DIR+'/fav.lst', 'a');
                f.close()

            for cfg in os.listdir(CFG_DIR):
                # read all files in CFG_DIR
                f = open(CFG_DIR+'/'+cfg, 'r')
                game = cfg[:-4]
                if game in self.games:
                    for line in f:
                        self.games.get(game).append(line.strip())
                f.close
            
            if not os.path.lexists(CFG_DIR+'/config.py'):
                shutil.copy(os.path.dirname(sys.argv[0])+'/config.sample.py', CFG_DIR+'/config.py')
            execfile(CFG_DIR+'/config.py')
        except Exception, e:
            sys.exit("can't write or read in "+CFG_DIR+"\n"+str(e))

    def refresh(self, game, host, showPlayers=False):
        if game not in self.games:
            if game not in self.alias:
                return False
            else:
                game = self.alias.get(game)
        if game != 'fav':
            p = subprocess.Popen('qstat -P -'+game+' '+host, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            text = p.communicate()
            return game+' | '+text[0]
        return ""

    def add(self, game, host, fav=False):
        if fav == True:
            host = game+'|'+host
            game = 'fav'

        if host not in self.games[game]:
            f = open(CFG_DIR+'/'+game+'.lst', 'a+');
            f.write(host+"\n")
            f.close()
            self.games[game].append(host)
            return True
        else:
            return False
        
    def bookmark(self, game, host):
        return self.add(game, host, fav=True)
    
    def play(self, game, host):
        if game not in self.games:
            if game not in self.alias:
                return False
            else:
                game = self.alias.get(game)
        if game in self.config['binaries']:
            redirect2null = open(os.devnull, 'w')
            subprocess.call(self.config['binaries'][game].replace('%s', host), shell=True, stdout=redirect2null, stderr=redirect2null)
            redirect2null.close()
            return True
        return False

def clear_help(stdscr):
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    y = stdscr_y-PADDING_Y
    for line in range(y-9, y):
        stdscr.move(line, PADDING_X)
        stdscr.clrtoeol()
    
def display_help(stdscr):
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    y = stdscr_y-PADDING_Y
    stdscr.addstr(y-9, PADDING_X, 'HELP')
    stdscr.addstr(y-8, PADDING_X, ':fav | :favorite - Display favorite servers')
    stdscr.addstr(y-7, PADDING_X, ':moh | :mohaa - Display mohaa servers')
    stdscr.addstr(y-6, PADDING_X, ':q3 | :quake3 - Display quake3 servers')
    stdscr.addstr(y-5, PADDING_X, ':# - Refresh server # (unavailable yet)')
    stdscr.addstr(y-4, PADDING_X, ':e - Refresh current page')
    stdscr.addstr(y-3, PADDING_X, ':h | :help - Display this message')
    stdscr.addstr(y-2, PADDING_X, ':q | :quit - Quit C\'hoari')

def display_servers(stdscr, choari, strgame):
    # erase previous page
    stdscr.move(PADDING_Y+3, PADDING_X)
    stdscr.clrtobot()
    # change title
    stdscr.move(PADDING_Y, PADDING_X)
    stdscr.clrtoeol()
    if strgame == 'fav':
        stdscr.addstr(PADDING_Y, PADDING_X, 'C\'hoari - Main menu')
    else:
        stdscr.addstr(PADDING_Y, PADDING_X, 'C\'hoari - %s'%(strgame))
    
    i = PADDING_Y+3
    numhost = 0
    game = strgame
    for host in choari.games[strgame]:
        if strgame == 'fav':
            game = host.split('|')[0]
            host = host.split('|')[1]
        numhost = numhost + 1
        text = choari.refresh(game, host, True).split("\n")
        if len(text) > 1:
            stdscr.addstr(i, 2, '#%i %s'%(numhost, text[1]))
            if len(text) > 2:
                i = i + 1
                for line in text[2:]:
                    stdscr.addstr(i, 2, '%s'%(line))
                    i = i + 1

def loop(stdscr):
    # init
    choari = Choari()
    strgame = ''
    showHelp = False
    currentPage = 'fav'
    tabbing = ['add', 'bookmark', 'e', 'refresh', 'play', 'h', 'help', 'q', 'quit']
    for alias in choari.alias:
        tabbing.append(alias)
    tabbing.sort()

    stdscr.clear()
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    display_servers(stdscr, choari, 'fav')
    stdscr.move(stdscr_y-2, PADDING_X)

    # Draw a border around the board
    """ border_line = '+'+(stdscr_x*'-')+'+'
    stdscr.addstr(0, 0, border_line)
    # stdscr.addstr(stdscr_y+1, 0, border_line)
    for y in range(0, stdscr_y):
        stdscr.addstr(1+y, 0, '|')
        stdscr.addstr(1+y, stdscr_x+1, '|')
    stdscr.refresh() """
    
    # set title
    stdscr.addstr(PADDING_Y, PADDING_X, 'C\'hoari - Main menu')
    stdscr.addstr(PADDING_Y+1, PADDING_X, '------------------------------------------------------------------')
    stdscr.addstr(PADDING_Y+2, PADDING_X, 'ID       ADDRESS             PLAYERS MAP     RESPONSE TIME    NAME')
    stdscr.refresh()
    stdscr.move(stdscr_y-PADDING_Y, PADDING_X)

    # Main loop:
    while (1):
        c = stdscr.getch()                # Get a keystroke
        if 0<c<256:
            # stdscr.addstr('%i'%(c))
            if chr(c) in ':':
                # waiting for commands
                stdscr.move(stdscr_y-3, PADDING_X)
                stdscr.clrtoeol()
                stdscr.move(stdscr_y-2, PADDING_X)
                stdscr.clrtoeol()
                stdscr.addstr(':')
                strgame = ""
                tab = False
                while (1):
                    ch = stdscr.getch()
                    if 0<ch<256:
                        # stdscr.addstr('%i'%(ch))
                        if ch == 10:
                            # enter
                            if tab == True:
                                strgame = tabwords[tabmark]
                            break;
                        elif ch == 9:
                            # tabulation
                            if tab == False:
                                tab = True
                                tabmark = 0
                                tabwords = [strgame]
                                tablen = len(strgame)
                                for word in tabbing:
                                    if word[:tablen] == strgame:
                                        tabwords.append(word)
                                tabwordslen = len(tabwords)
                                
                            oldlen = len(tabwords[tabmark][tablen:])
                            tabmark = tabmark + 1
                            if tabmark >= tabwordslen:
                                tabmark = 0
                            
                            cy, cx = stdscr.getyx()
                            for l in range(0, oldlen):
                                stdscr.delch(cy, cx)
                            stdscr.addstr(cy, cx, tabwords[tabmark][tablen:])
                            stdscr.move(cy, cx)
                            
                        elif ch == 127:
                            # backspace
                            tab = False
                            cy, cx = stdscr.getyx()
                            if cx == PADDING_X:
                                break
                            elif cx > PADDING_X:
                                stdscr.delch(cy, cx-1)
                                stdscr.move(cy, cx-1)
                                strgame = strgame[:-1]
                        else:
                            tab = False
                            stdscr.addstr(chr(ch))
                            strgame += chr(ch)
                if ch != 033:
                    if strgame in choari.alias:
                        strgame = choari.alias[strgame]

                    if strgame == 'e':
                        strgame = currentPage

                    if strgame in ['h','help']:
                        # display help
                        display_help(stdscr)
                        showHelp = True
                    elif strgame in ['q','quit']:
                        # quit
                        break
                    elif strgame in choari.games:
                        if len(choari.games[currentPage]) > 0 and strgame in range(1, len(choari.games[currentPage])):
                            # TODO: refresh only this server
                            pass
                        else:
                            # list all servers
                            currentPage = strgame
                            display_servers(stdscr, choari, strgame)
                    else:
                        lstgame = strgame.split(' ')
                        if lstgame[0] == 'play':
                            if len(lstgame) == 2:
                                try:
                                    lstgame[1] = int(lstgame[1])
                                    if len(choari.games[currentPage]) >= lstgame[1]:
                                        if currentPage == 'fav':
                                            game = choari.games[currentPage][lstgame[1]-1].split('|')[0]
                                            host = choari.games[currentPage][lstgame[1]-1].split('|')[1]
                                        else:
                                            game = currentPage
                                            host = choari.games[currentPage][lstgame[1]-1]
                                        if choari.play(game, host) == False:
                                            # show error message
                                            stdscr.addstr(stdscr_y-3, PADDING_X, '%s is probably not configured in %s/config.py'%(game, CFG_DIR))
                                    else:
                                        # show error message
                                        stdscr.addstr(stdscr_y-3, PADDING_X, 'wrong index')
                                except Exception, e:
                                    # show error message
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'param must be an integer %s'%str(e))
                            else:
                                # show error message
                                stdscr.addstr(stdscr_y-3, PADDING_X, 'syntax is :play <id>')
                        elif lstgame[0] == 'bookmark':
                            if currentPage == 'fav':
                                # show error message
                                stdscr.addstr(stdscr_y-3, PADDING_X, 'already in your bookmarks')
                            elif len(lstgame) == 2:
                                try:
                                    lstgame[1] = int(lstgame[1])
                                    if len(choari.games[currentPage]) >= lstgame[1]:
                                        if choari.bookmark(currentPage, choari.games[currentPage][lstgame[1]-1]) == False:
                                            # show error message
                                            stdscr.addstr(stdscr_y-3, PADDING_X, 'already in your bookmarks')
                                    else:
                                        # show error message
                                        stdscr.addstr(stdscr_y-3, PADDING_X, 'wrong index')
                                except:
                                    # show error message
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'param must be an integer')
                            else:
                                stdscr.addstr(stdscr_y-3, PADDING_X, 'syntax is :bookmark <#id>')
                        elif lstgame[0] == 'add':
                            error = True
                            game = currentPage
                            if len(lstgame) == 2:
                                if currentPage == 'fav':
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'missing game')
                                else:
                                    host = lstgame[1]
                                    error = False
                            elif len(lstgame) == 3:
                                if lstgame[1] == 'fav':
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'use :bookmark <#id> syntax')
                                elif lstgame[1] in choari.alias:
                                    game = choari.alias[lstgame[1]]
                                    host = lstgame[2]
                                    error = False
                                else:
                                    # show error message
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'unknow game "%s"'%(lstgame[1]))

                            if error == False:
                                if currentPage == 'fav':
                                    fav = True
                                else:
                                    fav = False
                                if choari.add(game, host, fav) == False:
                                    # show error message
                                    stdscr.addstr(stdscr_y-3, PADDING_X, 'already in your bookmarks')
                                else:
                                    # refresh
                                    if game == currentPage or currentPage == 'fav':
                                        display_servers(stdscr, choari, currentPage)
                if strgame not in ['h','help'] and showHelp == True:
                    clear_help(stdscr)
                    showHelp = False
            elif c == 127:
                # backspace
                display_servers(stdscr, choari, 'fav')
                currentGame = 'fav'
            elif chr(c) in 'Qq':
                break
            elif strgame in ['q','quit']:
                break
            else: 
                # print c
                pass                  # Ignore incorrect keys
        # elif c == curses.KEY_UP and ypos>0:            ypos -= 1
        # elif c == curses.KEY_DOWN and ypos<board.Y-1:  ypos += 1
        # elif c == curses.KEY_LEFT and xpos>0:          xpos -= 1
        # elif c == curses.KEY_RIGHT and xpos<board.X-1: xpos += 1
        else:
            # Ignore incorrect keys
            pass
        
        # erase last line
        stdscr.move(stdscr_y-2, PADDING_X)
        stdscr.clrtoeol() 

def main(stdscr):
    loop(stdscr)                    # Enter the main loop


if __name__ == '__main__':
    curses.wrapper(main)
