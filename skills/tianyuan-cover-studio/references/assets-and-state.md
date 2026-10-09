# 工作区资产与状态

以用户当前项目为根目录；用户指定位置优先。田园默认 `course-covers/tianyuan/`，枯笔默认 `course-covers/kubi/`。原项目已有记录时先定位课程，避免另建重复任务。新接手建议使用独立制作工作区；本包可整体移动，运行资产不要存进 Skill 安装目录。

## 单课目录

按阶段创建实际需要的文件，不预造用户确认或检查结果：

```text
courses/课程编号_课程名/
  course.md                       # 原文摘录、来源版本、表达边界
  feedback.md                     # 用户真实输入与后续反馈，按时间追加
  status.json                     # 当前阶段、确认版本、生成版本与结果
  briefs/proposals_v01.md          # 全部文字建议与依据
  briefs/confirmed_v01.md          # 用户确认的完整画面与确认回复
  prompts/v01.txt                  # 实际传给工具的完整提示词
  generated/编号_名称_v01.png      # 原始生成结果，不覆盖
  review/v01/call.json             # 调用时间、工具、返回源路径/ID、状态
  review/v01/geometry.json         # 实际尺寸比例；只代表技术检查
  review/v01/thumbnail.png         # 320px缩图
  review/v01/comparison.jpg        # 当前图与三张风格参考并排
  review/v01/qa.md                 # 实际视觉结论与证据
  final/编号_名称_v01.png          # 检查通过的交付副本
```

方案编号和生成图编号各自递增。一份确认方案可在后来获准重生成，因此每次调用记录对应 `confirmed_plan` 和真实授权，不凭相同 v 号推断关系。用户更改内容后先新建方案版本并确认，再生成；只保留历史，不覆盖原文件。

上述 PNG 是路径示例；原图保留工具返回的真实格式，不能只改扩展名冒充转换。文件名中不适用当前系统的字符做安全替换，课程编号和原始名称另存记录。

`confirmed_vNN.md` 至少记录：课程、完整画面、对应及边界、构图、必要字符、用户确认原话、时间或可核对的对话位置。没有回复时用提案文件，不能提前创建“已确认”证据。

`call.json` 在调用前保存实际工具、提示词路径、确认版本、参考使用方式、授权范围及开始时间；返回后补结果标识、源文件、结束时间。工具结果不明确时标记待核实并查原调用，不能直接重发。

## 状态

```text
AWAITING_DIRECTION → AWAITING_CONFIRMATION → CONFIRMED
→ GENERATING → REVIEW_PENDING → QA_PASS → DELIVERED
```

- 初始方案等待选择为 `AWAITING_DIRECTION`；整理版等待确认为 `AWAITING_CONFIRMATION`。
- 已看到完整方案的“就按A出图”可直接确认；一条回复只覆盖其明确范围。
- 未通过成图检查为 `QA_FAILED`，另记失败类型 `CONTENT_EXECUTION`、`STYLE`、`TECHNICAL` 或 `PLAN_MISMATCH`，可多选；后续按用户回复回到对应环节。
- 工具不可用、结果不明、关键原文缺失，记 `NEEDS_INPUT` 或 `TOOL_BLOCKED` 并写明恢复条件，不伪造图片或通过状态。
- `QA_PASS` / `DELIVERED` 是 Skill 自检与交付状态；用户是否接受成图另记 `user_image_accepted: null/true/false`。自检不是用户验收。

`status.json` 建议字段：`course_id`、`course_name`、`style`、`stage`、`active_plan`、`confirmation`（方案路径、真实回复、时间/对话位置、范围）、`generations`（版本、方案、提示词、调用记录、检查、输出）、`user_image_accepted`、`next_action`、`updated_at`。尚不存在的事实用 null，不填虚构值。

## 汇总与交付

在风格根目录维护 `index.md`：每课当前状态、当前方案、最新检查结果、采用文件和待决事项。用户输入多个课程时只创建指定课，不推断整库重做范围。

回复时展示成图并附本课目录或最终文件；尚未生图则交付方案和当前待确认项。所有链接对应真实文件。用户撤回某幅成图时记录采用状态变化，保留旧资产；没有明确清理请求时不删除历史。
