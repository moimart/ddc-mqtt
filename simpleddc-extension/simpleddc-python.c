#include <Python.h>
#include "simple-ddc.h"

static PyObject* switch_to_input(PyObject* self, PyObject* args) {
    uint8_t* display = malloc(sizeof(uint8_t));
    uint8_t* input = malloc(sizeof(uint8_t));;

    if (!PyArg_ParseTuple(args, "ii", display, input))
        return NULL;

    DDCA_Display_Handle* handle = open_first_display_by_dlist();
    switch_input(handle,*input);
    ddca_close_display(handle);

    free(display);
    free(input);

    Py_RETURN_NONE;
}

static PyObject* show_input(PyObject* self, PyObject* args) {
    uint8_t* display = malloc(sizeof(uint8_t));

    if (!PyArg_ParseTuple(args, "i", display))
        *display = 0;

    DDCA_Display_Handle* handle = open_display_by_dlist(*display);
    int result = show_any_value(handle,DDCA_NON_TABLE_VCP_VALUE, 0x60);
    ddca_close_display(handle);

    free(display);
    return PyLong_FromLong(result);
}

static PyMethodDef Methods[] = {
    {"switch_to_input",  switch_to_input, METH_VARARGS, "Switch to input"},
    {"show_input", show_input, METH_VARARGS, "Show input"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "simpleddc", 
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    Methods
};

PyMODINIT_FUNC PyInit_simpleddc(void) {
    return PyModule_Create(&module);
}
