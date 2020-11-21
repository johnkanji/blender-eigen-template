#include <npe.h>
#include <sstream>

// This file creates a binding named 'add_matrices' which will be callable from python.
// This function will take in two numpy arrays and add them together a number of times, returning the result.
// If the input arrays' shapes don't match, this function will throw a ValueError


// A docstring for the function (see below)
const char* add_matrices_doc = R"Qu8mg5v7(
Add two Eigen matrices
Parameters
----------
m1 : The first matrix to add
m2 : The second matrix to add
num_additions : The number of times to repeat the addition
in_place : if True, the result is stored in m2, False by default
Returns
-------
The sum of the two matrices
)Qu8mg5v7";


// Begin defining the binding. Bound functions are defined by
//     `npe_function(func_name)`
// where `func_name` is the name of the function exposed to Python
npe_function(add_matrices)

// Define a docstring for this function. The argument to `npe_doc` is a string  defined at compile time or a string literal. 
// This docstring will be shown in the help for this function
npe_doc(add_matrices_doc)

// Specify arguments to `add_matrices` as well as their allowed dtypes:
//
// Numpyeigen enables constant time to functions are specified by:
//    `npe_arg(argname, type1, type2, ..., typeN)`
// where `typeX` specifies the dtype of the input and whether the input is dense or sparse
// For example, `dense_float` means this argument can be a dense array with dtype float, 
//              `sparse_float` means this argument can be a sparse matrix with dtype float, 
// 
// Here we're specifying that `m1` must be a dense array with dtype `double`, `float`, `int`, `long`, or `longlong`
// 
npe_arg(m1, dense_float, dense_double, dense_int, dense_longlong)

// Specify a second argument `m2` which will be added to `m1`. 
//
// In C++, we can only add matrices together which have the same type and layout (column-major/row-major)
// For this reason, instead of passing in a list of types, we specify the type with `npe_matches` which has the form
//     `npe_matches(other_arg)`
// where `other_arg` is the name of another argument specified with `npe_arg`
//
// When `npe_matches` is specified, the user will get a runtime error if they pass in arguments which have either
// (i) different dtypes
// (ii) a different layout (i.e. column-major, row-major, or unaligned (e.g. arr[0:-1:7] will not be aligned)
//
// You can specify as many arguments as you want with npe_matches
npe_arg(m2, npe_matches(m1))

// Specify a non-numpy/scipy typed argument. Numpyeigen uses pybind11 under the hood. 
// Non numpy/scipy arguments get converted from python to C++ in the same way as pybind11. 
// See https://pybind11.readthedocs.io/en/stable/advanced/cast/ for details on how pybind converts types.
//
// Non numpy types are specified by
//     `npe_arg(argname, type)`
// where `argname` is the name of the argument, and `type` is the C++ type of the argument
npe_arg(num_additions, int)

// Specify an optional argument to the function. This works the same way as specifying normal arguments but allows a default value.
// Note that default arguments do not yet work with numpy/scipy arguments.
// Default arguments are passed in with
//     `npe_default_arg(argname, type, default_value)`
// Where `argname` is the name of the argument, `type` is the C++ type of the argument, 
// and `default_value` is a C++ expression returning the default value of the argument if it is not explicitly passed in
npe_default_arg(in_place, bool, false)

// Begin the actual code for the binding
npe_begin_code()

    // Inside the body of a numpyeigen binding, you have access to all the arguments specified in the definition.
    // Numpy/Scipy arguments are automatically converted to Eigen matrix and sparsematrix types. 
    //
    // Several macros/typedefs are also defined for Numpy/Scipy arguments. Suppose `nparg` is the name of a Numpy or Scipy argument. Then 
    //     `npe_Matrix_nparg` is the Eigen::Matrix or Eigen::SparseMatrix type of the argument
    //     `npe_Scalar_nparg` is the scalar type of the Eigen tyep
    //     `npe_Map_nparg' is the Eigen::Map type wrapping the argument
    // These can be used to declare temporary variables of the right type or as template arguments.

    // Check if `m1` and `m2` have the same shape, if not throw a ValueError
    if (m1.rows() != m2.rows() || m1.cols() != m2.cols()) {
        std::stringstream ss;
        ss << "Matrices m1 and m2 must have the same shape. Got m1.shape = (" << m1.rows() << ", " << m1.cols() << "), ";
        ss << "m2.shape = (" << m2.rows() << ", " << m2.cols() << ").";
        throw pybind11::value_error(ss.str());
    }
    
    // If we're doing things in place, accumulate the sum of matrices into `m2`
    if (in_place) {
        for (int i = 0; i < num_additions; i += 1) {
            m2 += m1;
        }
        
        // To return a Eigen::Matrix without copying, you need to wrap it in `npe_move` which creates a Python object from the matrix
        // and gives ownership of the matrix's memory to the python runtime
        return npe::move(m2);
        
    // Otherwise create a new matrix to accumulate into
    } else {
        // Create a matrix m3 which is a copy of m2
        npe_Matrix_m2 m3 = m2;
        for (int i = 0; i < num_additions; i += 1) {
            m3 += m1;
        }
        // To return a Eigen::Matrix without copying, you need to wrap it in `npe_move` which creates a Python object from the matrix
        // and gives ownership of the matrix's memory to the python runtime
        return npe::move(m3);
    }

npe_end_code()