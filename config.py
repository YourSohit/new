import requests
import os
from dotenv import load_dotenv
from tokens import STRING, INDEX, DRIVE_ID

if os.path.exists("config.env"):
    load_dotenv('config.env', override=True)

class Config(object):
    SESSION_STRING = STRING
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", ))
    API_HASH = os.environ.get("API_HASH", "")
    TG_SPLIT_SIZE = int(os.environ.get("TG_SPLIT_SIZE","4000000000"))
    DB_URL = os.environ.get("DB_URL", "")
    OWNER_ID = [int(i) for i in  os.environ.get("OWNER_ID", "").split(" ")]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
    GDRIVE_FOLDER_ID = DRIVE_ID
    USE_SERVICE_ACCOUNTS = os.environ.get("USE_SERVICE_ACCOUNTS","False")
    IS_TEAM_DRIVE = os.environ.get("IS_TEAM_DRIVE", "True")
    INDEX_LINK = INDEX
    #Zee5 token
    ZEE5_EMAIL = os.environ.get("ZEE5_EMAIL", "geervani28@gmail.com")
    ZEE5_PASS = os.environ.get("ZEE5_PASS", "Race2002")
    IS_4K_SUPPORTED = os.environ.get("IS_4K_SUPPORTED", "True")
    #SONYLIV TOKEN
    
    #JIO_CINEMA_TOKEN
    JIO_CINEMA_TOKEN = os.environ.get("JIO_CINEMA_TOKEN", "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImF1dGhUb2tlbklkIjoiNTIyZDU3OWUtNjU3Ny00ZjU2LWE5MTItMGUxZTc3MWIyNTA4IiwidXNlcklkIjoiNmYxYzg3YjktYmI0ZS00NTY2LWE5NWYtNTUyYTk4ZDg0OTA1IiwidXNlclR5cGUiOiJOT05KSU8iLCJvcyI6ImlvcyIsImRldmljZVR5cGUiOiJwaG9uZSIsImFjY2Vzc0xldmVsIjoiOSIsImRldmljZUlkIjoiMjMwMDE3NDQ1MCIsImV4dHJhIjoie1wibnVtYmVyXCI6XCJKRTNPMWZBeUpKUXlDcHEwWnlXQUZVTkpVZW9sWDVUeEp3SFpjZEUwWmxCZlArY0F2WFRXcWljPVwiLFwiYWRzXCI6XCJ5ZXNcIixcInBsYW5kZXRhaWxzXCI6e1wiYWRzXCI6XCJ5ZXNcIixcIlBhY2thZ2VJbmZvXCI6W3tcInBsYW5pZFwiOlwicGxhbi03ZDZmM2E2YS0zNmU1LTRmNzAtODExZi0xNTMwNWE2MDMyNTZcIixcInN1YnNjcmlwdGlvbnN0YXJ0XCI6MTY4Njg0ODk4MjI2MyxcInN1YnNjcmlwdGlvbmVuZFwiOjE3MTg3NjIzOTk5OTksXCJwbGFudHlwZVwiOlwicHJlbWl1bVwiLFwiYnVzaW5lc3NUeXBlXCI6XCJQcmVtaXVtXCIsXCJpblN0cmVhbUFkc1wiOlwiRW5hYmxlXCIsXCJkaXNwbGF5QWRzXCI6XCJFbmFibGVcIixcImlzYWN0aXZlXCI6dHJ1ZSxcIm5vdGVzXCI6XCJcIixcInBsYW5EZXRhaWxzXCI6e1wiZmVhdHVyZVwiOntcInZhbHVlXCI6e1wiQWRzQ29uZmlnXCI6e1wiZGlzcGxheUFkc1wiOntcIm1hc3RoZWFkXCI6bnVsbCxcImJhbm5lckFkc1wiOntcImluQmV0d2VlblRyYXlBZHNcIjpudWxsLFwiYmVsb3dQbGF5ZXJBZHNcIjpudWxsfX0sXCJpbnN0cmVhbUFkc1wiOntcImxpdmVcIjp7XCJwcmVSb2xsXCI6bnVsbCxcIm1pZFJvbGxcIjpudWxsfSxcInZvZFwiOntcInByZVJvbGxcIjpudWxsLFwibWlkUm9sbFwiOm51bGx9fX19fX19XX0sXCJqVG9rZW5cIjpcIlwiLFwidXNlckRldGFpbHNcIjpcIkQ2ZG1mNTRmaHVPMERlM29WYUFEZS9Vb3dYTEVyOGF2YXVmbnlsOUN2UUhreDZqL1IrdnUyOUI1UnY2Nlg5TDBLRzdLQVE0NkdYanduUERkZXEyeXdEUjErb1FrTlBhQ1dtb2w4Y2pCSDgvYUgvSzVSU0N5cm9TOFJCVS9ndERSeG5MeGljdkFneDZXYXZvTzBtbGhUOHJac280M0w2Y01sUVI3RktEMnZ3PT1cIn0iLCJzdWJzY3JpYmVySWQiOiIiLCJhcHBOYW1lIjoiUkpJTF9KaW9DaW5lbWEiLCJkZWdyYWRlZCI6ImZhbHNlIiwiYWRzIjoieWVzIiwicHJvZmlsZUlkIjoiZGQzNGYxMjAtYWFlMy00NmM4LWE1MGMtNTY4MjU2M2VjNThjIiwiYWRJZCI6IjIzMDAxNzQ0NTAiLCJhZHNDb25maWciOnsiaW5zdHJlYW1BZHMiOnsibGl2ZSI6eyJlbmFibGVkIjp0cnVlfSwidm9kIjp7ImVuYWJsZWQiOnRydWV9fX0sImV4cGVyaW1lbnRLZXkiOnsiY29uZmlnS2V5IjoiZGQzNGYxMjAtYWFlMy00NmM4LWE1MGMtNTY4MjU2M2VjNThjIiwiZ3JvdXBJZCI6NTY0NH19LCJleHAiOjE2OTgwODU0NjgsImlhdCI6MTY5ODA3ODI2OH0.ZM25DKlsNiECQUFlYdaRwKiFMDXdTslYv28WArPLyh9mHuO2fAa-AIjVbS8yA5YKrHVfLIrJ3BFFXi4Ue2xo0g")
    #HotsStar
    
    TAG = "ANToNi"
    TEMP_DIR = os.environ.get("TEMP_DIR", "ThEott")
    #######Dont touch########
    if SESSION_STRING == "" or SESSION_STRING == "None":
        TG_SPLIT_SIZE = TG_SPLIT_SIZE/2
    USE_SERVICE_ACCOUNTS = USE_SERVICE_ACCOUNTS.lower() == "true"
    IS_TEAM_DRIVE = IS_TEAM_DRIVE.lower() == "true"
    IS_4K_SUPPORTED = IS_4K_SUPPORTED.lower() == "true"
    HOTSTAR_REFRESH = 0.0
    CR_CONTENTID = None
    CR_PLAYBACKID = None
