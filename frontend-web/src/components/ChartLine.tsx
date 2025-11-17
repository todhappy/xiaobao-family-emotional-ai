import ReactECharts from "echarts-for-react"

export default function ChartLine({ series }: { series: number[] }) {
  const option = { xAxis: { type: "category", data: Array.from({ length: series.length }, (_, i) => i + 1) }, yAxis: { type: "value" }, series: [{ data: series, type: "line", smooth: true }] }
  return <ReactECharts option={option} style={{ height: 280 }} />
}