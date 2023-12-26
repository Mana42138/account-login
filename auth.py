import os
import subprocess
import platform
import requests

class AccountManager:
    def __init__(self, cookie):
        self.cookie = cookie

    def get_xsrf(self):
        auth_url = "https://auth.roblox.com/v2/logout"
        xsrf_request = requests.post(auth_url, cookies={'.ROBLOSECURITY': self.cookie})
        return xsrf_request.headers["x-csrf-token"]

    def get_authentication_ticket(self):
        launch_url = 'https://auth.roblox.com/v1/authentication-ticket/'
        response = requests.post(launch_url, headers={'X-CSRF-Token': self.get_xsrf(), "Referer": "https://www.roblox.com/games/4924922222/Brookhaven-RP"}, cookies={'.ROBLOSECURITY': self.cookie})
        ticket = response.headers.get("rbx-authentication-ticket", "")
        return ticket

    def job_id(self):
        response = requests.get("https://games.roblox.com/v1/games/10515146389/servers/0?sortOrder=1&excludeFullGames=true&limit=25").json()
        data = response["data"][0]
        return data["id"]
    
    def launch_roblox(self, ticket, place_id, job_id): # ticket, place_id, access_code, link_code, join_vip, follow_user, job_id
        roblox_executable_path = None
        current_version = requests.get("https://clientsettings.roblox.com/v1/client-version/WindowsPlayer").json()["clientVersionUpload"]
        print(current_version)
        r_path = os.path.join("C:\\Program Files (x86)\\Roblox\\Versions", current_version)

        if not os.path.exists(r_path):
            r_path = os.path.join(os.environ.get("LocalAppData"), "Roblox\\Versions", current_version)

        if not os.path.exists(r_path):
            return "ERROR: Failed to find ROBLOX executable"

        roblox_executable_path = os.path.join(r_path, "RobloxPlayerBeta.exe")

        arguments = ""


        arguments = f"--app -t {ticket} -j \"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame{'' if not job_id else 'Job'}&placeId={place_id}{'' if not job_id else '&gameId=' + job_id}&isPlayTogetherGame=false\""

        if platform.system() == "Windows":
            subprocess.Popen([roblox_executable_path, arguments])

        return "Success"
