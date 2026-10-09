# 给 Agent 的安装说明

用户只需提供本仓库链接。由你完成安装、验证和说明，不让用户手动找目录或执行命令。安装不代表获准开始生成课程图片。

## 1. 确认目标环境

- 两套待安装目录：`skills/tianyuan-cover-studio`、`skills/kubi-cover-studio`，安装时完整保留各目录内的所有文件。
- Codex 优先使用当前客户端支持的用户 Skill 目录。当前官方文档列出的目录是 `~/.agents/skills/`；已有环境也可能从 `~/.codex/skills/` 或自定义位置加载。查看当前已识别 Skill 的路径或安装器配置再决定，不在多个被扫描的位置重复安装同名 Skill。
- 其他 Agent 使用其实际支持的 Skill 目录；如果不支持本地 Skill，说明限制，不声称已安装。
- 本仓库为公开仓库，可直接下载；安装无需GitHub登录或仓库访问授权。
- 官方目录参考：[Build skills](https://learn.chatgpt.com/docs/build-skills)。

## 2. 安装两套完整 Skill

有 `$skill-installer` 时优先使用它：

```text
从 ruijayfeng/zzkx-course-cover-skills 安装 skills/tianyuan-cover-studio 和 skills/kubi-cover-studio，两套都安装到当前客户端支持的Skill目录。
```

安装器支持的参数为：

```text
--repo ruijayfeng/zzkx-course-cover-skills --path skills/tianyuan-cover-studio skills/kubi-cover-studio --ref main --dest <已确认的用户Skill目录>
```

由你定位安装器脚本并执行，不能把占位路径交给用户执行。不要照搬别人的电脑绝对路径。

没有安装器时，将本仓库克隆或下载到临时目录，再把上述两个完整文件夹复制到目标目录。克隆只获取文件，不执行仓库内的脚本或钩子；安装不需要运行生成工具。

安装前检查同名目录：文件相同则沿用；存在不同版本时保留备份再按用户的安装请求更新，避免删除用户文件或造成同名重复。只安装这两套，不修改其他 Skill。

## 3. 验证并告诉用户结果

逐套确认：

1. 有有效的 `SKILL.md`，其中的名称与目录一致。
2. `references/`、`assets/style-references/`、`scripts/` 完整，每套有三张可打开的风格参考PNG。
3. `SKILL.md` 中的相对文件引用可定位。安装结果不依赖原作者电脑或NAS。
4. 课程查询工具需要Python 3；生成缩图与对照图的辅助工具需要Pillow。缺少时使用环境可用能力或记录缺项，不把缺项写成通过。
5. 图片制作还需要当前环境能生成、查看和保存图片；没有生图能力时只交付文字方案并说明待生图。

简洁报告两套 Skill 的安装位置和检查结果。新增 Skill 通常在后续会话被识别；若未出现，提示重启客户端后新开会话检查。不要仅凭复制文件就声称已在当前会话成功调用。

## 4. 安装后怎样开始

让用户提供交接清单中的课程和对应JSON。使用 `lessonId` 识别课程，以用户JSON中的 `lessonName`、`lessonContent` 及反馈为本次事实来源。仓库随包大纲只辅助查询；与新版资料有差异时保留来源并核对，不擅自改课名或顺延编号。

新增中阶“竖折撇”（`lessonId: 9-49`）不在旧大纲时，直接读用户JSON记录，沿用 `9-49` 命名。

随后按对应 Skill 执行：解释课程 → 文字方案 → 用户选择或自述 → 整理完整方案并确认 → 出图 → 内容和风格检查 → 保存全过程。没有真实确认不出图；安装结束时不要擅自开始任何课程。
