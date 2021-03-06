# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Iterative-gradient Attack test.
"""
import numpy as np
import pytest

from mindspore.ops import operations as P
from mindspore.nn import Cell
from mindspore import context

from mindarmour.attacks import BasicIterativeMethod
from mindarmour.attacks import MomentumIterativeMethod
from mindarmour.attacks import ProjectedGradientDescent
from mindarmour.attacks import IterativeGradientMethod
from mindarmour.attacks import DiverseInputIterativeMethod
from mindarmour.attacks import MomentumDiverseInputIterativeMethod

context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")


# for user
class Net(Cell):
    """
    Construct the network of target model.

    Examples:
        >>> net = Net()
    """

    def __init__(self):
        super(Net, self).__init__()
        self._softmax = P.Softmax()

    def construct(self, inputs):
        """
        Construct network.

        Args:
            inputs (Tensor): Input data.
        """
        out = self._softmax(inputs)
        return out


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_basic_iterative_method():
    """
    Basic iterative method unit test.
    """
    input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
    label = np.asarray([2], np.int32)
    label = np.eye(3)[label].astype(np.float32)

    for i in range(5):
        net = Net()
        attack = BasicIterativeMethod(net, nb_iter=i + 1)
        ms_adv_x = attack.generate(input_np, label)
        assert np.any(
            ms_adv_x != input_np), 'Basic iterative method: generate value' \
                                   ' must not be equal to original value.'


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_momentum_iterative_method():
    """
    Momentum iterative method unit test.
    """
    input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
    label = np.asarray([2], np.int32)
    label = np.eye(3)[label].astype(np.float32)

    for i in range(5):
        attack = MomentumIterativeMethod(Net(), nb_iter=i + 1)
        ms_adv_x = attack.generate(input_np, label)
        assert np.any(ms_adv_x != input_np), 'Momentum iterative method: generate' \
                                             ' value must not be equal to' \
                                             ' original value.'


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_projected_gradient_descent_method():
    """
    Projected gradient descent method unit test.
    """
    input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
    label = np.asarray([2], np.int32)
    label = np.eye(3)[label].astype(np.float32)

    for i in range(5):
        attack = ProjectedGradientDescent(Net(), nb_iter=i + 1)
        ms_adv_x = attack.generate(input_np, label)

        assert np.any(
            ms_adv_x != input_np), 'Projected gradient descent method: ' \
                                   'generate value must not be equal to' \
                                   ' original value.'


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_diverse_input_iterative_method():
    """
    Diverse input iterative method unit test.
    """
    input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
    label = np.asarray([2], np.int32)
    label = np.eye(3)[label].astype(np.float32)

    attack = DiverseInputIterativeMethod(Net())
    ms_adv_x = attack.generate(input_np, label)
    assert np.any(ms_adv_x != input_np), 'Diverse input iterative method: generate' \
                                             ' value must not be equal to' \
                                             ' original value.'


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_momentum_diverse_input_iterative_method():
    """
    Momentum diverse input iterative method unit test.
    """
    input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
    label = np.asarray([2], np.int32)
    label = np.eye(3)[label].astype(np.float32)

    attack = MomentumDiverseInputIterativeMethod(Net())
    ms_adv_x = attack.generate(input_np, label)
    assert np.any(ms_adv_x != input_np), 'Momentum diverse input iterative method: ' \
                                             'generate value must not be equal to' \
                                             ' original value.'


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_error():
    with pytest.raises(TypeError):
        # check_param_multi_types
        assert IterativeGradientMethod(Net(), bounds=None)
    attack = IterativeGradientMethod(Net(), bounds=(0.0, 1.0))
    with pytest.raises(NotImplementedError):
        input_np = np.asarray([[0.1, 0.2, 0.7]], np.float32)
        label = np.asarray([2], np.int32)
        label = np.eye(3)[label].astype(np.float32)
        assert attack.generate(input_np, label)
