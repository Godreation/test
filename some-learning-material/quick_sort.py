import random
import time
import sys
import tracemalloc
from typing import List, Tuple, Dict, Any


def quick_sort(arr: List[int]) -> List[int]:
    """
    快速排序算法实现
    
    Args:
        arr: 待排序的整数列表
        
    Returns:
        排序后的整数列表
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    原地快速排序算法实现（更节省空间）
    
    Args:
        arr: 待排序的整数列表
        low: 起始索引
        high: 结束索引
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    """
    分区函数，用于原地快速排序
    
    Args:
        arr: 待分区的数组
        low: 起始索引
        high: 结束索引
        
    Returns:
        基准元素的最终位置
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def generate_test_data(size: int = 1000, min_val: int = 0, max_val: int = 10000) -> List[int]:
    """
    生成随机测试数据
    
    Args:
        size: 数据规模
        min_val: 最小值
        max_val: 最大值
        
    Returns:
        随机生成的整数列表
    """
    return [random.randint(min_val, max_val) for _ in range(size)]


def monitor_sort_performance(sort_func, test_data: List[int], algorithm_name: str = "排序算法") -> Dict[str, Any]:
    """
    监控排序算法性能
    
    Args:
        sort_func: 排序函数
        test_data: 测试数据
        algorithm_name: 算法名称
        
    Returns:
        包含性能指标的字典
    """
    # 复制测试数据以避免修改原始数据
    data_copy = test_data.copy()
    
    # 开始内存跟踪
    tracemalloc.start()
    
    # 记录开始时间
    start_time = time.time()
    
    # 执行排序
    if algorithm_name == "原地快速排序":
        # 对于原地排序，直接修改数据
        sort_func(data_copy)
        sorted_data = data_copy
    else:
        # 对于非原地排序，返回新列表
        sorted_data = sort_func(data_copy)
    
    # 记录结束时间
    end_time = time.time()
    
    # 获取内存使用情况
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 计算性能指标
    execution_time = (end_time - start_time) * 1000  # 转换为毫秒
    memory_usage = peak / 1024  # 转换为KB
    
    # 验证排序结果
    is_sorted = all(sorted_data[i] <= sorted_data[i + 1] for i in range(len(sorted_data) - 1))
    
    return {
        "algorithm": algorithm_name,
        "data_size": len(test_data),
        "execution_time_ms": execution_time,
        "peak_memory_kb": memory_usage,
        "is_correct": is_sorted,
        "original_data_sample": test_data[:10] if len(test_data) > 10 else test_data,
        "sorted_data_sample": sorted_data[:10] if len(sorted_data) > 10 else sorted_data
    }


def print_performance_report(performance_data: Dict[str, Any]) -> None:
    """
    打印性能报告
    
    Args:
        performance_data: 性能数据字典
    """
    print(f"=== {performance_data['algorithm']} 性能报告 ===")
    print(f"数据规模: {performance_data['data_size']} 个元素")
    print(f"执行时间: {performance_data['execution_time_ms']:.2f} 毫秒")
    print(f"峰值内存使用: {performance_data['peak_memory_kb']:.2f} KB")
    print(f"排序结果正确性: {'✓ 正确' if performance_data['is_correct'] else '✗ 错误'}")
    print(f"原始数据样本: {performance_data['original_data_sample']}")
    print(f"排序后样本: {performance_data['sorted_data_sample']}")
    print("-" * 50)


def compare_sorting_algorithms():
    """
    比较不同排序算法的性能
    """
    # 生成测试数据
    test_sizes = [100, 1000, 5000]
    
    for size in test_sizes:
        print(f"\n测试数据规模: {size} 个元素")
        print("=" * 60)
        
        test_data = generate_test_data(size)
        
        # 测试标准快速排序
        perf1 = monitor_sort_performance(quick_sort, test_data, "标准快速排序")
        print_performance_report(perf1)
        
        # 测试原地快速排序
        perf2 = monitor_sort_performance(quick_sort_inplace, test_data, "原地快速排序")
        print_performance_report(perf2)


def main():
    """
    主函数 - 演示快速排序算法
    """
    print("快速排序算法演示")
    print("=" * 60)
    
    # 演示小规模数据排序
    small_data = generate_test_data(20, 1, 100)
    print(f"原始数据: {small_data}")
    
    # 使用标准快速排序
    sorted_data = quick_sort(small_data)
    print(f"标准快速排序结果: {sorted_data}")
    
    # 使用原地快速排序
    data_copy = small_data.copy()
    quick_sort_inplace(data_copy)
    print(f"原地快速排序结果: {data_copy}")
    
    # 比较不同规模数据的性能
    compare_sorting_algorithms()


if __name__ == "__main__":
    main()