import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql
import os
import json

# 시크릿에서 서비스 계정 키를 환경 변수로 가져오기
service_account_info = json.loads(os.getenv('GCP_SERVICE_ACCOUNT_KEY'))
credentials = Credentials.from_service_account_info(service_account_info)

# gspread 클라이언트 생성
client = gspread.authorize(credentials)

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
