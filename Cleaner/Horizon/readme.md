## Horizon代码简介
该Horizon的目标是通过分析功能依赖（FD）的约束来修复数据中的错误。Horizon的主要组件包括图数据结构的构建、功能依赖模式图的生成、强连通分量的分析、拓扑排序以及基于这些模式的脏数据修复方法。

## 文件结构
### 1. `graph.py`
- **`Vertex` 类**: 表示图中的一个顶点，通常为一个属性或属性-值对。顶点包含属性标识符、类型（受限属性或自由属性）、连接的邻居顶点以及与这些邻居的连接权重和质量得分。
    - **方法**:
      - `addNeighbor(nbr)`: 向当前顶点添加与邻居顶点的连接。
      - `getConnections()`: 获取所有邻居顶点。
      - `getWeight(nbr)`: 获取与指定邻居的连接权重。
- **`Graph` 类**: 表示功能依赖的图，顶点代表属性或属性值，边表示属性间的功能依赖关系。
    - **方法**:
      - `addVertex(key, key1, type)`: 添加一个新顶点。
      - `addEdge(f, t)`: 添加一条从顶点f到顶点t的边。
      - `getVertices()`: 返回图中所有顶点的ID。
- **辅助函数**:
  - `tr(G)`: 计算图的转置，即反转所有边的方向。
  - `topoSort(G)`: 对图进行拓扑排序。
  - `walk(G, s)`: 从某个顶点开始遍历图，并返回遍历路径。

### 2. `horizon.py`
- **`BuildFDPatternGraph`**: 根据数据文件和功能依赖约束文件构建功能依赖模式图。该图用于表示属性之间的依赖关系。
- **`ComputePatternQulity`**: 计算图中每个模式的质量，包括支持度和边权重。
- **`BuildSCCGraghAndSort`**: 构建功能依赖的强连通分量图，并对其进行拓扑排序。返回排序结果、顶点到分量的映射以及分量列表。
- **`OrderFDs`**: 根据强连通分量和拓扑排序，对功能依赖进行排序。
- **`GeneratePatternPreservingRepairs`**: 根据功能依赖图和排序修复脏数据，生成保持模式的修复结果。
- **`dirty_cells`**: 识别脏数据文件与干净数据文件中的脏单元格。
- **`Horizon`**: Horizon的主函数，执行数据清洗过程并返回修复后的模式表达式。

### 3. `util.py`
- **`check_string(string)`**: 检查字符串中是否包含特定错误标记，并返回相应的错误类型。
- **`calF1(precision, recall)`**: 计算 F1 值。
- **`calRepPrec(pattern_expressions, dirty_path, clean_path)`**: 计算修复的精度。
- **`calRepRec(pattern_expressions, dirty_path, clean_path)`**: 计算修复的召回率。

## 流程说明
1. **构建功能依赖模式图**:
   - 调用 `BuildFDPatternGraph` 读取数据文件和功能依赖约束，构建图对象。
   - 每个顶点表示数据中的属性或属性值，边表示功能依赖关系。
   
2. **计算模式质量**:
   - 调用 `ComputePatternQulity` 使用深度优先搜索遍历图，计算每个模式的支持度和质量得分。

3. **强连通分量分析**:
   - 使用 `BuildSCCGraghAndSort` 识别图中的强连通分量并对其进行拓扑排序。

4. **功能依赖排序**:
   - 调用 `OrderFDs` 对功能依赖进行排序，以便根据依赖关系修复数据。

5. **修复脏数据**:
   - 调用 `GeneratePatternPreservingRepairs` 根据排序后的功能依赖修复脏数据，生成保持模式的修复表达式。
   - 最终修复结果通过 `Horizon` 函数执行，并返回模式表达式。

## 主要功能
- **模式修复**: Horizon根据功能依赖约束修复数据中的脏单元格。
- **拓扑排序**: 使用图的拓扑排序保证修复顺序符合功能依赖的约束。
- **质量评分**: 通过计算支持度和连接质量评估修复模式的优劣。
