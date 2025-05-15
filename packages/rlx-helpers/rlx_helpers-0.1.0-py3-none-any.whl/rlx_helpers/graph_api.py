import requests
from re import match

class GraphAPI:

    def __init__(self, token: str):

        self.token = token

    def get_graph_resource(self, url_substring: str, as_json: bool = True) -> dict:
        """
        Makes a GET request to the specified Microsoft Graph API endpoint.
        
        Params: 
            url_substring: The endpoint path after the base Graph API URL.
            as_json: Determines whether to return the response content in json
            format or as binary data.

        Returns: 
            The JSON response as a dictionary, or the byte representation.
        """
        # Construct headers
        headers = {"Authorization": f"Bearer {self.token}"}

        # Send GET request
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/{url_substring}", 
            headers=headers
        )

        # Check response for errors
        response.raise_for_status()

        if as_json:
            return response.json()
        else:
            return response.content
    
    def list_sharepoint_folder(self, site_id, drive_id, folder_path) -> str:
        '''
        Lists the details of a given SharePoint folder using the MS Graph API.

        Params:
            site_id: The ID of the SharePoint site the folder is located in.
            drive_id: The ID of the document library the folder is located in.
            folder_path: The path to the folder excluding the root directory.
        
        Returns:
            The JSON response as a dictionary.
        '''
        substring = f'sites/{site_id}/drives/{drive_id}/root:/{folder_path}:/children'
        return self.get_graph_resource(substring)
    
    def find_single_item(self, site_id, drive_id, folder_path, regex_pattern):
        '''
        Locate a single item of given parameters within a folder by using a
        regex search for the item name. This function must return one and only
        one item, or else throw a ValueError.
        '''

        folder_contents = self.list_sharepoint_folder(site_id, drive_id, folder_path)
        data = folder_contents.get('value', [])
   
        matches = []
        for item in data:
            if match(regex_pattern, item.get('name', '')):
                matches.append(item)
                if len(matches) > 1:
                    raise ValueError('More than 1 item was found. Refine search pattern.')
        
        if not matches:
            raise ValueError('No items matching the pattern were found.')
        
        return matches[0]
    
    def find_and_download_single_item(self, site_id, drive_id, folder_path, regex_pattern):
        """
        Downloads a single item from a SharePoint folder based on a regex 
        pattern.

        Args:
            site_id: The ID of the SharePoint site.
            drive_id: The ID of the document library.
            folder_path: The path to the folder.
            regex_pattern: The regex pattern to match the item name.

        Returns:
            The content of the item as bytes.
        """
        item = self.find_single_item(site_id, drive_id, folder_path, regex_pattern)
        file_id = item.get('id', '')

        substring = f"sites/{site_id}/drives/{drive_id}/items/{file_id}/content"
        data = self.get_graph_resource(substring, as_json=False)

        return data

    def download_all_items_in_folder(self, site_id, drive_id, folder_path):
        """
        Downloads all items from a SharePoint folder.

        Params:
            site_id: The ID of the SharePoint site.
            drive_id: The ID of the document library.
            folder_path: The path to the folder within the doc library.

        Returns:
            A list of tuples, where each tuple contains the item's name and its 
            content as bytes.
        """
        folder_contents = self.list_sharepoint_folder(site_id, drive_id, folder_path)
        data = folder_contents.get('value', [])

        downloaded_items = []
        for item in data:
            item_id = item.get('id', '')
            item_name = item.get('name', '')
            substring = f"sites/{site_id}/drives/{drive_id}/items/{item_id}/content"
            item_data = self.get_graph_resource(substring, as_json=False)
            downloaded_items.append((item_name, item_data))

        return downloaded_items
