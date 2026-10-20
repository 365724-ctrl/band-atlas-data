# Band Atlas · 全球频段通 — open data

**Which cellular IoT modules and devices work on which networks, country by country** — 4G/5G bands of 465 networks in 172 countries, 2G/3G switch-offs, LTE-M / NB-IoT / 5G RedCap availability, eSIM by network, an IoT readiness index for every country, and network-by-network verdicts for 39 modules, DTUs, industrial routers, vehicle trackers and dongles.

- Live tool: <https://www.aiotrf.com/en/ai/band-atlas/> · 中文：<https://www.aiotrf.com/ai/band-atlas/> · 繁體：<https://www.aiotrf.com/zh-hant/ai/band-atlas/>
- Also in Español <https://www.aiotrf.com/es/ai/band-atlas/> · Português <https://www.aiotrf.com/pt/ai/band-atlas/> · Français <https://www.aiotrf.com/fr/ai/band-atlas/> · Italiano <https://www.aiotrf.com/it/ai/band-atlas/>
- Global IoT readiness index (172 countries): <https://www.aiotrf.com/en/ai/band-atlas/readiness/> · data checks: <https://www.aiotrf.com/en/ai/band-atlas/quality/>
- Fewest-SKU planner: <https://www.aiotrf.com/en/ai/band-atlas/sku/> · multi-country project report: <https://www.aiotrf.com/en/ai/band-atlas/project/>
- Maintained by [Hyper Nexus](https://www.aiotrf.com/en/) · data checked 2026-10-06 · synced here every day · every value carries a source with an evidence grade

## Files

| File | Contents | Rows |
|---|---|---|
| `atlas.json` | Everything in one JSON file | — |
| `bands.csv` | 4G/5G band reference | 148 |
| `iot_networks.csv` | LTE-M and NB-IoT networks | 208 |
| `model_verdicts.csv` | Every module and device rated on every network, with the bands it lacks | 18135 |
| `models.csv` | Modules and IoT devices (DTUs, routers, trackers): bands and sources | 39 |
| `network_bands.csv` | The 4G/5G bands each network uses | 1732 |
| `networks.csv` | Networks: market, operator, technologies and switch-off status | 465 |
| `pulse.csv` | Network pulse: industry indicators over time, with sources | 48 |
| `redcap_networks.csv` | 5G RedCap launches, deployments and trials | 27 |
| `sources.csv` | Sources and evidence grades (A official / B industry / C distributors and media) | 476 |
| `sunset.csv` | 2G, 3G and NB-IoT switch-off events | 77 |
| `readiness.json` / `readiness.csv` | Global IoT readiness index: score, rank and the four parts (coverage, LTE-M/NB-IoT, 5G and RedCap, device fit) per country | 172 |
| `quality.json` | The data-quality checks run before every update, and the cross-verification shares | — |
| `esim.json` | Consumer eSIM availability by network | — |

## How verdicts work

A device is rated **good** on a network when it supports the bands that carry the network's service, **limited** when it lacks some of them (typically a coverage band), and **no** when it cannot attach. `missing_bands` lists what is lacking. Receive-only bands (for example LTE B29 and B32) are not counted as bands that can carry a connection alone. Third-party bands come from each maker's datasheets, wiki or product pages; listing a product is not an endorsement.

## Use it from an AI assistant

The same data answers through an MCP server (7 tools: band check, country, operator, project report, IoT readiness and more) and a public JSON API with an OpenAPI description. See <https://www.aiotrf.com/en/ai/band-atlas/developers/>.

## How to cite

Use the "Cite this repository" button (from `CITATION.cff`), or:

> Hyper Nexus (2026). *Band Atlas: cellular IoT bands, networks and device verdicts* [data set]. https://www.aiotrf.com/ai/band-atlas/ — CC BY 4.0

## License

**CC BY 4.0** — free to use, share and adapt, including commercially, as long as you give credit:

> Band Atlas · Hyper Nexus (https://www.aiotrf.com/ai/band-atlas/), CC BY 4.0

## Corrections

Found something out of date? Open an issue with a link to the operator's or maker's announcement, or use the correction button on any page of the live tool. Networks are re-checked every quarter.

---

# 全球频段通 · 开放数据

**哪些蜂窝物联网模组与设备，能在哪个国家的哪张网络上使用**：172 个国家 465 张网络的 4G/5G 频段、2G/3G 退网时间、LTE-M / NB-IoT / 5G RedCap 状态，以及 39 款模组、DTU、工业路由器、车载定位器与数据卡的逐网评级。每一项数据都附来源与证据等级；数据核对日期 2026-10-06，每天自动同步。另有 172 个国家的物联网联接就绪指数和各网络的 eSIM 开通情况。

| 文件 | 内容 | 行数 |
|---|---|---|
| `atlas.json` | 全部数据（JSON） | — |
| `bands.csv` | 4G/5G 频段参数 | 148 |
| `iot_networks.csv` | LTE-M 与 NB-IoT 网络 | 208 |
| `model_verdicts.csv` | 每款模组与设备在每张网络上的评级与缺少的频段 | 18135 |
| `models.csv` | 模组与物联网设备（DTU、路由器、定位器）：频段与来源 | 39 |
| `network_bands.csv` | 每张网络在用的 4G/5G 频段 | 1732 |
| `networks.csv` | 网络清单（国家、运营商、技术与退网状态） | 465 |
| `pulse.csv` | 网络脉搏：行业指标的历史数据与来源 | 48 |
| `redcap_networks.csv` | 5G RedCap 商用、部署与试验 | 27 |
| `sources.csv` | 来源清单与证据等级（A 官方 / B 行业 / C 经销商与媒体） | 476 |
| `sunset.csv` | 2G、3G 与 NB-IoT 退网事件 | 77 |
| `readiness.json` / `readiness.csv` | 全球物联网联接就绪指数：每个国家的分数、排名与四个分项（覆盖、LTE-M/NB-IoT、5G 与 RedCap、设备适配） | 172 |
| `quality.json` | 每次更新前运行的数据校验与交叉印证比例 | — |
| `esim.json` | 各网络的手机 eSIM 开通情况 | — |

**授权**：CC BY 4.0，可自由使用、分享和修改（包括商业用途），注明出处即可：
> 全球频段通 · 超级联接（<https://www.aiotrf.com/ai/band-atlas/>），CC BY 4.0

