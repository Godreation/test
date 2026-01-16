from pathfinding import GridPathfinder

# 示例网格：0表示可通行，1表示障碍物
# 10x10网格
EXAMPLE_GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0]
]

START = (0, 0)  # 起点：左上角
END = (9, 9)    # 终点：右下角

def print_grid(grid, path=None):
    """打印网格，可选显示路径"""
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[0])):
            pos = (i, j)
            if pos == START:
                row.append('S')  # 起点
            elif pos == END:
                row.append('E')  # 终点
            elif path and pos in path:
                row.append('*')  # 路径
            elif grid[i][j] == 1:
                row.append('#')  # 障碍物
            else:
                row.append('.')  # 可通行
        print(' '.join(row))
    print()

def print_results(results):
    """打印所有算法的结果比较"""
    print("=" * 80)
    print("网格寻路算法性能比较")
    print("=" * 80)
    print(f"起点: {START}, 终点: {END}")
    print(f"网格大小: {len(EXAMPLE_GRID)}x{len(EXAMPLE_GRID[0])}")
    print("=" * 80)
    
    # 格式化输出表头
    header = f"{'算法':<10} {'路径长度':<10} {'运行时间(ms)':<15} {'访问节点数':<12} {'最大内存使用':<15} {'是否找到路径':<15}"
    print(header)
    print("-" * 80)
    
    for result in results:
        path_length = len(result['path']) if result['path'] else 0
        time_ms = result['time'] * 1000
        nodes_visited = result['nodes_visited']
        max_memory = result['max_memory']
        found = "是" if result['path'] else "否"
        
        row = f"{result['algorithm']:<10} {path_length:<10} {time_ms:<15.3f} {nodes_visited:<12} {max_memory:<15} {found:<15}"
        print(row)
    
    print("=" * 80)
    
    # 打印最佳算法
    successful_results = [r for r in results if r['path']]
    if successful_results:
        # 按运行时间排序
        fastest = min(successful_results, key=lambda x: x['time'])
        # 按访问节点数排序
        most_efficient = min(successful_results, key=lambda x: x['nodes_visited'])
        
        print(f"\n最快算法: {fastest['algorithm']} ({fastest['time']*1000:.3f} ms)")
        print(f"最节省节点算法: {most_efficient['algorithm']} ({most_efficient['nodes_visited']} 个节点)")
        
        # 打印最佳路径
        print(f"\n{fastest['algorithm']} 算法找到的路径:")
        if fastest['path']:
            print(f"路径长度: {len(fastest['path'])} 步")
            print(f"路径: {fastest['path']}")
            print_grid(EXAMPLE_GRID, fastest['path'])

def main():
    print("初始网格:")
    print_grid(EXAMPLE_GRID)
    
    # 创建寻路器实例
    pathfinder = GridPathfinder(EXAMPLE_GRID, START, END)
    
    # 运行所有算法
    print("正在运行所有寻路算法...")
    results = pathfinder.run_all_algorithms()
    
    # 打印结果
    print_results(results)

if __name__ == "__main__":
    main()
