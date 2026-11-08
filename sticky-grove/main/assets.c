#include "assets.h"

#ifdef ESP_PLATFORM
// EMBED_FILES in CMakeLists.txt turns each file into a pair of linker symbols.
#define X(name, ext, width, height, fmt) extern const uint8_t _binary_##name##_##ext##_start[];
ASSET_LIST
#undef X
#define DATA(name, ext) _binary_##name##_##ext##_start
#else
#include <stdio.h>
#include <stdlib.h>
static const uint8_t *load(const char *file, size_t size)
{
    char path[256];
    snprintf(path, sizeof(path), ASSET_DIR "/%s", file);
    FILE *f = fopen(path, "rb");
    uint8_t *buf = calloc(1, size);
    if (f) {
        fread(buf, 1, size, f);
        fclose(f);
    } else {
        fprintf(stderr, "missing asset %s\n", path);
    }
    return buf;
}
#define DATA(name, ext) load(#name "." #ext, (size_t)asset_##name.header.w * asset_##name.header.h)
#endif

#define X(name, ext, width, height, fmt) \
    lv_image_dsc_t asset_##name = { \
        .header = { .magic = LV_IMAGE_HEADER_MAGIC, .cf = fmt, .w = width, .h = height, .stride = width }, \
        .data_size = (uint32_t)width * height, \
    };
ASSET_LIST
#undef X

void assets_init(void)
{
#define X(name, ext, width, height, fmt) asset_##name.data = DATA(name, ext);
    ASSET_LIST
#undef X
}
