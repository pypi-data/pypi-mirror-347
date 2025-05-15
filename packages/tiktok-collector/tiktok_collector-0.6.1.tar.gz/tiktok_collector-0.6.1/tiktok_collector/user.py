import requests
import time


class TiktokUserCollector:
    """
    A class to collect TikTok posts by hashtag.
    """

    # Constants
    API_USER_INFO = "https://api.tokapi.online/v1/user/{user_id}"
    RAPID_API_HOST = "tokapi"

    def __init__(self, api_key, country_code="US"):
        self.api_key = api_key
        self.country_code = country_code
        self.headers = {
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST
        }

    def collect_user_info(self, user_id):
        try:
            user_info = self._get_user_id(user_id)
            if user_info is None:
                print(f"Could not find username for {user_id}")
                return None

            return user_info

        except Exception as e:
            print(f"Error collecting posts for hashtag {user_id}: {e}")
            return []

    def _get_user_id(self, user_id):
        user_info = None
        url = self.API_USER_INFO.format(
            user_id=user_id)
        retry = 0

        while True:
            try:
                response = requests.get(
                    url, headers=self.headers)

                data = response.json()
                user = data.get("user", {})
                if user.get("uid"):
                    other_social_networks = []
                    if instagram_username := user.get("instagram_username"):
                        other_social_networks.append(
                            {
                                "social_type": "instagram",
                                "username": instagram_username,
                                "social_url": f"https://www.instagram.com/{instagram_username}/",
                            }
                        )

                    if youtube_id := user.get("youtube_id"):
                        other_social_networks.append(
                            {
                                "social_type": "youtube",
                                "_id": youtube_id,
                                "social_url": f"https://www.youtube.com/channel/{youtube_id}",
                            }
                        )
                    scheduled_live_events = []
                    if len(user.get("scheduled_live_events", [])) > 0:
                        scheduled_live_events = list(
                            map(
                                lambda x: {
                                    **x,
                                    "end_time": x.get("duration", 0) + x.get("start_time", 0),
                                },
                                user.get("scheduled_live_events"),
                            )
                        )
                    user_info = {
                        "user_id": user.get("uid"),
                        "full_name": user.get("nickname"),
                        "bio": user.get("signature"),
                        "num_follower": user.get("follower_count"),
                        "num_following": user.get("following_count"),
                        "num_post": user.get("aweme_count"),
                        "region": user.get("region"),
                        "num_favorite": user.get("favoriting_count"),
                        "has_livestream": True if user.get("room_id") else False,
                        "livestream_info": {
                            "time": int(time.time()),
                            "live_status": "now"
                            } if user.get("room_id") else False,
                        "other_social_networks": other_social_networks,
                        "scheduled_live_events": scheduled_live_events
                    }
                    break
                if (response.status_code != 200):
                    raise Exception('Error request')

            except Exception as e:
                print("Load user id error", e)

            retry += 1
            if retry > 3:
                break
        return user_info
