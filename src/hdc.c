#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>

static PyObject* bind_vectors(PyObject* self, PyObject* args) {
    PyArrayObject *a, *b;
    if (!PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &a, &PyArray_Type, &b)) return NULL;
    
    int n = PyArray_SIZE(a);
    int8_t *a_data = (int8_t*)PyArray_DATA(a);
    int8_t *b_data = (int8_t*)PyArray_DATA(b);
    
    npy_intp dims[1] = {n};
    PyObject *out = PyArray_SimpleNew(1, dims, NPY_INT8);
    int8_t *out_data = (int8_t*)PyArray_DATA((PyArrayObject*)out);
    
    for (int i = 0; i < n; i++) {
        out_data[i] = a_data[i] * b_data[i];
    }
    return out;
}

static PyMethodDef HDCMethods[] = {
    {"bind", bind_vectors, METH_VARARGS, "XOR bind two vectors"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hdcmodule = {
    PyModuleDef_HEAD_INIT, "hdc_engine", NULL, -1, HDCMethods
};

PyMODINIT_FUNC PyInit_hdc_engine(void) {
    import_array();
    return PyModule_Create(&hdcmodule);
}
