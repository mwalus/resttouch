RestTouch v0.1
=========
REST client for Python

## Installation:
    pip install resttouch

## Example usage:
    from resttouch import Service, serializator, end_point
    from resttouch.params import QueryParam, PathParam
    from resttouch.routes import Route
    from resttouch.serializators import SimpleJSON

    @serializator(SimpleJSON)
    @end_point('https://api.twitter.com')
    class TwitterService(Service):
      retweeted_by = Route('GET', '1/statuses/%(id)s/retweeted_by.json',
            PathParam('id'),
            QueryParam('count', required=False),
            QueryParam('page', required=False)
      )
    
      users_shows = Route('GET', '1/users/show.json',
            QueryParam('id'),
            QueryParam('include_entities', default='true')
      )
      
    twitter = TwitterService()
     
    print twitter.retweeted_by(id="21947795900469248", count=5)
    print twitter.users_shows(id='6253282')

    
 
