import time


class _DateParser:

    class Error(Exception):
        pass

    def __init__( self ):

        self._formats = []
        self._formats.append( "%H:%M %B %d, %Y" )
        self._formats.append( "%B %d, %Y" )
        self._formats.append( "%B %d, %y" )
        self._formats.append( "%b %d, %Y" )
        self._formats.append( "%a, %d %b %Y" )
        self._formats.append( "%a, %d %b %Y %H:%M:%S -0700 (MST)" )
        self._formats.append( "%a, %d %b %Y %H:%M:%S -0600 (MDT)" )
        self._formats.append( "%a, %d %b %Y %H:%M:%S -0600" )
        self._formats.append( "%a %b %d %H:%M:%S %Y" )
        self._formats.append( "%b %d, %Y %H:%M" )
        self._formats.append( "%a %b  %d %Y %H:%M:%S %Y" )
        self._formats.append( "%b %d %Y %H:%M:%S -0600" )
        self._formats.append( "%d %b %Y %H:%M:%S -0600" )
        self._formats.append( "%d %b %Y %H:%M:%S -0700" )
        self._formats.append( "%d %b %Y %H:%M:%S" )
        self._formats.append( "%a %b %d %H:%M:%S MDT %Y" )

    def parse( self, str ):

        for frmt in self._formats:
            try:
                return time.strptime( str, frmt )

            except ValueError:
                pass

        raise "DateParser: couldn't parse " + str + "\n"
        return None

    

DATE_PARSER = _DateParser()
def parseDate( date ):
    return DATE_PARSER.parse( str(date).strip() )

