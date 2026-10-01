# Issue 跟踪

!!! note "中文版"
    本页是中文说明；英文原文见本页的 English 版本（右上角切换）。

Issue 放在 fork 的 GitHub Issues 里，全部用 `gh` CLI 驱动。

## 常用命令

```sh
gh issue create --title "..." --body "..."        # 多行正文用 heredoc
gh issue view <number> --comments                 # 读 issue（含评论）
gh issue list --state open --json number,title,body,labels,comments \
  --jq '[.[] | {number, title, labels: [.labels[].name]}]'
gh issue comment <number> --body "..."
gh issue edit <number> --add-label "..." --remove-label "..."
gh issue close <number> --comment "..."
```

## PR 也是 triage 入口

```sh
gh pr view <number> --comments
gh pr diff <number>
gh pr list --state open --json number,title,body,labels,author,authorAssociation
```

只看 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR`、`NONE` 的（外部贡献），忽略 `OWNER`/`MEMBER`/`COLLABORATOR`。

## 当别的技能说"发布到 issue tracker" / "取出相关工单"

按上面的命令创建或读取对应 issue；读的时候要把评论一起读进来，并按 `jq` 过滤出关键字段（标题、正文、标签、评论），不要只看第一屏。
