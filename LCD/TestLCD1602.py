from pnhLCD1602 import LCD1602
import pygame

if __name__ == "__main__":
    lcd = LCD1602()
    
    # try:
        
    #     lcd.clear()
    #     # Hiển thị cả hai dòng cùng lúc
    #     lcd.write_string("NGU VAI ON")
    #     lcd.set_cursor(1, 0)  # Đặt con trỏ ở dòng thứ 2
    #     lcd.write_string("9999999999999989")
    #     # pygame.time.delay(3000)  # Hiển thị trong 3 giây
    #     # lcd.backlight_off()
    #     # pygame.time.delay(1000)
    #     # lcd.backlight_on()
    #     # pygame.time.delay(1000)
    #     # lcd.home()
    #     # pygame.time.delay(2000)
    #     lcd.backlight_on()
    # finally:
    #     lcd.close();

    try:
        lcd.clear()
        lcd.write_string("UAL CLO")
        lcd.set_cursor(1, 0)
        lcd.write_string("20")
        lcd.backlight_on()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Nhấn phím 'q' để tắt đèn nền
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        lcd.backlight_off()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        lcd.backlight_on()

            # Vẽ lại màn hình
            lcd.display()
            
            # Thêm khoảng thời gian nghỉ để tránh quá tải CPU
            pygame.time.delay(100)

    finally:
        lcd.close()