from __future__ import unicode_literals

import logging
import time
import discid
import CDDB, DiscID
import unicodedata

logger = logging.getLogger(__name__)

class Cdrom(object):

    def __init__(self):
        self.refresh()
    
    def sanitizeString(self, string):
        return unicode(string.decode('iso-8859-1').encode('utf-8'), 'utf-8')

    def refresh(self):
        self.disc = discid.read()
        logger.debug("Cdrom: reading cd")
        self.n = len(self.disc.tracks)
        logger.debug('Cdrom: %d tracks found',self.n)
        read_info = {}
        try:
            self.disc_id = DiscID.disc_id(DiscID.open())
            (query_status, query_info) = CDDB.query(self.disc_id)
            (read_status, read_info) = CDDB.read(query_info['category'], query_info['disc_id'])
        except:
            pass
        if 'DYEAR' in read_info:
            self.year = read_info['DYEAR']
        else:
            self.year = ''
        if 'DGENRE' in read_info:
            self.genre = read_info['DGENRE']
        else:
            self.genre = 'unknown'
        if 'DTITLE' in read_info:
            self.albumtitle = self.sanitizeString(read_info['DTITLE'])
        else:
            self.albumtitle = 'CD'
        self.tracks=[]
        for track in self.disc.tracks:
            number = track.number
            duration = track.seconds
            key = 'TTITLE' + `(track.number-1)`
            if key in read_info:
                name = self.sanitizeString(read_info[key])
            else:
                name = 'Cdrom Track %s (%s)' % (number, time.strftime('%H:%M:%S', time.gmtime (duration)))
            self.tracks.append((number,name,duration,self.albumtitle,self.genre,self.year))
