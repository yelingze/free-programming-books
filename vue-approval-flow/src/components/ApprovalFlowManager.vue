<template>
  <div>
    <h2>创建审批流</h2>
    <div>
      <label>审批流名称:</label>
      <input v-model="newFlowName" placeholder="例如: 采购申请" />
    </div>
    <div v-for="(node, index) in newFlowNodes" :key="index" class="node-config">
      <h3>节点 {{ index + 1 }}</h3>
      <label>所需角色:</label>
      <input v-model="node.role" placeholder="例如: manager" />
      <label>所需权限:</label>
      <input v-model="node.permission" placeholder="例如: approve_purchase" />
      <button @click="removeNode(index)">删除节点</button>
    </div>
    <button @click="addNode">添加节点</button>
    <button @click="createFlow">创建审批流</button>

    <h2>现有审批流</h2>
    <ul>
      <li v-for="flow in flows" :key="flow.name">
        <strong>{{ flow.name }}</strong>
        <ul>
          <li v-for="(node, index) in flow.nodes" :key="index">
            节点{{ index + 1 }}: 角色({{ node.role }}), 权限({{ node.permission }})
          </li>
        </ul>
        <button @click="deleteFlow(flow.name)">删除</button>
      </li>
    </ul>

    <h2>用户权限校验</h2>
    <div>
      <label>用户名:</label>
      <input v-model="currentUser" placeholder="例如: alice" />
    </div>
    <div>
      <label>选择审批流:</label>
      <select v-model="selectedFlowName">
        <option v-for="flow in flows" :key="flow.name" :value="flow.name">
          {{ flow.name }}
        </option>
      </select>
    </div>
    <button @click="checkUserPermission">校验权限</button>
    <div v-if="checkResult !== null">
      <h3>校验结果:</h3>
      <p :class="{ 'result-pass': checkResult, 'result-fail': !checkResult }">
        {{ checkResult ? '通过' : '不通过' }}
      </p>
    </div>
  </div>
</template>

<script>
// 模拟后端权限校验API
const mockCheckPermissionAPI = (username, flow) => {
  // 模拟逻辑：假设用户 alice 拥有 manager 角色和 approve_purchase 权限
  // 假设用户 bob 拥有 employee 角色
  const userPermissions = {
    'alice': { roles: ['manager'], permissions: ['approve_purchase'] },
    'bob': { roles: ['employee'], permissions: [] }
  };

  const user = userPermissions[username];
  if (!user) {
    return false; // 用户不存在
  }

  // 模拟超级用户
  if (username === 'admin') {
    return true;
  }

  // 检查审批流中的每个节点
  for (const node of flow.nodes) {
    const hasRole = user.roles.includes(node.role);
    const hasPermission = user.permissions.includes(node.permission);
    if (!hasRole || !hasPermission) {
      return false; // 用户缺少任一节点的任一权限
    }
  }
  return true; // 所有节点权限都满足
};

export default {
  name: 'ApprovalFlowManager',
  data() {
    return {
      newFlowName: '',
      newFlowNodes: [{ role: '', permission: '' }],
      flows: [
        // 初始示例数据
        {
          name: '采购申请',
          nodes: [
            { role: 'employee', permission: 'submit_purchase' },
            { role: 'manager', permission: 'approve_purchase' }
          ]
        }
      ],
      currentUser: '',
      selectedFlowName: '',
      checkResult: null
    };
  },
  methods: {
    addNode() {
      this.newFlowNodes.push({ role: '', permission: '' });
    },
    removeNode(index) {
      if (this.newFlowNodes.length > 1) {
        this.newFlowNodes.splice(index, 1);
      }
    },
    createFlow() {
      if (!this.newFlowName || this.newFlowNodes.some(node => !node.role || !node.permission)) {
        alert('请填写完整的审批流信息');
        return;
      }
      const newFlow = {
        name: this.newFlowName,
        nodes: JSON.parse(JSON.stringify(this.newFlowNodes)) // 深拷贝
      };
      this.flows.push(newFlow);
      // 重置表单
      this.newFlowName = '';
      this.newFlowNodes = [{ role: '', permission: '' }];
    },
    deleteFlow(flowName) {
      this.flows = this.flows.filter(flow => flow.name !== flowName);
    },
    checkUserPermission() {
      if (!this.currentUser || !this.selectedFlowName) {
        alert('请选择用户和审批流');
        return;
      }
      const flowToCheck = this.flows.find(f => f.name === this.selectedFlowName);
      if (flowToCheck) {
        // 调用模拟API
        this.checkResult = mockCheckPermissionAPI(this.currentUser, flowToCheck);
      }
    }
  }
};
</script>

<style scoped>
.node-config {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}
.result-pass {
  color: green;
  font-weight: bold;
}
.result-fail {
  color: red;
  font-weight: bold;
}
</style>