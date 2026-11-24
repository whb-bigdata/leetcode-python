import math

import pytest


class OrderSystem:
    def split_order(self, parent_order: dict, split_ratios: list[float]) -> list[dict]:
        """
    根据比例将一个大订单拆分为多个子订单。
    parent_order: 主订单数据，例如 {'order_id': 1001, 'total_price': 100.0}
    split_ratios: 拆分比例列表，例如 [0.3, 0.3, 0.4]（总和必须为 1.0）
    """
        total_price = parent_order['total_price']
        child_orders = []
        allocated_amount = 0.0

        # 1. 业务逻辑：根据比例拆分前 N-1 个子订单
        for i in range(len(split_ratios) - 1):
            # 故意留一个小 Bug：这里用 round 可能会导致最后几分钱对不上
            child_price = round(total_price * split_ratios[i], 2)
            child_orders.append({'child_id': i, 'price': child_price})
            allocated_amount += child_price

        # 2. 最后一个子订单拿走剩下的尾款
        last_price = round(total_price - allocated_amount, 2)
        child_orders.append({'child_id': len(split_ratios) - 1, 'price': last_price})

        # ======================================================================
        # 3. 开发者红线：断言（Assert）
        # 无论中间的拆分逻辑、优惠券扣减有多复杂，最终子订单总和必须绝对等于主订单。
        # 这是写给开发人员的：如果这里报错，说明上游的拆分算法有逻辑漏洞，必须立刻停下修！
        # ======================================================================
        actual_total = sum(child['price'] for child in child_orders)

        assert math.isclose(actual_total, total_price, abs_tol=1e-2), \
            f"⚠️ 核心账目对不上！原单: {total_price}, 拆分后总和: {actual_total}。内部结算逻辑已写崩！"

        return child_orders


# ==================== 测试运行 ====================
# 初始化被测系统
@pytest.fixture
def order_sys():
  return OrderSystem()


# ======================================================================
# 测试用例 1：对应文档 TC_ORDER_001（正常比例拆分）
# ======================================================================
def test_normal_order_split(order_sys):
  # 1. 准备测试数据
  parent_order = {'order_id': 1001, 'total_price': 100.00}
  ratios = [0.3, 0.3, 0.4]

  # 2. 执行被测业务
  result = order_sys.split_order(parent_order, ratios)

  # 3. 使用 assert 进行“预期结果”的判定
  assert len(result) == 3, "应该拆分成3个子订单"
  assert result[0]['price'] == 30.00, "第一个子订单金额应为 30.00"
  assert result[1]['price'] == 30.00, "第二个子订单金额应为 30.00"
  assert result[2]['price'] == 40.00, "第三个子订单金额应为 40.00"

  # 核心总账断言
  total_split_price = sum(child['price'] for child in result)
  assert total_split_price == 100.00, "拆分后的总金额必须等于原订单金额"


# ======================================================================
# 测试用例 2：对应文档 TC_ORDER_002（三分之一除不尽的特殊情况）
# ======================================================================
# def test_floating_point_split(order_sys):
  # 1. 准备测试数据：10块钱，平分给3个人，10/3 = 3.33333...
  parent_order = {'order_id': 1002, 'total_price': 10.00}
  ratios = [1 / 3, 1 / 3, 1 / 3]

  # 2. 执行被测业务
  result = order_sys.split_order(parent_order, ratios)

  # 3. 断言验证：测试业务逻辑是否处理了“尾款补齐”，确保钱没有凭空消失或变多
  # 预期前两单是 3.33，最后一单补齐是 3.34
  assert result[0]['price'] == 3.33
  assert result[1]['price'] == 3.33
  assert result[2]['price'] == 3.34

  # 核心总账断言：加起来必须死死等于 10.00
  total_split_price = sum(child['price'] for child in result)
  assert total_split_price == 10.00, "除不尽时，最终总和也必须严格等于原订单 10.00"

