idf_component_register(
    SRCS "epaper_panel.c" "driver/uc8179.c" "driver/ssd1677.c"
    INCLUDE_DIRS "."
    REQUIRES esp_driver_gpio esp_driver_spi esp_timer
)
target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-unused-variable)
