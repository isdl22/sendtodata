import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql

# 구글 시트 API 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("studious-hydra-414101-aa7da5d30255.json", scope)
client = gspread.authorize(creds)
client

# 시트 열기
sheet = client.open_by_key("1hmz9ER8b2JqXo6XTLmlB8cSyX-SxNcHsn4mu-tQWr3M").sheet1

# 시트의 모든 데이터 가져오기
data = sheet.get_all_records()

# MySQL 연결 정보
mysql_host = 'sql6.freemysqlhosting.net'
mysql_user = 'sql6685448'
mysql_password = 'dDDNLD7kwG'
mysql_db = 'sql6685448'
mysql_port = 3306

# MySQL 연결
connection = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db,
    port=mysql_port
)

try:
    with connection.cursor() as cursor:
        # 테이블 생성 (필요시)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sample_Dataset (
            id INT PRIMARY KEY AUTO_INCREMENT,
            `성함` VARCHAR(255),
            `직무` VARCHAR(255),
            `링크` VARCHAR(255),
            `트랙` VARCHAR(255)
        );
        """)

        # 데이터 삽입
        for row in data:
            cursor.execute("""
            INSERT INTO sample_Dataset (`성함`, `직무`, `링크`, `트랙`)
            VALUES (%s, %s, %s, %s);
            """, (row['성함'], row['직무\n(본인 작성)'], row['링크'], row['트랙']))

    # 커밋
    connection.commit()

finally:
    connection.close()

print("Data successfully inserted into MySQL!")