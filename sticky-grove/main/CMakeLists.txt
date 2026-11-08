idf_component_register(
    SRCS
        "main.c" "board.c" "display.c" "touch.c" "rtc_pcf8563.c" "sht40.c"
        "store.c" "net.c" "venice.c"
        "ui/theme.c" "ui/ui.c" "ui/page_home.c" "ui/page_todo.c" "ui/page_habits.c"
        "ui/page_calendar.c" "ui/page_note.c" "ui/page_chat.c" "ui/page_settings.c"
    INCLUDE_DIRS "."
    REQUIRES seeed_epaper esp_driver_gpio esp_driver_i2c esp_driver_spi esp_driver_ledc
             esp_timer nvs_flash esp_wifi esp_netif esp_event esp_http_client esp-tls
             json lwip
)
