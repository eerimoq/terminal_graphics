#include <Python.h>
#include "numpy/ndarraytypes.h"

static PyObject *m_write(void *self_p,
                         PyObject *args_p,
                         PyObject *kwargs_p)
{
    int height;
    int width;
    int i;
    int j;
    int red;
    int green;
    int blue;
    PyArrayObject *image_p;
    uint8_t *image_buf_p;
    uint8_t *image_row_background_buf_p;
    uint8_t *image_row_foreground_buf_p;
    int nrows;
    int ncols;

    if (!PyArg_ParseTuple(args_p, "iiO", &nrows, &ncols, &image_p)) {
        return (NULL);
    }

    height = PyArray_DIMS(image_p)[0];
    width = PyArray_DIMS(image_p)[1];
    image_buf_p = (uint8_t *)PyArray_BYTES(image_p);

    for (i = 0; i < height / 2; i++) {
        image_row_background_buf_p = &image_buf_p[2 * i * ncols * 3];
        image_row_foreground_buf_p = image_row_background_buf_p + (ncols * 3);

        for (j = 0; j < width; j++) {
            red = image_row_background_buf_p[3 * j + 0];
            green = image_row_background_buf_p[3 * j + 1];
            blue = image_row_background_buf_p[3 * j + 2];
            printf("\x1b""[48;2;%d;%d;%dm", red, green, blue);
            red = image_row_foreground_buf_p[3 * j + 0];
            green = image_row_foreground_buf_p[3 * j + 1];
            blue = image_row_foreground_buf_p[3 * j + 2];
            printf("\x1b""[38;2;%d;%d;%dm", red, green, blue);
            printf("\xe2\x96\x84");
        }

        printf("\x1b""[39m\x1b""[49m\n");
    }

    Py_INCREF(Py_None);

    return (Py_None);
}

static PyMethodDef module_methods[] = {
    { "write", (PyCFunction)m_write, METH_VARARGS },
    { NULL }
};

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "terminal_graphics.ctext",
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = module_methods
};

PyMODINIT_FUNC PyInit_ctext(void)
{
    PyObject *module_p;

    module_p = PyModule_Create(&module);

    if (module_p == NULL) {
        return (NULL);
    }

    return (module_p);
}
