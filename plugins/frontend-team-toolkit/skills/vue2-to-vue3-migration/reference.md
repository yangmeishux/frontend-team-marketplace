# Vue 2 → Vue 3 迁移参考

与 `SKILL.md` 配套：提供可复用的**转换模式与对照表**。业务文件名、目录名请以实际仓库为准；下文示例使用中性命名。

**建议阅读顺序**：先读 `SKILL.md` 主路径（两阶段协议、工程就绪提要）→ 本文件 §1–§7（语法与工具链）→ §8（一页纸模板）→ §9–§12（工程就绪展开、完整扫雷、完整校验、完整坑点）。

---

## 1. Options API → `<script setup>`（节选）

以下演示 **`.sync` / `input` 型 v-model** 与 **计算属性**：逻辑迁到 Vue 3 时需统一为 `modelValue` + `update:modelValue`（或显式 props/emit 名称）。

### Vue 2（Options API）

```vue
<script>
export default {
  props: {
    value: { type: Boolean, default: false },
    record: { type: Object, required: true },
  },
  data() {
    return { busy: false, draft: null };
  },
  computed: {
    open: {
      get() {
        return this.value;
      },
      set(v) {
        this.$emit('input', v);
      },
    },
    title() {
      return this.draft?.title;
    },
  },
  watch: {
    open(visible) {
      if (visible) this.draft = cloneDeep(this.record);
    },
  },
  methods: {
    async submit() {
      this.busy = true;
      try {
        this.$emit('confirm', this.draft);
      } finally {
        this.busy = false;
      }
    },
  },
};
</script>
```

### Vue 3（`<script setup>`）

```vue
<script setup>
import { ref, computed, watch } from 'vue';
import { cloneDeep } from 'lodash';

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  record: { type: Object, required: true },
});

const emit = defineEmits(['update:modelValue', 'confirm']);

const busy = ref(false);
const draft = ref(null);

const open = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
});

const title = computed(() => draft.value?.title);

watch(open, (visible) => {
  if (visible) draft.value = cloneDeep(props.record);
});

async function submit() {
  busy.value = true;
  try {
    emit('confirm', draft.value);
  } finally {
    busy.value = false;
  }
}
</script>
```

---

## 2. 模板 ref、`defineExpose` 与父组件读取

子组件在 `<script setup>` 中默认不暴露实例，需通过 **`defineExpose`** 暴露方法或只读数据；父组件通过 **`ref`** 获取子组件引用。

**子组件（示意）**

```vue
<script setup>
import { ref, computed } from 'vue';

const formRef = ref(null);
const fields = computed(() => /* ... */);

async function validate() {
  await formRef.value?.validate?.();
  return Object.fromEntries(fields.value.map((f) => [f.key, f.value]));
}

defineExpose({ validate, fields });
</script>
```

**父组件（示意）**

```vue
<script setup>
import { ref, unref } from 'vue';

const childRef = ref(null);

async function collect() {
  const list = unref(childRef.value?.fields) ?? [];
  const data = await childRef.value?.validate?.();
  return { list, data };
}
</script>
```

说明：若子组件暴露的是 `ref`，在父侧可能呈现为嵌套 ref；用 **`unref`** 统一取值更稳妥。

---

## 3. 可选全局 store（`inject` + 降级）

当迁移包可能在「带 Vuex/Pinia 的应用」与「无 store 的 Story/文档站」两用的场景，可用 **`inject` 默认值**避免硬依赖：

```vue
<script setup>
import { inject } from 'vue';

const store = inject('store', null);

function sync(payload) {
  store?.commit?.('UPDATE', payload);
}
</script>
```

宿主应用需 **`provide('store', store)`**；无 provide 时逻辑应可安全跳过或走本地状态（在 `SKILL.md` 的行为表中标明）。

---

## 4. 路径别名落地为相对导入（示例）

隔离包迁移时，常将 **`@/`** 等与内部目录结构绑定的别名改为相对新根目录的路径。以下为**示意对照**（路径以你的工程为准）：

| 原别名引用（示例） | 隔离包内落地（示例） |
|--------------------|----------------------|
| `@/shared/utils/request` | `./utils/request.js` |
| `@/theme/variables.less` | `./assets/styles/variables.less` |
| `@/components/base/Button` | `./components/base/Button.vue` |
| 某功能域 `@/features/foo/api` | `./utils/fooApi.js` 或 `./api/foo.js`（按闭包拓扑命名） |

跨多个子目录的大功能域：在依赖闭包中把 **API / 常量 / 纯逻辑** 与 **UI** 分层落盘，避免循环依赖；若 Vue 2 侧存在循环引用，迁移时优先抽离纯函数或类型到中间模块。

---

## 5. 常用 API 对照（Vue 2 → Vue 3）

| Vue 2 / 工程习惯 | Vue 3 |
|------------------|--------|
| `data()` | `ref` / `reactive` |
| `methods` | 普通函数 |
| `computed` | `computed()` |
| `$refs.x` | `ref()` + `.value` |
| `$emit('input', v)`（默认 v-model） | `emit('update:modelValue', v)` |
| `$listeners`（合并） | `$attrs`（含事件）+ 显式 `emit` |
| `this.$set` / `Vue.set` | 直接赋值或 `reactive` 替换对象引用 |
| `$destroy` / `beforeDestroy` | `onBeforeUnmount` |
| `>>>` / `/deep/` | `:deep()` |
| 过滤器 `filter` | 函数或计算属性（Vue 3 已移除过滤器） |

---

## 6. 附录：UI 库大版本升级（示例对照）

以下以常见移动端库为例，**仅作升级时查阅**；以项目 `package.json` 与官方迁移指南为准。

| 常见变更点 | 方向 |
|------------|------|
| 消息类 API | 全局方法改为具名导入或实例方法（如 `showToast`） |
| 日期选择类组件 | 组件名、事件名、`v-model` 绑定字段可能变化 |
| `van-field` 等插槽 | 插槽名调整（如 `#button` → `#extra`，以文档为准） |
| 选择器 `@confirm` 回调参数 | 由选中项数组变为 `{ selectedOptions }` 等包装（以文档为准） |

---

## 7. `peerDependencies` 示意（隔离包）

隔离包在 `package.json` 中声明宿主应提供的运行时，避免重复打包核心框架（版本范围按团队规范收紧）：

```json
{
  "peerDependencies": {
    "vue": "^3.3.0"
  }
}
```

其余依赖（HTTP 客户端、工具库、UI 库）按闭包真实引用列出；勿在仓库中提交机密环境变量。

---

## 8. 一页纸模板（依赖登记册 · 因果链）

以下与 **`SKILL.md` 两阶段协议**配套：第一轮交付至少包含本节约表格骨架与 §10 扫雷勾选；可在业务仓库 PR / 迁移说明中**整段复制**，删去示例行后填写。

### 8.1 元信息

| 项目 | 填写 |
|------|------|
| 迁移目标（Vue 2 入口路径） |  |
| 迁移产出（Vue 3 路径或包名） |  |
| 策略 | 就地升级 / 隔离包 |
| 负责人 / 日期 |  |
| 关联需求或 issue |  |
| 工程就绪（§9）结论摘要 | 已核对 / 部分不适用（说明） |

### 8.2 依赖登记册

| 路径（V2 → V3） | 类型 | 被谁引用 | 迁移动作 | 备注（动态 import / 别名 / 副作用 import） |
|-----------------|------|----------|----------|--------------------------------------------|
| `…/Foo.vue` → `…/Foo.vue` | SFC | 入口 | 迁入 | |
| `…/api.js` → `…/api.js` | JS | `Foo.vue` | 迁入 | |

**模板边须补扫**（无则填「无」）：全局注册组件、`<component :is>`、`$t` key、样式 `@import` 与 `url()`、`process.env` / `import.meta.env`。

### 8.3 因果链登记表

| 因（触发） | 中间条件 / 状态 | 果（可观测） | Vue 3 侧落点（函数或 watch 名） |
|------------|-----------------|--------------|----------------------------------|
| 某 `prop` 变化 | 重置 `draft` | 表单与 V2 同序刷新 | `watch(…)` |
| 用户点击确认 | 校验通过 | `emit('confirm', payload)` 与 V2 载荷一致 | `submit()` |

### 8.4 隐式耦合与宿主约定

| 耦合类型 | Vue 2 表现 | 迁移处理方式 | 宿主须提供（若适用） |
|----------|------------|----------------|----------------------|
| 示例：全局 store | `this.$store` | `inject('store', null)` + 降级分支 | `provide('store', …)` |

### 8.5 双重闸门（收口勾选项）

- [ ] **结构门**：闭包内引用均可解析；模板标签均有组件来源；`package.json` 与 import 一致  
- [ ] **行为门**：上表「因果链」逐行已对照 Vue 2，或通过已批准差异说明  

### 8.6 已知风险 / 待跟进

| 条目 | 风险 | 跟进方式 |
|------|------|----------|
|  |  |  |

---

## 9. 工程就绪核对（展开）

在扩张闭包与改码前，建议对**目标 Vue 3 宿主或隔离包预期宿主**完成下列核对（与 `SKILL.md`「工程就绪」五 checklist 对应）。

### 9.1 依赖与运行时

- 阅读 **`package.json`**（及 monorepo 根 package，若适用）：**`vue`**、路由、状态库、UI、请求库、工具库版本是否与迁移策略一致；是否残留 **仅 Vue 2 可用** 的依赖（须剔除或替换）。  
- 确认 **锁文件** 与团队约定（`pnpm-lock.yaml` / `package-lock.json` / `yarn.lock`），避免本地与 CI 安装不一致。

### 9.2 构建与路径

- 定位 **构建入口**：`vite.config.*`、`webpack.config.*`、`rsbuild.config.*`、`vue.config.js` 等；记录 **dev / build** 命令。  
- 阅读 **`tsconfig.json`**（若存在）：**`paths`** 是否与迁移后别名策略一致；**`strict`**、**`verbatimModuleSyntax`** 等是否要求调整 import 写法。

### 9.3 验证与运行环境

- 至少明确一种 **可重复验证**：`test`、`typecheck`、`lint`、E2E；迁移后用于佐证 **结构门**。  
- 若有 **Storybook / 文档站**，确认迁移包在该环境下的 **peer / alias** 是否与主应用一致。  
- 若有 **SSR**：核对 `mounted` 与仅在客户端执行的代码是否与部署方式一致。

可将本节结论摘要记入 **§8.1 元信息**「工程就绪」一行或 PR 正文。

---

## 10. 易漏项扫雷（完整清单）

执行时逐项勾选；无法排除则写入 §8.6 风险表。

- [ ] **动态 `import()` / 异步路由组件**：条件分支是否全覆盖  
- [ ] **字符串组件名 + 全局注册**：迁移后是否仍可解析，或已改为显式 import  
- [ ] **`$attrs` / `.sync` / `v-on="$listeners"`**：Vue 3 合并规则不同，父链是否已对齐  
- [ ] **插槽与作用域插槽**：更名、参数解构、默认插槽是否逐一对照  
- [ ] **事件总线、全局单例、prototype 方法**：是否纳入闭包或改为显式依赖  
- [ ] **列表 `key`、`<keep-alive>`、`activated` / `deactivated`**：生命周期与缓存语义是否保留  
- [ ] **SSR / 无 DOM 环境**（若有）：`mounted` 前后逻辑是否与运行环境一致  
- [ ] **i18n key 与词条**：`$t` 是否在闭包或宿主约定范围内  
- [ ] **样式副作用 `import`、CSS Modules 类名**：是否与构建配置一致  

---

## 11. 校验清单（完整版）

迁移完成后建议全量核对（可依项目增删）；与 **`SKILL.md` 核心校验**及 **§8 登记**联动。

- [ ] **登记册齐备**：依赖登记册覆盖闭包内全部文件与非文件资源边；因果链覆盖**业务关键链路**（主用户路径、提交/支付级链路若存在）  
- [ ] **双重闸门**：结构门、行为门均已按判据通过  
- [ ] **闭包**：无未解析路径；未纳入闭包的外部引用均有文档或宿主约定  
- [ ] **模板-脚本一致**：模板中每个自定义组件均在脚本或宿主约定中有对应来源  
- [ ] **动态与边角**：动态 `import`、`require`、条件分支、`<component :is>` 解析路径已审查  
- [ ] **别名**：隔离包内无悬挂 `@/` 等（或已与宿主别名策略对齐并文档化）  
- [ ] **语法**：setup 区域内无遗留误用 **`this.`**；无 Vue 2 已移除且未替换的全局 API  
- [ ] **v-model / emit**：与父级调用方一致；多 `v-model` 与 `.sync` 合并已按 Vue 3 命名  
- [ ] **子组件**：`defineExpose` 与父组件 `ref` / `unref` 读取路径正确  
- [ ] **逻辑链**：因果链登记表与 **watch / computed / 生命周期** 与迁移前语义一致或有已批准差异说明  
- [ ] **样式与资源**：变量、`:deep()`、`url()`、样式 `@import` 在构建链路中可解析  
- [ ] **第三方**：所用 UI/工具 API 已与目标版本文档对齐（插槽名、回调参数、toast 类等）  
- [ ] **可选 store**：`inject` 默认值路径下逻辑可降级，与 Vue 2 分支一致  
- [ ] **构建与类型**（若项目具备）：目标工程下相关包可成功类型检查 / 生产构建，无仅迁移目录内才暴露的缺失模块  
- [ ] **交付物**：README（隔离包）或 PR 描述含入口、`peer`、`inject`、已知限制、**登记册/因果表链接或摘要**

---

## 12. 常见坑点（完整）

1. **闭包扩张在「第二次」才想到模板**：先扫 script 再扫 template，顺序错误会导致 **漏组件、漏指令、漏动态 `is`**。  
2. **`reactive` 解构丢失响应式**：需要解构时用 `toRefs` 或改用 `ref` 明确边界。  
3. **`watch` 默认非深度**：Vue 2 侧深度监听的对象在 Vue 3 需 **`deep: true`** 或重写为等价监听目标；**`flush`** 差异也会表现为「少一次更新」。  
4. **事件载荷历史包袱**：多签名 emit 兼容时父侧须分支或收敛约定并文档化。  
5. **工厂函数返回新对象**：与共享引用混用时注意 `watch` 频率与引用相等性，防止漏更新或死循环。  
6. **过滤器与全局 mixin**：Vue 3 无 filter；mixin 收敛为 composable 或显式 import，避免隐式顺序依赖。  
7. **仅开发环境 polyfill**：生产构建 tree-shaking 变化后需验证目标浏览器与构建配置。  
8. **`package.json` 与闭包脱节**：漏写 **实际 import 的组织内包或工具库**，他机报错 `Cannot find module`。

