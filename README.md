# Band Atlas · 全球频段通 — open data

**Which cellular IoT modules and devices work on which networks, country by country** — 4G/5G bands of 155 networks in 46 countries, 2G/3G switch-offs, LTE-M / NB-IoT / 5G RedCap availability, and network-by-network verdicts for 31 modules, DTUs, industrial routers, vehicle trackers and dongles.

- Live tool: <https://www.aiotrf.com/en/ai/band-atlas/> · 中文：<https://www.aiotrf.com/ai/band-atlas/>
- Fewest-SKU planner: <https://www.aiotrf.com/en/ai/band-atlas/sku/>
- Maintained by [Hyper Nexus](https://www.aiotrf.com/en/) · data checked 2026-10-02 · every value carries a source with an evidence grade

## Files

| File | Contents | Rows |
|---|---|---|
| `atlas.json` | Everything in one JSON file | — |
| `bands.csv` | 4G/5G band reference | 148 |
| `iot_networks.csv` | LTE-M and NB-IoT networks | 208 |
| `model_verdicts.csv` | Every module and device rated on every network, with the bands it lacks | 4805 |
| `models.csv` | Modules and IoT devices (DTUs, routers, trackers): bands and sources | 31 |
| `network_bands.csv` | The 4G/5G bands each network uses | 992 |
| `networks.csv` | Networks: market, operator, technologies and switch-off status | 155 |
| `pulse.csv` | Network pulse: industry indicators over time, with sources | 48 |
| `redcap_networks.csv` | 5G RedCap launches, deployments and trials | 27 |
| `sources.csv` | Sources and evidence grades (A official / B industry / C distributors and media) | 387 |
| `sunset.csv` | 2G, 3G and NB-IoT switch-off events | 77 |

## How verdicts work

A device is rated **good** on a network when it supports the bands that carry the network's service, **limited** when it lacks some of them (typically a coverage band), and **no** when it cannot attach. `missing_bands` lists what is lacking. Receive-only bands (for example LTE B29 and B32) are not counted as bands that can carry a connection alone. Third-party bands come from each maker's datasheets, wiki or product pages; listing a product is not an endorsement.

## License

**CC BY 4.0** — free to use, share and adapt, including commercially, as long as you give credit:

> Band Atlas · Hyper Nexus (https://www.aiotrf.com/ai/band-atlas/), CC BY 4.0

## Corrections

Found something out of date? Open an issue with a link to the operator's or maker's announcement, or use the correction button on any page of the live tool. Networks are re-checked every quarter.

---

# 全球频段通 · 开放数据

**哪些蜂窝物联网模组与设备，能在哪个国家的哪张网络上使用**：46 个国家 155 张网络的 4G/5G 频段、2G/3G 退网时间、LTE-M / NB-IoT / 5G RedCap 状态，以及 31 款模组、DTU、工业路由器、车载定位器与数据卡的逐网评级。每一项数据都附来源与证据等级。

| 文件 | 内容 | 行数 |
|---|---|---|
| `atlas.json` | 全部数据（JSON） | — |
| `bands.csv` | 4G/5G 频段参数 | 148 |
| `iot_networks.csv` | LTE-M 与 NB-IoT 网络 | 208 |
| `model_verdicts.csv` | 每款模组与设备在每张网络上的评级与缺少的频段 | 4805 |
| `models.csv` | 模组与物联网设备（DTU、路由器、定位器）：频段与来源 | 31 |
| `network_bands.csv` | 每张网络在用的 4G/5G 频段 | 992 |
| `networks.csv` | 网络清单（国家、运营商、技术与退网状态） | 155 |
| `pulse.csv` | 网络脉搏：行业指标的历史数据与来源 | 48 |
| `redcap_networks.csv` | 5G RedCap 商用、部署与试验 | 27 |
| `sources.csv` | 来源清单与证据等级（A 官方 / B 行业 / C 经销商与媒体） | 387 |
| `sunset.csv` | 2G、3G 与 NB-IoT 退网事件 | 77 |

**授权**：CC BY 4.0，可自由使用、分享和修改（包括商业用途），注明出处即可：
> 全球频段通 · 超级联接（<https://www.aiotrf.com/ai/band-atlas/>），CC BY 4.0

