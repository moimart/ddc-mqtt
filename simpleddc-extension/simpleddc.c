#include "simple-ddc.h"

#define DDC_ERRMSG(function_name,status_code)    \
   do {                                               \
      printf("(%s) %s() returned %d (%s): %s\n",      \
             __func__, function_name, status_code,    \
             ddca_rc_name(status_code),               \
             ddca_rc_desc(status_code));              \
   } while(0)

DDCA_Display_Handle * open_first_display_by_dlist() {
   printf("Check for monitors using ddca_get_displays()...\n");
   DDCA_Display_Handle dh = NULL;

   // Inquire about detected monitors.
   DDCA_Display_Info_List* dlist = NULL;
   ddca_get_display_info_list2(
         false,    // don't include invalid displays
         &dlist);

   if (dlist->ct == 0) {
      printf("   No DDC capable displays found\n");
   }
   else {
      DDCA_Display_Info * dinf = &dlist->info[0];
      DDCA_Display_Ref * dref = dinf->dref;
      printf("Opening display %s\n", dinf->model_name);
      printf("Model: %s\n", dinf->model_name);
      //printf("Model: %s\n", dinf->mmid.model_name);
      DDCA_Status rc = ddca_open_display2(dref, false, &dh);
      if (rc != 0) {
          DDC_ERRMSG("ddca_open_display2", rc);
      }
   }
   ddca_free_display_info_list(dlist);
   return dh;
}

uint8_t show_any_value(
        DDCA_Display_Handle     dh,
        DDCA_Vcp_Value_Type     value_type,
        DDCA_Vcp_Feature_Code   feature_code)
{
    DDCA_Status ddcrc;
    DDCA_Any_Vcp_Value * valrec;

    ddcrc = ddca_get_any_vcp_value_using_explicit_type(
            dh,
            feature_code,
            value_type,
            &valrec);
    if (ddcrc != 0) {
        DDC_ERRMSG("ddca_get_any_vcp_value_using_explicit_type", ddcrc);
        goto bye;
    }

    if (valrec->value_type == DDCA_NON_TABLE_VCP_VALUE) {
        uint8_t ret_value = valrec->val.c_nc.sl;
        free(valrec);
        return ret_value;
    }
    else {
       assert(valrec->value_type == DDCA_TABLE_VCP_VALUE);
       printf("Table value: 0x");
       for (int ndx=0; ndx<valrec->val.t.bytect; ndx++)
          printf("%02x", valrec->val.t.bytes[ndx]);
       puts("");
    }

 bye:
   if (valrec != NULL)
      free(valrec);
   return 0;
}

DDCA_Status switch_input(DDCA_Display_Handle* handle, uint8_t input) {
    bool saved_enable_verify = ddca_enable_verify(true);

    DDCA_Status ddcrc = ddca_set_non_table_vcp_value(handle,0x60, 0, input);

    if (ddcrc == DDCRC_VERIFY) {
        printf("Value verification failed.  Current value is now:\n");
        show_any_value(handle, DDCA_NON_TABLE_VCP_VALUE, 0x60);
     }
     else if (ddcrc != 0) {
        DDC_ERRMSG("ddca_set_non_table_vcp_value", ddcrc);
     }
     else {
        printf("Setting new value succeeded.\n");
     }

     ddca_enable_verify(saved_enable_verify);
     return ddcrc;
}
