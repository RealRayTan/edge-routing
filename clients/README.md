# 客户端配置

## 小火箭

`shadowrocket.conf` 基于使用者提供的懒人配置合并而成，包含原有服务分流、广告过滤和 CF 故障切换，不含节点认证信息。节点仍由原来的 EdgeTunnel 订阅提供；不要把它当成节点订阅导入。

在小火箭「配置」页添加以下地址，下载后选择「使用配置」，首页「全局路由」选择「配置」：

```
https://raw.githubusercontent.com/RealRayTan/edge-routing/main/clients/shadowrocket.conf
```

配置保留原有 DNS、Host、Google 重写与服务分流设置，把原来使用 `PROXY` 的规则改为 `日常流媒体`，并增加 `AI-专线` 独立调度 Gemini/Google 流量。Steam 下载域名和 SteamCN 直连，Steam 其他服务仍按原规则代理。首次下载后选择「使用配置」，以后只使用这一份，不必来回切换配置。

原文本没有广告拦截规则，本版补充 AdvertisingLite 广告域名集与规则集；域名拦截不需要安装解密证书，但不能保证清除 YouTube 视频等与内容共用域名的广告。原文本只指定 Google 中国域名的解密范围，本版保留该范围，没有新增证书或开启 HTTPS 解密。

Apple、WeChat、Global、China 改为原生 Shadowrocket 格式；Apple、Global、China 按规则作者说明同时引用 `_Domain.list`，避免遗漏拆分的域名规则。其余服务规则保留，没有仅因名称相似就删除。

配置的 `update-url` 已指向本仓库合并版。远程规则集仍来自各原作者并随其更新。配置源码保持精简，去掉了教学示例注释和空配置项。

策略组包含两大专线：
- `日常流媒体`：默认直连 `CF-MEDIA`（由 EdgeTunnel 订阅提供），专职负责 YouTube 4K、Twitter/X、GitHub 及通用下载，享受极速千兆带宽。
- `AI-专线`：独立调度 Gemini、Google AI Studio 等对出口 IP 敏感的业务。优先接入低延迟直连节点（如本地导入的新加坡 TT 节点），彻底杜绝地区风控限制。

无需开启频繁的心跳探测与节点竞速，长连接极其稳固，杜绝频繁切换导致的连接中断与 502 错误。

节点订阅更新与配置文件更新是两个独立设置。推荐使用本地测速固化的静态入口列表，并在小火箭中关闭频繁的自动订阅更新，避免由于入口 IP 频繁更换造成断连。

## 桌面客户端配置 (Clash Verge Rev / FlClash)

### Clash Verge Rev (扩展配置 Merge 模式)
在「扩展配置 (Merge)」中添加以下规则订阅，并与主订阅合并激活。若直连 GitHub 出现拦截，优先使用免翻 CDN 镜像：
```
https://fastly.jsdelivr.net/gh/RealRayTan/edge-routing@main/clients/clash.yaml
```
备用官方 Raw 链接：
```
https://raw.githubusercontent.com/RealRayTan/edge-routing/main/clients/clash.yaml
```

### FlClash (单体独立配置模式)
由于 FlClash 不支持远程规则自动 Merge，且公共在线订阅转换服务存在格式兼容与故障风险，推荐直接在本地一键生成专属完整配置：
```bash
python3 scripts/generate_local_config.py
```
运行后将自动结合本地最优 Anycast 入口与鉴权参数，在 `clients/flclash.local.yaml` 输出就绪配置。在 FlClash 中选择「配置 -> 从本地文件导入」即可秒级连通，无需依赖任何第三方转换后端。

配置均内置 QUIC (UDP 443) 阻断规则，防止 YouTube 视频在无 UDP 支持的 EdgeTunnel 上遭遇缓冲卡死，强制浏览器使用高速 TCP (HTTP/2) 流畅播放。

参考：[分组及自动更新说明](https://github.com/LOWERTOP/Shadowrocket/wiki) · [分组配置语法](https://github.com/LOWERTOP/Shadowrocket/blob/main/lazy_group.conf)
