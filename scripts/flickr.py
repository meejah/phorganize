##
## NOTE: this was copied from mike-warren stuff on may 4, 2010
##


class ApiError:
    def __init__(self,*args):
        self.text = reduce(lambda x, y: str(x) + ' ' + str(y), args, '').strip()
    def __repr__(self):
        return '<ApiError "%s">' % self.text
    def __str__(self):
        return self.__repr__()

class MikeFlickr:
    def __init__(self,fapi,apikey,authtoken):
        self.fapi = fapi
        self.apiKey = apikey
        self.authToken = authtoken

    def replace(self, filename, photoidToReplace, title='', description='', tags='', isPublic=False, isFriend=False, isFamily=False):
        
        fapi = self.fapi
        args = {'title':str(title),
                'description':str(description),
                'tags':str(tags),
                'is_public':isPublic and '1' or '0',
                'is_friend':isFriend and '1' or '0',
                'is_family':isFamily and '1' or '0',
                'api_key':self.apiKey,
                'auth_token':self.authToken,
                'photo_id':str(photoidToReplace)
                }
        rsp = fapi.upload(filename=filename, **args)
        self.raiseOnError(rsp)
        fapi.testFailure(rsp)
        photoid = rsp.photoid[0].elementText
        return int(photoid)

    def imagesByTag(self, tags, privateOnly=False):
        fapi = self.fapi
        page = 1
        args = {'tags':str(tags),
                'tag_mode':'all',       # "any" for OR or "all" for AND-type operation
                'user_id':'me',
                'page':str(page),
                'per_page':str(400),
                
                'api_key':self.apiKey,
                'auth_token':self.authToken
                }

#        if privateOnly:
#            args['privacy_filter'] = 5

        rtn = []

        total = None
        while True:
            rsp = fapi.photos_search(**args)
            self.raiseOnError(rsp)
            fapi.testFailure(rsp)
            print rsp,dir(rsp)
            print rsp.attrib.items()
            if total is None:
                print rsp.photos[0].attrib
                total = int(rsp.photos[0]['total'])
                print "TOTAL",total
            
            for p in rsp.photos[0].photo:
                rtn.append( (p['id'], p['title']) )

            if total and len(rtn) == total:
                return rtn
            else:
                print "total=",total
                print "so far=",len(rtn)
            page = page + 1
            args['page'] = str(page)
            
        return rtn
        
        
    def upload(self, filename, title='', description='', tags='', isPublic=False, isFriend=False, isFamily=False):
        """replace flickrapi's upload method with something useful"""

        fapi = self.fapi
        args = {'title':str(title),
                'description':str(description),
                'tags':str(tags),
                'is_public':isPublic and '1' or '0',
                'is_friend':isFriend and '1' or '0',
                'is_family':isFamily and '1' or '0',
                'api_key':self.apiKey,
                'auth_token':self.authToken
                }
        rsp = fapi.upload(filename=filename, **args)
        self.raiseOnError(rsp)
        fapi.testFailure(rsp)
        photoid = rsp.photoid[0].elementText
        return int(photoid)

    def delete(self,photoid):
        args = {'api_key':self.apiKey,
                'auth_token':self.authToken,
                'photo_id':str(photoid)
                }
        rsp = self.fapi.photos_delete(**args)
        self.raiseOnError(rsp)
        return

    def isErrorResponse(self,rsp):
        if rsp['stat'] == 'fail':
            return int(rsp.err[0]['code'])
        return False
    def raiseOnError(self,rsp):
        code = self.isErrorResponse(rsp)
        if code:
            raise ApiError(code,rsp.err[0]['msg'])
