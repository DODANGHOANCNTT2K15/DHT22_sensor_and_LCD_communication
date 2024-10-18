import threading
from GPIOEmulator.EmulatorGUI import GPIO
from LCD.LCD1602 import LCD1602
from DHT22.DHT22 import DHT22, readSensor
import time

def main():
    # Thiết lập chế độ GPIO
    GPIO.setmode(GPIO.BCM)

    # Thiết lập chân GPIO 14 làm INPUT với pull-up resistor cho nút bấm
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Thiết lập chân GPIO 15 làm INPUT với pull-up resistor cho DHT22
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Khởi tạo màn hình LCD
    lcd = LCD1602()

    # Chạy vòng lặp sự kiện Pygame trong một luồng riêng
    lcd_loop = threading.Thread(target=lcd.run, args=(lcd,))
    lcd_loop.start()

    # Khởi tạo các trang màn hình
    pages = ["Temp: {:.2f}C Hum: {:.2f}%".format(0, 0),
             "Set Temp: {:.2f}C Mode: Auto".format(22.0),
             "Fan Speed: Medium Timer: 10min"]
    current_page = 0

    try:
        while True:
            # Đọc dữ liệu từ cảm biến DHT22 kết nối với GPIO15
            temp, hum = readSensor(15)
            print(f"Nhiệt độ: {temp:.2f}°C, Độ ẩm: {hum:.2f}%")

            # Cập nhật thông tin trang hiện tại
            if current_page == 0:
                lcd.clear()
                lcd.write_string(f"Temp: {temp:.2f}C", line=0)
                lcd.write_string(f"Hum: {hum:.2f}%", line=1)
            elif current_page == 1:
                set_temp = 22.0  # Ví dụ: setpoint nhiệt độ
                mode = "Auto"     # Ví dụ: chế độ hoạt động
                lcd.clear()
                lcd.write_string(f"Set Temp: {set_temp:.2f}C", line=0)
                lcd.write_string(f"Mode: {mode}", line=1)
            elif current_page == 2:
                fan_speed = "Medium"  # Ví dụ: tốc độ quạt
                timer = "10min"       # Ví dụ: thời gian hẹn giờ
                lcd.clear()
                lcd.write_string(f"Fan Speed: {fan_speed}", line=0)
                lcd.write_string(f"Timer: {timer}", line=1)

            lcd.backlight_on()

            # Kiểm tra trạng thái của GPIO 14 (nút bấm để chuyển trang)
            input_value = GPIO.input(14)
            if not input_value:  # Khi nút được nhấn (IN=0)
                print("Nút GPIO14 được nhấn!")
                current_page = (current_page + 1) % len(pages)
                lcd.clear()
                # Thêm debounce để tránh chuyển trang nhiều lần khi nhấn một lần
                time.sleep(0.5)

            # Thêm khoảng thời gian nghỉ để tránh quá tải CPU
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        lcd.close()
        print("Đã dừng chương trình.")
        lcd_loop.join()

# Chạy chương trình chính
if __name__ == "__main__":
    main()