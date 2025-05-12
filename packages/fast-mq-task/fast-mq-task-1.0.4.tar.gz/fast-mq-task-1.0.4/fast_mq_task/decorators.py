# -*- coding: utf-8 -*-
import logging
from typing import Callable, Dict
from .models import RabbitMeta


# --------------------------
# 装饰器模块 (decorators.py)
# --------------------------
class TaskRegistry:
    _handlers: Dict[str, RabbitMeta] = {}

    @classmethod
    def decorator_handler(cls, task_type: str) -> Callable:
        # 新增参数校验
        if not task_type:
            raise ValueError("`task_type`不能全部为空")

        def decorator(func: Callable) -> Callable:
            meta = RabbitMeta(
                task_type=task_type,
                handler_func=func
            )
            cls._handlers[task_type] = meta
            logging.info(f"处理器注册: task_type={task_type}, exchange={meta.queue_key}, func={func}")

            return func

        return decorator

    @classmethod
    def register_handler(cls, task_type: str, func: Callable) -> Callable:
        # 新增参数校验
        if not task_type:
            raise ValueError("`task_type`不能全部为空")

        meta = RabbitMeta(
            task_type=task_type,
            handler_func=func
        )
        cls._handlers[task_type] = meta
        logging.info(f"处理器注册: task_type={task_type}, exchange={meta.queue_key}, func={func}")

        return func


task_handler = TaskRegistry.decorator_handler


def ref_to_obj(ref):
    """
    将包与路径引用串反序列化成可执行对象
    Returns the object pointed to by ``ref``.
    :type ref: str
    """
    if not isinstance(ref, str):
        raise TypeError('References must be strings')
    if ':' not in ref:
        raise ValueError('Invalid reference')

    module_name, rest = ref.split(':', 1)
    try:
        obj = __import__(module_name, fromlist=[rest])
    except ImportError:
        raise LookupError('Error resolving reference %s: could not import module' % ref)

    try:
        for name in rest.split('.'):
            obj = getattr(obj, name)
        return obj
    except Exception:
        raise LookupError('Error resolving reference %s: error looking up object' % ref)
