import requests, time, os, copy, math, re
from datetime import datetime, timedelta
from .utils import utils_save_json, utils_read_json, print_deb
from .mal_config_utils import config_setup, regenerate_token, minimal_setup

# Paths

script_path = os.path.dirname(os.path.abspath(__file__))
mal_id_cache_path = os.path.join(script_path, 'cache', 'myanimelist_id_cache.json')
mal_search_cache_path = os.path.join(script_path, 'cache', 'myanimelist_search_cache.json')
mal_to_al_cache_path = os.path.join(script_path, 'cache', 'mal_to_al_cache.json')
config_path = os.path.join(script_path, 'config', 'config.json')
anime_request_url = "https://api.myanimelist.net/v2/anime"

# Global vars

al_to_mal_user_status = {
    'CURRENT': "watching",
    'COMPLETED': "completed",
    'PAUSED': "on_hold",
    'DROPPED': "dropped",
    'PLANNING': "plan_to_watch"
}

mal_to_al_user_status = {v:k for k, v in al_to_mal_user_status.items()}

al_to_mal_status = {
    'FINISHED': "finished_airing",
    'RELEASING': "currently_airing",
    'NOT_YET_RELEASED': "not_yet_aired"
}

mal_to_al_status = {v:k for k, v in al_to_mal_status.items()}
status_options = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
media_formats = ['TV', 'MOVIE', 'SPECIAL', 'OVA', 'ONA', 'MUSIC']

# Minimal user setup to interact with MyAnimeList API
config = utils_read_json(config_path)
client_id = minimal_setup()

# Utils

def clear_cache():
    config = utils_read_json(config_path)
    try:
        del config["checked_date"]
    except:
        pass
    os.remove(mal_id_cache_path)
    os.remove(mal_search_cache_path)

def check_status_in_cache():
    og_cache = utils_read_json(mal_id_cache_path)
    if not og_cache: return
    cache = copy.deepcopy(og_cache)
    config_dict = utils_read_json(config_path) if utils_read_json(config_path) else {}
    current_date = datetime.now().date()
    try:
        checked_date = datetime.strptime(config_dict['checked_date'], '%Y-%m-%d').date()
    except:
        config_dict['checked_date'] = current_date.strftime('%Y-%m-%d')
        utils_save_json(config_path, config_dict)
        checked_date = current_date
    if current_date > checked_date:
        for anime in og_cache:
            try:
                release_date = datetime.strptime(cache[anime]['release_date'], '%Y-%m-%d').date()
            except:
                release_date = None
            try:
                end_date = datetime.strptime(cache[anime]['end_date'], '%Y-%m-%d').date()
            except:
                end_date = None
            status = cache[anime]['status']
            if status == "NOT_YET_RELEASED":
                cache.update(get_anime_info(anime, True)) #force update everytime
            elif status == "RELEASING" and release_date:
                    try:
                        next_ep_date = release_date + timedelta(cache[anime]['upcoming_ep'] * 7)
                        if end_date and current_date > end_date:
                            updated_info = get_anime_info(anime, True)
                            cache.update(updated_info)
                        if current_date > next_ep_date:
                            updated_info = get_anime_info(anime, True)
                            cache.update(updated_info)
                    except: #force update if we don't have the next episode
                        updated_info = get_anime_info(anime, True)
                        cache.update(updated_info)
        config_dict['checked_date'] = current_date.strftime('%Y-%m-%d')
        utils_save_json(config_path, config_dict)
        utils_save_json(mal_id_cache_path, cache, True)

def load_cache():
    check_status_in_cache()
    return utils_read_json(mal_id_cache_path)

def load_config():
    config = utils_read_json(config_path)
    try:
        return config['myanimelist_user_token']
    except:
        return config_setup()['myanimelist_user_token']

# Functions

def make_mal_request(mal_api_url, params, method='get', mal_token=None, user_request = False):
    local_token = False
    if user_request:
        if mal_token:
            pass
        elif 'myanimelist_key' in os.environ:
            mal_token = os.getenv('myanimelist_key')
            if not os.path.exists(config_path):
                os.makedirs(os.path.dirname(config_path))
        else:
            mal_token = load_config()
            local_token = True
        HEADERS = {'Authorization': f"Bearer {mal_token}"}
    else:
        HEADERS = {'X-MAL-CLIENT-ID': f"{client_id}"}

    def make_request():
        request_func = getattr(requests, method.lower(), None)
        if method.lower() == 'put':
           response = request_func(mal_api_url, data=params, headers=HEADERS)
        else: 
            response = request_func(mal_api_url, params=params, headers=HEADERS)    
        return response

    retries = 0
    while True:
        response = make_request()
        if response.status_code == 200:
            json_response = response.json()
            if 'data' in json_response:
                return json_response['data']
            return json_response
        elif response.status_code == 429:
            print_deb(f"Rate limit exceeded. Waiting before retrying...")
            print_deb(params, HEADERS, sep="\n")
            print_deb(response.json())
            retry_after = int(response.headers.get('retry-after', 1))
            time.sleep(retry_after)
            retries += 1
        elif response.status_code == 500 or response.status_code == 400:
            print_deb(f"Unknown error occurred, retrying...")
            print_deb(params, HEADERS, sep="\n")
            print_deb(response.json())
            retries += 1
        elif response.status_code == 404:
            print(f"Anime not found")
            return None
        elif response.status_code == 401 and local_token:
            print_deb(f"Access token expired, refreshing")
            regenerate_token()
            retries += 1
        else:
            print_deb(f"Error {response.status_code}: {params}")
            return {}

        # Exponential backoff with a maximum of 5 retries
        if retries >= 5:
            print_deb("Maximum retries reached. Exiting.")
            return {}
                
        print(f"Retrying... (Attempt {retries})")

def get_all_anime_for_user(status_list="ALL", media_format = None, amount = 0, mal_token=None, username = None):
    if not username:
        username = get_userdata(mal_token)[0]
        user_request = True
    else:
        user_request = False
        
    def main_function(status):
        status = status.upper()
        params = {}
        params['sort'] = "list_updated_at"
        params['limit'] = 1000 if not amount else amount
        params['fields'] = (
            "id,"
            "title,"
            "alternative_titles,"
            "start_date,"
            "end_date,"
            "nsfw,"
            "media_type,"
            "status,"
            "genres,"
            "my_list_status{status,num_times_rewatched,is_rewatching,num_episodes_watched},"
            "num_episodes,"
            "related_anime"
        )
        if status != "ALL" and status != "REPEATING":
            if not status in status_options:
                print("Invalid status option. Allowed options are:", ", ".join(str(option) for option in status_options))
                return
            params['status'] = al_to_mal_user_status[status]

        request_url = f"https://api.myanimelist.net/v2/users/{username}/animelist"
        data = make_mal_request(request_url, params, mal_token = mal_token, user_request = user_request)

        user_ids = {}
            
        if data:
            for anime_entry in data:
                anime_entry_data = anime_entry['node']
                if status == "REPEATING" and not anime_entry_data['my_list_status']['is_rewatching']:
                    continue
                if media_format and media_format != anime_entry_data['media_type']:
                    continue
                anime_id = anime_entry_data['id']
                anime_id = str(anime_id)
                anime_info = generate_anime_entry(anime_entry_data, mal_token)
                if not anime_id in user_ids:
                    user_ids[anime_id] = {}    # Initialize as a dictionary if not already initialized
                user_ids[anime_id].update(anime_info)
                try:
                    user_ids[anime_id]['watched_ep'] = anime_entry_data['my_list_status']['num_episodes_watched']
                    user_ids[anime_id]['watching_status'] = 'REPEATING' if anime_entry_data['my_list_status']['is_rewatching'] else mal_to_al_user_status[anime_entry_data['my_list_status']['status']]
                    user_ids[anime_id]['rewatch_count'] = anime_entry_data['my_list_status']['num_times_rewatched'] if 'num_times_rewatched' in anime_entry_data['my_list_status'] else 0
                except:
                    pass
            return user_ids
        print(f"No entries found for {username}'s {status.lower()} anime list.")
        return None    

    if isinstance(status_list, str):
        status_list = status_list.upper()
        main_function(status_list)
        return main_function(status_list)
    elif len(status_list) == 1:
        status = status_list[0].upper()
        main_function(status)
        return main_function(status_list)
    elif isinstance(status_list, list):
        ani_list = {}
        for status in status_list:
            status.upper()
            ani_list.update(main_function(status))
        return ani_list

def get_latest_anime_entry_for_user(status = "ALL", media_format = None, mal_token=None,  username = None):
    if not username:
        username = get_userdata(mal_token)[0]

    status = status.upper()
    data = get_all_anime_for_user(status, media_format, 1, mal_token, username)
    if data:
        return data
    print(f"No entries found for {username}'s {status.lower()} anime list.")
    return None

def get_anime_entry_for_user(mal_id, mal_token=None):
    mal_id = str(mal_id)

    params = {}
    params['fields'] = (
        "id,"
        "title,"
        "alternative_titles,"
        "start_date,"
        "end_date,"
        "nsfw,"
        "media_type,"
        "status,"
        "genres,"
        "my_list_status{status,num_times_rewatched,is_rewatching,num_episodes_watched},"
        "num_episodes,"
        "related_anime"
    )
    request_url = f"{anime_request_url}/{mal_id}"
    data = make_mal_request(request_url, params, mal_token = mal_token, user_request=True)
    anime_data = {}
    if data:
        anime_id = str(data['id'])
        if 'my_list_status' not in data:
            return None
        anime_data[anime_id] = generate_anime_entry(data, mal_token)
        anime_data[anime_id]['watched_ep'] = data['my_list_status']['num_episodes_watched']
        anime_data[anime_id]['watching_status'] = mal_to_al_user_status[data['my_list_status']['status']]
        anime_data[anime_id]['watching_status'] = 'REPEATING' if data['my_list_status']['is_rewatching'] else mal_to_al_user_status[data['my_list_status']['status']]
        anime_data[anime_id]['rewatch_count'] = data['my_list_status']['num_times_rewatched'] if 'num_times_rewatched' in data['my_list_status'] else 0
        return anime_data
    return None

def get_anime_info(anime_id, force_update = False, mal_token=None):
    if force_update:
        anime_cache = {}
    else:
        anime_cache = load_cache()
    anime_id = str(anime_id)
    if not anime_id:
        return None
    def fetch_from_mal():
        # Fetch anime info from myanimelist API or any other source
        anime_info = mal_fetch_anime_info(anime_id, mal_token)
        # Cache the fetched anime info
        utils_save_json(mal_id_cache_path, anime_info, False)
        return anime_info
    # Check if anime_id exists in cache
    try:
        if anime_id in anime_cache and not force_update:
                print_deb("Returning cached result for anime_id:", anime_id)
                return {anime_id: anime_cache[anime_id]}
        else:
            return fetch_from_mal()
    except TypeError:
        return fetch_from_mal()

def mal_fetch_anime_info(mal_id, mal_token=None):
    params = {
        'fields': (
            "id,"
            "title,"
            "alternative_titles,"
            "start_date,"
            "end_date,"
            "nsfw,"
            "media_type,"
            "status,"
            "genres,"
            "my_list_status,"
            "num_episodes,"
            "related_anime"
        )
    }
    
    request_url = f'{anime_request_url}/{mal_id}'
    data = make_mal_request(request_url, params, mal_token = mal_token)
    anime_data = {}
    if data:
        anime_id = str(data['id'])
        anime_data[anime_id] = {}
        anime_data[anime_id].update(generate_anime_entry(data, mal_token))
    return anime_data

def generate_anime_entry(anime_info, mal_token):
    def getRelated():
        def get_additional_info(relation_id):
            params = {
                'fields': "status, related_anime"
            }
            data = make_mal_request(anime_request_url + f"/{relation_id}", params, mal_token = mal_token)
            return data            
        
        relations = {}
        try:
            edges = anime_info['related_anime']
        except:
            edges = get_additional_info(anime_info['id'])['related_anime']
        for edge in edges:
            relation_type = edge['relation_type'].upper()
            if relation_type == "PREQUEL" or relation_type == "SEQUEL":
                relation_id = str(edge['node']['id'])
                relations[relation_id] = {}
                relations[relation_id]['main_title'] = edge['node']['title']
                relations[relation_id]['status'] = mal_to_al_status[get_additional_info(relation_id)['status']]
                relations[relation_id]['type'] = relation_type
        if not relations:
            relations = None
        return relations

    def is_sus(anime_data):
        genres = [item['name'] for item in anime_data['genres']]
        adult_status = False if anime_data['nsfw']== 'white' else True
        sus_genres = ['Hentai', 'Ecchi', 'Erotica']
        for sus_genre in sus_genres:
            if sus_genre in genres:
                return True
        return adult_status

    def generate_upcoming_ep(release_date):
            current_date = datetime.now().date()
            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            upcoming_ep = math.ceil(int((current_date - release_date).days)/7) + 1
            return upcoming_ep

    def ensure_day_in_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            try:
                year_month = datetime.strptime(date_str, '%Y-%m')
                full_date = year_month.replace(day=1)
                return full_date.strftime('%Y-%m-%d')
            except ValueError:
                return None

    anime_id = str(anime_info['id'])
    anime_data = {}
    anime_data['al_id'] = mal_to_al_id(anime_id)
    anime_data['total_eps'] = anime_info['num_episodes']
    anime_data['is_sus'] = is_sus(anime_info)
    anime_data['main_title'] = anime_info['title']
    anime_data['synonyms'] = [
            anime_info['alternative_titles']['ja'],
            anime_info['alternative_titles']['en'],
    ] + anime_info['alternative_titles']['synonyms']
    anime_data['synonyms'] = [item for item in anime_data['synonyms'] if item is not None]    
    anime_data['status'] = mal_to_al_status[anime_info['status']]
    anime_data['release_date'] = ensure_day_in_date(anime_info['start_date']) if 'start_date' in anime_info else None
    anime_data['end_date'] = ensure_day_in_date(anime_info['end_date']) if 'end_date' in anime_info else None
    anime_data['upcoming_ep'] = generate_upcoming_ep(anime_data['release_date']) if anime_data['status'] == "RELEASING" else None
    anime_data['format'] = anime_info['media_type'].upper()
    anime_data['related'] = getRelated()
    utils_save_json(mal_id_cache_path, {anime_id: anime_data}, False)
    return anime_data

def get_id(name, media_format = None, amount = 1, mal_token=None):
    search_cache = utils_read_json(mal_search_cache_path)
    id_dict = {}
    amount = int(amount)
    format_name = name
    media_format = media_format.upper() if media_format else None
    if media_format:
        if media_format not in media_formats:
            print("Invalid media format. Please choose from:", media_formats)
            return
        format_name = f"{name}_{media_format}"
    def fetch_from_mal():
        # Fetch anime info from Anilist API or any other source
        missing_amount = amount - len(search_cache.get(format_name, []))
        anime_ids = mal_fetch_id(name, media_format, missing_amount, mal_token)
        if anime_ids:
            if format_name in search_cache:
                existing_ids = set(search_cache[format_name])
                new_anime_ids = [anime_id for anime_id in anime_ids if anime_id not in existing_ids]
                search_cache[format_name].extend(new_anime_ids) 
            else:
                search_cache[format_name] = anime_ids
            utils_save_json(mal_search_cache_path, search_cache)
            for anime_id in search_cache[format_name][:amount]:
                id_dict.update(get_anime_info(anime_id, True, mal_token))
            return id_dict
        return None
    # Check if anime_id exists in cache
    try:
        if search_cache and format_name in search_cache and len(search_cache[format_name]) >= amount:
            print_deb("Returning cached result for search query:", name)
            found_ids = search_cache[format_name]
            for found_id in found_ids:
                id_dict.update(get_anime_info(found_id, False, mal_token))
            return id_dict
        else:
            return fetch_from_mal()
    except:
        return fetch_from_mal()
            
def mal_fetch_id(name, media_format, amount, mal_token=None):
    anime_ids = []
    params = {
        'q': name,
        'limit': 100 if not amount else amount,
        'fields': (
            "id,"
            "media_type"
        )
    }
    data = make_mal_request(anime_request_url, params, mal_token = mal_token)

    if data:
        for item in data:
            if media_format and item['media_type'].upper() != media_format:
                continue
            anime_ids.append(item['node']['id'])
        return anime_ids

    return None

def get_userdata(mal_token):
    params = {}
    request_url = "https://api.myanimelist.net/v2/users/@me"
    data = make_mal_request(request_url, params, mal_token = mal_token, user_request = True)

    if data:
        # Extract the username from the response data
        username = data['name']
        profile_pic = data['picture']
        return [username, profile_pic]

def mal_to_al_id(mal_id):
    query = """
    query ($malId: Int) {
        Media(idMal: $malId type: ANIME) {
            id
        }
    }
    """
    cached_al_ids = utils_read_json(mal_to_al_cache_path)
    if cached_al_ids and mal_id in cached_al_ids:
        return int(cached_al_ids[mal_id])
    # Constants for GraphQL endpoint and headers
    ANILIST_API_URL = "https://graphql.anilist.co"
    HEADERS = {'Content-Type': "application/json"}
    variables = {'malId': mal_id}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    while response.status_code == 429: # retry if we hit rate limit
        time.sleep(int(response.headers['Retry-After']))
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    response_dict = response.json()

    if response_dict:
        if response.status_code == 200:
            utils_save_json(mal_to_al_cache_path, {mal_id: response_dict['data']['Media']['id']}, False)
            return int(response_dict['data']['Media']['id'])
    return None

def get_season_ranges(anime_id):
    anime_id = str(anime_id)
    def go_to_first_season(anime_id):
        anime_info = get_anime_info(anime_id)[anime_id]
        related_anime = None
        if not anime_info['related']:
            return anime_id
        for relation in anime_info['related']:
            if anime_info['related'][relation]['type'] == 'PREQUEL':
                related_anime = get_anime_info(relation)[relation]
                has_prequel = True
                break
        if not related_anime:
            return anime_id
        while related_anime:
            related_anime = anime_info['related']
            if related_anime and has_prequel:
                has_prequel = False
                for relation in related_anime:
                    if related_anime[relation]['type'] == 'PREQUEL':
                        anime_id = relation
                        has_prequel = True
                        anime_info = get_anime_info(relation)[relation]
                        break
            else:
                return anime_id

    def skip_movies(anime_id):
        while True:
            anime_info = get_anime_info(anime_id)[anime_id]
            if anime_info['format'] != 'MOVIE':
                break
            related_anime = anime_info['related']
            if not related_anime:
                break
            next_anime_id = None
            for relation in related_anime:
                if related_anime[relation]['type'] == 'SEQUEL':
                    next_anime_id = relation
                    break
            if not next_anime_id:
                break
            anime_id = next_anime_id
        return anime_id

    season_ranges = {}
    range_start = 1
    anime_id = go_to_first_season(anime_id)
    anime_id = skip_movies(anime_id)
    anime_info = get_anime_info(anime_id)[anime_id]
    backup_season_counter = 0
    try:
        range_end = int(anime_info['total_eps'])
    except:
        range_end = 9999
    while anime_id:
        anime_info = get_anime_info(anime_id)[anime_id]
        season_regex = re.search(r"(\d+)\w\w season", anime_info['main_title'].lower()) 
        if season_regex:
            season = int(season_regex.group(1))
        else:
            season = backup_season_counter + 1
        backup_season_counter = season
        try:
            season_ranges[season]['end'] = season_ranges[season]['end'] + anime_info['total_eps']
            season_ranges[season]['total_eps'] = season_ranges[season]['total_eps'] + anime_info['total_eps']
            range_end = season_ranges[season]['end']
        except:
            season_ranges[season] = {'id': anime_id, 'start': range_start, 'end': range_end, 'total_eps': anime_info['total_eps']}
        related_anime = anime_info['related']
        if related_anime:
            anime_id = None
            for relation in related_anime:
                relation_info = get_anime_info(relation)[relation]
                if related_anime[relation]['type'] == 'SEQUEL' and related_anime[relation]['status'] != 'NOT_YET_RELEASED':
                    range_start = range_end + 1
                    try:
                        range_end = range_start + int(relation_info['total_eps'])
                    except:
                        range_end = 9999
                    anime_id = relation
                    anime_id = skip_movies(anime_id)
        else:
            break
    return season_ranges

def update_entry(anime_id, progress, mal_token=None):
    if not mal_token:
        mal_token = load_config()
    anime_id = str(anime_id)
    progress = int(progress)
    try:
        anime_info = get_anime_entry_for_user(anime_id, mal_token=mal_token)[anime_id]
        current_status = anime_info['watching_status']
    except:
        anime_info = get_anime_info(anime_id)[anime_id]
        current_status = 'PLANNING'
    total_eps = anime_info['total_eps']
    if progress > total_eps:
        season_ranges = get_season_ranges(anime_id)
        skipped_eps = 0
        for season in season_ranges:
            if progress <= season_ranges[season]['end']:
                anime_id = str(season_ranges[season]['id'])
                progress = progress - skipped_eps
                try:
                    anime_info = get_anime_entry_for_user(anime_id)[anime_id]
                    current_status = anime_info['watching_status']
                except:
                    anime_info = get_anime_info(anime_id)[anime_id]
                    current_status = 'PLANNING'
                total_eps = anime_info['total_eps']
                break
            skipped_eps += season_ranges[season]['total_eps']
    try:
        user_eps = anime_info['watched_ep']
    except:
        user_eps = -1 #allow for 0 as a value

    if progress <= user_eps and user_eps != total_eps:
        print_deb('Not updating, progress is lower or equal than user progress')
        return

    params = {}
    params['num_watched_episodes'] = progress
    if progress == total_eps and current_status != 'REPEATING':
        params['status'] = 'completed'
    elif progress == 0:
        params['status'] = 'plan_to_watch'
    else:
        if current_status == 'COMPLETED':
            params['is_rewatching'] = 'true'
        elif current_status == 'REPEATING':
            if progress == total_eps:
                params['num_times_rewatched'] = anime_info['rewatch_count'] + 1
                params['is_rewatching'] = 'false'
                params['status'] = 'completed'
        else:
            if current_status != 'CURRENT':
                params['status'] = 'watching'
    request_url = f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status"
    make_mal_request(request_url, params, 'put', mal_token, True)
    print_deb('Updating progress successful')
