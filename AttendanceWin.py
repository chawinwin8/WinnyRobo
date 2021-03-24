import mysql.connector

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
import time

reader = SimpleMFRC522()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="attendance"
)

mycursor = mydb.cursor()





try:
    while True:
        mycursor.execute("CREATE TABLE IF NOT EXISTS students(RFID TEXT, name TEXT,time datetime)")
        
        print("Please scan")
        lcd.write_string("Please Scan")
        id, text = reader.read()
        text = text.strip()
        print(id)
        print(text)
        lcd.clear()
        lcd.cursor_pos = (1,8)
        lcd.write_string(text)
        time.sleep(2)
        lcd.clear()
        
        
        sql = "INSERT INTO students (RFID, name, time) VALUES (%s,%s,NOW())"
        val = [id, text]
        mycursor.execute(sql, val)
        mydb.commit()
        print("Finish scan")
        
        Q = "SELECT RFID,name,DATE_FORMAT(time, '%Y-%m-%d %T') FROM students ORDER BY time DESC LIMIT 5"
        mycursor.execute(Q)
        myresult = mycursor.fetchall()
        for row in myresult:
            print(row)
        
    
finally:
    GPIO.cleanup()

    
