idf_component_register(
    SRCS
        "main.c" "board.c" "display.c" "touch.c" "rtc_pcf8563.c" "sht40.c" "imu.c"
        "store.c" "net.c" "venice.c" "assets.c"
        "fonts/eagle_22.c" "fonts/eagle_30.c" "fonts/eagle_40.c"
        "ui/theme.c" "ui/ui.c" "ui/page_home.c" "ui/page_todo.c" "ui/page_habits.c"
        "ui/page_calendar.c" "ui/page_note.c" "ui/page_chat.c" "ui/page_settings.c"
    INCLUDE_DIRS "."
    EMBED_FILES "assets/frame_land.a8" "assets/frame_port.a8" "assets/figure_l.l8" "assets/figure_s.l8"
                "assets/divider.a8" "assets/crescent.a8" "assets/rose.a8" "assets/star.a8"
                "assets/star_s.a8" "assets/laurel.a8"
    REQUIRES seeed_epaper esp_driver_gpio esp_driver_i2c esp_driver_spi esp_driver_ledc
             esp_timer nvs_flash esp_wifi esp_netif esp_event esp_http_client esp-tls
             json lwip
)
