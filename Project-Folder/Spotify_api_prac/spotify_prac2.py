import base64
from requests import post, get
import json
import datetime
from urllib.parse import urlencode
import time

client_id = "2630db6077e3463ab075a88b69cb120e"
client_secret = "ff314ca0a3f941a999638e2e40e53fdf"

class SpotifyAPI(object):
    access_token = None
    access_token_expiration = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret


    def get_client_credentials(self):
        """
        returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        
        if client_secret == None or client_id == None:
            raise Exception("You must set client id and client secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
        "Authorization": f"Basic {client_creds_b64}"
    }

    def get_token_data(self):
        return {
        "grant_type": "client_credentials"
    }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        result = post(token_url, data=token_data, headers=token_headers)

        if result.status_code not in range(200, 299):
            raise Exception("Could Not Authenticate Client... ")
            # return False
        data = json.loads(result.content)
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expiration = expires
        self.access_token_did_expire = expires < now
        # print(expires)
        return True
    


    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expiration
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            return self.get_access_token()
        return token



    def get_resource_header(self):
        access_token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers



    def get_resource(self, lookup_id, resource_type='albums', version='v1', search_type='None'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{search_type}?country=US"
        headers = self.get_resource_header()
        results = get(endpoint, headers=headers)
        if results.status_code not in range(200, 299):
            return {}
        return results.json()



    def get_artist_albums(self, _id):
        get_resource = self.get_resource(_id, resource_type='artists', search_type='albums')
        json_results = get_resource['items']
        return json_results

    def get_artist_top_tracks(self, _id):
        get_resource = self.get_resource(_id, resource_type='artists', search_type='top-tracks')
        json_results = get_resource['tracks']
        return json_results



    def search_for_query(self, query_params):
        headers = self.get_resource_header()

        endpoint = "https://api.spotify.com/v1/search"

        lookup_url = f"{endpoint}?{query_params}"
        results = get(lookup_url, headers=headers)
        # print(results.status_code)
        if results.status_code not in range(200, 299):
            return {}
        json_results = results.json()['artists']['items']
        if len(json_results) == 0:
            print("No artist with that name exists...")
            return None
        return json_results[0]
        


    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
                if operator.lower() == "or" or operator == "not":
                    operator = operator.upper()
                    if isinstance(operator_query, str):
                        query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower(), "limit":'1'})
        
        return self.search_for_query(query_params)



# Function to call what data you would like to pull
    def get_which_data(self):
        choice = 'none'
 
        while choice not in ['1','2']:
            print("Which artist data are you looking for?")
            time.sleep(.3)
            print("For top songs, type: 1")
            time.sleep(.3)
            print("For their albums, type: 2")
            time.sleep(.3)
            choice = input("Choose:  ")
        if choice not in ['1','2']:
            print("Choices are: ")
            time.sleep(.3)
            print("Top songs which is: 1")
            time.sleep(.3)
            print("Albums which is 2")
        return int(choice)
    
    def return_data(self, dataChoice, artist_id):
        if dataChoice == 2:
            artist_albums = self.get_artist_albums(artist_id)
            for idx, album in enumerate(artist_albums):
                print(f"{idx + 1}. {album['name']}")
                
        elif dataChoice == 1:
            artistSongs = self.get_artist_top_tracks(artist_id)
            for idx, song in enumerate(artistSongs):
                print(f"{idx + 1}. {song['name']}")
                
        





def put_together():
    query_params = str(input("What artist to search for?: "))
    client = SpotifyAPI(client_id, client_secret)
    # print(client.perform_auth())
    results = client.search(query_params)
    artist_id = results["id"]
    data = client.get_which_data()
    client.return_data(data, artist_id)
    


def main():
    put_together()




if __name__ == "__main__":
    main()