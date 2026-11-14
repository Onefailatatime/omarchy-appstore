// Artwork baked into the firmware: Art Nouveau frames, the Moon figure, ornaments.
// Raw pixel files under main/assets/, made by tools/art/img2bin.py.
// A8 files are ink lines (alpha), drawn in ink colour; L8 files are four-grey pictures.
#pragma once
#include "lvgl.h"

#define ASSET_LIST \
    X(frame_land, a8, 800, 480, LV_COLOR_FORMAT_A8) \
    X(frame_port, a8, 480, 800, LV_COLOR_FORMAT_A8) \
    X(figure_l,   l8, 190, 285, LV_COLOR_FORMAT_L8) \
    X(figure_s,   l8, 134, 200, LV_COLOR_FORMAT_L8) \
    X(divider,    a8, 420, 100, LV_COLOR_FORMAT_A8) \
    X(crescent,   a8,  64,  70, LV_COLOR_FORMAT_A8) \
    X(rose,       a8,  44,  76, LV_COLOR_FORMAT_A8) \
    X(star,       a8,  50,  60, LV_COLOR_FORMAT_A8) \
    X(star_s,     a8,  20,  24, LV_COLOR_FORMAT_A8) \
    X(laurel,     a8, 300,  58, LV_COLOR_FORMAT_A8)

#define X(name, ext, width, height, fmt) extern lv_image_dsc_t asset_##name;
ASSET_LIST
#undef X

void assets_init(void);
