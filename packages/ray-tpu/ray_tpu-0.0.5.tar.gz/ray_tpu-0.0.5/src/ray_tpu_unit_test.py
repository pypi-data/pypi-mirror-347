"""TODO: ricliu - DO NOT SUBMIT without either providing a detailed docstring or
removing it altogether.
"""


import unittest
from unittest.mock import patch
import pytest
import ray
import ray_tpu
import logging
from ray_tpu import RayTpu


logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()


RAY_RESOURCES = {
  'TPU': 16,
  'TPU-v4-16-head': 1
}

TPU_METADATA = (
    "my_tpu",    # TPU name
    4,           # num_hosts
    4,           # chips_per_host
    "127.0.0.1"  # head_ip
)


@ray_tpu.remote(
    topology={"v4-16": 1},
)
class MyActor:
    def __init__(self, data: str):
        self._data = data

    def my_task(self):
        return self._data

@ray_tpu.remote(
    topology={"v4-16": 1},
)
def my_task():
    return "hello world"


class FakeActorHandle:
  def my_task(self):
    return "do nothing"


class FakeActionWrapper:
  def remote(self, *args, **kwargs):
    return FakeActorHandle()


@patch('ray.get')
@patch('ray.available_resources')
def test_get_available_resources(mock_ray_resources, mock_ray_get):
    mock_ray_resources.return_value = RAY_RESOURCES
    mock_ray_get.return_value = [TPU_METADATA]
    ray_tpu.init()
    tpu_resources = ray_tpu.available_resources()
    expected_resources = {"v4-16": [RayTpu(name="my_tpu", num_hosts=4, chips_per_host=4, head_ip="127.0.0.1", topology="v4-16")]}

    assert tpu_resources == expected_resources


@patch('ray.get')
@patch('ray.available_resources')
def test_ray_task(mock_ray_resources, mock_ray_get):
    mock_ray_resources.return_value = RAY_RESOURCES
    mock_ray_get.return_value = [TPU_METADATA]
    ray_tpu.init()
    handles = my_task()

    assert len(handles) == 4


@patch('ray.get')
@patch('ray.available_resources')
def test_ray_actor(mock_ray_resources, mock_ray_get):
    mock_ray_resources.return_value = RAY_RESOURCES
    mock_ray_get.return_value = [TPU_METADATA]
    ray_tpu.init()

    with patch.object(ray.actor.ActorClass, 'options') as mock_remote:
      mock_remote.return_value = FakeActionWrapper()
      a = MyActor(data="hello from actor")
      mylogger.debug(f"a: {a}")
      handles = a.my_task()

    #ray.get(a.my_task())
