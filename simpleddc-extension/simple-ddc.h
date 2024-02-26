#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ddcutil_c_api.h>
#include <ddcutil_status_codes.h>

DDCA_Display_Handle * open_first_display_by_dlist();
DDCA_Status switch_input(DDCA_Display_Handle* handle, uint8_t input);
uint8_t show_any_value(
        DDCA_Display_Handle     dh,
        DDCA_Vcp_Value_Type     value_type,
        DDCA_Vcp_Feature_Code   feature_code);
