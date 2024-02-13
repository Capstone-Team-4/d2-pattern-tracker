#!/usr/bin/python3
import json
import requests
import urllib
from urllib.parse import quote
import os
import zipfile
import pickle
import sqlite3




"""
Major Section - Helper Data
"""
hashes = {
    'DestinyActivityDefinition': 'activityHash',
    'DestinyActivityTypeDefinition': 'activityTypeHash',
    'DestinyClassDefinition': 'classHash',
    'DestinyGenderDefinition': 'genderHash',
    'DestinyInventoryBucketDefinition': 'bucketHash',
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyProgressionDefinition': 'progressionHash',
    'DestinyRaceDefinition': 'raceHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyUnlockFlagDefinition': 'flagHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyDirectorBookDefinition': 'bookHash',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyDestinationDefinition': 'destinationHash',
    'DestinyPlaceDefinition': 'placeHash',
    'DestinyActivityBundleDefinition': 'bundleHash',
    'DestinyStatGroupDefinition': 'statGroupHash',
    'DestinySpecialEventDefinition': 'eventHash',
    'DestinyFactionDefinition': 'factionHash',
    'DestinyVendorCategoryDefinition': 'categoryHash',
    'DestinyEnemyRaceDefinition': 'raceHash',
    'DestinyScriptedSkullDefinition': 'skullHash',
    'DestinyGrimoireCardDefinition': 'cardId',
    'DestinyRecordDefinition': 'hash'
}

hashes_trunc = {
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyStatGroupDefinition': 'statGroupHash'
}



"""
Major Section - Helper Functions
"""
# This function checks for the local file, "manifest.pickle".
# If it exists, it loads it (hopefully a dictionary representation of the SQLITE manifest)
# If it doesn't, it will make it and return a dictionary representation of the SQLITE manifest (this will always be correct).
def get_manifest(filepath, hash_dict):
    if (not os.path.exists(filepath)):
        manifest_response = requests.get(f"http://www.bungie.net/platform/Destiny/Manifest/", headers = HEADERS)
        manifest = json.loads((manifest_response.content).decode(manifest_response.encoding))
        for key,value in manifest['Response'].items():
            print(key)
        manifest_content_en_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']

        db_file = requests.get(manifest_content_en_url)
        with open("MANIFEST-ZIP", "wb") as zipped:
            zipped.write(db_file.content)
        print("Downloaded compressed manifest to 'MANIFEST-ZIP'")

        with zipfile.ZipFile("MANIFEST-ZIP") as zipped:
            name = zipped.namelist()
            zipped.extractall()
        os.rename(name[0], 'manifest.content')
        print("Unzipped namifest to 'manifest.content'")


        con = sqlite3.connect('manifest.content')
        print("Connected to local SQLITE database.")

        cur = con.cursor()

        all_data = {}
        for table_name in hash_dict.keys():
            cur.execute('SELECT json from ' + table_name)
            print("Generating " + table_name + " dictionary...")

            items = cur.fetchall()

            item_jsons = [json.loads(item[0]) for item in items]

            item_dict = {}
            hashed = hash_dict[table_name]
            for item in item_jsons:
                item_dict[item[hashed]] = item

            all_data[table_name] = item_dict
        print("Dictionary Generated.")
        with open(filepath, "wb") as data:
            pickle.dump(all_data, data)
            print(f"Manifest Dictionary placed into '{filepath}'")
        return(all_data)

    else:
        with open(filepath, "rb") as data:
            all_data = pickle.load(data)
        return(all_data)

# I should make a wrapper for actually doing the "get" with headers and parameters, and then another for decoding the response and parsing it for errors.



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
    querystring = "Profiles,Characters,CharacterRenderData,CharacterEquipment,CharacterLoadouts,Records,Craftables"
    querystring = "Craftables"
    querystring_int = "100,200,203,205,206,900,1300"

    if (1 not in applicable_membership_types):
        print("Can't complete this request. Invalid membership types available.")
        sys.exit("Fatal Error: Could not not retrieve Profile endpoint. Membership type '1' not available.")

    bungie_account_response = requests.get(f"http://www.bungie.net/Platform/Destiny2/1/Profile/{membership_id}/?components={querystring}", headers = HEADERS)
    if (bungie_account_response.status_code != 200):
        print(f"Response from bungie was not 200:\n\t{bungie_account_response.status_code}\n\t{bungie_account_response.content}")
        sys.exit("Fatal Error: Could not not retrieve Profile endpoint.")

    bungie_account = json.loads((bungie_account_response.content).decode(bungie_account_response.encoding))

    #print(json.dumps(bungie_account['Response'], indent = 2))

    profile_data = bungie_account['Response']['profile']
    character_ids = bungie_account['Response']['profile']['data']['characterIds']
    characters = bungie_account['Response']['characters']
    character_loadouts = bungie_account['Response']['characterLoadouts']
    character_render_data = bungie_account['Response']['characterRenderData']
    profile_records = bungie_account['Response']['profileRecords']
    character_craftables = bungie_accont['Response']['characterCraftables']['data']

    """
    print("Profile Data\n====================================================")
    print(profile_data)
    print("\n\nCharacter Ids\n====================================================")
    print(character_ids)
    print("\n\nCharacter Data\n====================================================")
    print(characters)
    print("\n\nCharacter Loadouts\n====================================================")
    print(character_loadouts)
    print("\n\nCharacter Render Data\n====================================================")
    print(character_render_data)
    print("\n\nProfile Record Data\n====================================================")
    print(json.dumps(profile_records, indent = 2))
    """

    # For getting a specific character:
    #/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/
    manifest = get_manifest("manifest.pickle", hashes)
    flag = False

    """
    for key,value in manifest.items():
        print(f"{key}")

    for key,value in manifest['DestinyRecordDefinition'].items():
        print(f"{key} :")
        for key2,val2 in value.items():
            print(f"\t{key2} : {val2}")
        if (value['displayName'] == "Father's Sins"):
            flag = True
        print("")
    if flag:
        print("Found it!")

    """
    for character in character_craftables:
        print(character)

except Exception as e:
    print("no work")
    print(str(e))
    print(e)
