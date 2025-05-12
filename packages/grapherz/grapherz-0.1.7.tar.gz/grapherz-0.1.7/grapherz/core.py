import json
import re
import uuid

class CanvasMermaidConverter:
    def __init__(self):
        self.canvas_data = None
        self.mermaid_text = None
        
    def load_canvas(self, canvas_json):
        """加载 Canvas JSON 数据"""
        if isinstance(canvas_json, str):
            self.canvas_data = json.loads(canvas_json)
        else:
            self.canvas_data = canvas_json
        return self
    
    def load_mermaid(self, mermaid_text):
        """加载 Mermaid 文本"""
        self.mermaid_text = mermaid_text
        return self
    
    def canvas_to_mermaid(self):
        """将 Canvas 数据转换为 Mermaid 文本"""
        if not self.canvas_data:
            raise ValueError("No Canvas data loaded")
        
        lines = []
        lines.append("%%% CANVAS-DATA: " + json.dumps({"version":"1.0"}))
        lines.append("graph TD;")
        
        # 添加节点
        for node in self.canvas_data.get('nodes', []):
            # 保存节点的所有属性，而不仅仅是固定的几个
            node_metadata = node.copy()
            
            # 添加节点元数据注释
            lines.append(f"    %% NODE: {json.dumps(node_metadata)}")
            
            # 节点定义 - 如果有颜色，则添加样式
            node_style = ""
            if 'color' in node:
                node_style = f",color:{node['color']}"
            
            # 添加节点定义，可能包含样式
            if node_style:
                lines.append(f"    {node['id']}[\"{node['text']}\"]:::style{node['id']};")
                lines.append(f"    classDef style{node['id']} fill:#f9f{node_style};")
            else:
                lines.append(f"    {node['id']}[\"{node['text']}\"];")
            
        # 添加边
        edge_style_lines = []  # 收集所有边样式定义
        edge_count = 0
        
        for edge in self.canvas_data.get('edges', []):
            # 保存边的所有属性
            edge_metadata = edge.copy()
            
            # 添加边元数据注释
            lines.append(f"    %% EDGE: {json.dumps(edge_metadata)}")
            
            # 边的标签
            label_text = ""
            if 'label' in edge:
                label_text = f"|{edge['label']}|"
            
            # 添加边定义，可能包含标签
            lines.append(f"    {edge['fromNode']} -->{label_text} {edge['toNode']};")
            
            # 如果有颜色，添加边的样式（放在后面统一添加）
            if 'color' in edge:
                edge_style = f",color:{edge['color']}"
                edge_style_lines.append(f"    linkStyle {edge_count} stroke:#f9f{edge_style};")
            
            edge_count += 1
        
        # 添加所有边的样式定义（在所有边定义之后）
        lines.extend(edge_style_lines)
        
        return "```mermaid\n" + "\n".join(lines) + "\n```"
    
    def mermaid_to_canvas(self):
        """将 Mermaid 文本转换为 Canvas 数据"""
        if not self.mermaid_text:
            raise ValueError("No Mermaid text loaded")
        
        # 去除 mermaid 代码块标记
        content = self.mermaid_text.strip()
        if content.startswith("```mermaid"):
            content = content[len("```mermaid"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()
        
        nodes = []
        edges = []
        
        # 解析节点和边
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 解析节点元数据
            if line.startswith("%% NODE:"):
                try:
                    # 直接从元数据注释提取完整节点信息
                    node_data = json.loads(line[len("%% NODE:"):].strip())
                    nodes.append(node_data)
                except json.JSONDecodeError:
                    pass
            
            # 解析边元数据
            elif line.startswith("%% EDGE:"):
                try:
                    # 直接从元数据注释提取完整边信息
                    edge_data = json.loads(line[len("%% EDGE:"):].strip())
                    edges.append(edge_data)
                except json.JSONDecodeError:
                    pass
            
            i += 1
        
        return {'nodes': nodes, 'edges': edges}
    
    # CRUD 操作
    def add_node(self, text, x=0, y=0, width=260, height=60, node_type="text", color=None, **kwargs):
        """添加新节点，支持额外属性"""
        if not self.canvas_data:
            self.canvas_data = {'nodes': [], 'edges': []}
            
        # 使用短UUID形式，不包含破折号
        node_id = str(uuid.uuid4())[:16].replace('-', '')
        
        new_node = {
            'id': node_id,
            'text': text,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'type': node_type,
            'styleAttributes': {}
        }
        
        # 添加颜色属性
        if color:
            new_node['color'] = color
            
        # 添加任何其他额外属性
        for key, value in kwargs.items():
            new_node[key] = value
        
        self.canvas_data['nodes'].append(new_node)
        return node_id
    
    def add_edge(self, from_node_id, to_node_id, from_side="right", to_side="left", 
                 color=None, label=None, **kwargs):
        """添加新边，支持颜色和标签"""
        if not self.canvas_data:
            self.canvas_data = {'nodes': [], 'edges': []}
            
        # 验证节点是否存在
        node_ids = [n['id'] for n in self.canvas_data['nodes']]
        if from_node_id not in node_ids or to_node_id not in node_ids:
            return None
            
        # 使用短UUID形式，不包含破折号
        edge_id = str(uuid.uuid4())[:16].replace('-', '')
        
        new_edge = {
            'id': edge_id,
            'fromNode': from_node_id,
            'toNode': to_node_id,
            'fromSide': from_side,
            'toSide': to_side,
            'styleAttributes': {'pathfindingMethod': 'a-star'}
        }
        
        # 添加颜色和标签
        if color:
            new_edge['color'] = color
        if label:
            new_edge['label'] = label
            
        # 添加任何其他额外属性
        for key, value in kwargs.items():
            new_edge[key] = value
        
        self.canvas_data['edges'].append(new_edge)
        return edge_id
    
    def delete_node(self, node_id):
        """删除节点及相关的边"""
        if not self.canvas_data:
            return False
            
        # 删除节点
        self.canvas_data['nodes'] = [n for n in self.canvas_data['nodes'] if n['id'] != node_id]
        
        # 删除相关的边
        self.canvas_data['edges'] = [e for e in self.canvas_data['edges'] 
                                    if e['fromNode'] != node_id and e['toNode'] != node_id]
        return True
    
    def delete_edge(self, edge_id):
        """删除边"""
        if not self.canvas_data:
            return False
            
        self.canvas_data['edges'] = [e for e in self.canvas_data['edges'] if e['id'] != edge_id]
        return True
    
    def update_node(self, node_id, **kwargs):
        """更新节点属性"""
        if not self.canvas_data:
            return False
            
        for i, node in enumerate(self.canvas_data['nodes']):
            if node['id'] == node_id:
                for key, value in kwargs.items():
                    self.canvas_data['nodes'][i][key] = value
                return True
        return False
    
    def update_edge(self, edge_id, **kwargs):
        """更新边属性"""
        if not self.canvas_data:
            return False
            
        for i, edge in enumerate(self.canvas_data['edges']):
            if edge['id'] == edge_id:
                for key, value in kwargs.items():
                    self.canvas_data['edges'][i][key] = value
                return True
        return False