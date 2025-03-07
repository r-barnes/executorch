# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# Kernel library for portable kernels. Please this file formatted by running:
# ~~~
# cmake-format --first-comment-is-literal=True CMakeLists.txt
# ~~~

cmake_minimum_required(VERSION 3.19)
project(arm_example)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT PYTHON_EXECUTABLE)
  set(PYTHON_EXECUTABLE python3)
endif()
# Source root directory for executorch.
if(NOT EXECUTORCH_ROOT)
  set(EXECUTORCH_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../..)
endif()
# Source root directory for pytorch.
if(NOT TORCH_ROOT)
  set(TORCH_ROOT ${EXECUTORCH_ROOT}/third-party/pytorch)
endif()

set(_common_compile_options -Wno-deprecated-declarations -fPIC)

# Let files say "include <executorch/path/to/header.h>".
set(_common_include_directories ${EXECUTORCH_ROOT}/..)

find_package(executorch CONFIG REQUIRED HINTS ${CMAKE_INSTALL_PREFIX})
target_include_directories(executorch INTERFACE ${_common_include_directories})

include(${EXECUTORCH_ROOT}/build/Utils.cmake)
include(${EXECUTORCH_ROOT}/build/Codegen.cmake)

# Generate C++ bindings to register kernels into both PyTorch (for AOT) and
# Executorch (for runtime). Here select all ops in functions.yaml
gen_selected_ops("" "${EXECUTORCH_SELECT_OPS_LIST}" "")
generate_bindings_for_kernels(
  ${EXECUTORCH_ROOT}/kernels/portable/functions.yaml "")
gen_operators_lib("portable_ops_lib" portable_kernels executorch)
