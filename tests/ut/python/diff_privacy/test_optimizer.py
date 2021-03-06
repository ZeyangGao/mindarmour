# Copyright 2020 Huawei Technologies Co., Ltd
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
import pytest

from mindspore import nn
from mindspore import context
from mindspore.train.model import Model

from mindarmour.diff_privacy import DPOptimizerClassFactory

from test_network import LeNet5


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_optimizer():
    context.set_context(mode=context.PYNATIVE_MODE, device_target="Ascend")
    network = LeNet5()
    lr = 0.01
    momentum = 0.9
    micro_batches = 2
    loss = nn.SoftmaxCrossEntropyWithLogits()
    gaussian_mech = DPOptimizerClassFactory(micro_batches)
    gaussian_mech.set_mechanisms('Gaussian', norm_bound=1.5, initial_noise_multiplier=5.0)
    net_opt = gaussian_mech.create('SGD')(params=network.trainable_params(), learning_rate=lr,
                                          momentum=momentum)
    _ = Model(network, loss_fn=loss, optimizer=net_opt, metrics=None)


@pytest.mark.level0
@pytest.mark.platform_x86_gpu_inference
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_optimizer_gpu():
    context.set_context(mode=context.PYNATIVE_MODE, device_target="GPU")
    network = LeNet5()
    lr = 0.01
    momentum = 0.9
    micro_batches = 2
    loss = nn.SoftmaxCrossEntropyWithLogits()
    gaussian_mech = DPOptimizerClassFactory(micro_batches)
    gaussian_mech.set_mechanisms('Gaussian', norm_bound=1.5, initial_noise_multiplier=5.0)
    net_opt = gaussian_mech.create('SGD')(params=network.trainable_params(), learning_rate=lr,
                                          momentum=momentum)
    _ = Model(network, loss_fn=loss, optimizer=net_opt, metrics=None)


@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_optimizer_cpu():
    context.set_context(mode=context.PYNATIVE_MODE, device_target="CPU")
    network = LeNet5()
    lr = 0.01
    momentum = 0.9
    micro_batches = 2
    loss = nn.SoftmaxCrossEntropyWithLogits()
    gaussian_mech = DPOptimizerClassFactory(micro_batches)
    gaussian_mech.set_mechanisms('Gaussian', norm_bound=1.5, initial_noise_multiplier=5.0)
    net_opt = gaussian_mech.create('SGD')(params=network.trainable_params(), learning_rate=lr,
                                          momentum=momentum)
    _ = Model(network, loss_fn=loss, optimizer=net_opt, metrics=None)
