#!/usr/bin/python3
import json
import requests
import urllib
from urllib.parse import quote

j = None

try:
    with open("./bungieapi.json", "r") as f:
        j = json.load(f)
except Exception as e:
    if (debug):
        print(str(e))
        sys.exit("Fatal Error: could not resolved json.")

if not (j):
    sys.exit("Fatal Error: could not resolved json.")

membership_type = 254
membership_id = 4611686018431237019

try:
    HEADERS = {
        "X-API-Key": j['api_key']
    }


    """
    #print(HEADERS)
    #GetMembershipDataById (bungie id to destiny id)
    #r = requests.get("https://www.bungie.net/platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/gun", headers=HEADERS)
    #r = requests.get("https://www.bungie.net/platform/User/GetBungieNetUserById/4611686018431237019", headers=HEADERS)
    bungie_response = requests.get(f"https://www.bungie.net/platform/Destiny2/{membership_type}/Profile/{membership_id}/LinkedProfiles/", headers = HEADERS)

    if (bungie_response.status_code != 200):
        #print(f"Response from bungie was not 200:\n\t{bungie_response.status_code}\n\t{bungie_response.content}")
        sys.exit("Fatal Error: Could not retrieve LinkedProfiles endpoint.")


    bungie_record = json.loads((bungie_response.content).decode(bungie_response.encoding))
    bungie_response = bungie_record['Response']
    bnet_info = bungie_response['bnetMembership']

    applicable_membership_types = []
    #print(bnet_info)
    for profile in bungie_response['profiles']:
        #print(profile)
        applicable_membership_types = profile['applicableMembershipTypes']
    #applicable_membership_types = bungie_record['Response']['profiles']['applicableMembershipTypes']
    #print(applicable_membership_types)
    """
    
    # This would ususally get grabbed by a previous set of calls, same as the membership_id.
    applicable_membership_types = [3, 1]

    # Gets a Destiny account (has profile/character/item data, whatever we request in the querystring parameters)
    #/Destiny2/{membershipType}/Profile/{destinyMembershipId}/
    querystring = "Profiles,Characters,CharacterRenderData,CharacterEquipment,CharacterLoadouts"
    querystring_int = "100,200,203,205,206"
    
    if (1 not in applicable_membership_types):
        print("Can't complete this request. Invalid membership types available.")
        sys.exit("Fatal Error: Could not not retrieve Profile endpoint. Membership type '1' not available.")

    bungie_account_response = requests.get(f"http://www.bungie.net/Platform/Destiny2/1/Profile/{membership_id}/?components={querystring}", headers = HEADERS)
    if (bungie_account_response.status_code != 200):
        print(f"Response from bungie was not 200:\n\t{bungie_account_response.status_code}\n\t{bungie_account_response.content}")
        sys.exit("Fatal Error: Could not not retrieve Profile endpoint.")
    
    bungie_account = json.loads((bungie_account_response.content).decode(bungie_account_response.encoding))
    
    profile_data = bungie_account['Response']['profile']
    character_ids = bungie_account['Response']['profile']['data']['characterIds']
    characters = bungie_account['Response']['characters']
    character_loadouts = bungie_account['Response']['characterLoadouts']
    character_render_data = bungie_account['Response']['characterRenderData']    
    
    print("Profile Data\n====================================================")
    print(profile_data)
    print("\n\nCharacter Ids\n====================================================")
    print(character_ids)
    print("\n\nCharacter Data\n====================================================")
    print(characters)
    print("\n\nCharacter Loudouts\n====================================================")
    print(character_loadouts)
    print("\n\nCharacter Render Data\n====================================================")
    print(character_render_data)
    
    # For getting a specific character:
    #/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/
    

except Exception as e:
    print("no work")
    print(str(e))


# I should make a wrapper for actually doing the "get" with headers and parameters, and then another for decoding the response and parsing it for errors.
