import flickrapi
import ffrsettings

def get_flickr():

    settings = ffrsettings.ffrsettings()

    api_key = settings.flickrkey
    api_secret = settings.flickrsecret

    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    # Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='write'):

        print('To authenticate visit the following URL')

        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='write')
        print(authorize_url)
        #webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)

    return flickr

if __name__ == "__main__":
    get_flickr()
