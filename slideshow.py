

import os.path
import pygame
import time
import sys


pygame.init()
pygame.display.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((1024,768))
font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',42)
#QUICK_BURN = True
QUICK_BURN = False
DEFAULT_DELAY = 4
preIntermission = True
postIntermission = False
if len(sys.argv) > 1:
    if 'post' in sys.argv:
        postIntermission = True
        preIntermission = False
    if 'all' in sys.argv:
        postIntermission = True
        preIntermission = True
        




def waitForKey(key=32):
    while 1:
        evt = pygame.event.poll()
        if evt.type == pygame.KEYUP and evt.key == key:
            print "starting..."
            break

def music(sndtrack,t=None,art=None):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)

    pygame.time.delay(400)
    pygame.mixer.music.load(sndtrack)
    pygame.mixer.music.play(2)
    global screen

    if t:
        text = t
    else:
        text = sndtrack.split('/')[-1].split('.')[0]
        text = ' '.join(map(lambda a: a.capitalize(), text.split('-')))

    if art and os.path.isfile(art):
        arttitle(text, pygame.image.load(art))
    else:
        title(text,3,(200,255,200))


def title(text,delay=1.5,color=(255,255,255)):
    if QUICK_BURN: delay = 0.25
    global font
    lines = None
    if '\n' in text:
        lines = text.split('\n')

    screen.fill((0,0,0))
    
    if not lines:
        surf = font.render(text, True, color, (0,0,0))
        (w,h) = surf.get_size()
        x = (1024/2) - (w/2)
        y = (768/2) - (h/2)
        screen.blit(surf, (x,y))
        pygame.display.update()

    else:
        # multiline
        yinc = font.get_linesize() + 20
        y = (768/2) - ((len(lines)*yinc)/2);
        for line in lines:
            surf = font.render(line, True, color, (0,0,0))
            (w,h) = surf.get_size()
            x = (1024/2) - (w/2)
            screen.blit(surf, (x,y))
            y = y + yinc
            
        pygame.display.update()

    if delay:
        pygame.time.delay(int(delay*1000))
    

def arttitle(text,pic):
    global font
    lines = None
    color = (255,255,255)
    if '\n' in text:
        lines = text.split('\n')

    screen.fill((0,0,0))

    y = 50
    if not lines:
        surf = font.render(text, True, color, (0,0,0))
        (w,h) = surf.get_size()
        x = (1024/2) - (w/2)
        screen.blit(surf, (x,y))
        pygame.display.update()

    else:
        # multiline
        yinc = font.get_linesize() + 2
        for line in lines:
            surf = font.render(line, True, color, (0,0,0))
            (w,h) = surf.get_size()
            x = (1024/2) - (w/2)
            screen.blit(surf, (x,y))
            y = y + yinc
            
        pygame.display.update()

    if None:
        (w,h) = surf.get_size()
        x = (1024/2) - (w/2)
        y = 70
        screen.blit(surf, (x,y))
    image = pygame.transform.scale(pic, (300,300))
    screen.blit(image, (362,234))
    pygame.display.update()

    if QUICK_BURN:
        pygame.time.delay(250)
    else:
        pygame.time.delay(4000)
    
def credittitle(text,pic):
    global font
    lines = None
    screen.fill((0,0,0))
    
    surf = font.render(text, True, (255,255,255), (0,0,0))
    (w,h) = surf.get_size()
    x = (1024/2) - (w/2)
    y = 70
    screen.blit(surf, (x,y))
    image = pygame.transform.scale(pic, (768,576))
    screen.blit(image, (128, 150))
    pygame.display.update()

    if QUICK_BURN:
        pygame.time.delay(250)
    else:
        pygame.time.delay(3000)
    

def show(image,delay,author=None):
    global screen
    if QUICK_BURN: delay=0.25

    (width,height) = image.get_size()

    if author:
        author = font.render(author, True, (128,128,128))
        author = pygame.transform.rotate(author, 90)

    print "width,height:",width,height
    if height > 768:
        if width > height:
            scaleratio = height/768.0
            newheight = 768
            newwidth = int(width / scaleratio)
            print "scaling to",newwidth,newheight

        else:
            print "WERD"
            scaleratio = height/768.0
            newheight = 768
            newwidth = int(width / scaleratio)
    #         scaleratio = width/1024.0
    #         newwidth = 1024
    #         newheight = int(height/scaleratio)
            print "scaling to",newwidth,newheight

        scaled = pygame.transform.scale(image, (newwidth,newheight))
        scaled.set_colorkey()
    else:
        scaled = image
        newwidth = width
        newheight = height

    if newwidth > 1024 and height >= 760:

        dims = (1024,int(1024*float(height)/float(width)))
        print "TINY is",dims
        tiny = pygame.transform.scale(image, dims)
        screen.fill((0,0,0))
        screen.blit(tiny, (0,384-(dims[1]/2)))
        pygame.display.update()
        start = time.time()
        if QUICK_BURN:
            pygame.time.delay(250)
            return
        
        ## make zoomed images

        steps = 20
        step = (768-dims[1]) / steps
        w = 1024
        h = dims[1]
        zooms = []
        for foo in range(steps):
            h = h + step
            w = int(h * (float(width)/height))
            zoom = pygame.transform.scale(image, (w,h))
            zooms.append( (zoom,384-(h/2),w) )

        ## check time
        if None:
            elapsed = time.time() - start
            if elapsed < delay:
                print "EXTRA DELAY:",delay-elapsed
                pygame.time.delay(int((delay-elapsed)*1000))
            else:
                print "elapsed was",elapsed
        else:
            pygame.time.delay(2000)

        for (zoom,y,mywidth) in zooms:
            screen.blit(zoom, (0,y))
            pygame.display.flip()
            evt = pygame.event.poll()
            if evt.type == pygame.KEYUP and evt.key == 32:
                break
            
        ## pan
        
        xrange = newwidth - 1024
        #step = xrange / float(steps)
        #steps = 200
        step = 7.0
        steps = xrange/step
        x = 0
        print "step is",step
        for foo in range(steps):
            screen.blit(scaled, (int(x),0))
            x = x - step
            pygame.display.flip()
            evt = pygame.event.poll()
            if evt.type == pygame.KEYUP and evt.key == 32:
                break
            #pygame.display.update()
            #pygame.time.delay(10)

        zooms.reverse()
        for (zoom,y,mywidth) in zooms:
            screen.fill((0,0,0))
            screen.blit(zoom, (1024-mywidth,y))
            pygame.display.flip()
            evt = pygame.event.poll()
            if evt.type == pygame.KEYUP and evt.key == 32:
                break
            
        screen.fill((0,0,0))
        screen.blit(tiny, (0,384-(dims[1]/2)))
        pygame.display.flip()
        pygame.time.delay(1500)
        
    else:
        x = (1024/2) - (newwidth/2)
        y = (768/2) - (newheight/2)
        screen.blit(scaled, (x,y))
        if author:
            screen.blit(author,(0,0))
        pygame.display.flip()
        pygame.time.delay(int(delay*1000))
    
def startmovie(fname, sndtrack,size=None):
    global screen
    
    movie = pygame.movie.Movie(fname)
    if sndtrack:
        pygame.mixer.music.load(sndtrack)

    screen.fill((0,0,0))
    pygame.display.update()
    if size == None:
        movie.set_display(screen, (0,0,1024,768))
    else:
        (w,h) = size
        movie.set_display(screen, (512-int(w/2),0,w,h))
    movie.play()
    if sndtrack:
        pygame.mixer.music.play()

    if not movie.has_video():
        raise "No video in movie " + str(fname)
    return movie


def makeimages(dir,delay=DEFAULT_DELAY):
    rtn = []
    directory = os.listdir(dir)
    directory.sort()
    for x in directory:
        path = os.path.join(dir,x)
        if x.split('.')[-1].lower() in ['jpg','jpeg']:
            rtn.append( (pygame.image.load(path),delay,x) )
            title('loading...\n%s'%x,0,(100,100,100))
    return rtn

def makeactions(imgs):
    rtn = []
    for (img,delay,path) in imgs:
        author = None
        if '_' in path:
            author = ' '.join(path.split('_')[1].split('-'))
        rtn.append( (show, (img,delay,author)))
    return rtn



##
## shit still todo TODO FIXE
##

if None:
    (title, ('February 3, 2007\n"Guiness Stout"\nBrad',)),


actions = []

if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/red-snapper/red-snapper-reeled-and-skinned--hot-flush.ogg','Red Snapper\nReeled and Skinned\n"Hot Flush"','/home/mike/sound/albums/red-snapper--red-snapper-reeled-and-skinned/art.jpeg')) )
    actions.append( (title, ('Without the participation\nof the following partners, none\n of these pictures would be possible', 10)) )
    actions.append( (title, ('thanks, everyone:', 5)) )
    actions.append( (title, ('(alphabetically)', 1, (128,128,128))) )
    actions.append( (credittitle, ('Rene Chapman', pygame.image.load('/home/mike/photos/slideshow/portraits/rene.jpeg'))) )
    actions.append( (credittitle, ('Diane Colwell', pygame.image.load('/home/mike/photos/slideshow/portraits/diane.jpeg'))) )
    actions.append( (credittitle, ('Brad Cooke', pygame.image.load('/home/mike/photos/slideshow/portraits/brad.jpeg'))) )
    actions.append( (credittitle, ('Kevin Embacher', pygame.image.load('/home/mike/photos/slideshow/portraits/kevin.jpeg'))) )
    actions.append( (credittitle, ('Shaun Fluker', pygame.image.load('/home/mike/photos/slideshow/portraits/shaun.jpeg'))) )
    actions.append( (credittitle, ('Robin Harnett', pygame.image.load('/home/mike/photos/slideshow/portraits/robin.jpeg'))) )
    actions.append( (credittitle, ('Florian Jungen', pygame.image.load('/home/mike/photos/slideshow/portraits/florian.jpeg'))) )
    actions.append( (credittitle, ('Joel Knopff', pygame.image.load('/home/mike/photos/slideshow/portraits/joel.jpeg'))) )
    actions.append( (credittitle, ('Craig Smith', pygame.image.load('/home/mike/photos/slideshow/portraits/craig.jpeg'))) )
    actions.append( (credittitle, ('Ryan Steenbergen', pygame.image.load('/home/mike/photos/slideshow/portraits/ryan.jpeg'))) )
    actions.append( (credittitle, ('Esther Visser', pygame.image.load('/home/mike/photos/slideshow/portraits/esther.jpeg'))) )
    actions.append( (credittitle, ('Esther Visser', pygame.image.load('/home/mike/photos/slideshow/portraits/esther-2.jpeg'))) )
    actions.append( (credittitle, ('Esther Visser', pygame.image.load('/home/mike/photos/slideshow/portraits/esther-3.jpeg'))) )
    actions.append( (title, ('and', 1)) )
    #actions.append( (credittitle, ('Neil Warren', pygame.image.load('/home/mike/photos/slideshow/portraits/neil.jpeg'))) )
    actions.append( (credittitle, ('Neil Warren', pygame.image.load('/home/mike/photos/slideshow/portraits/neil-2.jpeg'))) )

if preIntermission:
    actions.append( (title, ('May 20-21, 2006',)) )
    actions.append( (title, ('Ghost River Wilderness',)) )
    actions.append( (title, ('Esther\nCraig\nCarlyle',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/consolation'))

if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/gorillaz/gorillaz-g-sides--faust.ogg','Gorillaz\nG Sides\n"Faust"','/home/mike/sound/albums/gorillaz--gorillaz-g-sides/art.jpeg')) )
    actions.append( (title, ('July 3, 2006',)) )
    actions.append( (title, ('Kananaskis Lakes',)) )
    actions.append( (title, ('Esther\nFlorian',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/joy'))

if preIntermission:
    actions.append( (title, ('July 12 - 16, 2006',)) )
    actions.append( (title, ('Vancouver Island\n+\nSunshine Coast',)) )
    actions.append( (title, ('Nick',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/cycling'))

if preIntermission:
    actions.append( (title, ('July 22, 2006',)) )
    actions.append( (title, ('Canmore',)) )
    actions.append( (title, ('Esther',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/eeor'))

if preIntermission:
    actions.append( (title, ('August 3 - 6, 2006',)) )
    actions.append( (title, ('Bugaboo Provicial Park',)) )
    actions.append( (title, ('Esther',)) )
    bugs = makeactions(makeimages('/home/mike/photos/slideshow/bugaboos'))
    bugs.insert(13, (title, ('Hardest alpine route either\nof us have done...',3)) )
    actions = actions + bugs
    

if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/the-kingpins/the-kingpins-plan-of-action--designated-driver.ogg','The Kingpins\nPlan of Action\n"Designated Driver"','/home/mike/sound/albums/the-kingpins--the-kingpins-plan-of-action/art.jpeg')) )
    actions.append( (title, ('September 4, 2006',)) )
    actions.append( (title, ('Glacier National Park',)) )
    actions.append( (title, ('Esther',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/hermit-meadows'))


if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/the-clash/london-calling--the-guns-of-brixton.mp3','The Clash\nLondon Calling\n"The Guns of Brixton"','/home/mike/sound/albums/the-clash--london-calling/art.jpeg')) )
    actions.append( (title, ('October 28, 2006',)) )
    actions.append( (title, ('Kananaskis Country',)) )
    actions.append( (title, ('Florian',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/mt-lorette'))


if preIntermission:
    actions.append( (title, ('November 12, 2006',)) )
    actions.append( (title, ('Neil',)) )
    actions.append( (show, (pygame.image.load('/home/mike/photos/slideshow/portraits/neil.jpeg'),1,None)) )
    actions.append( (title, ('(first ski of the year)',)) )
    actions.append( (show, (pygame.image.load('/home/mike/photos/slideshow/portraits/neil.jpeg'),4,None)) )
    
if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/buck-65/buck-65-vertex--the-centaur.ogg','Buck 65\nVertex\n"The Centaur"','/home/mike/sound/albums/buck-65--buck-65-vertex/art.jpeg')) )
    actions.append( (title, ('November 16 - 21, 2006',)) )
    actions.append( (title, ('Joshua Tree, California',)) )
    actions.append( (title, ('Brad',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/joshua-tree'))
    
if preIntermission:
    surprisecol =  makeactions(makeimages('/home/mike/photos/slideshow/surprise-col'))
    surprisecol.insert(1, (title, ('(-30 C)',)))
    surprisecol.insert(10, (title, ('Tanner moved to Sask. the next day...',5)))
    actions = actions + [
        (music, ('/home/mike/sound/artists/corb-lund-band/corb-lund-band-unforgiving-mistress--young-and-jaded.ogg','Corb Lund Band\nUnforgiving Mistress\n"Young and Jaded"','/home/mike/sound/albums/corb-lund-band--corb-lund-band-unforgiving-mistress/art.jpeg')),

        (title, ('November 26, 2006',)),
        (title, ('Lake Louise',)),
        (title, ('Neil\nTanner\nKira\nDiane\nShaun',)),
        surprisecol
        ]

if preIntermission:
    actions = actions + [
        (music, ('/home/mike/sound/artists/white-stripes/elephant--seven-nation-army.mp3','White Stripes\nElephant\n"Seven Nation Army"','/home/mike/sound/albums/white-stripes--elephant/art.jpeg')),
        (title, ('December 4 - 6, 2006',)),
        (title, ('Moraine Lake',)),
        (title, ('Neil\nBrad\nFlorian',)),
        makeactions(makeimages('/home/mike/photos/slideshow/wenkchemna-pass'))
        ]

if preIntermission:
    actions = actions + [
        (music, ('/home/mike/sound/artists/various-artists/various-artists-go-ahead-punk-make-my-day--the-vandals-let-the-bad-times-roll.ogg','The Vandals\nLive Fast Diarrhea\n"Let The Bad Times Roll"')),
        (title, ('December 19, 2006',)),
        (title, ('Lake Louise area',)),
        (title, ('Neil\nScott',)),
        makeactions(makeimages('/home/mike/photos/slideshow/popes-peak'))
        ]

if preIntermission:
    actions.append( (music, ('/home/mike/sound/artists/operation-ivy/operation-ivy-energy--freeze-up.ogg','Operation Ivy\nEnergy\n"Freeze Up"','/home/mike/sound/albums/operation-ivy--operation-ivy-energy/art.jpeg')) )
    thighs = makeactions(makeimages('/home/mike/photos/slideshow/house-of-sky'))
    thighs.insert(6, (title, ('(Safety first...)',)))
    actions = actions + [
        (title, ('January 2, 2007',)),
        (title, ('Ghost River Wilderness',)),
        (title, ('Brad',)),
        thighs
        ]

if preIntermission:
    burstall = makeactions(makeimages('/home/mike/photos/slideshow/burstall-pass'))
    burstall.insert(11, (startmovie, ('/home/mike/photos/slideshow/burstall-pass/neil-skiing.mpg',None,(576,768))) )
    actions = actions + [
        (music, ('/home/mike/sound/artists/the-suicide-machines/the-suicide-machines-destruction-by-definition--sos.ogg','The Suicide Machines\nDestruction by Definition\n"SOS"','/home/mike/sound/albums/the-suicide-machines--the-suicide-machines-destruction-by-definition/art.jpeg')),
        (title, ('January 21-23, 2007',)),
        (title, ('Smith Dorrien',)),
        (title, ('Neil\nFlorian',)),
        burstall
        ]

if preIntermission:
    actions = actions + [
        (music, ('/home/mike/sound/artists/system-of-a-down/system-of-a-down--ddevil.mp3','System Of A Down\n"DDevil"','/home/mike/sound/albums/system-of-a-down--system-of-a-down/art.jpeg'))
        ]
    actions = actions + [
        (title, ('January 26-27, 2007',)),
        (title, ('"Hell Patrol"\n(Ghost River Wilderness)',)),
        (title, ('Kevin',)),
        makeactions(makeimages('/home/mike/photos/slideshow/ghost--january-26-27-2007'))
        ]

if preIntermission:
    actions.append( (title, ('February 3, 2007',)) )
    actions.append( (title, ('Field, BC',)) )
    actions.append( (title, ('Brad',)) )
    actions.append( makeactions(makeimages('/home/mike/photos/slideshow/guiness-stout')) )

if preIntermission:
    beowulf = makeactions(makeimages('/home/mike/photos/slideshow/beowulf'))
    beowulf.insert(0, (title, ('Brad\nCraig',)))
    beowulf.insert(0, (title, ('Ghost River Wilderness',)))
    beowulf.insert(0, (title, ('February 6, 2007',)))
    beowulf.insert(0, (music, ('/home/mike/sound/artists/hell/hell-munich-maschine--berimbau.ogg','Hell\nMunich Maschine\n"Berimbau"','/home/mike/sound/albums/hell--hell-munich-maschine/art.jpeg')) )
    beowulf.insert(7, (title, ('My first WI4 lead:',)))
    beowulf.insert(13, (startmovie, ('/home/mike/photos/slideshow/beowulf/climbing.mpeg',None)))
    
    actions = actions + beowulf

if preIntermission:
    ### FIXME TODO new music here
    ### (caveat?)
    actions = actions + [
        (title, ('February 23, 2007',)),
        (title, ('Evan Thomas Creek',)),
        (title, ('Kevin',)),
        makeactions(makeimages('/home/mike/photos/slideshow/evan-thomas--february-23-2007'))
        ]
    
if preIntermission:
    hell2 = makeactions(makeimages('/home/mike/photos/slideshow/ghost--february-24-2007'))
    actions = actions + [
        (title, ('February 24, 2007',)),
        (title, ('"Hell Patrol 2"\n(Ghost River Wilderness)',)),
        (title, ('Kevin',)),
        hell2
        ]

if preIntermission:
    actions.append( (music, ('/home/mike/sound/INCOMING/bad_brains-black_dots/Bad_Brains_-_07_-_Dont_Bother_Me.mp3','Bad Brains\nBlack Dots\n"Don\'t Bother Me"','/home/mike/sound/INCOMING/bad_brains-black_dots/art.jpeg')) )
    actions.append( (title, ('February 25, 2007',)) )
    actions.append( (title, ('Field, B.C.',)) )
    actions.append( (title, ('Kevin\nBrad',)) )
    pilsner = makeactions(makeimages('/home/mike/photos/slideshow/carlsberg-pilsner'))
    pilsner.insert(9, (startmovie, ('/home/mike/photos/slideshow/carlsberg-pilsner/imgp2603-edited-reencoded.mpeg',None)))
    actions = actions + pilsner

if preIntermission:
    actions.append( (title, ('Intermission',3)) )
    actions.append( (title, ('no, really:\npee, grab another beer\n5 minutes...',3)) )
    actions.append( (title, ('Intermission...',1)) )

if postIntermission:
    ## FIXME TODO add neil's video
    actions.append( (music, ('/home/mike/sound/artists/dj-mark-farina/dj-mark-farina-mushroom-jazz-2--mark-rae-mr-scruff-how-sweet-it-is.ogg','DJ Mark Farina\nMushroom Jazz 2\n"How Sweet It Is"','/home/mike/sound/albums/dj-mark-farina--dj-mark-farina-mushroom-jazz-2/art.jpeg')) )
    actions.append( (title, ('February 27, 2007',)) )
    actions.append( (title, ('Smith Dorrien',)) )
    actions.append( (title, ('Neil\nFlorian\nBrad',)) )
    actions = actions +  makeactions(makeimages('/home/mike/photos/slideshow/pink-spot'))

if postIntermission:
    actions = actions + [
        (music, ('/home/mike/sound/artists/dead-kennedys/dead-kennedys-give-me-convenience-or-give-me-death--i-fought-the-law.ogg','Dead Kennedys\nGive Me Convenience or Give Me Death\n"I Fought The Law"','/home/mike/sound/albums/dead-kennedys--dead-kennedys-give-me-convenience-or-give-me-death/art.jpeg')),
        (title, ('March 3, 2007',)),
        (title, ('Highway 66',)),
        (title, ('Anthony',)),
        makeactions(makeimages('/home/mike/photos/slideshow/elbow-falls'))
    ]

if postIntermission:
    actions.append( (title, ('March 10, 2007',)) )
    actions.append( (title, ('Kananaskis',)) )
    actions.append( (title, ('Rene',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/a-bridge-too-far'))

if postIntermission:
    actions.append( (music, ('/home/mike/sound/artists/rancid/and-out-come-the-wolves--daly-city-train.mp3','Rancid\nAnd Out Come the Wolves\n"Daly City Train"','/home/mike/sound/albums/rancid--and-out-come-the-wolves/art.jpeg')) )
    actions.append( (title, ('March 23, 2007',)) )
    actions.append( (title, ('Banff',)) )
    actions.append( (title, ('Shaun',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/march-23-2007--professors-falls'))

if postIntermission:
    actions.append( (title, ('March 27, 2007',)) )
    actions.append( (title, ('Lake Louise area',)) )
    actions.append( (title, ('Neil\nJoel\nFlorian',)) )
    pics = makeactions(makeimages('/home/mike/photos/slideshow/niblock'))
    pics.append( (startmovie, ('/home/mike/photos/slideshow/niblock/following-neil.mpeg', None)) )
    actions = actions + pics

if postIntermission:
    actions.append( (music, ('/home/mike/sound/INCOMING/Bad Brains - I + I Survived/01 - Jah Love.mp3','Bad Brains\nI & I Survived\n"Jah Love"','/home/mike/sound/INCOMING/Bad Brains - I + I Survived/art.jpeg')) )
    actions.append( (title, ('March 30, 2007',)) )
    actions.append( (title, ('Lake Louise area',)) )
    actions.append( (title, ('Brad',)) )
    aemmer = makeactions(makeimages('/home/mike/photos/slideshow/aemmer'))
    aemmer.insert( 9, (startmovie, ('/home/mike/photos/slideshow/aemmer/aemmer-short-no-sound.mpeg', None)) )
    actions = actions + aemmer

if postIntermission:
    actions = actions + [
        (music, ('/home/mike/sound/INCOMING/toots-and-the-maytals--funky-kingston/funky-kingston--funky-kingston.mp3','Toots and the Maytals\nFunky Kingston\n"Funky Kingston"','/home/mike/sound/INCOMING/toots-and-the-maytals--funky-kingston/art.jpeg')),
        (title, ('March 11 - 18, 2007',)),
        (title, ('Maui, Hawai\'i',)),
        (title, ('Esther',)),
        makeactions(makeimages('/home/mike/photos/slideshow/maui'))
    ]

if postIntermission:
    ## TODO process video on day 5
    actions.append( (title, ('April 5 - 11, 2007',)) )
    actions.append( (title, ('Drummond/Bonnet Traverse',)) )
    actions.append( (title, ('(Mosquito Creek to Rockbound Lake)',)) )
    actions.append( (title, ('Florian\nBrad',)) )
    actions.append( (title, ('Day 1:\nMosquito Creek to Elk Lakes',)) )
    actions.append( makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day1')) )
    actions.append( (music, ('/home/mike/sound/artists/lionrock/lionrock-city-delirious--zip-gun-rumble.ogg','Lionrock\nCity Delirious\n"Zip Gun Rumble"','/home/mike/sound/albums/lionrock--lionrock-city-delirious/art.jpeg')) )
    actions.append( (title, ('Day 2:\ngain Drummond Glacier',)) )
    day2 = makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day2'))
    day2.insert( 4, (title, ('Expanding the lungs\nfor the big climb:',)) )
    actions.append( day2 )
    actions.append( (title, ('Day 3:\nclimb Pipestone Minora',)) )
    day3 = makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day3'))
    day3.insert( 4, (title, ('Crack o\' Noon club\nstill in full effect...',)) )
    day3.insert( 5, (title, ('(*gong*)',)) )
    day3.insert( 9, (music, ('/home/mike/sound/artists/nofx/white-trash-two-heebs-and-a-bean--i-wanna-be-your-baby.mp3','NOFX\nWhite Trash, Two Heebs and a Bean\n"I Wanna Be Your Baby"','/home/mike/sound/albums/nofx--white-trash-two-heebs-and-a-bean/art.jpeg')) ) 
    day3.insert( -2, (title, ('Brad getting Florian\'s ski...',3)) )
    day3.insert( -2, (title, ('...which was lost a few\nhundred meters earlier',3)) )
    actions.append( day3 )
    actions.append( (title, ('Day 4:\ngain Triffid Glacier',)) )
    day4 = makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day4'))
    day4.insert( 9, (title, ('Windless ridge-top cooking @ 3000m',4)) )
    day4.insert( 11, (title, ('(wow)',)) )
    day4.insert( 6, (music, ('/home/mike/sound/artists/bad-religion/bad-religion-recipe-for-hate--american-jesus.ogg','Bad Religion\nRecipe for Hate\n"American Jesus"','/home/mike/sound/albums/bad-religion--bad-religion-recipe-for-hate/art.jpeg')) )
    actions.append( day4 )
    actions.append( (title, ('Day 5:\nto Bonnet Glacier',)) )
    day5 = makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day5'))
    day5.insert(1, (title, ('...where\'d the sun go?!',)) )
    day5.insert(1, (title, ('Uhm...',)) )
    actions.append( day5 )
    actions.append( (startmovie, ('/home/mike/photos/slideshow//april-12-2007--drummond-bonnet-traverse/day5/bar.mpeg', None)) )
    actions.append( (title, ('Day 6:\nwallow down Johnson Creek',)) )
    actions.append( makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day6')) )
    actions.append( (title, ('Day 7:\nexit via\nLuellen Lake/Rockbound',3)) )
    day7 = makeactions(makeimages('/home/mike/photos/slideshow/april-12-2007--drummond-bonnet-traverse/day7'))
    day7.insert(2, (title, ('Prepare for extreme tree-humping...',4)) )
    day7.insert(4, (music, ('/home/mike/sound/artists/nirvana/nevermind--stay-away.ogg','Nirvana\nnevermind\n"Stay Away"','/home/mike/sound/albums/nirvana--nevermind/art.jpeg')) )
    day7.insert(-2, (title, ('Releasing the demons...',)) )
    day7.insert(-1, (title, ('...from Brad\'s socks',)) )
    actions.append( day7 )


if postIntermission:
    actions.append( (music, ('/home/mike/sound/artists/nofx/punk-in-drublic--my-heart-is-yearning.mp3','NOFX\nPunk in Drublic\n"My Heart is Yearning"','/home/mike/sound/albums/nofx--punk-in-drublic/art.jpeg')) )
    actions.append( (title, ('April 21 - 24, 2007',)) )
    actions.append( (title, ('Columbia Icefields',)) )
    actions.append( (title, ('Shaun\nRobin\nDiane',)) )
    pics = makeactions(makeimages('/home/mike/photos/slideshow/april-21-2007--columbia'))
    ### different muzack?
    pics.insert(19, (music, ('/home/mike/sound/artists/rjd2/deadringer--ghostwriter.mp3','RJD2\nDeadringer\n"Ghostwriter"', '/home/mike/sound/albums/rjd2--deadringer/art.jpeg')) )
    actions = actions + pics
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/april-21-2007--columbia/ymca',0.5))
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/april-21-2007--columbia/post-ymca'))

if postIntermission:
    actions.append( (title, ('May 5, 2006',)) )
    actions.append( (title, ('Cochrane/Kananaskis',)) )
    actions.append( (title, ('www.AlbertaRandonneurs.com',)) )
    actions = actions + makeactions(makeimages('/home/mike/photos/slideshow/may-5-2007--rando'))

if postIntermission:
    actions.append( (music, ('/home/mike/sound/artists/the-beatles/rubber-soul--nowhere-man.mp3','The Beatles\nRubber Soul\n"Nowhere Man"','/home/mike/sound/albums/the-beatles--rubber-soul/art.jpeg')) )
    actions.append( (title, ('', 1 )) )
    actions.append( (title, ('Made using the following\nFree/Open-Source Software:', 5 )) )
    actions.append( (title, ('GNU/Linux\nwww.gnu.org\nwww.kernel.org', 3 )) )
    actions.append( (title, ('The GIMP\nwww.thegimp.org', 2 )) )
    actions.append( (title, ('Python\nwww.python.org', 2 )) )
    actions.append( (title, ('pygame\nwww.pygame.org', 2 )) )
    actions.append( (title, ('LiVES\n(video editing)\nlives.sourceforge.net', 3 )) )
    actions.append( (title, ('(and l33t h4x0r sk1llz...)', 2 )) )

if postIntermission:
    actions.append( (title, ('Thanks for the pictures made by:', 5 )) )
    actions.append( (title, ('Florian Jungen', )) )
    actions.append( (title, ('Neil Warren', )) )
    actions.append( (title, ('Esther Visser', )) )
    actions.append( (title, ('Craig Smith', )) )
    actions.append( (title, ('Brad Cooke', )) )
    actions.append( (title, ('Rene Chapman', )) )
    actions.append( (title, ('Robin Harnett', )) )

if postIntermission:
    actions.append( (title, ('and thanks for video from', 3 )) )
    actions.append( (title, ('Neil Warren', )) )
    actions.append( (title, ('Brad Cooke', )) )


if postIntermission:
    actions.append( (title, ('', )) )
    actions.append( (title, ('The End', )) )

if 0:
    title( '(hit space)', 1, (100,100,100))
    #pygame.display.toggle_fullscreen()
    waitForKey()

if 1:
    if preIntermission:
        title("Mike and Esther's\nSpring Slide Show Extravaganza\n\n\"Fun in 2006 + 2007\"")
    else:
        title("Welcome back to\nMike and Esther's\nSpring Slide Show Extravaganza")
    waitForKey()

print actions
print "total actions:",len(actions)

movie = None
paused = False
nextActionImmediately = True
autopilot = True
action = None
while 1:
    evt = pygame.event.poll()

    doaction = False
    if evt.type == pygame.NOEVENT:
        if nextActionImmediately is True or autopilot:
            if not movie or not movie.get_busy():
                doaction = True
                nextActionImmediately = False

        pygame.time.delay(25)
    
    print evt
    if evt.type == pygame.KEYUP:
        if evt.key == 113:
            print "QUIT!"
            break
        elif evt.key == 112:
            if movie:
                if not paused:
                    print "pausing movie"
                    movie.pause()
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    print "resuming movie"
                    movie.pause()
                    pygame.mixer.music.unpause()
                    paused = False
                    
        elif evt.key == 32 or evt.key == 110:
            if movie and movie.get_busy():
                if evt.key == 32:
                    print "  movie still playing; be patient"
                    continue
                else:
                    movie.stop()
                    pygame.mixer.music.stop()
            doaction = True

    if doaction:
        doaction = False

                                        # try to use ref-counting, not
                                        # the garbage-collector
        if action:
            (fn, args) = action
            for foo in args:
                del foo
            del args

        if len(actions) == 0:
            print "nothing else!"
            break;
        action = actions[0]
        if type(action) == type([]):
            actions = action + actions[1:]
            action = actions[0]
        actions = actions[1:]
        print "next-action:",action
        screen.fill((0,0,0))
        (fn,args) = action
        rtn = fn(*args)
        if rtn:
            movie = rtn
#        if fn == music:
#            nextActionImmediately = True

if postIntermission:
    waitForKey()
