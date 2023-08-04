# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Example of showcasing registering custom operator through torch library API."""
import torch

from examples.export.export_example import export_to_ff
from torch.library import impl, Library

my_op_lib = Library("my_ops", "DEF")

# registering an operator that multiplies input tensor by 3 and returns it.
my_op_lib.define("mul3(Tensor input) -> Tensor")  # should print 'mul3'


@impl(my_op_lib, "mul3", dispatch_key="CompositeExplicitAutograd")
def mul3_impl(a: torch.Tensor) -> torch.Tensor:
    return a * 3


# registering the out variant.
my_op_lib.define(
    "mul3.out(Tensor input, *, Tensor(a!) output) -> Tensor(a!)"
)  # should print 'mul3.out'


@impl(my_op_lib, "mul3.out", dispatch_key="CompositeExplicitAutograd")
def mul3_out_impl(a: torch.Tensor, *, out: torch.Tensor) -> torch.Tensor:
    a.mul_(3)
    out.copy_(a)
    return out


# example model
class Model(torch.nn.Module):
    def forward(self, a):
        return torch.ops.my_ops.mul3.default(a)


def main():
    m = Model()
    input = torch.randn(2, 3)
    # capture and lower
    export_to_ff("custom_ops_1", m, (input,))


if __name__ == "__main__":
    main()
