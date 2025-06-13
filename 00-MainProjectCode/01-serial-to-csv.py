import serial
from serial.serialutil import SerialException
import pandas as pd
import re
from datetime import datetime
import time

try:
    ser = serial.Serial('COM9', 115200)
    ser.flush()
except SerialException:
    print("ไม่สามารถเชื่อมต่อกับพอร์ต COM9")
    exit()

data = []

try:
    while True:
        try:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue

                # pattern ใหม่: R[...] IR[...] G[...]
                match = re.search(r'R\[(\d+)\]\s+IR\[(\d+)\]\s+G\[(\d+)\]', line)
                if match:
                    r_val = int(match.group(1))
                    ir_val = int(match.group(2))
                    g_val = int(match.group(3))

                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # มีมิลลิวินาที

                    data.append([timestamp, r_val, ir_val, g_val])
                    print(f"{timestamp} - R: {r_val}, IR: {ir_val}, G: {g_val}")
            else:
                time.sleep(0.01)

        except SerialException:
            print("การเชื่อมต่อกับ Serial ถูกตัด")
            break

except KeyboardInterrupt:
    print("\nหยุดการอ่านข้อมูลด้วยผู้ใช้")

finally:
    ser.close()

    df = pd.DataFrame(data, columns=['Timestamp', 'R', 'IR', 'G'])
    filename = f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nบันทึกข้อมูลเรียบร้อย: {filename}")


# import os
# import csv
# import time
# import requests
# import sseclient
# from datetime import datetime

# # IP ของ ESP32
# ESP32_IP = "192.168.0.42"
# SSE_URL = f"http://{ESP32_IP}/sse"

# # โฟลเดอร์ที่ใช้เก็บ CSV
# SAVE_PATH = r'D:/1-BukAILab/01-MAX30102/csv'
# if not os.path.exists(SAVE_PATH):
#     os.makedirs(SAVE_PATH)
#     print(f"✅ สร้างโฟลเดอร์ {SAVE_PATH} แล้ว")

# def generate_filename():
#     current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
#     return os.path.join(SAVE_PATH, f"max30102_data_{current_time}.csv")

# def start_logging():
#     filename = generate_filename()
#     print(f"📡 กำลังเชื่อมต่อกับ ESP32 ที่ {ESP32_IP}...")
#     print(f"💾 บันทึกข้อมูลที่: {filename}")

#     try:
#         # สร้างการเชื่อมต่อกับ SSE
#         response = requests.get(SSE_URL, stream=True)
#         client = sseclient.SSEClient(response)

#         with open(filename, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['Timestamp', 'IR', 'Red', 'DateTime'])

#             start_time = time.time()
#             record_count = 0

#             for event in client.events():
#                 if event.data:
#                     data = event.data.strip()
#                     values = data.split(',')

#                     if len(values) >= 3:
#                         timestamp, ir, red = values[:3]
#                         now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#                         writer.writerow([timestamp, ir, red, now_str])
#                         csvfile.flush()

#                         record_count += 1
#                         if record_count % 100 == 0:
#                             elapsed = time.time() - start_time
#                             rate = record_count / elapsed
#                             print(f"📝 บันทึก {record_count} รายการ ({rate:.1f} records/sec)")

#     except KeyboardInterrupt:
#         print("\n🛑 หยุดการบันทึกข้อมูล")
#     except requests.exceptions.ConnectionError:
#         print("❌ ไม่สามารถเชื่อมต่อกับ ESP32 ได้")
#     except Exception as e:
#         print(f"⚠️ เกิดข้อผิดพลาด: {e}")
#     finally:
#         print(f"✅ บันทึกไฟล์เสร็จ: {filename}")

# if __name__ == "__main__":
#     print("📥 เริ่มรับข้อมูลจากเซ็นเซอร์ MAX30102 (ESP32)")
#     print("🔌 กด Ctrl+C เพื่อหยุดการบันทึก\n")
#     start_logging()


# import os
# import csv
# import time
# import requests
# import sseclient
# from datetime import datetime

# # ตั้งค่า IP ของ ESP32 ที่รันเซ็นเซอร์ MAX30102
# ESP32_IP = "192.168.0.42"
# SSE_URL = f"http://{ESP32_IP}/sse"

# # พาธที่จะบันทึกไฟล์ CSV
# SAVE_PATH = r'D:/1-BukAILab/01-MAX30102/csv'

# # สร้างโฟลเดอร์ถ้ายังไม่มี
# if not os.path.exists(SAVE_PATH):
#     os.makedirs(SAVE_PATH)
#     print(f"สร้างโฟลเดอร์ {SAVE_PATH} สำเร็จ")

# def generate_filename():
#     """สร้างชื่อไฟล์ที่มีวันที่และเวลาปัจจุบัน"""
#     current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
#     return os.path.join(SAVE_PATH, f"max30102_data_{current_time}.csv")

# def start_logging():
#     """เริ่มบันทึกข้อมูลจาก SSE stream"""
#     filename = generate_filename()
    
#     print(f"กำลังเชื่อมต่อกับ ESP32 ที่ {ESP32_IP}...")
#     print(f"กำลังบันทึกข้อมูลไปที่: {filename}")
    
#     try:
#         # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
#         with open(filename, 'w', newline='') as csvfile:
#             csv_writer = csv.writer(csvfile)
            
#             # เขียนส่วนหัวของไฟล์ CSV (แก้ไขให้สอดคล้องกับข้อมูลที่ส่งมา)
#             csv_writer.writerow(['Timestamp', 'IR', 'Red', 'DateTime'])
            
#             # เชื่อมต่อกับ SSE stream
#             response = requests.get(SSE_URL, stream=True)
            
#             start_time = time.time()
#             record_count = 0
            
#             for line in response.iter_lines():
#                 if line:
#                     # ตรวจสอบว่าเป็นข้อมูล SSE (เริ่มต้นด้วย data:)
#                     if not line.startswith(b'data:'):
#                         continue
                        
#                     # แยกข้อมูลจาก SSE format
#                     data_str = line.decode('utf-8').replace('data:', '').strip()
                    
#                     # แยกค่าจากข้อมูล (timestamp, ir, red)
#                     values = data_str.split(',')
                    
#                     # ตรวจสอบจำนวนค่าต้องมี 3 ค่า
#                     if len(values) == 3:
#                         timestamp, ir, red = values[0], values[1], values[2]
#                         current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        
#                         # เขียนลงไฟล์ CSV
#                         csv_writer.writerow([timestamp, ir, red, current_datetime])
#                         csvfile.flush()  # บังคับให้เขียนลงดิสก์ทันที
                        
#                         record_count += 1
                        
#                         # แสดงสถานะทุกๆ 25 records (ประมาณทุก 1 วินาที)
#                         if record_count % 25 == 0:
#                             elapsed = time.time() - start_time
#                             rate = record_count / elapsed if elapsed > 0 else 0
#                             print(f"บันทึกแล้ว {record_count} รายการ ({rate:.1f} รายการ/วินาที)")
    
#     except KeyboardInterrupt:
#         print("\nหยุดการบันทึกข้อมูล")
#     except requests.exceptions.ConnectionError:
#         print(f"ไม่สามารถเชื่อมต่อกับ ESP32 ที่ IP: {ESP32_IP}")
#         print("กรุณาตรวจสอบว่า:")
#         print("1. ESP32 เปิดอยู่และทำงานปกติ")
#         print("2. คอมพิวเตอร์เชื่อมต่อกับเครือข่ายเดียวกับ ESP32")
#         print("3. IP ที่ตั้งค่าถูกต้อง")
#     except Exception as e:
#         print(f"เกิดข้อผิดพลาด: {e}")
#     finally:
#         print(f"บันทึกข้อมูลลงไฟล์ {filename} เสร็จสิ้น")

# if __name__ == "__main__":
#     print("โปรแกรมบันทึกข้อมูลจากเซ็นเซอร์ MAX30102")
#     print("กด Ctrl+C เพื่อหยุดการบันทึกข้อมูล")
#     start_logging()


# import os
# import csv
# import time
# import requests
# from datetime import datetime

# # ตั้งค่า IP ของ ESP32 ที่รันเซ็นเซอร์ MAX30102
# ESP32_IP = "192.168.0.42"
# SSE_URL = f"http://{ESP32_IP}/sse"

# # พาธที่จะบันทึกไฟล์ CSV
# SAVE_PATH = r'D:/1-BukAILab/01-MAX30102/csv'

# # สร้างโฟลเดอร์ถ้ายังไม่มี
# if not os.path.exists(SAVE_PATH):
#     os.makedirs(SAVE_PATH)
#     print(f"สร้างโฟลเดอร์ {SAVE_PATH} สำเร็จ")

# def generate_filename():
#     """สร้างชื่อไฟล์ที่มีวันที่และเวลาปัจจุบัน"""
#     current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
#     return os.path.join(SAVE_PATH, f"max30102_data_{current_time}.csv")

# def start_logging():
#     """เริ่มบันทึกข้อมูลจาก SSE stream"""
#     filename = generate_filename()
    
#     print(f"กำลังเชื่อมต่อกับ ESP32 ที่ {ESP32_IP}...")
#     print(f"กำลังบันทึกข้อมูลไปที่: {filename}")
    
#     try:
#         # เปิดไฟล์ CSV เพื่อเขียนข้อมูล
#         with open(filename, 'w', newline='') as csvfile:
#             csv_writer = csv.writer(csvfile)
            
#             # เขียนส่วนหัวของไฟล์ CSV
#             csv_writer.writerow(['Timestamp', 'IR', 'Red', 'Green', 'DateTime'])
            
#             # เชื่อมต่อกับ SSE stream
#             response = requests.get(SSE_URL, stream=True)
            
#             start_time = time.time()
#             record_count = 0
            
#             for line in response.iter_lines():
#                 if line:
#                     # ข้ามบรรทัดที่ไม่ใช่ข้อมูล
#                     if not line.startswith(b'data:'):
#                         continue
                        
#                     # แยกข้อมูลจาก SSE format
#                     data_str = line.decode('utf-8').replace('data:', '').strip()
                    
#                     # แยกค่าจากข้อมูล (timestamp,ir,red,green)
#                     values = data_str.split(',')
                    
#                     if len(values) >= 4:
#                         timestamp, ir, red, green = values[0], values[1], values[2], values[3]
#                         current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        
#                         # เขียนลงไฟล์ CSV
#                         csv_writer.writerow([timestamp, ir, red, green, current_datetime])
#                         csvfile.flush()  # บังคับให้เขียนลงดิสก์ทันที
                        
#                         record_count += 1
                        
#                         # แสดงสถานะทุกๆ 25 records (ประมาณทุก 1 วินาที)
#                         if record_count % 25 == 0:
#                             elapsed = time.time() - start_time
#                             rate = record_count / elapsed if elapsed > 0 else 0
#                             print(f"บันทึกแล้ว {record_count} รายการ ({rate:.1f} รายการ/วินาที)")
    
#     except KeyboardInterrupt:
#         print("\nหยุดการบันทึกข้อมูล")
#     except requests.exceptions.ConnectionError:
#         print(f"ไม่สามารถเชื่อมต่อกับ ESP32 ที่ IP: {ESP32_IP}")
#         print("กรุณาตรวจสอบว่า:")
#         print("1. ESP32 เปิดอยู่และทำงานปกติ")
#         print("2. คอมพิวเตอร์เชื่อมต่อกับเครือข่ายเดียวกับ ESP32")
#         print("3. IP ที่ตั้งค่าถูกต้อง")
#     except Exception as e:
#         print(f"เกิดข้อผิดพลาด: {e}")
#     finally:
#         print(f"บันทึกข้อมูลลงไฟล์ {filename} เสร็จสิ้น")

# if __name__ == "__main__":
#     print("โปรแกรมบันทึกข้อมูลจากเซ็นเซอร์ MAX30102")
#     print("กด Ctrl+C เพื่อหยุดการบันทึกข้อมูล")
#     start_logging()


# from flask import Flask, request
# import csv
# import os
# import logging
# from datetime import datetime
# import threading
# import time

# app = Flask(__name__)

# # ตั้งค่า path สำหรับบันทึกไฟล์ CSV
# base_path = 'D:/1-BukAILab/01-MAX30102/csv'
# os.makedirs(base_path, exist_ok=True)

# # สร้างชื่อไฟล์ตามวันเวลาปัจจุบัน
# start_time = datetime.now()
# filename = start_time.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
# file_path = os.path.join(base_path, filename)

# # ตั้งค่าระบบ logging ไฟล์ error log
# log_folder = os.path.join(base_path, 'error_log')
# os.makedirs(log_folder, exist_ok=True)
# log_file = os.path.join(log_folder, 'error_log.txt')

# logging.basicConfig(
#     level=logging.ERROR,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_file, encoding='utf-8'),
#         logging.StreamHandler()
#     ]
# )

# # สร้างไฟล์ CSV และเขียนหัวตาราง
# def create_csv():
#     try:
#         with open(file_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['ReceiveTimestamp', 'SensorTimestamp', 'IR', 'RED', 'GREEN'])
#         logging.info(f"CSV file created: {file_path}")
#     except Exception as e:
#         logging.error(f"Failed to create CSV file: {e}")

# create_csv()

# lock = threading.Lock()  # ป้องกันการเขียนไฟล์พร้อมกัน

# @app.route('/data', methods=['POST'])
# def receive_data():
#     try:
#         sensor_ts = request.form.get('timestamp', '')
#         ir = request.form.get('ir', '')
#         red = request.form.get('red', '')
#         green = request.form.get('green', '')

#         # เวลาที่ server รับข้อมูล
#         receive_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

#         # ตรวจสอบข้อมูลอย่างง่าย (ถ้าอยากละเอียดขึ้นให้เพิ่ม validation)
#         if not (sensor_ts and ir and red and green):
#             logging.error(f"Incomplete data received: {request.form}")
#             return 'Incomplete data', 400

#         # เขียนข้อมูลลง CSV ด้วย lock กันการเขียนพร้อมกัน
#         with lock:
#             with open(file_path, 'a', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow([receive_ts, sensor_ts, ir, red, green])

#         print(f"[{receive_ts}] Received: ts={sensor_ts}, IR={ir}, RED={red}, GREEN={green}")
#         return 'OK', 200

#     except Exception as e:
#         logging.error(f"Error in /data endpoint: {e}")
#         return 'Internal Server Error', 500

# def run_flask():
#     app.run(host='192.168.0.42', port=80)

# if __name__ == '__main__':
#     try:
#         run_flask()
#     except Exception as e:
#         logging.error(f"Flask app crashed: {e}")
